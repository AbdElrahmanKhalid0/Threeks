from flask import Flask, render_template

app = Flask(__name__)

posts=[]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts, usertname='abdelrahman')

@app.route('/about')
def about():
    return "about"


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
