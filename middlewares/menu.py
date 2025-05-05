from flask import Flask, request, jsonify, Blueprint, current_app
from flask_mail import Message
from app import db
from app import mail
from models.usuario_model import Usuarios
import random, string
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps

def token_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        token: None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token:
            return jsonify({'error':'Token Requerido'}),401
        
        try:
            datos=jwt.decode(token, current_app.config['SECRET_KEY'],algorithms=['HS256'])
            usuario=Usuarios.query.get(datos['id_usuario'])
        except:
            return jsonify({'error':'Token inválido o expirado'}), 401
        
        return f(usuario,*args,**kwargs)
    return decorador


