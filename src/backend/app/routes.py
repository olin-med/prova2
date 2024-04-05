from .models import Database
from datetime import datetime
from flask import request, jsonify, Blueprint, render_template, redirect, Response

db = Database('database/db.json')
banco = []

main = Blueprint('main', __name__)

@main.route('/')
def index():
    banco.append({
    "endereco":request.environ['REMOTE_ADDR'],
    "metodo": request.method,
    "hora":datetime.now()
    })
    registry = db.get_all_registrations()
    return render_template('index.html', registry=registry)

@main.route('/echo', methods=['POST'])
def add_registry():
    registry = request.form.get('registry')
    db.add_registry(registry)
    response = Response(status=200)
    response.headers['HX-Redirect'] = '/'
    return response


@main.route('/ping', methods=['GET'])
def ping():
    return {"response": "pong"}


@main.route('/dash')
def retorna_requisicoes():
    return render_template('info.html', logs=banco)

@main.route('/info', methods=['GET'])
def get_logs():
    logs_html = ""
    for log in banco:
        logs_html += f"<p>{log['endereco']} - {log['metodo']} - {log['hora']}</p>"
    return logs_html