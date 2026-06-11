import os
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi


#Carrega as senhas do meu cofre .env
load_dotenv()

MONGO_URI = os.getenv("URL_BANCO")

def get_db():
    #Docstring
    """
    Estabelece a conexão com o cluster do MongoDB e retorna o banco de dados
    """
    if not MONGO_URI:
        raise ValueError("ERRO: URL_BANCO não encontrada no .env!")
    
    try:
        #Tenta conectar ao servidor, usando o certifi como "passaporte"
        client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

        #Acessa o banco de dados principal do sistema, ou cria se não existe (Schema dinâmico)
        db = client["petsync_db"]

        #Teste rápido para ver se o banco está respondendo
        client.admin.command('ping')
        print("Conexão com o MongoDB estabelecida com sucesso!")

        return db
    except Exception as e:
        print(f"Erro ao conectar no banco:{e}")
        return None
