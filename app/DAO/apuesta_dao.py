from modelos.modelos import Apuesta
from config import db

class ApuestaDAO:
    def get_apuesta(id_apuesta):
        #obtiene una apuesta por su ID
        return db.session.query(Apuesta).filter_by(id_apuesta=id_apuesta).first()
    def get_apuesta_id_usuario(id_usuario):
        #obtiene una apuesta por su ID
        return db.session.query(Apuesta).filter_by(id_usuario=id_usuario).first()
    def get_apuestas():
        #obtiene todos los admins
        apuestas=Apuesta.query.all()
        return apuestas
    def get_apuestas_id_usuario(id_usuario):
        #obtiene todos los admins
        return Apuesta.query.filter_by(id_usuario=id_usuario).all()
    def get_apuestas(id_carrera):
        #obtiene todos los admins
        return db.session.query(Apuesta).filter_by(id_carrera=id_carrera).all()
    def agregar_apuesta(id_usuario, id_carrera, id_caballo, monto, estado, date):
        nueva_apuesta = Apuesta(
            id_usuario=id_usuario,
            id_carrera=id_carrera,
            id_caballo=id_caballo,
            monto=monto,
            estado=estado,
            date=date
        )
        db.session.add(nueva_apuesta)
        db.session.commit()
        return nueva_apuesta
    def actualizar_apuesta(id_apuesta,estado):
        #actualiza una apuesta existente
        apuesta=Apuesta.query.filter_by(id_apuesta=id_apuesta).first()
        if not apuesta:
            raise ValueError("Apuesta  no encontrada")
        if estado is not None:
            apuesta.estado=estado
        db.session.commit()
        return apuesta
    def borrar_apuesta(id_apuesta):
        #eliminar una apuesta por id
        apuesta=Apuesta.query.get(id_apuesta)
        if not apuesta:
            return None
        db.session.delete(id_apuesta)
        db.session.commit()
        return apuesta