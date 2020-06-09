from Threeks.users import users
from Threeks.users.forms import SignupForm, LoginForm, UpdateProfileForm, RequestResetPasswordForm, ResetPasswordForm
from Threeks.users.utils import send_reset_email, save_image
from Threeks.models import User, Post
from Threeks import bcrypt, db
from flask_login import current_user, login_user, logout_user, login_required
from flask import redirect, url_for, request, flash, render_template



@users.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f"You have Signed up Successfully as {form.username.data}", "success")
            return redirect(url_for('main.home'))
        else:
            flash("Please Check your email and password", "danger")
    return render_template('signup.html', form=form)

@users.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
                    return redirect(url_for('main.home'))
            else:
                flash("Please Check your email and password", "danger")
    return render_template('login.html', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))



@users.route('/profile', methods=['POST','GET'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.profile_image.data:
            current_user.image_file = save_image(form.profile_image.data)
            db.session.commit()
        
        current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.commit()
        flash('Your informations Has been updated!', 'success')
        return redirect(url_for('users.profile'))
    
    # whenever it is a GET request it will provide the fields with the current user data
    # other than that it won't, and that appears when the user enters an invalid input
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    return render_template('profile.html', profile=True, form=form)

@users.route('/user/<string:username>')
def user(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date.desc()).paginate(per_page=7, page=page)
    return render_template('user.html', user=user, posts=posts)

@users.route('/reset', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RequestResetPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('We sent you an email with the instructions to reset your password.', 'info')
        # FIXME: there is a bug here if you stayed in this page and changed the password
        # in another page you will be able in the first page to login with the old password
        # and that is because sqlalchemy locks the database on its state and didn't take the
        # updates, but I think with using the mysql.connector it will be fixed I will try it
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', form=form)

@users.route('/reset/<token>', methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    user = User.check_token(token)
    if not user:
        flash('your token is expired or invalid!', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been reset, Now you can login again!', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_password.html', form=form)