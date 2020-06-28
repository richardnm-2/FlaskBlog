from flaskblog import db
from flaskblog.models import User, Post, PostHistory, DeletedPost, DeletedPostHistory
from datetime import datetime

def delete_move_post(post):
    post_history = PostHistory.query.filter_by(post_id=post.id).all()  
    deleted_post = DeletedPost()
    deleted_post_history = DeletedPostHistory()
    
    # if len(post_history) > 0:
    deleted_post.title = post.title
    deleted_post.date_posted = post.date_posted
    deleted_post.date_edited = post.date_edited
    deleted_post.date_deleted = datetime.utcnow()
    deleted_post.content = post.content
    deleted_post.user_id = post.author.id
    post_id = post.id
    db.session.add(deleted_post)

    db.session.commit()
    db.session.delete(post)

    for posth in post_history:
        deleted_post_history = DeletedPostHistory()
        deleted_post_history.title = posth.title
        deleted_post_history.date_edited = posth.date_edited
        deleted_post_history.content = posth.content
        deleted_post_history.post_id = deleted_post.id
        db.session.add(deleted_post_history)
        db.session.delete(posth)

    db.session.commit()