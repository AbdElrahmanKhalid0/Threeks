from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from Threeks.models import User


class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(2,20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("We Already have an Account assigned with this email, maybe you tryna Login?!")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is not Available!")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me!")
    submit = SubmitField("Log In")


class UpdateProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(2,20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")
    profile_image = FileField("Update Your Profile Picture!", validators=[FileAllowed(['jpg','jpeg','png'], message="You should upload an image with one of these formats: jpg, jpeg, png")])

    def validate_email(self,email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("We Already have an Account assigned with this email, maybe you tryna Login?!")

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username is not Available!")


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class RequestResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("We don't have This email, you may wanna Sign up first!")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change Password')