"""Contains mapper for tags"""


template_mapper = {
    'image': '<img src="#dynamic_value_1">',
    'title': '<h1>#dynamic_value_1</h1>',
    'timestamp': '<time class="entry-date published" datetime="#dynamic_value_1">#dynamic_value_2</time>',
    'post': '<div id="post">\n\t<p>#dynamic_value_1</p>\n\t</div>',
    'tags': '<a href="/blog?category=#dynamic_value_1">#dynamic_value_2</a>',
    'previous': '<div class="align-left"><a href="#dynamic_value_1">#dynamic_value_2</a></div>',
    'next': '<div class="align-right"><a href="#dynamic_value_1">#dynamic_value_2</a></div>',
}

tag_mapper = {
    '<code>': '<pre>',
    '<bold>': '<strong>',
    '<italic>': '<i>',
    '<quote>': '<blockquote>',
    '<link>': '<a>'
}