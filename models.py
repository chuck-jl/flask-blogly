"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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