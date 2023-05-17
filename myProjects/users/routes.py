from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from myProjects.users.forms import RegistrationForm, RequestResetForm, ResetPasswordForm, LoginForm, ProfileUpdateForm
from myProjects import bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
from myProjects.models import User, Post
from myProjects.users.utils import save_picture, send_reset_mail
import os
import json
users = Blueprint('users', __name__)


@users.route('/register', methods = ['GET', 'POST'])
def register():
    leetcode = {}
    with open(os.path.join(current_app.root_path + '/static/leetcode.json'), 'r') as json_file:
        leetcode = json.load(json_file)
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(password = form.password.data).decode('utf-8')
        new_user = User(username = form.username.data, email = form.email.data, password = hashed_password) 
        db.session.add(new_user)
        db.session.commit()
        flash(message = f"Account creation successful. Welcome {form.username.data}", category = 'success')
        return redirect(url_for('main.home')) 

    return render_template('register.html', title = "Register", form = form, page_details = "Account Registration", **leetcode)
    
    



@users.route('/login', methods = ['GET', 'POST'])
def login():
    leetcode = {}
    with open(os.path.join(current_app.root_path + '/static/leetcode.json'), 'r') as json_file:
        leetcode = json.load(json_file)
    if current_user.is_authenticated:
        return redirect('users.profile')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first_or_404()
        if user and bcrypt.check_password_hash(pw_hash = user.password, password = form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            flash(message = "Successfully Logged In", category = 'success')
            return redirect(next_page) if next_page is not None else redirect(url_for('main.home'))
        flash(message = "Login Unsuccessful", category = "danger")
    return render_template('login.html', title = "LogIn", form = form, page_details = "Account Login", **leetcode)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    leetcode = {}
    with open(os.path.join(current_app.root_path + '/static/leetcode.json'), 'r') as json_file:
        leetcode = json.load(json_file)
    #print(current_user)
    image_file = url_for('static', filename = 'images/' + current_user.image_file)
    print(image_file)
    #print(image_file)
    form = ProfileUpdateForm()

    if form.validate_on_submit():
        print(form.data)
        if form.profile_image.data:
            print(form.profile_image.data)
            picture_file = save_picture(form.profile_image.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data 
        db.session.commit() 
        flash(message = "Account details updated", category = "info")
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email 

    return render_template('profile.html', image_file = image_file, form = form, page_details = "Account Information", **leetcode)


@users.route('/users/<string:username>')
def user_post(username):
    leetcode = {}
    with open(os.path.join(current_app.root_path + '/static/leetcode.json'), 'r') as json_file:
        leetcode = json.load(json_file)
    page = request.args.get('page', default = 1, type = int)
    user = User.query.filter_by(username = username).first_or_404()
    posts = Post.query.filter_by(author = user).order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5)

    return render_template('user_posts.html', posts = posts, user = user, title = f"Posts by {user.username}", page_details = f"Posts by {user.username}", **leetcode)



@users.route('/reset_request', methods = ['GET', 'POST'])
def reset_request():
    leetcode = {}
    with open(os.path.join(current_app.root_path + '/static/leetcode.json'), 'r') as json_file:
        leetcode = json.load(json_file)
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first_or_404()
        if user:
            print(user)
            send_reset_mail(user)
            flash(message = "Reset Link sent successfully. Please check your inbox", category = "info")
            return redirect(url_for('users.login'))
    return render_template('reset_request.html', form = form, page_details = 'Reset Password', **leetcode)

@users.route('/reset_password/<string:token>', methods = ['GET', 'POST'])
def reset_password(token):
    leetcode = {}
    with open(os.path.join(current_app.root_path + '/static/leetcode.json'), 'r') as json_file:
        leetcode = json.load(json_file)
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    
    if user is None:
        flash(message = "The Link has timed out. Please try again", category = "danger")
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(password = form.new_password.data).decode('utf-8')
        user.password = hashed_pw 
        db.session.commit()
        flash(message = "Password has been reset successfully, Please login with new credentials", category = "info")
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', form = form, page_details = 'Reset Password', **leetcode)