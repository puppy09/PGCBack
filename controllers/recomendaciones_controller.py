from flask import Flask, request, jsonify, Blueprint, current_app
from flask_mail import Message
from app import db
from app import mail
from models.usuario_model import Usuarios
from models.medidas_model import Medidas
from models.prediccion_model import Prediccion
from models.recomendaciones_model import Recomendaciones
import random, string
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from middlewares.menu import token_requerido
import numpy as np


recomendacionBP = Blueprint('recomendacion',__name__)
@recomendacionBP.route('/ver_recomendaciones',methods=['GET'])
@token_requerido
def ver_reco(usuario):
    try:
        all_reco = Recomendaciones.query.filter_by(id_usuario=usuario.id_usuario).all()

        resultados = []
        for reco in all_reco:
            resultados.append({
                'fecha': reco.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                'recomendaciones': reco.recomendaciones,
                'clasificacion': reco.clasificacion,
                'prediccion': reco.prediccion.prediccion if reco.prediccion else None  # <-- accede al valor desde Prediccion
            })

        return jsonify({'recomendaciones':resultados})

        return
    except Exception as e:
        return jsonify({'error':str(e)}),500