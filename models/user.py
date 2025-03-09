from app import db #variável declarada no app.py
from flask_login import UserMixin #utilizada para programar o login

#Criando usuário

'''O usuário vai ser criado utilizando a ajuda da variável db (que é uma instância do SQLAlchemy)'''

class User(db.Model, UserMixin):  #classe herdada do db.Model, que da a base para o flask alchemy reconhecer a classe como algo mapeável.

    #id (int), username (text), password (text)
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable = False, unique = True) #string com 80 caracteres, obrigatoriamente tem que ser um campo preenchido e registro único.
    password = db.Column(db.String(80), nullable = False)

    