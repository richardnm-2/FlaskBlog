from flask import render_template, url_for, flash, redirect, request, jsonify, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt, sess_uuid
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm,
                                   UpdateAccountForm, RequestResetForm,
                                   ResetPasswordForm)
from flaskblog.users.utils import (transfer_picture_to_main_folder,
                                   upload, send_reset_email)
from datetime import timezone


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).\
                            decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=form.remember.data)
        flash('Your account has been created! You are now able to log in',
              'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else\
                redirect(url_for('main.home'))
        else:
            flash('Login Unsuccesful. Please check email and password',
                  'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    image_file = request.args.get('file', type=str)
    form = UpdateAccountForm()
    picture_form = request.form
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        picture_upload = False
        try:
            picture_file, picture_upload =\
                transfer_picture_to_main_folder(current_user.image_file)
            print(current_user.image_file)
            current_user.image_file = picture_file
        except Exception:
            if picture_upload:
                flash('Something went wrong, please try again.', 'danger')
                current_user.image_file = "default.jpeg"
            return redirect(url_for('users.account'))

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    elif len(picture_form) > 0:
        form.picture.data, filename = upload(picture_form)
        image_file = url_for('static', filename=form.picture.data)
        print(str(form.picture.data))
        print(image_file)
        print("")

        return jsonify({'src': image_file})
        # return redirect(url_for('users.account', file=filename))

    image_file = url_for('static', filename='profile_pics/'
                            + current_user.image_file)
    return render_template('account.html', title='Account',
                            image_file=image_file, form=form)
        


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_edited.desc())\
        .paginate(page=page, per_page=5)

    tz = timezone.utc
    return render_template('user_posts.html', posts=posts, user=user, tz=tz)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('''
An email has been sent with instructions to reset your password.''',
              'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password',
                           form=form)


@users.route("/reset_password/<string:token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)

    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        login_user(user, remember=form.remember.data)
        flash('Your password has been updated! You are now able to log in',
              'success')
        return redirect(url_for('main.home'))

    return render_template('reset_token.html', title='Reset Password',
                           form=form)
