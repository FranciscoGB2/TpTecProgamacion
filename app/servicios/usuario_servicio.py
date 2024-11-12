from DAO.usuario_dao import UsuarioDAO




class UsuarioService:
    def obtener_usuario_por_id(id_usuario):
        #obtener usuario especifico
        try:
            usuario=UsuarioDAO.get_usuario(id_usuario)
            if not usuario:
                return{"Error": "Usuario no encontrado"},404
            return usuario
        except Exception as e:
            return{"error": str(e)},500
    def obtener_usuario_por_mail(email):
         #obtener usuario especifico con el mail, utilizado para el login
            try:
                 usuario=UsuarioDAO.get_usuario_mail(email)
                 if not usuario:
                    return 0
                 return usuario
            except Exception as e:
                 raise Exception("error en obtener usuario",str(e))
    def obtener_todos_los_usuarios():
         #obtener todos los admins
        try:
                usuario=UsuarioDAO.get_usuarios()
                if not usuario:
                     return "No hay admins creados"
                else:
                     return usuario
        except Exception as e:
                return{"Error": str(e)},500
    def agregar_usuarios(nombre,contraseña,email,saldo=0):
            #agregar usuarios
            try:
                if len(contraseña)<8:
                    return{"error": "la contraseña no cumple la minima cantidad de 8 caracteres."},400
                if '@' not in email:
                    return {"error":"el email ingresado debe ser valido"},400
                return UsuarioDAO.agregar_usuario(nombre,contraseña,email,saldo)
            except Exception as e:
                return {"Error": str(e)},500
            
    def actualizar_usuario(id_usuario,nombre=None,contraseña=None,email=None,saldo=None): #el none va especifica que puede ser que no se haya ingresado algo en ese espacio
            #valida y actualiza el usuario existente
            try:
                usuario=UsuarioDAO.get_usuario(id_usuario)
                if not usuario:
                    return {"Error":"El usuario no se encontro"},404
                if not nombre:
                     nombre=usuario.nombre
                if not contraseña or len(contraseña)<8: #valida si existe una contraseña y si es mayor a 8 caracteres
                    contraseña=usuario.contraseña
                if not email or '@' not in email: #valida si existe email y si tiene un @ de no ser asi error
                   email=usuario.email
                return UsuarioDAO.actualizar_usuario(id_usuario,nombre,contraseña,email,saldo)
            except Exception as e:
                return{"error": str(e)},500
    def eliminar_usuario(id_usuario):
            #logica que comprueba antes de eliminar un usuario
            try:
                usuario=UsuarioDAO.get_usuario(id_usuario)
                if not usuario:
                    return{"error":"Usuario no encontrado"},404
                UsuarioDAO.borrar_usuario(id_usuario)
            except Exception as e:
                return{"error":str(e)},500
    def agregar_monto(id_usuario, monto):
    # Validar monto positivo
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        usuario = UsuarioService.obtener_usuario_por_id(id_usuario)
        if not usuario:
            raise ValueError("Usuario no existente")
        
    
        nuevo_saldo = usuario.saldo + monto
        return UsuarioService.actualizar_usuario(id_usuario, saldo=nuevo_saldo)