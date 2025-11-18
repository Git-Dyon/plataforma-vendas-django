# Plataforma de Análise Preditiva de Vendas (Pipeline MLOPS)

Este projeto é uma API RESTful completa para análise preditiva de vendas. Ele implementa um pipeline MLOPS (Engenharia de Machine Learning) de ponta-a-ponta, totalmente "dockerizado", capaz de treinar modelos de ML automaticamente e servir previsões em tempo real.
Demonstração em Vídeo (16 Minutos)

Assista ao pipeline completo em ação: desde o upload de dados (`.parquet`), passando pelo treinamento automático com **PyCaret**, até o uso da API `/predict` para fazer uma previsão de vendas em tempo real.

[Projeto 01 - Full Stack Backend](https://youtu.be/6dEGr7MWtL8)

-----

## Funcionalidades Principais

Este sistema transforma dados brutos em poder de decisão.

  * **API RESTful Segura:** Construída com **Django REST Framework (DRF)**. Os usuários só podem ver ou interagir com seus *próprios* projetos.
  * **Pipeline de Treinamento (`/train`):**
    1.  O usuário faz upload de dados históricos (`.parquet`).
    2.  O **PyCaret** (`compare_models`) é acionado para testar múltiplos algoritmos de regressão e encontrar o "vencedor".
    3.  O "cérebro" treinado (`.pkl`) e o "boletim" de performance (`JSON de Métricas`) são salvos no **PostgreSQL**.
  * **Pipeline de Previsão (`/predict`):**
    1.  O usuário envia novos dados (ex: "Quero vender Creatina a R$ 150").
    2.  A API carrega o `.pkl` treinado, faz a previsão e retorna a resposta formatada (ex: `{"previsao_de_vendas": 188}`).
  * **Pronto para Produção:** O ambiente não usa o servidor de 'dev'. Ele roda com **Gunicorn** e serve arquivos estáticos (para o `/admin`) com **Whitenoise**.
  * **Qualidade Assegurada (DevSecOps):** O projeto inclui **Testes Automatizados** com **Pytest** que provam que a API é segura e que a lógica de negócios (privacidade de dados) está funcionando.

-----

## Stack de Tecnologias

| Categoria | Tecnologia | Propósito no Projeto |
| :--- | :--- | :--- |
| **Infraestrutura** | **Docker** / **Docker Compose** | Cria uma "oficina" isolada e replicável (App + BD). |
| **Back-End** | **Python** / **Django** | O "esqueleto" de toda a aplicação e lógica de negócios. |
| **Servidor de Produção**| **Gunicorn** / **Whitenoise** | O servidor web profissional e o "ajudante" de arquivos estáticos. |
| **Banco de Dados** | **PostgreSQL** | O banco de dados profissional para armazenar projetos, usuários e modelos. |
| **API** | **Django REST Framework (DRF)** | O "garçom" que cria e protege a API RESTful (endpoints JSON). |
| **Machine Learning** | **PyCaret** (AutoML) | O "cérebro robô" que automatiza o treinamento e a seleção de modelos. |
| **Manipulação de Dados** | **Pandas** / **PyArrow** | Ferramentas para ler e manipular os dados de entrada (`.parquet`). |
| **Testes de Qualidade** | **Pytest** / **pytest-django** | A "rede de segurança" que prova a segurança e funcionalidade da API. |
| **Versionamento** | **Git** / **GitHub** | O "cofre" que armazena o histórico do código-fonte. |

-----

## Como Rodar (Localmente)

Graças ao Docker, você pode rodar este projeto MLOPS completo com 4 comandos:

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/Git-Dyon/plataforma-vendas-django.git
    cd plataforma-vendas-django
    ```

2.  **Construa e inicie os contêineres:**
    *(Isso irá instalar tudo, ligar o Gunicorn e o PostgreSQL)*

    ```bash
    docker-compose up --build
    ```

3.  **Prepare o banco de dados (em um NOVO terminal):**
    *(Espere o comando anterior estar 100% no ar antes de rodar estes)*

    ```bash
    # 1. Crie as tabelas (users, projects, mlmodels)
    docker-compose exec app python manage.py migrate

    # 2. Crie seu usuário para o painel /admin
    docker-compose exec app python manage.py createsuperuser

    # 3. Prepare o CSS do /admin para o Whitenoise
    docker-compose exec app python manage.py collectstatic --noinput
    ```

4.  **Pronto\! Seu sistema está no ar.**

      * **Painel Admin:** `http://localhost:8000/admin`
      * **API (Project List):** `http://localhost:8000/api/v1/projects/`

-----

## Endpoints da API (O "Cardápio")

| Método | Endpoint | Ação |
| :--- | :--- | :--- |
| `GET` | `/api/v1/projects/` | Lista todos os *seus* projetos. |
| `POST` | `/api/v1/projects/` | Cria um novo projeto (com upload de `.parquet`). |
| `GET` | `/api/v1/projects/{id}/` | Vê os detalhes de um projeto. |
| `POST` | `/api/v1/projects/{id}/train/` | **(ML) Dispara o treinamento de ML.** |
| `POST` | `/api/v1/projects/{id}/predict/` | **(ML) Usa o modelo treinado para fazer uma previsão.** |
