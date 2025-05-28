from app import db

class Usuarios(db.Model):
    __tablename__ = 'tb_usuarios'

    id_usuario=db.Column(db.Integer, primary_key=True, autoincrement = True)
    nombre=db.Column(db.String(50),nullable=False)
    ap_paterno=db.Column(db.String(50),nullable=False)
    ap_materno=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(100), unique=True, nullable=False)
    contra=db.Column(db.String(100),nullable=False)
    sexo=db.Column(db.String(1))
    estatus=db.Column(db.String(1), default='P')

    def __init__(self, nombre, ap_paterno, ap_materno,email, contra, sexo, estatus):
        self.nombre = nombre
        self.ap_paterno=ap_paterno
        self.ap_materno=ap_materno
        self.email = email
        self.contra=contra
        self.sexo=sexo
        self.estatus = estatus

    def __repr__(self):
        return f'TbUsuarios {self.nombre}'