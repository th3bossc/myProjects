from flask import Blueprint, request, flash, redirect, render_template, url_for, abort
from flask_login import current_user, login_required
from myProjects.posts.forms import newPostForm
from myProjects.models import Post
from myProjects import db
posts = Blueprint('posts', __name__) 

@posts.route('/posts/new', methods = ['GET', 'POST'])
@login_required
def new_post():
    form = newPostForm()

    if form.validate_on_submit():
        newPost = Post(title = form.title.data, content = form.content.data, author = current_user)
        if form.link.data:
            newPost.link = form.link.data
        if form.source.data:
            newPost.source_code = form.source.data
        print(newPost.user_id)
        db.session.add(newPost)
        db.session.commit()
        flash(message = 'Post created successfully', category = "success")
        return redirect(url_for('posts.post', post_id = newPost.id))
    return render_template('newpost.html', page_details = 'New Post', title = 'New Post', form = form, legend = "Create Post")

@posts.route('/posts/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    print(post)
    return render_template('post.html', post = post, page_details = f"Post by {post.author.username}")


@posts.route('/posts/<int:post_id>/update', methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)
    form = newPostForm()

    if form.validate_on_submit():
        post.title = form.title.data 
        post.content = form.content.data
        post.link = form.link.data
        post.source_code = form.source.data
        db.session.commit()
        flash(message = "Post updated successfully", category = "info")
        return redirect(url_for('posts.post', post_id = post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        if post.link:
            form.link.data = post.link
        if post.source_code:
            form.source.data = post.source_code
    return render_template('newpost.html', page_details = "Edit Post", title = "Edit Post",  form = form, post = post, legend = "Edit Post")

@posts.route('/posts/<int:post_id>/delete')
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    flash(message = "Post deleted successfully", category = "info")
    return redirect(url_for('main.home'))

