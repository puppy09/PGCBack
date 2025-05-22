from flask import Flask, request, jsonify, Blueprint, current_app
from flask_mail import Message
from app import db
from app import mail
from models.usuario_model import Usuarios
from models.medidas_model import Medidas
from models.prediccion_model import Prediccion
import random, string
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from middlewares.menu import token_requerido
import numpy as np

prediccionBP = Blueprint('prediccion',__name__)

@prediccionBP.route('/predecir',methods=['POST'])
@token_requerido
def predecir(usuario):
    try:
        data=request.get_json()
        altura=data.get('altura')
        peso=data.get('peso')
        pecho=data.get('pecho')
        abdomen=data.get('abdomen')
        cadera=data.get('cadera')

        required_fields = ['abdomen','altura','peso','pecho','cadera']
        features = [float(data[field]) for field in required_fields]

        input_array = np.array([features])

        modelo = current_app.modelo
        prediccion = modelo.predict(input_array)

        new_medidas = Medidas(id_usuario=usuario.id_usuario, peso=peso, altura=altura, pecho=pecho, abdomen=abdomen, cadera=cadera)
        db.session.add(new_medidas)
        db.session.commit()

        nueva_prediccion = Prediccion(id_usuario=usuario.id_usuario, prediccion=prediccion)
        db.session.add(nueva_prediccion)
        db.session.commit()

        return jsonify({'prediccion':prediccion.tolist()})
    except Exception as e:
        return jsonify({'error':str(e)}),500
