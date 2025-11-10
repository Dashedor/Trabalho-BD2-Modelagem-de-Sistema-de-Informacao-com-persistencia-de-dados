# Pré-requisitos

-Docker e Docker Compose instalados

-Python 3.8 ou superior

# Como rodar

-Baixe os arquivos da aplicação

-Abra o Prompt de comando dentro da pasta da aplicação

-Instale as dependências digitando no terminal:

    pip install -r depedencias.txt
-Inicie o contêiner com o PostgreSQL no terminal utilizando o comando:

    docker compose up -d
-Verifique se o contêiner está rodando utilizando o comando:

    docker ps
-Para executar a aplicacão digite no terminal:

    python main.py
