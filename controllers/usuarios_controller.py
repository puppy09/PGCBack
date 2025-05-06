from flask import Flask, request, jsonify, Blueprint, current_app
from flask_mail import Message
from app import db
from app import mail
from models.usuario_model import Usuarios
import random, string
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from middlewares.menu import token_requerido

usuariosBP = Blueprint('usuarios',__name__)

def generar_contraseña():
    caracteres = string.ascii_letters + string.digits
    contra = ''.join(random.choice(caracteres) for _ in range(10))
    return contra

@usuariosBP.route('/registrar',methods=['POST'])
def registrar_usuario():
    try:
        data=request.get_json()
        nombre=data['nombre']
        email=data['email']
        ap_paterno=data['ap_paterno']
        ap_materno=data['ap_materno']
        

        #if Usuarios.query.filter_by(email=email).first():
        #    return jsonify({'error':'El correo ya esta registrado'}),400
        
        contra = generar_contraseña()
        contraHashed=generate_password_hash(contra)
        new_usuario = Usuarios(nombre=nombre, ap_paterno=ap_paterno, ap_materno=ap_materno,email=email,contra=contraHashed)
        db.session.add(new_usuario)
        db.session.commit()

        msg = Message(
            'Confirmacion de Correo Electronico', recipients=[email]
        )
        msg.body=f'Bienvenido {nombre}, se ha generado una contraseña para que entres por primera vez al sistema. {contra}. Podras cambiarla una vez ingreses'
        mail.send(msg)
        return jsonify({'message':'Usuario registrado con exito'}), 200
    except Exception as e:
        return jsonify({'error':str(e)}),500
    
@usuariosBP.route('/',methods=['POST'])
def login():
    try:
        data=request.get_json()
        email = data.get('email')
        contra=data.get('contra')

        usuario = Usuarios.query.filter_by(email=email).first()

        if not usuario or not check_password_hash(usuario.contra, contra):
            return jsonify({'Error':'Credenciales invalidas'}),401
        
        token = jwt.encode({
            'id_usuario': usuario.id_usuario,
        },current_app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token':token})

    except Exception as e:
        return jsonify({'error':str(e)}),500

@usuariosBP.route('/perfil',methods=['GET'])
@token_requerido
def obtener_perfil(request):
    id_usuario=request.id_usuario
    usuario=Usuarios.query.get(id_usuario)

    if not usuario:
        return jsonify({'error':'Usuario no encontrado'}),404
    
    return jsonify({
        'id':usuario.id_usuario,
        'nombre':usuario.nombre,
        'email':usuario.email
    })

@usuariosBP.route('/cambiar_contra',methods=['PUT'])
@token_requerido
def cambiar_contra(usuario):
    try:

        data = request.get_json()
        contra=data.get('contra')
        nueva_contra=data.get('nueva_contra')
        conf_nueva_con=data.get('conf_nueva_con')

        if not usuario or not check_password_hash(usuario.contra, contra):
            return jsonify({'error':'Usuario no encontrado o contraseña incorrecta'}),404
    
        if nueva_contra != conf_nueva_con:
            return jsonify({'error':'La contraseña nueva no coincide'}),500
    
        contraHashed=generate_password_hash(nueva_contra)
        usuario.contra=contraHashed
        db.session.commit()
        return jsonify({'message':'Contraseña cambiada con exito'})
    except Exception as e:
        return jsonify({'error':str(e)}),500
    



