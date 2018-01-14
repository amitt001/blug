import re
import os
import json

from datetime import datetime
from parser.mapper import template_mapper, tag_mapper
from config import config


url_prefix = '/blog'


def link_and_title(post_file):
    """Returns like and title of post_file"""
    blog_id, post_name = post_file.split('_')
    post_name = post_name.replace('.html', '')
    title = post_name.replace('-', ' ').title()
    link = '{}/{}'.format(blog_id, post_name)
    return link, title


def category_map(categories, post_name):
    """Creates a blog category mapper file."""
    if categories:
        category_data = {}
        mapper_file = config['parser']['category_mapper']
        if os.path.exists(mapper_file):
            with open(mapper_file, 'r') as f:
                category_data = json.load(f)
        for c in categories:
            category_data.setdefault(c, {})
            link, post_title = link_and_title(post_name)
            category_data[c][link] = post_title
        with open(mapper_file, 'w') as f:
            json.dump(category_data, f)


def create_post_file(blog_id, post_link, post_content, category=None):
    """Create the final html file."""
    # create post with name
    post_name = '{}_{}.html'.format(blog_id, post_link)
    # Create category maps
    category_map(category, post_name)
    # create blog html file
    with open('templates/posts/{}'.format(post_name), 'w') as f:
        f.write(post_content)


def create_timestamp(time_tag):
    # create date string
    if time_tag == 'now':
        now = datetime.now()
        time_code, time_val = now, now.date()
    return str(time_code), str(time_val)


def parse_tag(code_tag, post):
    """Parses tags in blog posts

    :param code_tag:
    :param post:
    :return:
    """
    new_post = post
    start = 0
    is_error = False
    html_tag_begin, html_tag_end = tag_mapper[code_tag], '</' + tag_mapper[code_tag].lstrip('<')
    some_val = len(html_tag_begin + html_tag_begin) + 1 - len(code_tag + code_tag)
    links = []
    while is_error is False:
        try:
            tmp_post = post[start:]
            code_start = start + tmp_post.index(code_tag) + len(code_tag)
            code_end = code_start + tmp_post[code_start-start:].index(code_tag)
            code = post[code_start:code_end]
            if code_tag == '<link>':
                href_link = re.search('\[.*?\]', code).group().strip('[]')
                links.append(href_link)
            add_val = 0 if start == 0 else some_val
            new_post = new_post[:code_start - len(code_tag) + add_val] + html_tag_begin + code + html_tag_end + post[code_end + len(code_tag):]
            start = code_end + len(code_tag)
        except ValueError:
            is_error = True
    new_post = re.sub('(<a>)\[.*?\]', '<a href="{}">', new_post).format(*links)
    return new_post


def parse_post(post):
    """Parse the content of blog post.

    :param post:
    :return: str
    """
    post = post.split("post:\n\t'''")[1].strip().rstrip("'''")
    post = post.strip()
    post = post.replace('\n', '<br>')
    post = post.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')
    for tag in tag_mapper:
        post = parse_tag(tag, post)
    return post


def apply_html_value(section, val1, val2=None):
    """
    :param section:
    :param val1:
    :param val2:
    :return:
    """
    section_html = template_mapper.get(section)
    if section_html is None:
        return ''
    section_html = section_html.replace('#dynamic_value_1', val1)
    if val2 is not None:
        section_html = section_html.replace('#dynamic_value_2', val2)
    return section_html


def section_pre_postfix(section):
    """Returns prefix and postfix HTMl content for sections

    :param section:
    :return: str
    """
    prefix, postfix = '', ''
    if section == 'previous':
        prefix = '<hr><div id="blog-footer">'
    elif section == 'next':
        postfix = '</div>'
    elif section == 'tags':
        prefix, postfix = '<div id="tags"><span id="tag-title">Category: </span>', '</div>'
    return prefix, postfix


def parse_blog(txt_blog_path):
    category = []
    blog_id = os.path.splitext(os.path.split(txt_blog_path)[-1])[0]
    with open(txt_blog_path) as f:
        post_text = f.read()
    parsed_html = ''
    post_link = ''
    for txt in post_text.split('# end'):
        if not txt:
            continue
        section, content = txt.split(':\n\t')[0].strip().strip("'''"), txt.split(':\n\t')[1].strip()
        parsed_content = None
        if section == 'post':
            content = parse_post(txt)
        elif section == 'timestamp':
            content, parsed_content = create_timestamp(content)
        elif section == 'link':
            post_link = content
        elif section == 'next' or section == 'previous':
            parsed_content = ' '.join([c.capitalize() for c in content.strip('/').split('-')])
            content = url_prefix + content

        # Attach prefix or postfix to a section
        prefix, postfix = section_pre_postfix(section)
        # A special case where html values to be applied repeatedly
        if section == 'tags':
            section_html = ''
            category = [v.strip().rstrip(',') for v in content.split(' ')]
            for val in category:
                section_html += apply_html_value(section, val, val)
        else:
            section_html = apply_html_value(section, content, parsed_content)
        parsed_html += '\n\t' + prefix + section_html + postfix
    # for section in ['previous', 'next']:
    #     prefix, postfix = section_pre_postfix(section)
    #     section_html = apply_html_value(section, '#', )
    #     # section_html = ''
    #     parsed_html += '\n\t' + prefix + section_html + postfix

    create_post_file(
        blog_id,
        post_link,
        '''{% extends "base.html" %}
        
        {% block content %}''' + parsed_html + '''{% endblock content %}''',
        category)


# parse_blog()

if __name__ == '__main__':
    pass


