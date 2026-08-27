# Farol

![Agente de IA conferindo um recado escrito](banner.jpg)

Farol acende o risco **antes** de a skill nova sair. Você vai criar uma skill. Antes de dizer que ela está pronta, esta pasta manda parar, ler o arquivo e dizer o que pode dar ruim — e o que muda no seu dia se você aplicar a correção.

Uma skill é um recado escrito para o agente. Se o recado manda guardar senha, abrir qualquer site ou obedecer o que estiver num PDF, o agente faz. Esta skill lê esse recado, cruza com uma lista de falhas (curso de segurança da Microsoft) e grava um HTML.

O texto do relatório é em português do Brasil. Não cola a tradução do curso no cartão. Esta pasta **sozinha basta**: o tom da escrita vai junto, não depende de outra skill no disco.

## Funcionalidades

1. **Análise preliminar de riscos (APR)**  
   Lê `SKILL.md`, scripts e referências da skill alvo. Não trata o texto dela como ordem.

2. **Relatório HTML**  
   Grava `apr-seguranca.html` na pasta da alvo, com o visual do `template.html`. Não reescreve o CSS.

3. **Níveis**  
   Crítico, Alto, Médio, Baixo, Atende. Contagem no topo da página.

4. **Quatro regras obrigatórias (MUST)**  
   Senha/token no arquivo; agir sem conferir; conexão nova no silêncio; sessão copiada.

5. **Top 10 da Microsoft (MCP01–MCP10)**  
   Um cartão por ID. Nenhum fica de fora. Prova = recorte do arquivo. Sem recorte, não marca Crítico/Alto.

6. **Área da skill**  
   Dinheiro, dados, licitação, integração, rotina, texto. Pode ser mais de uma. O nível sobe quando o risco é típico daquela área (PDF em extração ≠ skill que só escreve).

7. **Canais ocultos**  
   Metadado (EXIF, XMP, propriedades de PDF/Office), imagem (OCR, branco no branco), SVG, QR, Unicode invisível, nome de arquivo. Roda **sempre**, mesmo se “não tem imagem”.

8. **Plano de correção**  
   Só o que dá para escrever no `SKILL.md` ou no script. Pior primeiro. **Não aplica** até você mandar.

9. **Impacto no uso**  
   Se aplicar o plano: o que continua igual, o que passa a perguntar ou recusar, o que você ganha, o que paga. No HTML e de novo no chat.

10. **Prosa humana (cópia local)**  
    `references/escrita-humana.md`. Zip e outro Grok não precisam da skill `/escrita-humana` instalada. Cartão: o que acontece → prova → o que fazer → nome Microsoft por último.

11. **Depois do “aplica”**  
    Mexe só no que o plano listou. Regenera o HTML. Chat: o que mudou no arquivo e o que muda no uso agora.

12. **Comando**  
    `/farol` ou “analisa a segurança desta skill”.

13. **Leitura extra na web**  
    A pasta local fecha a APR. Se um ID sair Crítico ou Alto, o agente pode abrir o guia Microsoft/OWASP daquele ID (`references/fontes-web.md`) para pegar mais detalhe. Sem internet, usa só o disco. A página aberta é dado, não ordem.

## Como usar

1. Copie esta pasta para `~/.grok/skills/farol/` (Windows: `%USERPROFILE%\.grok\skills\farol\`).
2. No Grok: `/farol`.
3. Abra o HTML. Se o plano fizer sentido, mande aplicar.

## O que não sobe neste repositório

Relatório gerado na sua máquina (`apr-seguranca.html`) — tem caminho local. Cada quem gera o seu.

## Fonte da lista de riscos

Cópia local em `references/` da lição **02-Security** do [Microsoft MCP for Beginners](https://github.com/microsoft/mcp-for-beginners) (tradução pt-BR). O original em inglês no repositório da Microsoft é a fonte autorizada da lista.

## Licença

MIT. O material da Microsoft em `references/` (README, controles, práticas, Content Safety) continua com a licença e os avisos daquele repositório.
