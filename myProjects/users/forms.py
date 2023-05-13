from myProjects.models import User 
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField 
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators = [DataRequired(), Length(min = 2, max = 20)]
    )
    email = StringField(
        'Email',
        validators = [DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators = [DataRequired(), Length(min = 8)]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators = [DataRequired(), EqualTo('password')]
    )

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()

        if user:
            raise ValidationError('Username taken! Please choose a different one')
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()

        if user:
            raise ValidationError('Account already exists, Proceed to Login page')


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators = [DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators = [DataRequired(), Length(min = 8)]
    )
    remember = BooleanField('Remember me')
    submit = SubmitField('LogIn') 


class ProfileUpdateForm(FlaskForm):
    username = StringField(
        'Username',
        validators = [DataRequired()]
    )
    email = StringField(
        'Email',
        validators = [DataRequired(), Email()]
    )
    profile_image = FileField(
        'Update Profile Image',
        validators = [FileAllowed(['jpg', 'png', 'gif'])]
    )

    submit = SubmitField('Save Changes')

    def validate_username(self, username):
        if (username.data != current_user.username):
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Username taken! Please choose a different one')
            
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()

            if user:
                raise ValidationError('Another account exists with the entered Email ID')
            

class RequestResetForm(FlaskForm):
    email = StringField(
        'Email',
        validators = [DataRequired(), Email()]
    )

    submit = SubmitField('Send Verification Link')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('Email Does not exist within our servers, Please recheck entered information')
        

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField(
        'New Password',
        validators = [DataRequired(), Length(min = 8)]
    )

    confirm_new_password = PasswordField(
        'Confirm New Password',
        validators = [DataRequired(), Length(min = 8), EqualTo('new_password')]
    )

    submit = SubmitField('Confirm Changes')