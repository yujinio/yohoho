import multiprocessing as mp

from environs import Env

env = Env()
env.read_env()

host = env.str("GUNICORN_HOST", "0.0.0.0")
port = env.int("GUNICORN_PORT", 5000)
bind = f"{host}:{port}"
workers = env.int("GUNICORN_WORKERS", mp.cpu_count() * 2 + 1)
worker_class = "uvicorn.workers.UvicornWorker"
