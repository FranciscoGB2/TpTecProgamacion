from DAO.admin_dao import AdminDAO

class AdminService:
    def obtener_admin_por_id(id_admin):
        #obtener admin especifico
        try:
                admin=AdminDAO.get_admin(id_admin)
                if not admin:
                     return{"Error":"Usuario no encontrado"},404
                return admin
        except Exception as e:
             return{"Error":" Usuario no encontrado"},404
    def obtener_admin_por_mail(email):
         #obtiene los datos de un admin solicitando mail (es usado para el login)
        try:
           
            admin=AdminDAO.get_admin_mail(email)
            if not admin:
                 return 0
            return admin
        except Exception as e:
             return Exception("Error en obtener usuario", str(e))  
    def obtener_todos_los_admins():
         #obtener todos los admins
        try:
                admin=AdminDAO.get_admins()
                if not admin:
                     return "No hay admins creados"
                else:
                     return admin
        except Exception as e:
                return{"Error": str(e)},500
    def agregar_admins(nombre,contraseña,email):
         #agregar admins
            try:
                if len(contraseña)<8:
                     return{"Error": "La contraseña no cumple con la minima cantidad de 8 caracteres"}
                if '@' not in email:
                     return{"Error":"El mail ingresado debe ser valido"},400
                return AdminDAO.agregar_admin(nombre,contraseña,email)
            except Exception as e:
                 return{"Error": str(e)},500
    def actualizar_admin(id_admin,nombre=None,contraseña=None,email=None):
         #actualiza los datos de un admin
        try:
                admin=AdminDAO.get_admin(id_admin)
                if not admin:
                    return{"Error": "El admin no se encontro"},404
                if not contraseña or len(contraseña)<8:
                    contraseña=admin.contraseña
                if not email or '@' not in email:
                     email=admin.email
                return AdminDAO.actualizar_admin(id_admin,nombre,contraseña,email)
        except Exception as e:
            return{"Error": str(e)},500
        
    def eliminar_admin(id_admin):
        try:
            admin=AdminDAO.get_admin(id_admin)
            if not admin:
                 return{"Error":"Usuario no encontrado"},404
            AdminDAO.borrar_admin(id_admin)
        except Exception as e:
             return{"Error":str(e)},500

            