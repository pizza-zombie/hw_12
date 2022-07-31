import logging
from json import JSONDecodeError

from flask import Blueprint, request, render_template, send_from_directory
from functions import get_posts_by_word
from functions import load_post

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')


@main_blueprint.route('/')
def main_page():
    return render_template("index.html")


@main_blueprint.route('/list')
def page_tag():
    try:
        return render_template("post_list.html", posts=load_post())
    except FileNotFoundError:
        logging.error("Ошибка БД")
        return "Упала база"
    except JSONDecodeError:
        logging.error("Ошибка БД")
        return "База сломалась"


@main_blueprint.route('/search')
def search_page():
    s = request.args.get("s")
    logging.info("Выполняю поиск")
    try:
        if s:
            search_posts = get_posts_by_word(s)
            return render_template("post_list.html", s=s, posts=search_posts)
        else:
            return f'<h1>Вы ничего не ввели</h1>'
    except FileNotFoundError:
        logging.error("Ошибка БД")
        return "База лежит"
    except JSONDecodeError:
        logging.error("Ошибка БД")
        return "База сломалась"



@main_blueprint.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)



