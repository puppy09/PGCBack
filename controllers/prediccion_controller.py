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
        
        id_usuario=usuario.id_usuario
        usuariofind=Usuarios.query.get(id_usuario)
        auxGender = usuariofind.sexo


        new_medidas = Medidas(id_usuario=usuario.id_usuario, peso=peso, altura=altura, pecho=pecho, abdomen=abdomen, cadera=cadera)
        db.session.add(new_medidas)
        db.session.commit()

        nueva_prediccion = Prediccion(id_usuario=usuario.id_usuario, prediccion=prediccion)
        db.session.add(nueva_prediccion)
        db.session.commit()

        resultados = clasificacion(prediccion[0], auxGender)

        return jsonify({'prediccion':prediccion.tolist(), 'clasificacion':resultados['clasificacion'], 'recomendaciones':resultados['recomendaciones']})
    except Exception as e:
        return jsonify({'error':str(e)}),500


def clasificacion(pgc, genero):
    try:
        clasificacion = ''
        recomendaciones = []
        if genero == 'M':
            if pgc >= 6 and pgc <= 13:
                clasificacion = 'Atleta'
                recomendaciones = ['Ingesta adecuada de proteínas: Consume 1.6-2.2 g por kg de peso corporal, priorizando fuentes magras como pollo, pescado, claras de huevo y legumbres.','Carbohidratos estratégicos: Mantén una buena energía con carbohidratos complejos como arroz integral, avena, pan integral, legumbres como frijol, garbanzo lentejas; ajustando cantidad según actividad física.', 'Grasas saludables: Incluye grasas monoinsaturadas y poliinsaturadas como aguacate, frutos secos y aceite de oliva, clave para funciones hormonales.','Fibra para la digestión: Verduras y frutas mejoran el tránsito intestinal y la absorción de nutrientes.','Hidratación óptima: Mantén una ingesta suficiente de agua según actividad y clima.','Entrenamiento bien estructurado: Prioriza el trabajo de fuerza para mantener masa muscular, combinado con cardio moderado según objetivos específicos.']
            
            if pgc >= 14 and pgc <= 17:
                clasificacion = 'Fitness'
                recomendaciones = ['Calorías bien ajustadas: Consume lo suficiente para mantener energía sin generar acumulación de grasa. Usa herramientas para estimar tu gasto calórico.','Distribución de macronutrientes ideal: Mantén un equilibrio entre proteínas (1.6-2.2 g/kg) carbohidratos complejos y grasas saludables según tus actividades.','Entrenamiento estructurado: Prioriza el trabajo de fuerza para conservar masa muscular y agrega cardio moderado si lo necesitas para rendimiento y salud cardiovascular.','Calidad sobre cantidad en la alimentación: Evita ultraprocesados y prioriza alimentos naturales, ricos en micronutrientes esenciales.','Descanso y recuperación: El sueño es esencial para mantener el metabolismo eficiente y optimizar la composición corporal.','Monitoreo periódico: Ajusta en función de cómo responde tu cuerpo, observando progresos con mediciones o bioimpedancia.']

            if pgc >= 18 and pgc <= 24:
                clasificacion = 'Promedio'
                recomendaciones = ['Balance calórico adecuado: Consume las calorías necesarias para mantener tu energía sin generar exceso de grasa corporal.','Macronutrientes equilibrados: Mantén una distribución adecuada entre proteínas (1.2-2 g/kg de peso), carbohidratos complejos y grasas saludables.','Variedad nutricional: Incluye alimentos naturales ricos en vitaminas y minerales, como frutas, verduras, legumbres y proteínas magras.','Ejercicio regular: Integra una combinación de entrenamiento de fuerza y actividad cardiovascular para mantener una composición estable.','Hidratación adecuada: Bebe suficiente agua para favorecer el metabolismo y la función celular.','Descanso de calidad: Dormir bien es fundamental para mantener un metabolismo eficiente.','Monitoreo: Observa cómo responde tu cuerpo y ajusta alimentación y entrenamiento según necesidades.']

            if pgc >= 25:
                clasificacion = 'Obesidad'
                recomendaciones = ['Prioriza proteínas magras: Ayudan a preservar masa muscular y aumentan la saciedad. Incluye pollo, pescado, huevos y legumbres.','Reduce azúcares y harinas refinadas: Opta por carbohidratos integrales como avena, quinoa y arroz integral para mejor energía.','Aumenta fibra: Favorece la digestión y el control del apetito. Consume más verduras, frutas y semillas.','Controla porciones: Usa platos más pequeños y come con atención para evitar excesos.','Hidratación constante: El agua es fundamental para el metabolismo y la eliminación de toxinas.','Actividad física regular: Complementa tu alimentación con ejercicios de fuerza y cardiovasculares para mejorar tu composición corporal.']

        if genero == 'F':
            if pgc >= 14 and pgc <= 20:
                clasificacion = 'Atleta'
                recomendaciones = ['Ingesta adecuada de proteínas: Consume 1.6-2.2 g por kg de peso corporal, priorizando fuentes magras como pollo, pescado, claras de huevo y legumbres.','Carbohidratos estratégicos: Mantén una buena energía con carbohidratos complejos como arroz integral, avena, pan integral, legumbres como frijol, garbanzo lentejas; ajustando cantidad según actividad física.', 'Grasas saludables: Incluye grasas monoinsaturadas y poliinsaturadas como aguacate, frutos secos y aceite de oliva, clave para funciones hormonales.','Fibra para la digestión: Verduras y frutas mejoran el tránsito intestinal y la absorción de nutrientes.','Hidratación óptima: Mantén una ingesta suficiente de agua según actividad y clima.','Entrenamiento bien estructurado: Prioriza el trabajo de fuerza para mantener masa muscular, combinado con cardio moderado según objetivos específicos.']
            
            if pgc >= 21 and pgc <= 24:
                clasificacion = 'Fitness'
                recomendaciones = ['Calorías bien ajustadas: Consume lo suficiente para mantener energía sin generar acumulación de grasa. Usa herramientas para estimar tu gasto calórico.','Distribución de macronutrientes ideal: Mantén un equilibrio entre proteínas (1.6-2.2 g/kg) carbohidratos complejos y grasas saludables según tus actividades.','Entrenamiento estructurado: Prioriza el trabajo de fuerza para conservar masa muscular y agrega cardio moderado si lo necesitas para rendimiento y salud cardiovascular.','Calidad sobre cantidad en la alimentación: Evita ultraprocesados y prioriza alimentos naturales, ricos en micronutrientes esenciales.','Descanso y recuperación: El sueño es esencial para mantener el metabolismo eficiente y optimizar la composición corporal.','Monitoreo periódico: Ajusta en función de cómo responde tu cuerpo, observando progresos con mediciones o bioimpedancia.']

            if pgc >= 25 and pgc <= 31:
                clasificacion = 'Promedio'
                recomendaciones = ['Balance calórico adecuado: Consume las calorías necesarias para mantener tu energía sin generar exceso de grasa corporal.','Macronutrientes equilibrados: Mantén una distribución adecuada entre proteínas (1.2-2 g/kg de peso), carbohidratos complejos y grasas saludables.','Variedad nutricional: Incluye alimentos naturales ricos en vitaminas y minerales, como frutas, verduras, legumbres y proteínas magras.','Ejercicio regular: Integra una combinación de entrenamiento de fuerza y actividad cardiovascular para mantener una composición estable.','Hidratación adecuada: Bebe suficiente agua para favorecer el metabolismo y la función celular.','Descanso de calidad: Dormir bien es fundamental para mantener un metabolismo eficiente.','Monitoreo: Observa cómo responde tu cuerpo y ajusta alimentación y entrenamiento según necesidades.']

            if pgc >= 32:
                clasificacion = 'Obesidad'
                recomendaciones = ['Prioriza proteínas magras: Ayudan a preservar masa muscular y aumentan la saciedad. Incluye pollo, pescado, huevos y legumbres.','Reduce azúcares y harinas refinadas: Opta por carbohidratos integrales como avena, quinoa y arroz integral para mejor energía.','Aumenta fibra: Favorece la digestión y el control del apetito. Consume más verduras, frutas y semillas.','Controla porciones: Usa platos más pequeños y come con atención para evitar excesos.','Hidratación constante: El agua es fundamental para el metabolismo y la eliminación de toxinas.','Actividad física regular: Complementa tu alimentación con ejercicios de fuerza y cardiovasculares para mejorar tu composición corporal.']
        return {
            'clasificacion':clasificacion,
            'recomendaciones':recomendaciones
        }
    except Exception as e:
        return 'Error al clasificar'