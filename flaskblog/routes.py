from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post, PostHistory, DeletedPost, DeletedPostHistory
from flask_login import login_user, logout_user, current_user, login_required
from flaskblog.my_functions.upload import upload, transfer_picture_to_main_folder
from flaskblog.my_functions.delete import delete_move_post
from uuid import uuid4
from datetime import datetime, timezone


db.create_all()

@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.order_by(Post.date_edited).all()
    for post in posts:
        print(post.content + str(post.date_edited))
    posts_history = PostHistory.query.all()
    tz = timezone.utc
    return render_template('home.html', posts=posts, tz=tz, title='TESTE')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=form.remember.data)
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))    
    form = LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccesful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    picture_form = request.form
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        picture_upload = False
        try:
            picture_file, picture_upload = transfer_picture_to_main_folder(current_user.image_file)
            print(current_user.image_file)
            current_user.image_file = picture_file
        except:
            if picture_upload:    
                flash('Something went wrong, please try again.', 'danger')
                current_user.image_file = "default.jpeg"
            # return redirect(url_for('account'))
        
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    elif len(picture_form) > 0:
        form.picture.data = upload(picture_form)
        print(str(form.picture.data))
        print("")
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content = form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                            form=form, legend='New Post')

@app.route('/post/<int:post_id>')
def post(post_id):
    tz = timezone.utc
    post= Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, tz=tz)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post= Post.query.get_or_404(post_id)
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
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                            form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post= Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    delete_move_post(post)
   
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))