"""Blogly application."""

from flask import Flask, render_template, request, redirect
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "hush"
# debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home():
    return redirect('/users')


@app.route('/users')
def list_users():
    return render_template('users.html', users=User.query.all())


@app.route('/users/new', methods=['POST', 'GET'])
def add_user():
    if request.method == 'GET':
        return render_template('add_user_form.html')
    else:
        first_name = request.form['first-name-input']
        last_name = request.form['last-name-input']
        url = request.form['url-input']
        if url:
            new_user = User(first_name=first_name,
                            last_name=last_name, image_url=url)
        else:
            new_user = User(first_name=first_name,
                            last_name=last_name)

        db.session.add(new_user)
        db.session.commit()
        return redirect('/')


@app.route('/users/<user_id>')
def user_display(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_display.html', user=user)


@app.route('/users/<user_id>/edit', methods=['POST', 'GET'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if request.method == 'GET':
        return render_template('edit_user_form.html', user=user)
    else:
        user.first_name = request.form['first-name-input']
        user.last_name = request.form['last-name-input']
        user.image_url = request.form['url-input']

        # db.session.add(user)
        db.session.commit()
        return redirect(f'/users/{user.id}')


@app.route('/users/<user_id>/delete')
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')
