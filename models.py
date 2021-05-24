"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()


Default_img_url = "https://i.picsum.photos/id/1014/6016/4000.jpg?hmac=yMXsznFliL_Y2E2M-qZEsOZE1micNu8TwgNlHj7kzs8"


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """users table"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    image_url = db.Column(db.String(), nullable=True, default=Default_img_url)

    def __repr__(self):
        return f"User id={self.id} full name ={self.first_name} {self.last_name} image_url={self.image_url}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    full_name = property(get_full_name)


class Posts(db.Model):
    """Posts model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(), nullable=False)
    content = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    users = db.relationship('User', backref='Posts')

    def __repr__(self):
        return f'id={self.id} title={self.title} created={self.created_at} user={self.user_id}'
