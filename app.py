from flask import Flask
from flask_sqlalchemy import SQLAlchemy #classe que faz conexão com o banco de dados

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key" #secret key. utilizado pelo flask
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" #URI. o caminho em que o SQLAlchemy vai conectar o banco

#sqlite:///database.db representa o nome do banco de dados a ser utilizado sendo representado pelo caminho do arquivo

db = SQLAlchemy(app) #variável que vai armazenar a instância da classe SQLAlchemy.

# Session <- conexão ativa

@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello world"

if __name__ == "__main__":
    app.run(debug=True)