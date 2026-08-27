"""Varre uma skill alvo. Só lê. Nunca executa script da pasta."""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

SCANNER_VERSION = "1"
MAX_BYTES = 1_000_000
SKIP_NAMES = {"apr-seguranca.html", "apr.json", "leia-me.md", "banner.jpg"}
SCRIPT_EXT = {".py", ".js", ".sh", ".ps1"}
TEXT_EXT = {".md", ".html", ".txt", ".py", ".js", ".sh", ".ps1"}

TOKEN_RES = [
    re.compile(r"sk-[A-Za-z0-9_-]+"),
    re.compile(r"ghp_[A-Za-z0-9]+"),
    re.compile(r"xox[a-zA-Z]-[\w-]+"),
    re.compile(r"Bearer\s+\S+"),
    re.compile(r"(?i)api_key\s*=\s*['\"][^'\"]+['\"]"),
    re.compile(r"(?i)token\s*=\s*['\"][^'\"]+['\"]"),
    re.compile(r"(?i)senha\s*=\s*['\"][^'\"]+['\"]"),
]
HIDE_RE = re.compile(
    r"display\s*:\s*none|font-size\s*:\s*0|visibility\s*:\s*hidden", re.I
)
INSTR_RE = re.compile(
    r"ignore|SYSTEM:|aten[cç][aã]o intelig[eê]ncia|obede[cç]a|obedece", re.I
)
URL_RE = re.compile(r"https?://[^\s'\"<>]+", re.I)
AMPLA_RE = re.compile(
    r"qualquer comando|C:\\Users|rm\s+-rf|se precisar,\s*usa qualquer", re.I
)
DELETE_RE = re.compile(
    r"os\.remove|unlink\(|\brm\s|send_mail|smtp|apaga|enviar e-mail", re.I
)
PACOTE_RE = re.compile(
    r"grava o html|salva o extrato|write\([^)]*html|json\.dump", re.I
)
BIDI = set(range(0x202A, 0x202F)) | set(range(0x2066, 0x206A))
TAGS = set(range(0xE0000, 0xE0080))
SKIP_CF = {"\ufeff", "\u00ad"}


