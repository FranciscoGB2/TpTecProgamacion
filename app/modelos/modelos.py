from config import db

class Admin(db.Model):
    __tablename__ = 'administrador'

    id_admin = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'Admin {self.id_admin}>'

class Carrera(db.Model):
    __tablename__ = 'carrera'

    id_carrera = db.Column(db.Integer, primary_key=True)
    id_administrador = db.Column(db.Integer, db.ForeignKey('administrador.id_admin'), nullable=False)
    id_caballo_ganador = db.Column(db.Integer, nullable=True)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(100), nullable=False)

    # Define a relationship to the Admin model
    administrador = db.relationship('Admin', backref=db.backref('carrera', lazy=True))

    def __repr__(self):
        return f'Carrera {self.id_carrera}>'
# FILE: modelos.py

class Apuesta(db.Model):
    __tablename__ = 'apuesta'

    id_apuesta = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    id_carrera = db.Column(db.Integer, db.ForeignKey('carrera.id_carrera'), nullable=False)
    id_caballo = db.Column(db.Integer, db.ForeignKey('caballo.id_caballo'), nullable=False)
    monto = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('apuesta', lazy=True))
    carrera = db.relationship('Carrera', backref=db.backref('apuesta', lazy=True))
    caballo = db.relationship('Caballo', backref=db.backref('apuesta', lazy=True))

    def __repr__(self):
        return f'Apuesta {self.id_apuesta}>'
class Caballo(db.Model):
    __tablename__ = 'caballo'

    id_caballo= db.Column(db.Integer, primary_key=True)
    nombre =db.Column(db.String(100), nullable=False)
    raza=db.Column(db.String(50),nullable=False)
    id_carrera=db.Column(db.Integer, db.ForeignKey('carrera.id_carrera'), nullable=False)
    
    carrera = db.relationship('Carrera', backref=db.backref('carrera', lazy=True))


    def __repr__(self):
        return f'Caballo {self.nombre}>'
class Usuario(db.Model):
    __tablename__ = 'usuario'

    id_usuario= db.Column(db.Integer, primary_key=True)
    nombre =db.Column(db.String(100), nullable=False)
    contraseña=db.Column(db.String(255),nullable=False)
    email=db.Column(db.String(255),nullable=False)
    saldo=db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'