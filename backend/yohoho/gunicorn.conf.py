from . import config

host = config.GUNICORN_HOST
port = config.GUNICORN_PORT
bind = f"{host}:{port}"
workers = config.GUNICORN_WORKERS
worker_class = config.GUNICORN_WORKER_CLASS
