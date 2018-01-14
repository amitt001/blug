import os
import json

from flask import render_template, request
from config import config
from manage import app
from utils import posts_map, prev_next_post_dict


def index():
    category = request.args.get('category')
    if category:
        with open(config['parser']['category_mapper']) as f:
            category_mapper = json.load(f)
        blog_posts = sorted(category_mapper.get(category, {}).items(), reverse=True)
        category = [category]
    else:
        blog_posts = posts_map()
    return render_template('blog.html', blogs=blog_posts, category=category)


def blog(_id, blog_path):
    blog_file = os.path.join('{}_{}.html'.format(str(_id), blog_path))
    blog_path = '{}/{}'.format(config['templates']['directory'], blog_file)
    if not os.path.exists('{}/{}'.format(config['templates']['path'], blog_file)):
        return '404 page'
    context = prev_next_post_dict(blog_file)
    return render_template(blog_path, **context)


@app.errorhandler(404)
def error_handler_view(e):
    return render_template(
        'error.html', message=e.name, error_code=e.code), e.code


# TODO: handle in one view
@app.errorhandler(400)
def error_handler_view(e):
    return render_template(
        'error.html', message=e.name, error_code=e.code), e.code


@app.errorhandler(500)
def error_handler_view(e):
    e.name = 'Internal Server Error'
    e.code = 500
    return render_template(
        'error.html', message=e.name, error_code=e.code), e.code
