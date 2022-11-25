from flask import Flask
from modelos.modelos import db, Paciente
from flask_restful import Api
from vistas.vistas import VistaPacientes, VistaSignIn, VistaLogIn, VistaPaciente, VistaTratamientoPaciente
from flask_jwt_extended import JWTManager
from flask_injector import FlaskInjector

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pacientes_clinica.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    
app.config['JWT_SECRET_KEY']='secret-key'

app.config['PROPAGATE_EXCEPTIONS']=True
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaPacientes, '/pacientes')
api.add_resource(VistaPaciente, '/paciente/<int:id_paciente>')
api.add_resource(VistaTratamientoPaciente, '/paciente/<int:id_paciente>/tratamiento')
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/login')

FlaskInjector(app=app)

jwt = JWTManager(app)


def gunicorn():
    
    return app

if __name__ == "__main__":
    app.run(
        host="0.0.0.0", port=3020, debug=True
    )
