import logging
from json import JSONDecodeError
from flask import Blueprint, request, render_template, send_from_directory
from loader.utils import save_picture
from functions import add_post

loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates')


@loader_blueprint.route('/post')
def post_page():
    return render_template("post_form.html")


@loader_blueprint.route('/post', methods=['POST'])
def add_post_page():
    picture = request.files.get('picture')
    content = request.form.get('content')

    if not picture or not content:
        logging.error("Ошибка - отсутствует файл")
        return "Нет картинки или описания"
    extension = picture.filename.split(".")[-1]
    if extension not in ["jpeg", "png"]:
        logging.error("Ошибка расширения файла")
        return "Картинка - не картинка"
    picture_path: str = '/' + save_picture(picture)
    try:
        post: dict = add_post({'pic': picture_path, 'content': content})
        return render_template('post_uploaded.html', post=post)
    except FileNotFoundError:
        logging.error("Ошибка БД")
        return "База упала"

    except JSONDecodeError:
        logging.error("Ошибка БД")
        return "База сломалась"


@loader_blueprint.errorhandler(413)
def page_not_found(e):
    logging.error("Ошибка размера файла")
    return "<h1>Файл большеват</h1><p>Поищите поменьше, плиз!</p>", 413
