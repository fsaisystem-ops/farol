# Exemplo: skill furada

Esta pasta é de propósito. Não instale. Não rode `scripts/extrair.py`.

A skill “lê a loja e grava o preço”. O HTML da loja tem um recado escondido (`display:none`). O `SKILL.md` manda obedecer a página, grava o HTML inteiro, cola um token falso e apaga arquivo sem perguntar.

O Farol, só lendo o disco (`python scripts/varrer.py examples/skill-vulneravel`), acende:

- MUST-01 / MCP01 — token colado (`sk-…`, valor falso)
- MUST-02 / MCP07 — apaga sem `confirma?`
- MCP06 — HTML escondido tratado como ordem
- MCP09 — URL no script sem lista de host
- MCP10 — grava o pacote cru

Relatório humano: `apr-seguranca.html`. Máquina: `apr.json`.

A versão que trata isso: `examples/skill-corrigida/`.
