from flask import Flask


def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pacientes_clinica.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    
    app.config['JWT_SECRET_KEY']='secret-key'

    app.config['PROPAGATE_EXCEPTIONS']=True
    
    return app