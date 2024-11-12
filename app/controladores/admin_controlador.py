from flask import Blueprint,flash,session,redirect,url_for, jsonify,request,render_template
from servicios.admin_servicio import AdminService
from servicios.usuario_servicio import UsuarioService
from servicios.carrera_servicio import CarreraService
from servicios.caballo_servicio import CaballoService
from servicios.apuesta_servicio import ApuestaService
from datetime import datetime

admin_bp= Blueprint('admin_bp',__name__)

@admin_bp.route('/registrar',methods=['GET','POST'])
def registrar():
    id_admin= session.get('id_admin')
    if not id_admin:
        return redirect(url_for('admin_bp.login'))
    if request.method=='GET':
          return render_template('crear_admin.html')
    if request.method=='POST':
        nombre=request.form['nombre']
        email=request.form['email']
        password=request.form['password']
        admin = AdminService.obtener_admin_por_mail(email)

        if admin:
            flash('El email ya esta registrado')
            return render_template('crear_admin.html')
        if len(password)<8:
            flash('La contraseña debe tener al menos 8 caracteres')
            return render_template('crear_admin.html') 
        try:
            AdminService.agregar_admins(
                nombre=nombre,
                contraseña=password,
                email=email
            )
            flash("Se registro el admin correctamente","success")
            return redirect(url_for('admin_bp.login'))
        except ValueError as e:
            return jsonify({"error" : str(e)}),400
@admin_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
    #verificar credenciales
        admin=AdminService.obtener_admin_por_mail(email)
        if admin==0:
            error="Email o contraseña incorrectos"
            return render_template('login.html',error=error)
        if admin:
            #verifica si el usuario existe
            if admin.contraseña==password:
                session['id_admin']=admin.id_admin
                return redirect(url_for('admin_bp.menu', id_admin=admin.id_admin))
            else:
                    error="Error contraseña incorrecta"
                    return render_template('login.html',error=error)
        return render_template('login.html')
@admin_bp.route('/logout')
def logout():
    session.pop('id_admin',None)
    return redirect(url_for('admin_bp.login'))
@admin_bp.route('/menu',methods=['GET'])
def menu():
    id_admin=session.get('id_admin')
    if request.method=='GET':
        if not id_admin:
            return redirect(url_for('admin_bp.login'))
        admin=AdminService.obtener_admin_por_id(id_admin)
        if admin!=0:
            return render_template('menu_admin.html',nombre=admin.nombre,id_admin=admin.id_admin )
        else:
            return redirect(url_for('admin_bp.login'))
@admin_bp.route('/menu/admins',methods=['GET'])
def listar_admins():
    id_admin= session.get('id_admin')
    if not id_admin:
        return redirect(url_for('admin_bp.login'))
    admins=AdminService.obtener_todos_los_admins()
    return render_template('admins.html',admins=admins)
@admin_bp.route('/menu/usuarios',methods=['GET'])
def listar_usuarios():
    id_admin= session.get('id_admin')
    if not id_admin:
        return redirect(url_for('admin_bp.login'))
    usuarios=UsuarioService.obtener_todos_los_usuarios()
    return render_template('usuarios.html',usuarios=usuarios)   
@admin_bp.route('/menu/carreras',methods=['GET'])
def listar_carreras():
    id_admin= session.get('id_admin')
    if not id_admin:
        return redirect(url_for('admin_bp.login'))
    
    carreras=CarreraService.obtener_todas_las_carreras()
    return render_template('carreras.html',carreras=carreras)
@admin_bp.route('/menu/carreras/actualizar/borrar',methods=['POST'])
def borrar_caballo():
    id_admin= session.get('id_admin')
    if not id_admin:
        return redirect(url_for('admin_bp.login'))
    id_caballo=request.form.get('id_caballo')
    print("caballo ",  id_caballo)
    if id_caballo:
        try:
            caballo=CaballoService.eliminar_caballo(id_caballo)
            flash("Se elimino el caballo correctamente","success")
            return redirect(url_for('admin_bp.listar_caballos'))
        except Exception as e:
            print("Error ",e)
            flash("No se pudo eliminar el caballo","danger")   
            return jsonify({"error": str(e)}),400
    else:
        flash("No se pudo eliminar el caballo","danger")
        return redirect(url_for('admin_bp.listar_caballos'))

