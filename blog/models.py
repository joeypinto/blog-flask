from flask_login.mixins import UserMixin
from .config import db
from sqlalchemy.sql import func

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"<User(id='{self.id}', username='{self.first_name}', email='{self.email}'')>"
    
    def __init__(self,first_name,email,password):
        self.first_name = first_name
        self.email = email
        self.password = password

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    posts_content = db.relationship('Post', backref='content', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=func.now())
    description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Post(id='{self.id}', user_id='{self.user_id}', title='{self.title}', date_posted='{self.date_posted}',content_id='{self.content_id}')>"

    def to_dict(self):
        return {"id": self.id,
                "title": self.title,
                "date_posted": self.date_posted}
