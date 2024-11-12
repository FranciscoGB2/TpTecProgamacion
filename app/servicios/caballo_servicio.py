from DAO.caballo_dao import CaballoDAO

class CaballoService:
     def obtener_caballo_por_id_carrera(id_carrera):
        #obtener admin especifico
        try:
                caballos=CaballoDAO.get_caballos_carrera(id_carrera)
                if not caballos:
                     return 0
                return caballos
        except Exception as e:
             return{"Error":" Caballos no encontrados"},404
     def obtener_caballo_por_id(id_caballo):
        #obtener admin especifico
        try:
                caballo=CaballoDAO.get_caballo(id_caballo)
                if not caballo:
                     return 0
                return caballo
        except Exception as e:
             return{"Error":" Caballo no encontrado"},404
     
     def obtener_todos_los_caballos():
         #obtener todos los admins
        try:
                caballo=CaballoDAO.get_caballos()
                if not caballo:
                     return 0
                else:
                     return caballo
        except Exception as e:
                return{"Error": str(e)},500
     def agregar_caballos(nombre,raza):
         #agregar admins
            try:
                return CaballoDAO.agregar_caballo(nombre,raza)
            except Exception as e:
                 return{"Error": str(e)},500
     def actualizar_caballo(id_caballo,id_carrera=None,nombre=None,raza=None):
         #actualiza los datos de un admin
          
          try:
                caballo=CaballoDAO.get_caballo(id_caballo)
                if not caballo:
                    return{"Error": "El caballo no se encontro"},404
                if id_carrera is None:
                    id_carrera=caballo.id_carrera
                if id_carrera == 0:
                     id_carrera=None
                if not raza:
                    raza=caballo.raza
                if not nombre:
                     nombre=caballo.nombre
                return CaballoDAO.actualizar_caballo(id_caballo,nombre,raza,id_carrera)
          except Exception as e:
               print(e)
               return{"Error": str(e)},500
        
     def eliminar_caballo(id_caballo):
        try:
            caballo=CaballoDAO.get_caballo(id_caballo)
            if not caballo:
                 return{"Error":"Caballo no encontrado"},404
            CaballoDAO.borrar_caballo(id_caballo)
        except Exception as e:
             print(e)
             return{"Error":str(e)},500

            