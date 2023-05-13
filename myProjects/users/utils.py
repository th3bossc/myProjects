from PIL import Image 
import os 
import secrets
from flask import current_app, url_for
from myProjects import mail
from flask_mail import Message 

def send_reset_mail(user):
    token = user.get_reset_token()
    message = Message('PassWord Reset Request', 
                      sender = "noreply@demo.com", 
                      recipients = [user.email],
    )

    message.body = f''' To reset your password, visit the following link:
{url_for('users.reset_password', token = token, _external = True)}
The following message was intended for:
    user: {user.username}
The link expires in 30 minutes

If you didn't request a password reset, feel free to ignore this message    
'''
    mail.send(message)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    save_path = os.path.join(current_app.root_path + '/static/images/' + random_hex + file_ext)

    img = Image.open(form_picture)
    img.thumbnail((125, 125))
    img.save(save_path)
    return random_hex + file_ext 


