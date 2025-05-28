from app import db
from datetime import datetime

class Recomendaciones(db.Model):
    __tablename__ = 'tb_recomendaciones'

    id_recomendacion = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_prediccion = db.Column(db.Integer, db.ForeignKey('tb_prediccion.id_prediccion'))
#    prediccion=db.Column(db.Float,nullable=False)
    fecha = db.Column(db.DateTime, default = datetime.now)
    recomendaciones = db.Column(db.String(1000), nullable=False)
    clasificacion = db.Column(db.String(50), nullable=False)
    id_usuario = db.Column(db.Integer)

    prediccion = db.relationship("Prediccion", backref="recomendaciones")
    
    def __init__(self, id_prediccion, recomendaciones, clasificacion, id_usuario):
        self.id_prediccion = id_prediccion
        self.recomendaciones = recomendaciones
        self.clasificacion = clasificacion
        self.id_usuario = id_usuario
    def __repr__(self):
        return f'tbRecomendaciones {self.clasificacion}'