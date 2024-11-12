from modelos.modelos import Carrera
from config import db

class CarreraDAO:
    @staticmethod
    def get_carrera(id_carrera):
        #Obtiene una carrera por su ID
        return db.session.query(Carrera).filter_by(id_carrera=id_carrera).first()
    
    def get_carreras():
        carreras=Carrera.query.all()
        return carreras
    def agregar_carrera(id_administrador, fecha_hora, estado):
    # Agrega una nueva carrera
        nueva_carrera = Carrera(
            id_administrador=id_administrador,
            id_caballo_ganador=None,
            fecha_hora=fecha_hora,
            estado=estado
    )
        db.session.add(nueva_carrera)
        db.session.commit()
        return nueva_carrera
    def actualizar_carrera(id_carrera,id_caballo_ganador=None, fecha=None, estado=None):
        #actualiza un usuario existente
        carrera=Carrera.query.filter_by(id_carrera=id_carrera).first()
       
        if not carrera:
            raise ValueError("Carrera no encontrada")
        if fecha is not None:
            carrera.fecha=fecha
        if id_caballo_ganador is not None:
            carrera.id_caballo_ganador=id_caballo_ganador
        if estado is not None:
            carrera.estado=estado 
        db.session.commit()
        return carrera
    def borrar_carrera(id_carrera):
        #eliminar carrera por id
        carrera=Carrera.query.get(id_carrera)
        if not carrera:
            return None
        db.session.delete(carrera)
        db.session.commit()
        return carrera
    def get_carreras_por_estado(estado):
        carreras=Carrera.query.filter_by(estado=estado).all()
        return carreras