@admin_bp.route('/menu/carreras',methods=['POST'])
def registrar_carrera():
     if request.method=='POST':
        id_admin= session.get('id_admin')
        if not id_admin:
            return redirect(url_for('admin_bp.login'))
        date= datetime.now()
        estado="Espera"
        try:
            carrera=CarreraService.agregar_carreras(
                id_admin=id_admin,
                fecha=date,
                estado=estado
            )
            flash("Se registro la carrera correctamente","success")
            return redirect(url_for('admin_bp.listar_carreras'))
        except ValueError as e:
            flash("No se pudo registrar la carrera","danger")
            return jsonify({"error" : str(e)}),400
@admin_bp.route('/menu/carreras/iniciar',methods=['POST'])
def iniciar_carrera():
    contador=0
    id_admin= session.get('id_admin')
    if not id_admin:
        return redirect(url_for('admin_bp.login'))
    id_carrera = request.form.get('id_carrera')
    
    if id_carrera:
        try:
            caballos=CaballoService.obtener_caballo_por_id_carrera(id_carrera)
            if not caballos:
                flash("No se puede iniciar la carrera sin caballos","danger")
                return redirect(url_for('admin_bp.listar_carreras'))
            for caballo in caballos:
                contador+=1
                print("Contador",contador)
            if contador<2:
                flash("No se puede iniciar la carrera con menos de 2 caballos","danger")
                return redirect(url_for('admin_bp.listar_carreras'))
            carrera=CarreraService.actualizar_carrera(id_carrera=id_carrera,estado="En curso")
            apuestas=ApuestaService.obtener_apuestas_por_id_carrera(id_carrera)
            if not apuestas:
                return redirect(url_for('admin_bp.listar_carreras'))    
            for apuesta in apuestas:
                apuesta.estado="En curso"
                ApuestaService.actualizar_apuesta(apuesta.id_apuesta,estado="En curso")
            flash("Se inicio la carrera correctamente","success")
            return redirect(url_for('admin_bp.listar_carreras'))
        except Exception as e:
            flash("No se pudo iniciar la carrera","danger")
            return jsonify({"error": str(e)}),400
    else:
        return redirect(url_for('admin_bp.listar_carreras'))
@admin_bp.route('/menu/carreras/terminar',methods=['POST'])
def terminar_carrera():
    id_admin= session.get('id_admin')
    if not id_admin:
        return redirect(url_for('admin_bp.login'))
    id_carrera = request.form.get('id_carrera')
    id_caballo=int(request.form.get('id_caballo'))
    if id_carrera:
        try:
            
            carrera=CarreraService.obtener_carrera_por_id(id_carrera)
            if(carrera.estado=="Espera"):
                flash("No se puede terminar una carrera que no ha iniciado","danger")
                return redirect(url_for('admin_bp.listar_carreras'))
            if(carrera.estado=="Finalizada"):
                flash("La carrera ya ha finalizado","danger")
                return redirect(url_for('admin_bp.listar_carreras'))
            CarreraService.actualizar_carrera(id_carrera=id_carrera,id_caballo_ganador=id_caballo,estado="Finalizada")
            caballos = CaballoService.obtener_caballo_por_id_carrera(id_carrera)
            
            apuestas=ApuestaService.obtener_apuestas_por_id_carrera(id_carrera)
            if apuestas == 0:
                return redirect(url_for('admin_bp.listar_carreras'))
            
            for apuesta in apuestas:
                if apuesta.id_caballo==id_caballo:
                    usuario=UsuarioService.obtener_usuario_por_id(apuesta.id_usuario)
                    UsuarioService.actualizar_usuario(apuesta.id_usuario,saldo=usuario.saldo+apuesta.monto*2)
                    ApuestaService.actualizar_apuesta(apuesta.id_apuesta,estado="Ganada")
                else:
                    ApuestaService.actualizar_apuesta(apuesta.id_apuesta,estado="Perdida")
            for caballo in caballos:
                id_carrera=0
                CaballoService.actualizar_caballo(id_caballo=caballo.id_caballo,id_carrera=id_carrera)
            flash("Se termino la carrera correctamente","success")    
            return redirect(url_for('admin_bp.listar_carreras'))
        except Exception as e:
            flash("No se pudo terminar la carrera","danger")
            return jsonify({"error": str(e)}),400
