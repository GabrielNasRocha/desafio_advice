from utils import ler_json
import sqlite3


def conectar():
    return sqlite3.connect("database/database.db")

def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_id INTEGER NOT NULL,
            nome TEXT,
            processo TEXT,
            data_atuacao TEXT,
            situacao TEXT,
            orgao_julgador TEXT,
            juiz TEXT,
            classe_acao TEXT,
            codigo TEXT,
            descricao TEXT,

            FOREIGN KEY (nome_id)
                REFERENCES nomes(id)
        )
    """)
    conexao.commit()
    conexao.close()

def imprimir_tabela_nomes():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM nomes")
    nomes = cursor.fetchall()
    for nome in nomes:
        print(nome)
    conexao.close()

def inserir_nomes():
    conexao = conectar()
    cursor = conexao.cursor()
    nomes = ler_json(diretorio='nomes')
    for nome in nomes['names']:
        print(f'Inserindo na base: {nome}')
        cursor.execute("INSERT INTO nomes (nome) VALUES (?)",(nome,))
    conexao.commit()
    conexao.close()

def consultar_id(nome):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM nomes WHERE nome = ?",(nome,))
    id = cursor.fetchone()
    conexao.close()
    return id[0]

def limpar_base():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM nomes")
    cursor.execute("DELETE FROM resultados")
    conexao.commit()
    conexao.close()

def inserir_resultado(processo):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO resultados (
            nome_id,
            nome,
            processo,
            data_atuacao,
            situacao,
            orgao_julgador,
            juiz,
            classe_acao,
            codigo,
            descricao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        processo["nome_id"],
        processo["nome"],
        processo["processo"],
        processo["data_atuacao"],
        processo["situacao"],
        processo["orgao_julgador"],
        processo["juiz"],
        processo["classe_acao"],
        processo["codigo"],
        processo["descricao"]
    ))

    conexao.commit()
    conexao.close()

def imprimir_resultados():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM resultados")

    resultados = cursor.fetchall()

    for resultado in resultados:
        print(resultado)

    conexao.close()