import os
from flask import Flask, request, jsonify, render_template
from database import get_db
import certifi
import bcrypt
from datetime import datetime

#Mostrar para o Flask onde estão as pastas do Front-end
PASTA_BASE = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PASTA_TEMPLATES = os.path.join(PASTA_BASE, 'frontend', 'templates')
PASTA_STATIC = os.path.join(PASTA_BASE, 'frontend', 'static')

#Inicializar Flask com as pastas configuradas
app = Flask(__name__, template_folder=PASTA_TEMPLATES, static_folder=PASTA_STATIC)
db = get_db()

#ROTAS VISUAIS (Tela do navegador)
@app.route('/cadastro', methods=['GET'])
def pagina_cadastro():
    """Rota que apenas desenha o HTML na tela do navegador"""
    return render_template('cadastro.html')



#ROTAS DE API (Comunicação com o banco)
@app.route('/api/cadastro', methods=['POST'])
def cadastro_tutor():
    """
    Rota para cadastrar um novo tutor no sistema.
    Recebe os dados do Front-end, valida, criptografa a senha e salva no banco de dados.
    """
    if db is None:
        return jsonify({"erro": "Erro interno de conexão com o banco de dados"}), 500 #Erro 500 é o código de erro interno
    
    #Puxa os dados que vierem do Front-end
    dados = request.get_json()
    nome = dados.get('nome')
    email = dados.get('email')
    telefone = dados.get('telefone')
    senha_plana = dados.get('senha')

    #Validação Básica: Conferir se não há campos vazios
    if not all([nome, email, telefone, senha_plana]):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400 #Erro 400 é código de erro no cliente

    #Accessa a "gaveta" de tutores no banco
    colecao_tutores = db['tutores']

    #Regra de negócio, o email não pode ser repetido
    if colecao_tutores.find_one({"email": email}):
        return jsonify({"erro": "Este email já está cadastrado no sistema!"}), 409
    
    #Segurança: Criptografando a senha antes de salvar
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha_plana.encode('utf-8'), salt)

    #Montando o "pacote" para salvar no MongoDB
    novo_tutor = {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "senha": senha_hash,
        "data_criacao": datetime.utcnow()
    }

    #Salvando no banco de dados
    colecao_tutores.insert_one(novo_tutor)
    return jsonify({"mensagem": "Tutor cadastrado com sucesso!"}), 201 #Código de HTML de Sucesso


#MOTOR DO SERVIDOR
if __name__ == '__main__':
    #Roda o servidor na porta 5000 e ativa o modo de desenvolvimento (debug)
    app.run(debug=True, port=5000)

