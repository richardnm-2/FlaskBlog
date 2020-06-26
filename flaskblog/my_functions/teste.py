import os
import shutil
from pathlib import Path



def transfer_picture_to_main_folder(picture_path):
    picture_name = os.path.basename(picture_path)
    path = str(Path(picture_path).parent)
    print(str(Path(picture_path).parent) + os.sep + picture_name)
    dest = str(Path(str(Path(str(Path(picture_path).parent)).parent)).parent) + os.sep + picture_name

    shutil.move(picture_path, dest)

picture_path = r"C:\Users\Richard\Documents\Python\Flask\FlaskBlog\flaskblog\static\profile_pics\temp\f5f5144f-693e-4d74-b179-1e0052f9d8ed\28fd2bf85fcfaea1.jpeg"
transfer_picture_to_main_folder(picture_path)
    # path.parent