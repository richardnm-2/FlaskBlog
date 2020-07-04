import os
import secrets
from PIL import Image
from flask import url_for, request, current_app
from flask_mail import Message
import flaskblog
from flaskblog import sess_uuid, mail
from pathlib import Path
import shutil
# import json
# import glob
# from uuid import uuid4
# from functions import functions as fn


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
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    target = ""
    dirname = os.path.dirname(current_app.root_path)
    dirname = os.path.dirname(flaskblog.__file__)
    print("")
    print("")
    print("")
    print(dirname)
    print("")
    print("")
    print("")
    # target = os.path.normpath(os.path.join(dirname, r"static\profile_pics\temp\{}".
                        #   format(sess_uuid)))
    target = os.path.join(dirname, r"static/profile_pics/temp/{}".format(sess_uuid))
    tgt = os.path.normpath(os.path.join(dirname, r"static/profile_pics/temp"))
    print(tgt)
    if not os.path.exists(target):
        try:
            print(target)
            os.mkdir(target)
        except Exception as inst:
            print(inst)
            if is_ajax:
                print('Error creating folder')
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
    return rel_path, filename


def transfer_picture_to_main_folder(old_picture):
    dirname = os.path.dirname(flaskblog.__file__)
    sess_uuid_path = os.path.join(dirname, r"static/profile_pics/temp/{}".
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
        print(sess_uuid_path)
        os.rmdir(sess_uuid_path)
        picture_upload = True
    except OSError as e:
        picture_upload = False
        print("Error: %s : %s" % (sess_uuid_path, e.strerror))

    # print(os.path.join(os.sep, dirname, "static/profile_pics/", old_picture))
    try:
        rm_dir = os.path.join(dirname, r"static/profile_pics",
                              old_picture)
        print(rm_dir)

        os.remove(os.path.join(dirname, r"static/profile_pics",
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
