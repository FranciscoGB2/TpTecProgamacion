from modelos.modelos import Admin
from config import db

class AdminDAO:
    def get_admin(id_admin):
        #obtiene un admin por su ID
        return db.session.query(Admin).filter_by(id_admin=id_admin).first()
    def get_admin_mail(email):
        #obtener un admin por su email (usado para el login)
        return db.session.query(Admin).filter_by(email=email).first()
    def get_admins():
        #obtiene todos los admins
        admins=Admin.query.all()
        return admins
    def agregar_admin(nombre, contraseña, email):
        #agrega un nuevo admin
        nuevo_admin=Admin(nombre=nombre, contraseña=contraseña, email=email)
        db.session.add(nuevo_admin)
        db.session.commit()
        return nuevo_admin
    def actualizar_admin(id_admin,nombre=None, contraseña=None, email=None):
        #actualiza un admin existente
        admin=Admin.query.filter_by(id_admin=id_admin).first()
        if not admin:
            raise ValueError("Admin no encontrado")
        if nombre is not None:
            admin.nombre=nombre
        if contraseña is not None:
            admin.contraseña=contraseña
        if email is not email:
            admin.email=email
        db.session.commit()
        return admin
    def borrar_admin(id_admin):
        #eliminar admin por id
        admin=Admin.query.get(id_admin)
        if not admin:
            return None
        db.session.delete(id_admin)
        db.session.commit()
        return admin