from flask import Blueprint, request, jsonify
from database import get_db
import bcrypt
from datetime import datetime, timezone

#Criando a Blueprint exclusiva para tutores
tutores_bp = Blueprint('tutores', __name__)

@tutores_bp.route('/api/cadastro', methods=['POST'])
def api_cadastro_tutor():
    """
    Rota para cadastrar um novo tutor no sistema.
    Recebe os dados do Front-end, valida, criptografa a senha e salva no banco de dados.
    """

    db = get_db()
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
        "data_criacao": datetime.now(timezone.utc)
    }

    #Salvando no banco de dados
    colecao_tutores.insert_one(novo_tutor)
    return jsonify({"mensagem": "Tutor cadastrado com sucesso!"}), 201 #Código de HTML de Sucesso