# Segurança de skills

Você vai criar uma skill. Antes de dizer que ela está pronta, esta pasta manda parar, ler o arquivo e dizer o que pode dar ruim.

Uma skill é um recado escrito para o agente. Se o recado manda guardar senha, abrir qualquer site ou obedecer o que estiver num PDF, o agente faz. Esta skill lê esse recado, cruza com uma lista de falhas (curso de segurança da Microsoft, Top 10 MCP) e grava um HTML: o que pega, o quão grave, o que mudar no arquivo.


## O que ela faz

1. Lê a skill alvo (`SKILL.md`, scripts, referências).
2. Marca a área (dinheiro, dado, licitação, integração, rotina, texto). Pode ser mais de uma.
3. Olha canais escondidos: metadado, imagem, SVG, QR, Unicode, nome de arquivo.
4. Pontua os quatro “não pode” e os dez riscos da Microsoft. Nenhum ID fica de fora.
5. Grava `apr-seguranca.html` na pasta da skill alvo.
6. **Não** altera a skill alvo até você mandar aplicar.

## Como usar

1. Copie esta pasta para `~/.grok/skills/seguranca-skills/` (Windows: `%USERPROFILE%\.grok\skills\seguranca-skills\`).
2. No Grok: `/seguranca-skills` ou peça para analisar uma skill.
3. Abra o HTML que ela gravou.

Esta pasta **sozinha basta**. Não precisa de outra skill no disco para o tom do texto: a escrita humana está em `references/escrita-humana.md`.

## O que não sobe neste repositório

Relatório HTML gerado na sua máquina (`apr-seguranca.html`) — tem caminho local. Cada quem gera o seu.

## Fonte da lista de riscos

Cópia local em `references/` da lição **02-Security** do [Microsoft MCP for Beginners](https://github.com/microsoft/mcp-for-beginners) (tradução pt-BR). O original em inglês no repositório da Microsoft é a fonte autorizada da lista.

## Licença

MIT. O material da Microsoft em `references/` (README, controles, práticas, Content Safety) continua com a licença e os avisos daquele repositório.
