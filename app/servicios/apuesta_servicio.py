from DAO.apuesta_dao import ApuestaDAO

class ApuestaService:
     def obtener_apuesta_por_id(id_apuesta):
        #obtener admin especifico
        try:
                apuesta=ApuestaDAO.get_apuesta(id_apuesta)
                if not apuesta:
                     return 0
                return apuesta
        except Exception as e:
             return{"Error":" Apuesta no encontrada"},404
     def obtener_apuestas_por_id_usuario(id_usuario):
         #obtiene los datos de una apuesta solicitando id_usuario
        try:
            apuesta=ApuestaDAO.get_apuestas_id_usuario(id_usuario)
            if not apuesta:
                 return 0
            return apuesta
        except Exception as e:
             return Exception("Error en obtener apuesta", str(e))
     def obtener_apuestas_por_id_carrera(id_carrera):
         #obtiene los datos de una apuesta solicitando id_usuario
        try:
            apuestas=ApuestaDAO.get_apuestas(id_carrera)
            if not apuestas:
                 return 0
            return apuestas
        except Exception as e:
             return Exception("Error en obtener apuesta", str(e))
     def obtener_todos_las_apuestas():
         #obtener todos los admins
        try:
                apuestas=ApuestaDAO.get_apuestas()
                if not apuestas:
                     return "No hay apuestas creadas"
                else:
                     return apuestas
        except Exception as e:
                return{"Error": str(e)},500
     def agregar_apuestas(id_usuario, id_carrera, id_caballo, monto, estado, date):
        try:
            if id_usuario is None:
                raise ValueError("El id usuario no se encontró")
            if id_caballo is None:
                raise ValueError("No se pudo obtener el id del caballo")
            if monto is None or monto < 0:
                raise ValueError("El monto es inválido")
            return ApuestaDAO.agregar_apuesta(id_usuario, id_carrera, id_caballo, monto, estado, date)
        except Exception as e:
            raise ValueError(f"Error al agregar la apuesta: {str(e)}")
     def actualizar_apuesta(id_apuesta,estado):
         #actualiza el estado de la apuesta
        try:
                apuesta=ApuestaDAO.get_apuesta(id_apuesta)
                if not apuesta:
                    return{"Error": "La apuesta no se encontro"},404
                if estado is None:
                    estado=apuesta.estado
                return ApuestaDAO.actualizar_apuesta(id_apuesta,estado)
        except Exception as e:
            return{"Error": str(e)},500
        
     def eliminar_apuesta(id_apuesta):
        try:
            apuesta=ApuestaDAO.get_apuesta(id_apuesta)
            if not apuesta:
                 return{"Error":"Apuesta no encontrada"},404
            ApuestaDAO.borrar_apuesta(id_apuesta)
        except Exception as e:
             return{"Error":str(e)},500

            