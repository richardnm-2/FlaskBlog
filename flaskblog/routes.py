from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
from flaskblog.my_functions.upload import upload, transfer_picture_to_main_folder
from uuid import uuid4

db.create_all()

posts = [
    {
        'author': 'Richard',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2020',
    },

    {
        'author': 'Richard Meijerink',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2020',
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts, title='TESTE')

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
