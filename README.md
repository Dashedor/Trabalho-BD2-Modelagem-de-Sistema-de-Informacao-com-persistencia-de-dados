# Pre-requisitos

-Docker e Docker Compose instalados

-Python 3.8 ou superior

# Como rodar

-Baixe os arquivos da Aplicação

-Abra o Prompt de comando dentro da pasta da aplicação

-Instale as dependencias digitando no terminal:

    pip install -r depedencias.txt
-Inicie o container com o Postgresql no terminal utilizando o comando:

    docker compose up -d
-Verifique se o container esta rodando utilizando o comando:

    docker ps
-Para executar a aplicão digite no terminal:

    python main.py
