from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes import main as main_blueprint
from flask_mail import Mail
from flask_cors import CORS


db = SQLAlchemy()

mail = Mail()
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
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

    app.register_blueprint(main_blueprint)
    app.register_blueprint(usuariosBP)
    app.register_blueprint(medidasBP)

    CORS(app)
   # app.register_blueprint(main_blueprint)
    return app

