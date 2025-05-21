from flask import Flask, request, jsonify, Blueprint, current_app
from flask_mail import Message
from app import db
from app import mail
from models.usuario_model import Usuarios
from models.medidas_model import Medidas
import random, string
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from middlewares.menu import token_requerido

medidasBP = Blueprint('medidas',__name__)

@medidasBP.route('/hacer_prediccion',methods=['POST'])
@token_requerido
def hacer_prediccion(usuario):
    try:
        print(f"Usuaro",usuario.id_usuario)
        data = request.get_json()
        peso=data.get('peso')
        altura=data.get('altura')
        #cuello=data.get('cuello')
        pecho=data.get('pecho')
        abdomen=data.get('abdomen')
        cadera=data.get('cadera')
        #muslo=data.get('muslo')
        #bicep=data.get('bicep')

        new_medidas = Medidas(id_usuario=usuario.id_usuario, peso=peso, altura=altura, pecho=pecho, abdomen=abdomen, cadera=cadera)
        db.session.add(new_medidas)
        db.session.commit()
        return jsonify({'message':'Medidas guardadas con exito'})
    except Exception as e:
        return jsonify({'error':str(e)}),500