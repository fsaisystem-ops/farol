import json
from pathlib import Path

from varrer import varrer

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


def open_ids(pasta: Path) -> set[str]:
    result = varrer(pasta)
    return {f["id"] for f in result["findings"] if f.get("status") == "open"}


def test_token_exposto_marca_must01():
    ids = open_ids(FIXTURES / "token-exposto")
    assert "MUST-01" in ids


def test_unicode_invisivel_marca_mcp06_ou_mcp03():
    ids = open_ids(FIXTURES / "unicode-invisivel")
    assert "MCP06" in ids or "MCP03" in ids


def test_html_instrucao_escondida_marca_mcp06():
    ids = open_ids(FIXTURES / "html-instrucao-escondida")
    assert "MCP06" in ids


def test_permissao_ampla_marca_mcp02():
    ids = open_ids(FIXTURES / "permissao-ampla")
    assert "MCP02" in ids


def test_sem_confirmacao_marca_must02():
    ids = open_ids(FIXTURES / "sem-confirmacao")
    assert "MUST-02" in ids


def test_pacote_cru_marca_mcp10():
    ids = open_ids(FIXTURES / "pacote-cru")
    assert "MCP10" in ids


def test_rede_sem_restricao_marca_mcp09():
    ids = open_ids(FIXTURES / "rede-sem-restricao")
    assert "MCP09" in ids


def test_skill_de_agente_marca_mcp06():
    ids = open_ids(FIXTURES / "skill-de-agente")
    assert "MCP06" in ids


def test_example_vulneravel_ids_minimos():
    ids = open_ids(ROOT / "examples" / "skill-vulneravel")
    minimo = {"MUST-01", "MUST-02", "MCP06", "MCP10", "MCP09"}
    assert minimo <= ids


def test_example_corrigida_sem_ids_abertos():
    ids = open_ids(ROOT / "examples" / "skill-corrigida")
    proibidos = {"MUST-01", "MUST-02", "MCP06", "MCP10", "MCP09"}
    assert ids.isdisjoint(proibidos)


def test_apr_json_exemplos_tem_contrato():
    required = {
        "skill",
        "skill_path",
        "date",
        "farol_version",
        "catalog_spec",
        "areas",
        "risk_level",
        "complete",
        "counts",
        "findings",
        "plan",
        "impact",
        "scanner",
    }
    ids_fixos = {f"MUST-0{i}" for i in range(1, 5)} | {f"MCP{i:02d}" for i in range(1, 11)}
    for nome in ("skill-vulneravel", "skill-corrigida"):
        data = json.loads((ROOT / "examples" / nome / "apr.json").read_text(encoding="utf-8"))
        assert required <= set(data)
        got = {f["id"] for f in data["findings"]}
        assert ids_fixos <= got
        html = (ROOT / "examples" / nome / "apr-seguranca.html").read_text(encoding="utf-8")
        assert "__SKILL_NAME__" not in html
        assert "sk-EXEMPLO" not in html


def test_varrer_nao_executa_e_marca_scanner():
    result = varrer(FIXTURES / "token-exposto")
    assert result["scanner"]["ran"] is True
    assert result["scanner"]["version"] == "1"
    for f in result["findings"]:
        assert f["status"] == "open"
        assert "sk-EXEMPLO_NAO_E_CHAVE" not in (f.get("evidence") or "")
