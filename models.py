"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db= SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Class to refer to users"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    first_name = db.Column(db.String(50),
                            nullable = False)
    last_name = db.Column(db.String(50),
                            nullable = False)
    image = db.Column(db.Text, 
                        default='https://images.unsplash.com/photo-1519400197429-404ae1a1e184?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=700&q=80')
    posts = db.relationship('Post',backref='owner', cascade="all, delete-orphan" )

    @property
    def full_name(self):
        return self.get_full_name()
    
    def __repr__(self):
        """Show info about pet."""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image}>"
    
    def get_full_name(self):
        """Get full name """
        u = self
        return f"{u.first_name} {u.last_name}"

class Post(db.Model):
    """Class to refer to posts"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key= True, autoincrement= True)
    title = db.Column(db.Text, nullable = False, default= 'Unknown title')
    content = db.Column(db.Text, default= 'Woops, nothing has been added yet.')
    create_at = db.Column(db.DateTime,nullable = False, default = datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    

    def __repr__(self):
        p = self
        return f"<Post {p.id} {p.title} {p.create_at}>"
    
    def readable_time(self):
        time = self.create_at
        return time.strftime("%B %d, %Y %H:%M:%S")

class Tag(db.Model):
    """Class to refer to tags"""
    __tablename__= "tags"

    id=db.Column(db.Integer, primary_key=True, autoincrement= True)
    name = db.Column(db.String(25),nullable= False, unique=True)
    description= db.Column(db.Text, default= 'Woops, nothing has been added yet.')
    posts = db.relationship('Post', secondary='posts_tags', backref='tags')

class PostTag(db.Model):
    """Class to link Post and Tag together"""
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'),primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'),primary_key=True)
    

