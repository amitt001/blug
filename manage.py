from flask import Flask, render_template
from config import config
from utils import last_post_id


app = Flask(__name__)
app.debug = bool(int(config['server']['debug']))


from urls import *


def run():
    app.run(host=config['server']['host'], port=int(config['server']['port']))


def generate():
    """Read posts_base directory. Sort the files by id and create a new file
    with last_id + 1 from base.txt file."""
    import os
    import shutil
    txt_blog_dir = config['templates']['txt_blog_dir']
    txt_base_template = config['templates']['txt_base_template']
    post_id = last_post_id()
    # new text file path
    new_post = os.path.join(txt_blog_dir, '{}.txt'.format(post_id + 1))
    print('Creating new template file: {}'.format(new_post))
    # copy data
    shutil.copy(txt_base_template, new_post)
    print('Modify file and once done run python manage.py parse command.')


def parse():
    import os
    from parser.post_generator import parse_blog
    txt_blog_dir = config['templates']['txt_blog_dir']
    posts_base = sorted(os.listdir(txt_blog_dir))
    posts_base = [p for p in posts_base if p.endswith('.txt')]
    if not posts_base:
        print('No blog text files found.')
        return
    _ = posts_base.pop()
    for txt_post in posts_base:
        txt_post_path = os.path.join(txt_blog_dir, txt_post)
        parse_blog(txt_post_path)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'action', help='run/generate/parse', nargs='?', default='run')
    args = parser.parse_args()
    if args.action not in ['generate', 'parse', 'run']:
        raise Exception('Invalid action specified. Possible actions are:'
                        ' run/generate/parse')
    # Run the method
    locals()[args.action]()