@admin_bp.route('/menu/carreras/actualizar',methods=['GET'])
def ver_detalles_carreras():
    id_admin= session.get('id_admin')
    if not id_admin:
        return redirect(url_for('admin_bp.login'))
    id_carrera=request.args.get('id_carrera')
    print("id_carrera",id_carrera)
    if id_carrera:
        carrera=CarreraService.obtener_carrera_por_id(id_carrera)
        caballos=CaballoService.obtener_caballo_por_id_carrera(id_carrera=id_carrera)
        return render_template('ver_detalles.html',carrera=carrera,caballos=caballos)
    else:
        return redirect(url_for('admin_bp.listar_carreras'))
@admin_bp.route('/menu/carreras/borrar', methods=['POST'])
def borrar_carrera():
    id_admin = session.get('id_admin')
    if not id_admin:
        return redirect(url_for('admin_bp.login'))
    id_carrera = request.form.get('id_carrera')
    if id_carrera:
        try:
            CarreraService.eliminar_carrera(id_carrera)
            flash("Se elimino la carrera correctamente","success")
            return redirect(url_for('admin_bp.listar_carreras'))
        except Exception as e:
            flash("No se pudo eliminar la carrera","danger")
            print("Error ", e)
            return jsonify({"error": str(e)}), 400
    else:
        return redirect(url_for('admin_bp.listar_carreras'))
@admin_bp.route('/menu/caballos/crear',methods=['GET','POST'])
def registrar_caballo():
    id_admin= session.get('id_admin')
    if not id_admin:
        return redirect(url_for('admin_bp.login'))
    if request.method=='GET':
        return render_template('crear_caballos.html')
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        raza = request.form.get('raza')
        if not nombre or not raza:
            return redirect(url_for('admin_bp.registrar_caballo'))
        try:
            
            caballo = CaballoService.agregar_caballos(
                nombre=nombre,
                raza=raza
            )
            flash("Se registro el caballo correctamente","success")
            return redirect(url_for('admin_bp.listar_caballos'))
        except Exception as e:
            flash("No se pudo registrar el caballo","danger")
            return redirect(url_for('admin_bp.registrar_caballo'))
@admin_bp.route('/menu/caballos',methods=['GET'])
def listar_caballos():
    id_admin= session.get('id_admin')
    if not id_admin:
        return redirect(url_for('admin_bp.login'))
    caballos=CaballoService.obtener_todos_los_caballos()
    print(caballos)
    return render_template('caballos.html',caballos=caballos)
@admin_bp.route('/menu/caballos/actualizar',methods=['GET'])
def ver_detalles_caballos():
    id_admin= session.get('id_admin')
    if not id_admin:
        return redirect(url_for('admin_bp.login'))
    id_caballo=request.args.get('id_caballo')
    print("id_caballo",id_caballo)
    if id_caballo:
        estado="Espera"
        caballo=CaballoService.obtener_caballo_por_id(id_caballo)
        carreras=CarreraService.obtener_todas_las_carreras_estado(estado=estado)
        return render_template('ver_detalles_caballos.html',caballo=caballo,carreras=carreras)
    else:
        return redirect(url_for('admin_bp.listar_caballos'))
@admin_bp.route('/menu/caballos/actualizar',methods=['POST'])    
def ingresar_caballo():
    id_caballo=request.form.get('id_caballo')
    id_carrera=request.form.get('id_carrera')
    if id_caballo and id_carrera:
        try:
                caballo=CaballoService.obtener_caballo_por_id(id_caballo)
                if caballo.id_carrera is not None:
                    return redirect(url_for('admin_bp.listar_caballos',id_caballo=id_caballo))
                CaballoService.actualizar_caballo(id_caballo=id_caballo,id_carrera=id_carrera)

                return redirect(url_for('admin_bp.listar_caballos',id_caballo=id_caballo))
        except Exception as e:
            return jsonify({"error": str(e)}),400
    else:
        return redirect(url_for('admin_bp.ver_detalles_caballos',id_caballo=id_caballo))


