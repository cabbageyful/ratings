"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/register', methods=['GET'])
def new_user_form():
    """Go to register as a new user."""

    return render_template("register.html")

@app.route('/register', methods=['POST'])
def add_new_user():
    """Create new unique user."""

    # get value from register.html form for username
    username = request.form.get("username")
    password = request.form.get("password")  # need to fix 
    print username, password
    email_list_of_users = User.query.filter_by(email=username).all()
    print email_list_of_users
    # if username not in email_list_of_users:

    # query db for username attr
    # if not in db, add to db

    # if in db, redirect to /login 



@app.route('/users')
def user_list():
    """Show list of users."""

    users=User.query.all()
    return render_template("user_list.html",users=users)




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
