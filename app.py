"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from sqlalchemy.exc import IntegrityError
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Posts, Tags, PostTag

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
    return render_template('user_list.html', users=User.query.all())


@app.route('/users/new', methods=['POST', 'GET'])
def add_user():
    if request.method == 'GET':
        return render_template('new_user_form.html')
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
        db.session.commit()
        return redirect(f'/users/{user.id}')


@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')


@app.route('/users/<user_id>/posts/new', methods=['POST', 'GET'])
def add_post(user_id):
    if request.method == 'GET':
        user = User.query.get_or_404(user_id)
        tags = Tags.query.all()
        return render_template('new_post_form.html', user=user, tags=tags)
    else:
        title = request.form['title-input']
        content = request.form['content-input']
        tags = request.form.getlist('tag')
        new_post = Posts(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        if tags:
            for tag in tags:
                new_relation = PostTag(post_id=new_post.id, tag_id=tag)
                db.session.add(new_relation)
        db.session.commit()
        return redirect(f'/users/{user_id}')


@app.route('/posts/<post_id>')
def post_display(post_id):
    post = Posts.query.get_or_404(post_id)
    user = User.query.get(post.user_id)
    return render_template('post_display.html', post=post, user=user, tags=post.tags)


@app.route('/posts/<post_id>/edit', methods=['POST', 'GET'])
def post_edit(post_id):
    post = Posts.query.get_or_404(post_id)
    if request.method == 'GET':
        tags = Tags.query.all()
        return render_template('edit_post_form.html', post=post, tags=tags)
    else:
        post.title = request.form['title-input']
        post.content = request.form['content-input']
        tags = request.form.getlist('tag')
        for relation in PostTag.query.filter_by(post_id=post.id).all():
            db.session.delete(relation)

        if tags:
            for tag in tags:
                new_relation = PostTag(post_id=post.id, tag_id=tag)
                db.session.add(new_relation)

        db.session.commit()
        return redirect(f'/posts/{post.id}')


@app.route('/posts/<post_id>/delete', methods=['POST'])
def post_delete(post_id):
    post = Posts.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')


@app.route('/tags')
def tag_list():
    tags = Tags.query.all()
    return render_template('tag_list.html', tags=tags)


@app.route('/tags/new', methods=['POST', 'GET'])
def add_tag():
    if request.method == 'GET':
        return render_template('new_tag_form.html')
    else:
        name = request.form['name-input']
        new_tag = Tags(name=name)
        db.session.add(new_tag)
        try:
            db.session.commit()
            flash("Successfully added the tag.", "success")
        except IntegrityError:
            flash("Sorry this tag already exists.", "error")

        return render_template('new_tag_form.html')


@app.route('/tags/<tag_id>')
def tag_display(tag_id):
    tag = Tags.query.get(tag_id)
    return render_template('tag_display.html', tag=tag)


@app.route('/tags/<tag_id>/edit', methods=['POST', 'GET'])
def tag_edit(tag_id):
    tag = Tags.query.get(tag_id)
    if request.method == "GET":
        return render_template("edit_tag_form.html", tag=tag)
    else:
        tag.name = request.form['name-input']
        try:
            db.session.commit()
            flash("Successfully updated the tag.", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Sorry this tag already exists.", "error")

        return render_template('edit_tag_form.html', tag=tag)


@app.route('/tags/<tag_id>/delete')
def tag_delete(tag_id):
    tag = Tags.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag:{tag.name} successfully deleted", "success")
    return redirect('/tags')