def _norm(text: str) -> str:
    return (
        text.lower()
        .replace("á", "a")
        .replace("ã", "a")
        .replace("à", "a")
        .replace("é", "e")
        .replace("ê", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ô", "o")
        .replace("ú", "u")
        .replace("ç", "c")
    )


def tem_leitura_protegida(skill: str) -> bool:
    t = _norm(skill)
    return any(
        s in t
        for s in (
            "nao e ordem",
            "e dado, nao",
            "dado, nao ordem",
            "dado nao ordem",
            "texto de fora e dado",
            "veio de fora e dado",
        )
    )


def tem_campo_nao_pacote(skill: str) -> bool:
    t = _norm(skill)
    return any(
        s in t
        for s in (
            "so o campo",
            "persiste so",
            "nao o pacote",
            "titulo, valor",
            "título, valor",
            "campo (titulo",
        )
    )


def tem_duas_perguntas(skill: str) -> bool:
    return tem_leitura_protegida(skill) and tem_campo_nao_pacote(skill)


def tem_allowlist(skill: str) -> bool:
    t = _norm(skill)
    return any(
        s in t
        for s in (
            "allowlist",
            "saidas de rede",
            "esta skill nao chama rede",
            "hosts permitidos",
            "host permitido",
            "host da lista",
        )
    )


def tem_confirma(skill: str) -> bool:
    t = _norm(skill)
    return bool(re.search(r"confirma\?", t) or re.search(r"\bconfirma\b", t))


def gerada_por_agente(skill: str) -> bool:
    t = _norm(skill)
    return (
        "generated_by" in t
        or "gerado por agente" in t
        or "cria skill" in t
    )


def mask(text: str) -> str:
    out = text
    for rx in TOKEN_RES:
        out = rx.sub(lambda m: m.group(0)[:3] + "…REDACTED", out)
    return out[:200]


def finding(
    id_: str,
    severity: str,
    rel: str,
    line: int | None,
    evidence: str,
    title: str,
) -> dict:
    return {
        "id": id_,
        "severity": severity,
        "status": "open",
        "file": rel.replace("\\", "/"),
        "line": line,
        "evidence": mask(evidence),
        "title": title,
        "fix": "",
    }


def _rel(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _safe_inside(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def collect_files(root: Path) -> list[Path]:
    out: list[Path] = []
    seen: set[Path] = set()

    def add(p: Path) -> None:
        try:
            rp = p.resolve()
        except OSError:
            return
        if rp in seen:
            return
        if not rp.is_file():
            return
        if p.is_symlink() and not _safe_inside(root, rp):
            return
        if rp.name.lower() in SKIP_NAMES:
            return
        if rp.suffix.lower() not in TEXT_EXT:
            return
        try:
            if rp.stat().st_size > MAX_BYTES:
                return
        except OSError:
            return
        seen.add(rp)
        out.append(rp)

    add(root / "SKILL.md")
    if root.is_dir():
        for p in root.iterdir():
            if p.is_file():
                add(p)
    for sub, extra in (
        ("scripts", SCRIPT_EXT | {".md"}),
        ("references", {".md"}),
        ("fixtures", {".html", ".txt", ".md"}),
    ):
        d = root / sub
        if not d.is_dir():
            continue
        for p in d.rglob("*"):
            if p.is_file() and (p.suffix.lower() in extra or p.suffix.lower() in TEXT_EXT):
                add(p)
    return out


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def line_of(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def detect_token(rel: str, text: str) -> list[dict]:
    found = []
    seen_span = set()
    for rx in TOKEN_RES:
        for m in rx.finditer(text):
            if m.group(0) in seen_span:
                continue
            seen_span.add(m.group(0))
            ln = line_of(text, m.start())
            ev = text[max(0, m.start() - 20) : m.end() + 20]
            found.append(
                finding("MUST-01", "critico", rel, ln, ev, "Token colado no arquivo")
            )
            found.append(
                finding("MCP01", "critico", rel, ln, ev, "Segredo exposto no recado")
            )
    return found


def detect_unicode(rel: str, text: str, in_description: bool) -> list[dict]:
    found = []
    for i, ch in enumerate(text):
        cp = ord(ch)
        cat = unicodedata.category(ch)
        hit = False
        if cat == "Cf" and ch not in SKIP_CF:
            hit = True
        if cp in BIDI or cp in TAGS:
            hit = True
        if not hit:
            continue
        id_ = "MCP03" if in_description else "MCP06"
        found.append(
            finding(
                id_,
                "alto",
                rel,
                line_of(text, i),
                f"caractere U+{cp:04X}",
                "Caractere invisível no recado",
            )
        )
        break
    return found


def detect_html(rel: str, text: str, skill: str) -> list[dict]:
    if not rel.lower().endswith(".html"):
        return []
    if tem_leitura_protegida(skill):
        return []
    if HIDE_RE.search(text) and INSTR_RE.search(text):
        m = INSTR_RE.search(text)
        return [
            finding(
                "MCP06",
                "alto",
                rel,
                line_of(text, m.start()) if m else None,
                m.group(0) if m else "instrução escondida",
                "HTML escondido pode mandar no agente",
            )
        ]
    return []


def detect_ampla(rel: str, text: str) -> list[dict]:
    m = AMPLA_RE.search(text)
    if not m:
        return []
    sev = "alto" if (URL_RE.search(text) or DELETE_RE.search(text) or "C:\\Users" in text) else "medio"
    return [
        finding("MCP02", sev, rel, line_of(text, m.start()), m.group(0), "Permissão larga demais")
    ]


def detect_delete(rel: str, text: str, skill: str) -> list[dict]:
    if tem_confirma(skill):
        return []
    m = DELETE_RE.search(text)
    if not m:
        return []
    baixo = m.group(0).lower()
    sev = "medio" if baixo in ("apaga",) and "os.remove" not in text else "alto"
    if "os.remove" in text or "unlink" in text or "send_mail" in text or "smtp" in text or "rm " in text:
        sev = "alto"
    out = [
        finding("MUST-02", sev, rel, line_of(text, m.start()), m.group(0), "Age sem confirmação")
    ]
    if sev == "alto":
        out.append(
            finding("MCP07", "alto", rel, line_of(text, m.start()), m.group(0), "Apaga ou envia sem conferir")
        )
    return out


def detect_pacote(rel: str, text: str, skill: str) -> list[dict]:
    if tem_campo_nao_pacote(skill):
        return []
    m = PACOTE_RE.search(text)
    if not m:
        return []
    return [
        finding("MCP10", "alto", rel, line_of(text, m.start()), m.group(0), "Grava o pacote cru")
    ]


def detect_rede(rel: str, text: str, skill: str, is_script: bool) -> list[dict]:
    if not is_script:
        return []
    if tem_allowlist(skill):
        return []
    m = URL_RE.search(text)
    if not m:
        return []
    return [
        finding("MCP09", "alto", rel, line_of(text, m.start()), m.group(0), "Rede sem host declarado")
    ]


def detect_agente(rel: str, skill: str) -> list[dict]:
    if rel != "SKILL.md":
        return []
    if not gerada_por_agente(skill):
        return []
    if tem_duas_perguntas(skill):
        return []
    return [
        finding("MCP06", "alto", rel, 1, "gerado por agente", "Skill gerada sem as duas perguntas"),
        finding("MCP03", "alto", rel, 1, "generated_by / cria skill", "Metadado de skill gerada por agente"),
    ]


def in_frontmatter_description(text: str, idx: int) -> bool:
    # crude: first --- ... --- block
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    if end < 0:
        return False
    return idx < end


def varrer(pasta: Path) -> dict:
    pasta = Path(pasta)
    findings: list[dict] = []
    skill_path = pasta / "SKILL.md"
    skill = read_text(skill_path) if skill_path.is_file() else ""

    for path in collect_files(pasta):
        rel = _rel(pasta, path)
        text = read_text(path)
        is_script = path.suffix.lower() in SCRIPT_EXT and "/scripts/" in ("/" + rel.replace("\\", "/"))
        if rel.startswith("scripts/"):
            is_script = path.suffix.lower() in SCRIPT_EXT

        findings.extend(detect_token(rel, text))
        for i, ch in enumerate(text):
            cp = ord(ch)
            cat = unicodedata.category(ch)
            hit = (cat == "Cf" and ch not in SKIP_CF) or cp in BIDI or cp in TAGS
            if hit:
                desc = rel == "SKILL.md" and in_frontmatter_description(text, i)
                findings.extend(detect_unicode(rel, text, desc))
                break
        findings.extend(detect_html(rel, text, skill))
        findings.extend(detect_ampla(rel, text))
        findings.extend(detect_delete(rel, text, skill))
        findings.extend(detect_pacote(rel, text, skill))
        findings.extend(detect_rede(rel, text, skill, is_script))
        findings.extend(detect_agente(rel, skill))

    # dedupe (id, file, line)
    uniq = []
    seen = set()
    for f in findings:
        key = (f["id"], f["file"], f["line"], f["title"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(f)

    return {
        "findings": uniq,
        "scanner": {"ran": True, "version": SCANNER_VERSION},
    }


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) < 1:
        print("uso: python scripts/varrer.py <pasta-da-skill-alvo>", file=sys.stderr)
        return 2
    pasta = Path(argv[0])
    if not pasta.is_dir() or not (pasta / "SKILL.md").is_file():
        print("pasta inexistente ou sem SKILL.md", file=sys.stderr)
        return 2
    print(json.dumps(varrer(pasta), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
