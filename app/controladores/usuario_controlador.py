from flask import Blueprint,flash,session,redirect,url_for, jsonify,request,render_template
from config import db
from servicios.usuario_servicio import UsuarioService
from servicios.carrera_servicio import CarreraService
from servicios.caballo_servicio import CaballoService
from servicios.apuesta_servicio import ApuestaService
from datetime import datetime
usuario_bp= Blueprint('usuario_bp',__name__)

@usuario_bp.route('/registrarse',methods=['GET','POST'])
def registrarse():
     if request.method=='GET':
         return render_template('crear_usuario.html')
     #endpoint para agregar un usuario a la base de datos
     if request.method=='POST':
          nombre=request.form['nombre']
          email=request.form['email']
          password=request.form['password']
          usuario=UsuarioService.obtener_usuario_por_mail(email)
          if usuario:
               flash('El email ya esta registrado')
               return render_template('crear_usuario.html')
          if len(password)<8:
               flash('La contraseña debe tener al menos 8 caracteres')
               return render_template('crear_usuario.html') 
          try:
               usuario=UsuarioService.agregar_usuarios(
               nombre=nombre,
               contraseña=password,
               email=email,
               saldo=0
               )
               return redirect(url_for('usuario_bp.login'))
          except ValueError as e:
               return jsonify({"error":str(e)}),400
    
@usuario_bp.route('/menu/actualizar',methods=['PUT'])
def actualizar_usuario():
     id_usuario=session.get('id_usuario')
     if not id_usuario:
               return redirect(url_for('usuario_bp.login'))
     #endpoint para actualizar un usuario existente
     id_usuario=request.args.get('id_usuario')
     if not id_usuario:
          return jsonify({'error': 'Falta el id_usuario'}),400
     data=request.json
          
     try:
         usuario=UsuarioService.actualizar_usuario( id_usuario,
         nombre=data.get("nombre"),
         contraseña=data.get("contraseña"),
         email=data.get("email"),
         saldo=data.get("saldo")
         )
         print(usuario)
         return jsonify({
            "id_usuario": usuario.id_usuario,
            "nombre":usuario.nombre,
            "contraseña":usuario.contraseña,
            "email":usuario.email,
            "saldo":usuario.saldo
         }),200
     except ValueError as e:
         return jsonify({"error": str(e)}),400
    
@usuario_bp.route('/menu/eliminar', methods=['DELETE'])
def eliminar_usuario():
     id_usuario=request.args.get('id_usuario')
     #endpoint para eliminar un usuario
     try:
          UsuarioService.eliminar_usuario(id_usuario)
          return jsonify({"message":"Usuario eliminado"}),200
     except ValueError as e:
          return jsonify({"error":str(e)}),404
@usuario_bp.route('/menu/<int:id_usuario>/agregar_monto', methods=['GET','POST'])
def agregar_monto(id_usuario):
     id_usuario=session.get('id_usuario')
     if not id_usuario:
            return redirect(url_for('usuario_bp.login'))
     #endpoint par agregar monto al saldo del usuario y mostrar el formulario
     if request.method=='GET':
          return render_template('agregar_monto.html')
     if request.method=='POST':
          data=request.json or request.form
          monto= data.get("monto",0)
          try:
               usuario=UsuarioService.agregar_monto(id_usuario,monto)
               return jsonify({
                    "id_usuario":usuario.id_usuario,
                    "nombre":usuario.nombre,
                    "saldo":usuario.saldo
               }),200
          except ValueError as e:
               return jsonify({"error": str(e)}),400
#iniciar sesion
@usuario_bp.route('/login',methods=['GET','POST'])
def login():
     if request.method=='GET':
          return render_template('login.html')
     if request.method=='POST':
          email=request.form['email']
          password=request.form['password']
     #verificar las credenciales
          usuario=UsuarioService.obtener_usuario_por_mail(email)
          if usuario==0:
               error="Email o contraseña incorrectos"
               return render_template('login.html',error=error)
          if usuario:
               #verifica si el usuario existe
               if usuario.contraseña==password:
                    session['id_usuario']=usuario.id_usuario
                    return redirect(url_for('usuario_bp.menu', id_usuario=usuario.id_usuario))
               else:
                    error="Error contraseña incorrecta"
                    return render_template('login.html',error=error)
          return render_template('login.html')
