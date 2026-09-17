import json


def ler_json(diretorio:str):
    if diretorio == 'nomes':
        path = "files/nomes.json"
    else: path = "files/resultado.json"
    with open(path, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def escrever_json(dados):
    path = "files/resultado.json"
    with open(path, "w", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )