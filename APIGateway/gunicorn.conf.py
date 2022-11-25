"""
Archivo de configuracion para despliegue
con un servidor de producción como gunicorn
"""
import multiprocessing
import os

# Nombre de la aplicacion
wsgi_app = "app:gunicorn()"

# Puerto
bind = f"0.0.0.0:{os.environ.get('FLASK_PORT', '3000')}"

# Numero de workers
workers = multiprocessing.cpu_count() * 2 + 1

timeout = 200