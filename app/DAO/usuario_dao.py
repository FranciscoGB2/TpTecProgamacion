from modelos.modelos import Usuario
from config import db

class UsuarioDAO:
    @staticmethod
    def get_usuario(id_usuario):
        #Obtiene un usuario por su ID
        return db.session.query(Usuario).filter_by(id_usuario=id_usuario).first()
    def get_usuario_mail(email):
        #obtiene un usuaro por su mail
        return db.session.query(Usuario).filter_by(email=email).first()
    
    def get_usuarios():
        usuarios=Usuario.query.all()
        return usuarios
    def agregar_usuario(nombre, contraseña, email, saldo=0):
        #Agrega un nuevo usuario
        nuevo_usuario=Usuario(nombre=nombre, contraseña=contraseña, email=email, saldo=saldo)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return nuevo_usuario
    def actualizar_usuario(id_usuario, nombre=None,contraseña=None, email=None, saldo=None):
        #actualiza un usuario existente
        usuario=Usuario.query.filter_by(id_usuario=id_usuario).first()
        if not usuario:
            raise ValueError("Usuario no encontrado")
        if nombre is not None:
            usuario.nombre=nombre
        if contraseña is not None:
            usuario.contraseña=contraseña
        if email is not None:
            usuario.email=email
        if saldo is not None:
            usuario.saldo=saldo
        
        db.session.commit()
        return usuario
    def borrar_usuario(id_usuario):
        #eliminar usuario por id
        usuario=Usuario.query.get(id_usuario)
        if not usuario:
            return None
        db.session.delete(usuario)
        db.session.commit()
        return usuario