from modelos.modelos import Caballo
from config import db

class CaballoDAO:
    def get_caballo(id_caballo):
        #obtiene un caballo por su ID
        return db.session.query(Caballo).filter_by(id_caballo=id_caballo).first()
    def get_caballos_carrera(id_carrera):
        #obtiene caballos por la carrera en la que participan
        return db.session.query(Caballo).filter_by(id_carrera=id_carrera).all()
    def get_caballos():
        #obtiene todos los admins
        caballos=Caballo.query.all()
        return caballos
    def agregar_caballo(nombre,raza):
        #agrega un nuevo admin
        nuevo_caballo=Caballo(nombre=nombre, raza=raza)
        db.session.add(nuevo_caballo)
        db.session.commit()
        return nuevo_caballo
    def actualizar_caballo(id_caballo,nombre=None,raza=None,id_carrera=None):
        #actualiza un admin existente
        caballo=Caballo.query.filter_by(id_caballo=id_caballo).first()
        if not caballo:
            raise ValueError("Caballo no encontrado")
        if nombre is not None:
            caballo.nombre=nombre
        if raza is not None:
            caballo.raza=raza
        caballo.id_carrera=id_carrera
        db.session.commit()
        return caballo
    def borrar_caballo(id_caballo):
        #eliminar admin por id
        caballo=Caballo.query.get(id_caballo)
        if not caballo:
            return None
        db.session.delete(caballo)
        db.session.commit()
        return caballo