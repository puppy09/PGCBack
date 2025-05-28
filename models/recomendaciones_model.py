from app import db
from datetime import datetime

class Recomendaciones(db.Model):
    __tablename__ = 'tb_recomendaciones'

    id_prediccion=db.Column(db.Integer, primary_key=True)
#    prediccion=db.Column(db.Float,nullable=False)
    fecha = db.Column(db.DateTime, default = datetime.now)
    recomendaciones = db.Column(db.String(1000), nullable=False)
    clasificacion = db.Column(db.String(50), nullable=False)

    
    def __init__(self, id_prediccion, recomendaciones, clasificacion):
        self.id_prediccion = id_prediccion
        self.recomendaciones = recomendaciones
        self.clasificacion = clasificacion
    def __repr__(self):
        return f'tbRecomendaciones {self.clasificacion}'