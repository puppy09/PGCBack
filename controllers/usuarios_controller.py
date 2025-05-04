from flask import Flask, request, jsonify, Blueprint
from flask_mail import Message
from app import db
from app import mail
from models.usuario_model import Usuarios
import random, string


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
        new_usuario = Usuarios(nombre=nombre, ap_paterno=ap_paterno, ap_materno=ap_materno,email=email,contra=contra)
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