from flask import Blueprint, render_template, url_for, request, current_app
from myProjects.main.utils import get_leetcode, dict_to_file
from myProjects.models import Post, User
import os
import json
main = Blueprint('main', __name__) 


@main.route('/')
@main.route('/home')
def home():
    # dict_to_file(get_leetcode())
    # leetcode = {}
    # with open(os.path.join(current_app.root_path + '/static/leetcode.json'), 'r') as json_file:
    #     leetcode = json.load(json_file)
    page = request.args.get('page', type = int, default = 1)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5)
    return render_template('home.html', title = 'Home', page_details = "My Projects", posts = posts, page = page)


@main.route('/about')
def about():  
    # leetcode = {}
    # with open(os.path.join(current_app.root_path + '/static/leetcode.json'), 'r') as json_file:
    #     leetcode = json.load(json_file)
    return render_template('about.html', title = 'About', page_details = "About Me")


@main.route('/test')
def test(): 
    # leetcode = {}
    # with open(os.path.join(current_app.root_path + '/static/leetcode.json'), 'r') as json_file:
    #     leetcode = json.load(json_file)
    # print(leetcode)
    return render_template('about.html', title = "Test", page_details = 'Test TEST')


