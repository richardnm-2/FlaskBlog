import flaskblog
from flaskblog import sess_uuid
from flask import request
import os
import secrets
from pathlib import Path
import shutil
import json
import glob
from uuid import uuid4
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
    target = os.path.join(dirname, r"static\profile_pics\temp\{}".format(sess_uuid))
    # target = "C:/Users/Richard/Documents/Python/Flask/FlaskBlog/flaskblog/static/profile_pics"
    if not os.path.exists(target):
        try:
            os.mkdir(target)
        except:
            pass
            if is_ajax:
                print('Error creating folder')
                return ajax_response(False, "Couldn't create upload directory: {}".format(target))
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
        upload.save(destination)
    
    return destination

def transfer_picture_to_main_folder(old_picture):
    dirname = os.path.dirname(flaskblog.__file__)
    sess_uuid_path = os.path.join(dirname, r"static\profile_pics\temp\{}".format(sess_uuid)) 
    picture_path = os.path.join(os.sep, sess_uuid_path, os.listdir(sess_uuid_path)[0])
    picture_name = os.path.basename(picture_path)
    path = str(Path(picture_path).parent)
    print(str(Path(picture_path).parent) + os.sep + picture_name)
    dest = str(Path(str(Path(str(Path(picture_path).parent)).parent)).parent) + os.sep + picture_name

    shutil.move(picture_path, dest)
    
    try:
        os.rmdir(sess_uuid_path)
        picture_upload = True
    except OSError as e:
        picture_upload = False
        print("Error: %s : %s" % (sess_uuid_path, e.strerror))

    # print(os.path.join(os.sep, dirname, "static/profile_pics/", old_picture))
    try:
        os.remove(os.path.join(os.sep, dirname, "static/profile_pics/", old_picture))
    except:
        return picture_name, picture_upload    
    return picture_name, picture_upload
