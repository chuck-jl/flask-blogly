"""Blogly application."""

from flask import Flask,render_template,request,redirect,flash
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.route("/")
def home_page():
    """home page with top 5 recent posts"""
    posts= Post.query.order_by(Post.create_at.desc()).limit(5)
    return render_template("home.html", posts= posts)


@app.route("/users")
def list_users():
    """List users and show add form."""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("list.html", users=users)

@app.route("/users/<int:userid>")
def view_userdetail(userid):
    """List user detail and show post related."""

    user = User.query.get_or_404(userid)
    return render_template("detail.html", user = user)

@app.route("/users/new")
def form_addnew():
    """show add new user form."""
    return render_template("new_user.html")

@app.route("/users/<int:userid>/edit")
def form_edit(userid):
    """Show edit user info form."""
    user = User.query.get_or_404(userid)
    return render_template("edit_user.html",user = user)

@app.route("/users/new", methods= ["POST"])
def add_new():
    """Handle post request to add a user and redirect to users page."""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image = request.form['image_url']
    if((not first_name)  or (not last_name)):
        flash("First name or last name could not be null, please try again",'error')
        page = redirect("/users")
    else:
        if(not image):
            flash("You did not pick an image for yourself, we will use a default. You can edit it later.",'warning')
            image = None
        new_user = User(first_name = first_name, last_name = last_name, image = image)
        db.session.add(new_user)
        db.session.commit()
        page = redirect(f"/users/{new_user.id}")
        flash("User created!","info")
    return page

@app.route("/users/<int:userid>/edit", methods= ["POST"])
def submit_edit(userid):
    """Handle post request to edit a user and redirect to user page."""
    user = User.query.get_or_404(userid)
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image = request.form['image_url']
    if(first_name):
        user.first_name = first_name
    if(last_name):
        user.last_name = last_name
    if(image):
        user.image = image
    
    db.session.add(user)
    db.session.commit()
    flash("User info updated",'info')
    return redirect(f"/users/{user.id}")

@app.route("/users/<int:userid>/delete", methods= ["POST"])
def delete_user(userid):
    """Handle post request to delete a user and redirect to users page."""
    user = db.session.query(User).filter(User.id==userid).first()
    db.session.delete(user)
    db.session.commit()
    flash("User deleted",'info')
    return redirect("/users")

@app.route("/users/<int:userid>/posts/new")
def form_newpost(userid):
    """show add new post form for each user."""
    user = User.query.get_or_404(userid)
    return render_template("new_post.html", user = user)

@app.route("/users/<int:userid>/posts/new", methods = ["POST"])
def submit_newpost(userid):
    """Submit the new post and redirect back to user page."""
    title = request.form['title']
    content = request.form['content']
    if(not title):
        flash('No title captured from your new post, you can edit it later','warning')
        title = None
    if(not content):
        flash('No content captured from your new post, you can edit it later','warning')
        content = None
    new_post = Post(title = title, content = content, user_id = userid)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{userid}")

@app.route("/posts/<int:post_id>")
def show_postdetail(post_id):
    """show a page with detail information about a post"""
    post = Post.query.get_or_404(post_id)
    return render_template("post_detail.html", post = post)

@app.route("/posts/<int:post_id>/edit")
def form_editpost(post_id):
    """Show edit post form."""
    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html",post = post)

@app.route("/posts/<int:post_id>/edit", methods= ["POST"])
def submit_editpost(post_id):
    """Show edit post form."""
    post = Post.query.get_or_404(post_id)
    title = request.form['title']
    content = request.form['content']
    if(title):
        post.title = title
    if(content):
       post.content = content 
    flash('Post information updated','info')
    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:postid>/delete", methods= ["POST"])
def delete_post(postid):
    """Handle post request to delete a user and redirect to users page."""
    ownerid= Post.query.get_or_404(postid).owner.id

    post = Post.query.filter_by(id=postid).delete()
    db.session.commit()
    flash('Post deleted','info')
    return redirect(f"/users/{ownerid}")

@app.errorhandler(404)
def page_not_found(e):
    """404 page"""
    return render_template('404.html'), 404