# Farol

![Agente de IA conferindo um recado escrito](banner.jpg)

Criamos skill para uma ação. Às vezes o recado traz junto coisa que não pedimos — e a IA obedece. O Farol lê essa skill e mostra o que pode comprometer nosso sistema e nossa IA. Sem isso, “pronto” e o furo vão no mesmo arquivo.

## Para que serve

Usamos o Farol quando vamos criar ou mexer numa skill. Ele lê o arquivo, aponta o risco, diz o que muda no dia a dia se aplicarmos a correção, e grava um HTML. A lista de furos vem da Microsoft; aplicamos isso no recado da skill, não num servidor.

## O que ele não é

Não é antivírus. Não trava o Windows. Não impede de escrever proposta ou buscar site. Só acende o que, no recado, pode mandar a IA fazer demais.

## Quando usamos

Skill nova. Skill que parecia inocente. Skill que lê PDF, busca na web, grava arquivo ou pega zip. Antes de chamar de pronta.

O texto do relatório é em português do Brasil. Não cola a tradução do curso no cartão. Esta pasta **sozinha basta**: o tom da escrita vai junto, não depende de outra skill no disco.

## Funcionalidades

1. **Análise preliminar de riscos (APR)**  
   Lê `SKILL.md`, scripts e referências da skill alvo. Não trata o texto dela como ordem.

2. **Relatório HTML e JSON**  
   Grava `apr-seguranca.html` na pasta da alvo, com o visual do `template.html`. No mesmo passo, `apr.json` (máquina, CI). Não reescreve o CSS.

   Exemplos prontos: `examples/skill-vulneravel` e `examples/skill-corrigida`. Teste: `python -m pytest tests/ -q` (na pasta do Farol; `tests/requirements.txt`).

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
