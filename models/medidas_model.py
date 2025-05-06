from app import db

class Medidas(db.Model):
    __tablename__ = 'tb_medidas'

    id_usuario=db.Column(db.Integer, primary_key=True)
    peso=db.Column(db.Float,nullable=False)
    altura=db.Column(db.Float,nullable=False)
    cuello=db.Column(db.Float, nullable=False)
    pecho=db.Column(db.Float,nullable=False)
    abdomen=db.Column(db.Float,nullable=False)
    cadera=db.Column(db.Float, nullable=False)
    muslo=db.Column(db.Float,nullable=False)
    bicep=db.Column(db.Float,nullable=False)
    
    def __init__(self, id_usuario, peso,altura,cuello,pecho,abdomen,cadera,muslo,bicep):
        self.id_usuario=id_usuario
        self.peso = peso
        self.altura=altura
        self.cuello=cuello
        self.pecho = pecho
        self.abdomen=abdomen
        self.cadera=cadera
        self.muslo=muslo
        self.bicep=bicep

    def __repr__(self):
        return f'tbMedidas {self.peso}'