import os

from config import config


def posts_map():
    """Helper function that returns a dict of posts URL and title"""
    posts = os.listdir(config['templates']['path'])
    blog_posts = []
    for p in sorted(posts, reverse=True):
        if p.endswith('.html') is False:
            continue
        file_name = os.path.splitext(p)[0]
        _id, file_name = file_name.split('_')[0], file_name.split('_')[1]
        post_title = ''.join(file_name.replace('-', ' '))
        blog_posts.append(['{}/{}'.format(_id, file_name), post_title.title()])
    return blog_posts


def last_post_id():
    txt_blog_dir = config['templates']['txt_blog_dir']
    posts_base = sorted(os.listdir(txt_blog_dir))
    posts_base = [p for p in posts_base if p.endswith('.txt') is True]
    _ = posts_base.pop()
    # Calculate the new text template id
    post_id = 0
    if len(posts_base):
        post_id = int(os.path.splitext(posts_base[-1])[0])
    return post_id


def prev_next_post_dict(post_file):
    """Returns the previous and next blog post link and title of
    post_file file."""
    template_dir = config['templates']['path']
    posts = os.listdir(template_dir)
    all_posts = [p for p in sorted(posts) if p.endswith('.html') is True]
    posts_dict = {}
    try:
        index = all_posts.index(post_file)
        if index > 0:
            prev_index = index - 1
            prev_blog_id, blog_name = all_posts[prev_index].split('_')
            prev_post = blog_name.replace('.html', '')
            posts_dict.update(dict(
                previous_post=' '.join(prev_post.split('-')).title(),
                previous_post_link='{}/{}'.format(prev_blog_id, prev_post))
            )
        if len(all_posts) > index + 1:
            # import pdb;pdb.set_trace()
            next_index = index + 1
            next_blog_id, blog_name = all_posts[next_index].split('_')
            next_post = blog_name.replace('.html', '')
            posts_dict.update(dict(
                next_post=' '.join(next_post.split('-')).title(),
                next_post_link='{}/{}'.format(next_blog_id, next_post))
            )
    except ValueError:
        pass
    return posts_dict
