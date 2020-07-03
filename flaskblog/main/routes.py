from flaskblog import db
from flask import render_template, redirect, url_for,  request, Blueprint
from flaskblog.models import Post  # , PostHistory
from datetime import timezone

main = Blueprint('main', __name__)


db.create_all()


@main.route('/favicon.ico')
def favicon():
    # bg_scheduler(clearfolder, 'profile_pics/temp')
    return redirect(url_for('static', filename='favicon.ico'))


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(Post.date_edited).all()
    posts = Post.query.order_by(Post.date_edited.desc())\
        .paginate(page=page, per_page=5)
    # for post in posts.items:
    #     print(post.content + str(post.date_edited))
    # posts_history = PostHistory.query.all()
    tz = timezone.utc
    return render_template('home.html', posts=posts, tz=tz, title='TESTE')


@main.route('/about')
def about():
    return render_template('about.html')
