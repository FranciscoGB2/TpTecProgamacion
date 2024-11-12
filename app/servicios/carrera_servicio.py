from DAO.carrera_dao import CarreraDAO

class CarreraService:
    def obtener_carrera_por_id(id_carrera):
        #obtener admin especifico
        try:
                carrera=CarreraDAO.get_carrera(id_carrera)
                if not carrera:
                     return{"Error":"Carrera no encontrada"},404
                return carrera
        except Exception as e:
             return{"Error":" Carrera no encontrada"},404
    def obtener_todas_las_carreras():
         #obtener todas las carreras
        try:
                carreras=CarreraDAO.get_carreras()
                if not carreras:
                     return "No hay carreras creadas"
                else:
                     return carreras
        except Exception as e:
               return{"Error": str(e)},500
     
    def agregar_carreras(id_admin,fecha,estado):
         #agregar admins
            try:
                if id_admin is None:
                     return{"Error": "No se pudo obtener el id del admin"}
                if fecha is None:
                     return{"Error":"No se pudo obtener la fecha"},400
                
                return CarreraDAO.agregar_carrera(id_admin,fecha,estado)
            except Exception as e:
                 return{"Error": str(e)},500
    def actualizar_carrera(id_carrera,id_caballo_ganador=None, fecha=None, estado=None):
         #actualiza los datos de un admin
        try:
               carrera=CarreraDAO.get_carrera(id_carrera)
               if not carrera:
                    return{"Error": "La carrera no se encontro"},404
               if not fecha:
                    fecha=carrera.fecha_hora
               if not estado:
                    estado=carrera.estado
               if not id_caballo_ganador:
                    id_caballo_ganador=carrera.id_caballo_ganador
               return CarreraDAO.actualizar_carrera(id_carrera,id_caballo_ganador, fecha, estado)
        except Exception as e:
            return{"Error": str(e)},500
        
    def eliminar_carrera(id_carrera):
        try:
            carrera=CarreraDAO.get_carrera(id_carrera)
            if not carrera:
                 print("Carrera no encontrada")
            CarreraDAO.borrar_carrera(id_carrera)
        except Exception as e:
             print(e)
             return{"Error":str(e)},500

    def obtener_todas_las_carreras_estado(estado):
         #obtener todas las carreras con un estado en especifico
          try:
               carreras = CarreraDAO.get_carreras_por_estado(estado)
               if not carreras:
                    return 0
               else:
                    return carreras
          except Exception as e:
               return {"Error": str(e)}, 500 
               