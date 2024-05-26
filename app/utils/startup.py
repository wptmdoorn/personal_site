from nicegui import app
import importlib
from fastapi.middleware.wsgi import WSGIMiddleware
import os


def register_dash_apps():
    for f in os.listdir('app/software'):
        print(f)
        if os.path.isdir(f'app/software/{f}'):
            page_module = importlib.import_module(f'software.{f}.main')

            if page_module.SOFTWARE_TYPE == 'DASH':

                dash_app = page_module.page(
                    requests_pathname_prefix=f'/software_dash/{f}/')

                app.mount(f'/software_dash/{f}/',
                          WSGIMiddleware(dash_app.server))
