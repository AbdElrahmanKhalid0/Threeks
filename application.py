from flask import Flask, render_template
import datetime

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
