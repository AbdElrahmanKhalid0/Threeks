from Threeks.posts import posts
from Threeks.posts.forms import PostForm
from Threeks.models import Post
from Threeks import db
from flask import flash, redirect, url_for, render_template, request, abort
from flask_login import current_user

@posts.route('/add_post', methods=['POST','GET'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('You Threeked!', 'success')
        return redirect(url_for('main.home'))

    return render_template('add_post.html', form=form)

@posts.route('/post/<int:post_id>')
def post(post_id):
    # the get_or_404 function returns 404 error if the data wasn't found instead of returning
    # None like the get function
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@posts.route('/post/<int:post_id>/update', methods=['POST','GET'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()

    # this stops the user from getting this page if he isn't the post's author
    if post.author != current_user:
        abort(403)

    if request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        flash('Your Post Has been Updated!', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    
    return render_template('add_post.html', form=form)

@posts.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()

    flash('Your Post has Been Deleted!', 'success')
    return redirect(url_for('main.home'))