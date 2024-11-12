from flask import Flask,session,redirect,url_for,render_template
import os
from flask_cors import CORS
from config import db
from controladores.usuario_controlador import usuario_bp
from controladores.admin_controlador import admin_bp

def create_app():
    app=Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root123@localhost/apuesta_caballos'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)
    app.secret_key=os.urandom(24)
    return app

app=create_app()

    


app.register_blueprint(usuario_bp,url_prefix='/api')
app.register_blueprint(admin_bp,url_prefix='/admins')

    





#Verificacion que se inicio la base de datos correctamente
#@app.before_request
#def check_db():
#    try:
 #       conexion= db.engine.connect()
   #     resultado=conexion.execute(text('SELECT * FROM usuario')).fetchall() #Ejecuta consulta simple
   #     conexion.close()
  #      if resultado:
   #      for fila in resultado:
   #         print(fila._asdict())
   #     else:
   #         print("No se encontraron registros en al tabla usuario")
    #    print("Se conecto a la base de datos correctamente")        
   # except Exception as e:
   #     print("Error al conectar a al base de datos: ",str(e))

@app.route('/menu')
def menu():
        return render_template('index.html')

@app.route('/')
def index():
    return redirect(url_for('menu'))


if __name__=='__main__':
    
    app.run(debug=True)
