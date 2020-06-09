import datetime
from Threeks import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import itsdangerous

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20), default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    # the lazy=True makes SQLAlchemy loads this only when needed
    posts = db.relationship('Post', backref='author', lazy=True)

    # returns a token that will expire after 30 mins by default
    def get_token(self, expiring_time=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expiring_time)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    # this will check if the token is valid or not
    @staticmethod
    def check_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.image_file})"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post({self.id}, {self.date}, {self.title})"
