# Não rode este arquivo na análise. O Farol só lê.

URL = "https://loja.exemplo/item"

def extrair():
    html = open("fixtures/fonte.html", encoding="utf-8").read()
    open("saida.html", "w", encoding="utf-8").write(html)  # grava o html
    import os
    os.remove("tmp/extract.txt")
