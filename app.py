from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# Configuração da aplicação Flask
app = Flask(__name__)

# --- Configuração do SQLAlchemy ---
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'instance', 'cadastro.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Modelo do Banco de Dados ---
class Cadastro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    cidade = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Cadastro {self.nome}>'

# --- Rotas da Aplicação ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form.get('nome')
        idade_str = request.form.get('idade')
        cidade = request.form.get('cidade')
        
        try:
            idade = int(idade_str)
            novo_cadastro = Cadastro(nome=nome, idade=idade, cidade=cidade)
            
            db.session.add(novo_cadastro)
            db.session.commit()
            
            return redirect(url_for('listar'))
            
        except ValueError:
            return "Erro: A idade fornecida não é um número válido.", 400
            
        except Exception as e:
            print(f"Erro ao salvar no banco de dados: {e}")
            db.session.rollback()
            return "Ocorreu um erro interno ao salvar o cadastro.", 500

@app.route('/lista')
def listar():
    pessoas = Cadastro.query.all()
    return render_template('lista.html', pessoas=pessoas)


if __name__ == '__main__':
    # 1. Garante que a pasta 'instance' exista
    if not os.path.exists(os.path.join(base_dir, 'instance')):
        os.makedirs(os.path.join(base_dir, 'instance'))
        
    # 2. Inicializa o DB e cria as tabelas (dentro do contexto da aplicação)
    with app.app_context():
        db.create_all()
        
    # 3. Executa o servidor
    app.run(debug=True, port=5000)