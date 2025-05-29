from flask import Flask, request, jsonify, Blueprint, current_app
from flask_mail import Message
from app import db
from app import mail
from models.usuario_model import Usuarios
from models.medidas_model import Medidas
from models.recomendaciones_model import Recomendaciones
from models.prediccion_model import Prediccion
import random, string
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from middlewares.menu import token_requerido

usuarios_adminBP = Blueprint('usuarios_admin',__name__)

def generar_contraseña():
    caracteres = string.ascii_letters + string.digits
    contra = ''.join(random.choice(caracteres) for _ in range(10))
    return contra

@usuarios_adminBP.route('/registrar_admin',methods=['POST'])
def registrar_usuario():
    try:
        data=request.get_json()
        nombre=data['nombre']
        email=data['email']
        ap_paterno=data['ap_paterno']
        ap_materno=data['ap_materno']
        sexo=data['sexo']
    
        

        if Usuarios.query.filter_by(email=email).first():
            return jsonify({'error':'El correo ya esta registrado'}),400
        
        contra = generar_contraseña()
        contraHashed=generate_password_hash(contra)
        new_usuario = Usuarios(nombre=nombre, ap_paterno=ap_paterno, ap_materno=ap_materno,email=email,contra=contraHashed, sexo=sexo, estatus='A')
        db.session.add(new_usuario)
        db.session.commit()

        msg = Message(
            'Confirmacion de Correo Electronico', recipients=[email]
        )
        msg.body=f'Bienvenido {nombre}, se ha generado una contraseña para que entres por primera vez al sistema. Podras cambiarla una vez ingreses. Tu contraseña es:  {contra}'
        mail.send(msg)
        return jsonify({'message':'Usuario registrado con exito'}), 200
    except Exception as e:
        return jsonify({'error':str(e)}),500
    
@usuarios_adminBP.route('/login_admin',methods=['POST'])
def login():
    try:
        data=request.get_json()
        email = data.get('email')
        contra=data.get('contra')

        usuario = Usuarios.query.filter_by(email=email).first()

        if not usuario or not check_password_hash(usuario.contra, contra) or usuario.estatus != 'A':
            return jsonify({'Error':'Credenciales invalidas'}),401
        
        token = jwt.encode({
            'id_usuario': usuario.id_usuario,
        },current_app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token':token})

    except Exception as e:
        return jsonify({'error':str(e)}),500
    
@usuarios_adminBP.route('/panel',methods=['GET'])
@token_requerido
def verPacientes(usuario):
    try:
        pacientes = Usuarios.query.filter_by(estatus='P').all()

        pacientes_json = [{
            'id_usuario': p.id_usuario,
            'nombre': p.nombre,
            'ap_paterno': p.ap_paterno,
            'ap_materno': p.ap_materno,
            'email': p.email,
            'sexo': p.sexo,
            'estatus': p.estatus
        } for p in pacientes]


        return jsonify({'pacientes': pacientes_json})
    except Exception as e:
        return jsonify({'error':str(e)}),500

@usuarios_adminBP.route('/ver_paciente',methods=['GET'])
@token_requerido
def ver_paciente(usuario):
    try:
        data = request.get_json()
        paciente=data.get('paciente')

        pacienteFind = Usuarios.query.filter_by(id_usuario=paciente).first()

        if not pacienteFind:
            return jsonify({'error':'No se encuentro el paciente'})
        
        ultima_medida = Medidas.query.filter_by(id_usuario=pacienteFind.id_usuario).order_by(Medidas.fecha.desc()).first()

        ultima_prediccion = Prediccion.query.filter_by(id_usuario=pacienteFind.id_usuario).order_by(Prediccion.fecha.desc()).first()

        ultima_recomendacion = Recomendaciones.query.filter_by(id_usuario=pacienteFind.id_usuario).order_by(Recomendaciones.fecha.desc()).first()

        paciente_json = {
            'id_usario': pacienteFind.id_usuario,
            'nombre': pacienteFind.id_usuario,
            'ap_paterno':pacienteFind.ap_paterno,
            'ap_materno':pacienteFind.ap_materno,
            'email':pacienteFind.email,
            'sexo': pacienteFind.sexo,
            'ultima_medida':{
                'peso':ultima_medida.peso,
                'altura':ultima_medida.altura,
                'pecho':ultima_medida.pecho,
                'abdomen':ultima_medida.abdomen,
                'cadera':ultima_medida.cadera
            } if ultima_medida else None,
            'ultima_prediccion':{
                'prediccion':ultima_prediccion.prediccion
            } if ultima_prediccion else None,
            'ultima_recomendacion':{
                'clasificacion':ultima_recomendacion.clasificacion,
                'recomendaciones': ultima_recomendacion.recomendaciones,
            } if ultima_recomendacion else None           
        }
        return jsonify({'paciente':paciente_json})
    except Exception as e:
        return  jsonify({'error':str(e)}),500

@usuarios_adminBP.route('/corregir', methods=['PUT'])
@token_requerido
def corregir_datospaciente(usuario):
    try:
        data = request.get_json()
        paciente = data.get('paciente')
        altura=data.get('altura')
        peso=data.get('peso')
        pecho=data.get('pecho')
        abdomen=data.get('abdomen')
        cadera=data.get('cadera')
        pgc = data.get('pgc')
        clasificacion = data.get('clasificacion')
        recomendaciones=data.get('recomendaciones')

        #paciente = Usuarios.query.filter_by(id_usuario=paciente).first()
        #if not paciente:
        #    return jsonify({'error': 'Paciente no encontrado'}), 404
        
        ultima_medida = Medidas.query.filter_by(id_usuario=paciente).order_by(Medidas.fecha.desc()).first()
        if ultima_medida:
            ultima_medida.altura = altura
            ultima_medida.peso = peso
            ultima_medida.pecho = pecho
            ultima_medida.abdomen = abdomen
            ultima_medida.cadera = cadera

        ultima_prediccion = Prediccion.query.filter_by(id_usuario=paciente).order_by(Prediccion.fecha.desc()).first()
        if ultima_prediccion:
            ultima_prediccion.prediccion = pgc

        ultima_recomendacion = Recomendaciones.query.filter_by(id_usuario=paciente).order_by(Recomendaciones.fecha.desc()).first()
        if ultima_recomendacion:
            ultima_recomendacion.clasificacion = clasificacion
            ultima_recomendacion.recomendaciones = recomendaciones

        db.session.commit()
        return jsonify({'message': 'Datos actualizados correctamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500