from app import db
from datetime import datetime

class Prediccion(db.Model):
    __tablename__ = 'tb_prediccion'

    id_prediccion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario=db.Column(db.Integer, primary_key=True)
    prediccion=db.Column(db.Float,nullable=False)
    fecha = db.Column(db.DateTime, default = datetime.now)
    
    def __init__(self, id_usuario, prediccion):
        self.id_usuario=id_usuario
        self.prediccion = prediccion
    def __repr__(self):
        return f'tbPrediccion {self.prediccion}'