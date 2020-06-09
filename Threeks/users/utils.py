import secrets
import os
from PIL import Image
from Threeks import mail
from flask_mail import Message
from flask import url_for, current_app

def save_image(image_data):
    random_name = secrets.token_hex(8)
    _, img_ext = os.path.splitext(image_data.filename)
    image_name = random_name + img_ext
    image_path = os.path.join(current_app.root_path, r'static\images' ,image_name)

    img = Image.open(image_data)
    img_width, img_height = img.size
    # the crop function takes a tuble that is formatted like this in pixels
    # (left, top, right, bottom) and every measure should start from the point
    # (0,0) in the top left of the image
    # if the image is a square or close to a one it will be saved without cropping
    if img_width == img_height or abs(img_width - img_height) < 10:
        img.save(image_path)
    # if it's not it will crop it to its bigger center square
    else:
        if img_height > img_width:
            img = img.crop((0, (img_height - img_width) / 2, img_width, img_height - ((img_height - img_width) / 2)))
        else:
            img = img.crop(((img_width - img_height) / 2, 0, img_width - ((img_width - img_height) / 2), img_height))

    # then it will resize the image to decrease its size
    # the thumbnail function differes from the resize function that it keeps the aspect ratio of the image
    img.thumbnail((200, 200))
    # then saving it
    img.save(image_path)
    
    # returns the name of the image to be stored in the database
    return image_name

def send_reset_email(user):
    token = user.get_token()
    
    msg = Message('Password Reset Request',recipients=[user.email],sender='no-reply@threeks.com')
    msg.body = f"""To Reset Your password Follow this link:
{url_for('users.reset_password', token=token, _external=True)}

if you never sent this request please ignore it and nothing will be changed"""
    mail.send(msg)