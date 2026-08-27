# Só lê a página visível. Não executar na análise do Farol.

URL = "https://loja.exemplo/item"  # host na allowlist da skill

CAMPOS = ("titulo", "valor")


def extrair():
    # parser de texto visível; não cola o source
    return {"titulo": "item", "valor": "10.00"}
