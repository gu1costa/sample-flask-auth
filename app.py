from flask import Flask, request, jsonify
from models.user import User
from database import db #utilizado para passar o aplicativo para o db em database.
from flask_login import LoginManager #classe que vai ser responsável pelo gerenciamento do usuário.
from flask_login import login_user, current_user, logout_user, login_required
import bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key" #secret key. utilizado pelo flask

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:admin123@127.0.0.1:3306/flask-crud" #URI. o caminho em que o SQLAlchemy vai conectar o banco

#sqlite:///database.db representa o nome do banco de dados a ser utilizado sendo representado pelo caminho do arquivo

login_manager = LoginManager()
db.init_app(app) #inicializa
login_manager.init_app(app)

#View login
login_manager.login_view = "login"

# Session <- conexão ativa

@login_manager.user_loader  #recupera o objeto cadastrado no banco de dados.
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/login", methods=["POST"])
def login():
    data = request.json #pega os dados do usuário. importada do flask
    username = data.get("username")
    password = data.get("password")

    #Autenticação
    if username and password:
        # Login
        #buscando usuário na base de dados
        user = User.query.filter_by(username= username).first()

        #buscando senha na base de dados
        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)) == password: #se a senha do usuário foi igual a senha recebida.
            login_user(user)  #autenticação do usuário.
            print(current_user.is_authenticated)
            return jsonify({"message": "Autenticação realizada com sucesso."})            
    
        return jsonify({"message": "Credenciais inválidas."}), 400

#Logout
@app.route("/logout", methods=["GET"])
@login_required #Protegendo a rota de usuários que não estão autenticados
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso."})

#Cadastro
@app.route("/user", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username= username, password= hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso."})

    return jsonify({"message": "Dados inválidos."}), 400

#Recuperando informações do usuário.
@app.route("/user/<int:id_user>", methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return {"username": user.username}
    
    return jsonify({"message": "Usuário não encontrado."}), 404

@app.route("/user/<int:id_user>", methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if id_user != current_user.id and current_user.role == "user":
        return jsonify({"message": "Operação não permitida."}), 403
    '''controla as permissões de admin.'''

    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()

        return jsonify({"message": f"Usuário {id_user} atualizado com sucesso."})
    
    return jsonify({"message": "Usuário não encontrado."}), 404

#Delete
@app.route("/user/<int:id_user>", methods=["DELETE"])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if current_user.role != "admin":
        return jsonify({"message": "Operação não permitida."}), 403

    if id_user == current_user.id:
        return jsonify({"message": "Deleção não permitida."}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} deletado com sucesso."})
    
    return jsonify({"message": "Usuário não encontrado."}), 404

@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello world"

if __name__ == "__main__":
    app.run(debug=True)