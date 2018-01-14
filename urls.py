from manage import app
from views.blog import index, blog

app.add_url_rule('/blog', view_func=index, methods=['GET'])
app.add_url_rule('/blog/<_id>/<blog_path>', view_func=blog, methods=['GET'])
