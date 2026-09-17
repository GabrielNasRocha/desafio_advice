from utils import setup_logger, ler_json,escrever_json
from src import WebTribunal
from database import inserir_nomes, imprimir_tabela_nomes, imprimir_resultados, consultar_id, limpar_base
import os
import sys


logger = setup_logger(__name__)
logger.info('Iniciando o projeto Desafio Advice')

def verificar_resultados():
    imprimir_tabela_nomes()
    imprimir_resultados()

def execute():
    nomesPath = 'files/nomes.json'
    resultadoPath = 'files/resultados.json'
    if not os.path.exists(nomesPath):
        logger.info('Arquivo json com os nomes não existe. Finalizando o processo.')
        sys.exit(0)
    logger.info('Arquivo json com os nomes existe, seguindo processo.')
    escrever_json({"processos": []})
    logger.info('Criado o arquivo de resultados.')
    logger.info('Carregando os nomes para a variavel')
    limpar_base()
    inserir_nomes()
    nomes = ler_json(diretorio="nomes")
    tribunal = WebTribunal()
    for nome in nomes['names']:
        id_nome = consultar_id(nome)
        logger.info(f'Nome: {nome}')
        tribunal.buscaNome(nome, id_nome)
    logger.info('-----Automação Finalizada-----.')


if __name__ == '__main__':
    execute()
    verificar_resultados()
