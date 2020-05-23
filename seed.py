"""Seed file to make sample data for users db."""

from models import connect_db, db, User,Post,Tag,PostTag
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add Users
chuck= User(first_name='Chuck', last_name="Bruce", image= 'https://images.unsplash.com/photo-1515014031351-b162f196ba28?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60')
bowser = User(first_name='Bowser', last_name="Pitt", image= 'https://images.unsplash.com/photo-1589677981327-e614e1adf5f2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60')
spike = User(first_name='Spike', last_name="Solomon")

# Add new objects to session, so they'll persist
db.session.add(chuck)
db.session.add(bowser)
db.session.add(spike)

# Commit--otherwise, this never gets saved!
db.session.commit()

#Add posts
post1 = Post(title = "First post", content = "Hi, I am happy to be here.", user_id = chuck.id)
post2 = Post(title = "Second post", content = "Hi, it is me again.", user_id = chuck.id)
post3 = Post(title = "No content post test", user_id = bowser.id)
post4 = Post(title = "Spike needs a post", content = "idk, I just feel like I need to have something.", user_id = spike.id)

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(post4)

db.session.commit()

post1.tags.append(Tag(name="happy", description="I am really happy."))
post1.tags.append(Tag(name="rookie", description="I am new."))
post2.tags.append(Tag(name="cool"))

db.session.add(post1)
db.session.add(post2)
db.session.commit()