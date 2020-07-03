import os
import secrets
from PIL import Image
from flask import url_for, request
from flask_mail import Message

import flaskblog
from flaskblog import sess_uuid, mail
from pathlib import Path
import shutil
# import json
# import glob
# from uuid import uuid4
# from functions import functions as fn


# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.interval import IntervalTrigger
# import atexit
# import time

# def print_time(msg):
#     print(msg)
#     print (time.strftime('%H:%M:%S'))


# scheduler = BackgroundScheduler()
# scheduler.start()
# scheduler.add_job(
#     func=lambda: clearfolder(url_for('static', filename='profile_pics/temp')),
#     # func=lambda: print_time('a'),
#     trigger=IntervalTrigger(seconds=2),
#     id='printing_time_job',
#     name='Print time every 2 seconds',
#     replace_existing=True)
# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())



def clearfolder(folder_path):
    folder = folder_path
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def upload(form):
    form = request.form

    # upload_key = str(uuid4())
    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    # Target folder for these uploads.
    # target = "/static/profile_pics/temp{}".format(upload_key)
    target = ""
    dirname = os.path.dirname(flaskblog.__file__)
    print("")
    print("")
    print("")
    print(dirname)
    print("")
    print("")
    print("")
    target = os.path.join(dirname, r"static\profile_pics\temp\{}".
                          format(sess_uuid))

    if not os.path.exists(target):
        try:
            os.mkdir(target)
        except Exception:
            pass
            if is_ajax:
                print('Error creating folder')
                # return ajax_response(False, '''Couldn't create upload
                #  directory:
                return "Couldn't create upload directory: {}".format(target)

            else:
                return "Couldn't create upload directory: {}".format(target)
    else:
        pass
        clearfolder(target)

    print("=== Form Data ===")
    for key, value in list(form.items()):
        print(key, "=>", value)

    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]

        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(filename)
        filename = random_hex + f_ext

        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)

        output_size = (125, 125)
        i = Image.open(upload)
        i.thumbnail(output_size)
        i.save(destination)
        # upload.save(destination)
        rel_path = "profile_pics/temp/{}".\
            format(sess_uuid) + "/" + filename
    # return destination

    return rel_path, filename


def transfer_picture_to_main_folder(old_picture):
    dirname = os.path.dirname(flaskblog.__file__)
    sess_uuid_path = os.path.join(dirname, r"static\profile_pics\temp\{}".
                                  format(sess_uuid))
    picture_path = os.path.join(os.sep, sess_uuid_path,
                                os.listdir(sess_uuid_path)[0])
    picture_name = os.path.basename(picture_path)
    # path = str(Path(picture_path).parent)
    print(str(Path(picture_path).parent) + os.sep + picture_name)
    dest = str(Path(str(Path(str(Path(picture_path).parent)).parent)).parent)\
        + os.sep + picture_name

    shutil.move(picture_path, dest)
    try:
        os.rmdir(sess_uuid_path)
        picture_upload = True
    except OSError as e:
        picture_upload = False
        print("Error: %s : %s" % (sess_uuid_path, e.strerror))

    # print(os.path.join(os.sep, dirname, "static/profile_pics/", old_picture))
    try:
        os.remove(os.path.join(os.sep, dirname, "static/profile_pics/",
                               old_picture))
    except Exception:
        return picture_name, picture_upload
    return picture_name, picture_upload


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com', recipients=[user.email])
    msg.body = f''' To reset you password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes
will be made.
'''
    mail.send(msg)
