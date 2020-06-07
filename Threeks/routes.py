from flask import render_template, flash, url_for, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from Threeks.forms import SignupForm, LoginForm, UpdateProfileForm
from Threeks.models import User, Post
from Threeks import app, db, bcrypt
from PIL import Image
import datetime
import secrets
import os

posts=[
    {
        'author': 'Abdelrahman',
        'title': 'Hola, First one',
        'body': 'This is The first Post ever',
        'date': datetime.date.today()
    },
    {
        'author': 'Khalid',
        'title': 'Hola, not First one',
        'body': 'This is The second Post ever',
        'date': datetime.date(year=2014, month=2, day=16)
    },
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f"You have Signed up Successfully as {form.username.data}", "success")
            return redirect(url_for('home'))
        else:
            flash("Please Check your email and password", "danger")
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            next_page = request.args.get('next')
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash(f"You have Logged in Successfully", "success")
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for('home'))
            else:
                flash("Please Check your email and password", "danger")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_image(image_data):
    random_name = secrets.token_hex(8)
    _, img_ext = os.path.splitext(image_data.filename)
    image_name = random_name + img_ext
    image_path = os.path.join(app.root_path, r'static\images' ,image_name)

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

@app.route('/profile', methods=['POST','GET'])
@login_required
def profile():
    form = UpdateProfileForm()
    print(app.root_path)
    if form.validate_on_submit():
        if form.profile_image.data:
            current_user.image_file = save_image(form.profile_image.data)
            db.session.commit()
        
        current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.commit()
        flash('Your informations Has been updated!', 'success')
        return redirect(url_for('profile'))
    
    # whenever it is a GET request it will provide the fields with the current user data
    # other than that it won't, and that appears when the user enters an invalid input
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    return render_template('profile.html', profile=True, form=form)