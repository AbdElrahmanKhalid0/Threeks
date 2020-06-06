from flask import Flask, render_template, flash, url_for, redirect, request
from forms import SignupForm, LoginForm
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = '4bcde902803e55ae1211f9ba7f3ab7c1'

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
    return render_template('home.html', posts=posts, usertname='abdelrahman')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flash(f"You have Signed up Successfully as {form.username.data}", "success")
            return redirect(url_for('home'))
        else:
            flash("Please Check your email and password", "danger")
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flash(f"You have Logged in Successfully as {form.email.data}", "success")
            return redirect(url_for('home'))
        else:
            flash("Please Check your email and password", "danger")
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
