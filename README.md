# Desafio Advice

Automação desenvolvida em Python como parte da prova prática de programação da **Advice Compliance Solutions**.

O projeto realiza consultas de processos judiciais no portal de consulta pública do **Tribunal de Justiça de Minas Gerais (TJMG)**, utilizando automação web com Selenium, resolução automática de CAPTCHA através da API da Anti-Captcha e armazenamento dos resultados em banco de dados SQLite.

---

## 📋 Funcionalidades

* Leitura de nomes a serem consultados através de arquivo JSON;
* Automação do navegador utilizando Selenium;
* Consulta pública de processos no portal do TJMG;
* Resolução automática do CAPTCHA utilizando a API Anti-Captcha;
* Limitação da quantidade de consultas realizadas;
* Armazenamento dos nomes consultados em banco SQLite;
* Armazenamento dos processos encontrados em banco SQLite;
* Geração de arquivo JSON com os resultados;
* Registro das etapas da automação através de logs.

---

## 🛠️ Tecnologias utilizadas

* **Python 3**
* **Selenium**
* **SQLite**
* **Requests**
* **python-dotenv**
* **Anti-Captcha API**
* **JSON**
* **Chrome / ChromeDriver**

---

## 📁 Estrutura do projeto

```text
desafio_advice/
│
├── database/
│   ├── __init__.py
│   └── database.py
│
├── files/
│   └── nomes.json
│
├── src/
│   ├── __init__.py
│   └── web_tribunal.py
│
├── utils/
│   ├── __init__.py
│   ├── anticaptcha.py
│   ├── json_manager.py
│   └── logger_config.py
│
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

### Descrição dos principais arquivos

**`main.py`**

É o ponto de entrada da aplicação. Responsável por:

1. Validar a existência do arquivo de nomes;
2. Limpar os dados anteriores do banco;
3. Inserir os nomes na tabela;
4. Inicializar a automação;
5. Realizar as consultas;
6. Exibir os resultados obtidos.

**`src/web_tribunal.py`**

Contém a classe `WebTribunal`, responsável pela automação do portal do TJMG utilizando Selenium.

O fluxo inclui:

* abertura do navegador;
* preenchimento do nome;
* captura do CAPTCHA;
* envio da imagem para a Anti-Captcha;
* preenchimento do CAPTCHA resolvido;
* consulta dos processos;
* abertura dos processos encontrados;
* coleta dos dados;
* persistência dos resultados.

**`utils/anticaptcha.py`**

Responsável pela integração com a API da Anti-Captcha.

A imagem do CAPTCHA é enviada para a API através de uma tarefa `ImageToTextTask`, e o código aguarda até que a solução esteja disponível.

**`database/database.py`**

Responsável pela comunicação com o SQLite, incluindo:

* criação das tabelas;
* inserção dos nomes;
* consulta do ID de um nome;
* inserção dos resultados;
* limpeza da base;
* impressão dos dados armazenados.

**`utils/json_manager.py`**

Centraliza a leitura e escrita dos arquivos JSON utilizados pela aplicação.

**`utils/logger_config.py`**

Configura os logs da aplicação, permitindo acompanhar o andamento da automação através do console.

---

## ⚙️ Configuração

Antes de executar o projeto, é necessário criar um arquivo chamado:

```text
.env
```

Esse arquivo deve ficar na raiz do projeto.

Exemplo:

```env
anticaptchaApiKey=SUA_CHAVE_ANTI_CAPTCHA
limiteConsulta=5
```

### `anticaptchaApiKey`

Chave de acesso utilizada para realizar as requisições à API da **Anti-Captcha**.

Essa chave é utilizada para enviar a imagem do CAPTCHA e obter sua resolução automaticamente.

> **Importante:** o arquivo `.env` contém informações sensíveis e não deve ser versionado no Git. O projeto já possui `.env` configurado no `.gitignore`.

### `limiteConsulta`

Define a quantidade máxima de consultas que a automação deverá realizar.

Exemplo:

```env
limiteConsulta=5
```

Nesse caso, o projeto utiliza o valor `5` como limite de consultas durante a consulta dos processos.

Essa configuração existe para evitar que a automação realize uma quantidade excessiva de consultas ao portal durante a execução.

---

## 📄 Arquivo de entrada

Os nomes que serão consultados devem ser informados no arquivo:

```text
files/nomes.json
```

Formato esperado:

```json
{
    "names": [
        "ADILSON DA SILVA",
        "JOÂO DA SILVA MORAES",
        "RICARDO DE JESUS",
        "SERGIO FIRMINO DA SILVA"
    ]
}
```

Novos nomes podem ser adicionados ao array `names`.

---

## 🗄️ Banco de dados

O projeto utiliza **SQLite** para armazenamento dos dados.

O banco é criado em:

```text
database/database.db
```

### Tabela `nomes`

Armazena os nomes utilizados nas consultas.

| Campo  | Tipo    | Descrição             |
| ------ | ------- | --------------------- |
| `id`   | INTEGER | Identificador do nome |
| `nome` | TEXT    | Nome consultado       |

### Tabela `resultados`

Armazena os processos encontrados.

| Campo            | Tipo    | Descrição                   |
| ---------------- | ------- | --------------------------- |
| `id`             | INTEGER | Identificador do resultado  |
| `nome_id`        | INTEGER | ID do nome consultado       |
| `nome`           | TEXT    | Nome encontrado no processo |
| `processo`       | TEXT    | Número do processo          |
| `data_atuacao`   | TEXT    | Data de autuação            |
| `situacao`       | TEXT    | Situação do processo        |
| `orgao_julgador` | TEXT    | Órgão julgador              |
| `juiz`           | TEXT    | Magistrado                  |
| `classe_acao`    | TEXT    | Classe da ação              |
| `codigo`         | TEXT    | Código do assunto           |
| `descricao`      | TEXT    | Descrição do assunto        |

Existe uma relação entre as tabelas através do campo `nome_id`.

---

## 📤 Arquivo de resultados

Além do banco de dados, os resultados são armazenados em um arquivo JSON dentro do diretório:

```text
files/resultado.json
```

O arquivo possui a seguinte estrutura:

```json
{
    "processos": [
        {
            "nome_id": 1,
            "nome": "NOME CONSULTADO",
            "processo": "0000000-00.0000.0.00.0000",
            "data_atuacao": "00/00/0000",
            "situacao": "ATIVO",
            "orgao_julgador": "Órgão Julgador",
            "juiz": "Nome do Magistrado",
            "classe_acao": "Classe da Ação",
            "codigo": "000",
            "descricao": "Descrição do assunto"
        }
    ]
}
```

O JSON permite consultar e utilizar os resultados de maneira independente do banco de dados.

---

## 🚀 Instalação

### 1. Clonar o projeto

```bash
git clone <URL_DO_REPOSITORIO>
cd desafio_advice
```

### 2. Criar um ambiente virtual

Windows:

```bash
python -m venv venv
```

Ativar:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar o `.env`

Criar o arquivo `.env` na raiz:

```env
anticaptchaApiKey=SUA_CHAVE_ANTI_CAPTCHA
limiteConsulta=5
```

### 5. Executar

```bash
python main.py
```

---

## 🔐 Segurança

Informações sensíveis, como a chave da API da Anti-Captcha, devem ser armazenadas exclusivamente no arquivo `.env`.

Exemplo:

```env
anticaptchaApiKey=SUA_CHAVE
```

O `.env` está incluído no `.gitignore` para evitar que a chave seja enviada para o repositório.

Da mesma forma, arquivos gerados durante a execução, como o banco SQLite e o arquivo de resultados, estão configurados para não serem versionados.

---

## 📝 Logs

A aplicação possui um sistema de logging para acompanhar a execução.

Exemplo de mensagens:

```text
Iniciando o projeto Desafio Advice
Arquivo json com os nomes existe, seguindo processo.
Criado o arquivo de resultados.
Carregando os nomes para a variavel
Iniciando web tribunal
Iniciando openBrowser e abrindo o navegador
Chamando a função anticaptcha
CAPTCHA: XXXXX
Automação Finalizada.
```

Os logs permitem identificar em qual etapa da automação o processo está sendo executado e facilitam a identificação de eventuais problemas.

---

## ⚠️ Observações

* É necessário possuir o **Google Chrome** instalado para execução da automação.
* O Selenium utiliza o navegador Chrome para acessar o portal do TJMG.
* É necessária uma chave válida da **Anti-Captcha** para que os CAPTCHAs sejam resolvidos automaticamente.
* O número de consultas pode ser controlado através da variável `limiteConsulta` no `.env`.
* O portal consultado é um serviço externo, portanto alterações na estrutura HTML da página podem exigir ajustes nos seletores utilizados pelo Selenium.
* O banco de dados e os arquivos de resultado são gerados durante a execução e não precisam ser criados manualmente.

