from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, PostHistory
from flaskblog.posts.forms import PostForm
from datetime import datetime, timezone
from flaskblog.posts.utils import delete_move_post  # , create_mass

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route('/post/<int:post_id>')
def post(post_id):
    tz = timezone.utc
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, tz=tz)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post_edit = PostHistory()
        post_edit.title = post.title
        post_edit.date_edited = post.date_edited
        post_edit.content = post.content
        post_edit.post_id = post.id
        db.session.add(post_edit)

        post.date_edited = datetime.utcnow()
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    delete_move_post(post)

    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/post/create", methods=['GET', 'POST'])
@login_required
def create_json():
    # create_mass()
    return redirect(url_for('main.home'))