@usuario_bp.route('/logout')
def logout():
     session.pop('id_usuario',None)
     return redirect(url_for('usuario_bp.login'))
@usuario_bp.route('/menu',methods=['GET'])
def menu():
     id_usuario=session.get('id_usuario')
     if request.method=='GET':
          if not id_usuario:
               return redirect(url_for('usuario_bp.login'))
          usuario=UsuarioService.obtener_usuario_por_id(id_usuario)
          if usuario!=0:
               return render_template('menu_usuario.html', nombre=usuario.nombre, monto=usuario.saldo, id_usuario=id_usuario)
          else:
               return redirect(url_for('usuario_bp.login'))
@usuario_bp.route('/menu/carreras',methods=['GET'])
def carreras():
     id_usuario=session.get('id_usuario')
     if request.method=='GET':
          if not id_usuario:
               return redirect(url_for('usuario_bp.login'))
          estado="Espera"
          carreras=CarreraService.obtener_todas_las_carreras_estado(estado)
          if carreras:
               return render_template('usuario_carreras.html', carreras=carreras, id_usuario=id_usuario)
          else:
               flash('No hay carreras disponibles')
               return redirect(url_for('usuario_bp.menu'))
@usuario_bp.route('/menu/carreras/apostar', methods=['GET', 'POST'])
def apostar():
     id_usuario=session.get('id_usuario')
     if not id_usuario:
        return redirect(url_for('usuario_bp.login'))
     
     if request.method =='GET':
          id_carrera = request.args.get('id_carrera')
          carrera = CarreraService.obtener_carrera_por_id(id_carrera)
          caballos = CaballoService.obtener_caballo_por_id_carrera(id_carrera)
          usuario = UsuarioService.obtener_usuario_por_id(id_usuario)
          if not carrera or not caballos:
               flash('Selecciona una carrera')
               return redirect(url_for('usuario_bp.carreras'))
          return render_template('apostar.html', carrera=carrera, caballos=caballos, usuario=usuario)
     
     if request.method =='POST':
          id_carrera= request.form.get('id_carrera')
          carrera = CarreraService.obtener_carrera_por_id(id_carrera)
          id_caballo= request.form.get('id_caballo')
          monto = float(request.form.get('monto'))
          date= datetime.now()
          usuario= UsuarioService.obtener_usuario_por_id(id_usuario)
          if monto>usuario.saldo:
               flash('Saldo insuficiente')
               return redirect(url_for('usuario_bp.apostar', id_carrera=id_carrera))
          try:
               ApuestaService.agregar_apuestas(id_usuario, id_carrera, id_caballo, monto, carrera.estado, date)
               UsuarioService.actualizar_usuario(id_usuario, saldo=usuario.saldo-monto)
               flash('Apuesta realizada')
               return redirect(url_for('usuario_bp.menu', id_usuario=id_usuario))
          except Exception as e:
               print(e)
               flash('Error al realizar la apuesta')
               return redirect(url_for('usuario_bp.apostar', id_carrera=id_carrera))
@usuario_bp.route('/menu/apuestas',methods=['GET'])
def apuestas():
     id_usuario=session.get('id_usuario')
     if not id_usuario:
        return redirect(url_for('usuario_bp.login'))
     apuestas=ApuestaService.obtener_apuestas_por_id_usuario(id_usuario)
     return render_template('apuestas.html', apuestas=apuestas)
@usuario_bp.route('/menu/actualizar',methods=['GET'])
def actualizar():
     id_usuario=session.get('id_usuario')
     if request.method=='GET':
          if not id_usuario:
               return redirect(url_for('usuario_bp.login'))       
          return render_template('menu_actualizar.html', id_usuario=id_usuario)   
    