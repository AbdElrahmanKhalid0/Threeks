from Threeks.main import main
from flask import request, render_template
from Threeks.models import Post

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(per_page=7, page=page)
    return render_template('home.html', posts=posts)

@main.route('/about')
def about():
    return render_template('about.html')