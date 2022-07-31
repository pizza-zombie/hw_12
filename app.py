import logging

from flask import Flask, request, render_template, send_from_directory

# Импортируем блюпринты из их пакетов
from main.views import main_blueprint
from loader.views import loader_blueprint

# from functions import ...
POST_PATH = "posts.json"
UPLOAD_FOLDER = "uploads/images"

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

# Регистрируем блюпринты
app.register_blueprint(main_blueprint)
app.register_blueprint(loader_blueprint)

logging.basicConfig(filename="basic.log", level=logging.INFO)



app.run()

