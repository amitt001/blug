---------------------------
BLUG: Simple Blog Generator
---------------------------

This is a very simple static blog generator from the text file.

The text file has a simple template in which values can be filled and
when `parse` command is passed the template text file is parsed and an HTML
blog file is generated in `templates/posts`.

It is a very lightweight app and the only requirement is flask and Python 3.
There is no database file. Posts are listed based on content of `templates/posts`
directory. Posts sorting is done based on the integer prefix before the posts
files.


I was looking for a blog generator in which I can use the theme of https://amitt001.github.com
as it is, without any modification.


**It's usable but it is still under development**

To generate template blog text file:

Project root has `/posts_base` directory

⇒  python manage.py generate

    Creating new template file: posts_base/1.txt
    Modify file and once done run `python manage.py parse` command.

This creates a **<incremental_number>.txt** file. This file has an incremental number so when running for the first time it creates **1.txt** file and on next run **2.txt**.

The structure of the file is present in `posts_base/base.txt`_. It is divided into following sections:

.. code-block:: html

    # image: this section contains post image
    # title: Post title
    # link: post link
    # timestamp: blog timestamp, for now it can only be `now`
    # post: blog post
    # tags: blog tags

Each section is separated by `# end` tag.

The parsed html file is present in `templates/posts/1_my-first-blog.html`

Create your blog:

.. code-block:: bash

    ⇒  python manage.py generate

        Creating new template file: posts_base/1.txt
        Modify file and once done run python manage.py, compile command.


    ⇒ python manage.py parse

    ⇒ python manage.py

Visit `127.0.0.1:7100/blog`

Requirements
-------------

    `Python 3`

Install requirements:

    `pip install -r requirements.txt`



.. _`posts_base/base.txt`: https://github.com/amitt001/blug/blob/master/posts_base/base.txt