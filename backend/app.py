import os
from flask import Flask, request, jsonify, render_template
from database import get_db
import certifi
import bcrypt
from datetime import datetime, timezone

#Importar Blueprint do tutores.py
from rotas.tutores import tutores_bp

#Mostrar para o Flask onde estão as pastas do Front-end
PASTA_BASE = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PASTA_TEMPLATES = os.path.join(PASTA_BASE, 'frontend', 'templates')
PASTA_STATIC = os.path.join(PASTA_BASE, 'frontend', 'static')

#Inicializar Flask com as pastas configuradas
app = Flask(__name__, template_folder=PASTA_TEMPLATES, static_folder=PASTA_STATIC)
db = get_db()

#Conectar blueprint nas rotas do servidor principal (app.py)
app.register_blueprint(tutores_bp)

#ROTAS VISUAIS (Tela do navegador)
@app.route('/cadastro', methods=['GET'])
def pagina_cadastro():
    """Rota que apenas desenha o HTML na tela do navegador"""
    return render_template('cadastro.html')

#MOTOR DO SERVIDOR
if __name__ == '__main__':
    #Roda o servidor na porta 5000 e ativa o modo de desenvolvimento (debug)
    app.run(debug=True, port=5000)

