"""Blogly application."""

from flask import Flask,render_template,request,redirect
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

@app.route("/users")
def list_users():
    """List pets and show add form."""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("list.html", users=users)

@app.route("/users/<int:userid>")
def view_userdetail(userid):
    user = User.query.get_or_404(userid)
    return render_template("detail.html", user = user)

@app.route("/users/new")
def form_addnew():
    return render_template("new_user.html")

@app.route("/users/<int:userid>/edit")
def form_edit(userid):
    user = User.query.get_or_404(userid)
    return render_template("edit_user.html",user = user)

@app.route("/users/new", methods= ["POST"])
def add_new():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image = request.form['image_url']
    new_user = User(first_name = first_name, last_name = last_name, image = image)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users/{new_user.id}")

@app.route("/users/<int:userid>/edit", methods= ["POST"])
def submit_edit(userid):
    user = User.query.get_or_404(userid)
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image = request.form['image_url']
    user.first_name = first_name
    user.last_name = last_name
    user.image = image
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route("/users/<int:userid>/delete", methods= ["POST"])
def delete_user(userid):
    user = User.query.filter_by(id=userid).delete()
    db.session.commit()
    return redirect("/users")
