from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes import main as main_blueprint
from flask_mail import Mail
from flask_cors import CORS
from tensorflow.keras.models import load_model
import pickle



db = SQLAlchemy()

mail = Mail()
def create_app():
    app = Flask(__name__, instance_relative_config=True)

    modelo = load_model('modelo_ann/modelo_entrenado.h5', compile=False)
    print("Modelo cargado")
    app.modelo = modelo

    with open('modelo_ann/scaler.pkl','rb') as f:
        scaler = pickle.load(f)
    print("Scaler cargado")
    app.scaler = scaler
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_pgc.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT']=587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE SSL'] = False
    app.config['MAIL_USERNAME']='sweeneyoficial@gmail.com'
    app.config['MAIL_PASSWORD']='cehf yvsq tfsy nsmg'
    app.config['MAIL_DEFAULT_SENDER']='sweeneyoficial@gmail.com'
    app.config['SECRET_KEY']='secreto0009'

    mail.init_app(app)
    db.init_app(app)


    from .routes import main as main_blueprint
    from controllers.usuarios_controller import usuariosBP
    from controllers.medidas_controller import medidasBP
    from controllers.prediccion_controller import prediccionBP
    from controllers.recomendaciones_controller import recomendacionBP
    from controllers.admin_controller import usuarios_adminBP

    app.register_blueprint(main_blueprint)
    app.register_blueprint(usuariosBP)
    app.register_blueprint(medidasBP)
    app.register_blueprint(prediccionBP)
    app.register_blueprint(recomendacionBP)
    app.register_blueprint(usuarios_adminBP)

    # Configurar CORS: en producción solo permite el dominio específico
    import os
    if os.environ.get('FLASK_ENV') == 'production' or not app.debug:
        CORS(app, resources={r"/*": {
            "origins": ["https://proyectomedico.xyz"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }})
    else:
        CORS(app)  # En desarrollo permite todos los orígenes
   # app.register_blueprint(main_blueprint)
    return app

