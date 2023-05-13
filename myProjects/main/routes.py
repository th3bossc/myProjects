from flask import Blueprint, render_template, url_for, request
from myProjects.models import Post, User
main = Blueprint('main', __name__) 


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', type = int, default = 1)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5)
    return render_template('home.html', title = 'Home', page_details = "My Projects", posts = posts, page = page)



@main.route('/about')
def about():
    return render_template('about.html', title = 'About', page_details = "About Me")


