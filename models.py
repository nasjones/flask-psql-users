"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """USER"""
    ___tablename___ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(), nullable=False)

    last_name = db.Column(db.String(), nullable=False)

    image_url = db.Column(db.String(), nullable=True,
                          default="https://i.picsum.photos/id/1014/6016/4000.jpg?hmac=yMXsznFliL_Y2E2M-qZEsOZE1micNu8TwgNlHj7kzs8")

    def __repr__(self):
        return f"User id={self.id} full name ={self.first_name} {self.last_name} image_url={self.image_url}"
