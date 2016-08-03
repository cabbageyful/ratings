"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user
# may not need UserMixin

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

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
    password = request.form.get("password") 
    print username
    email_list_of_users = User.query.filter_by(email=username).first()
    print email_list_of_users.email

    if username != email_list_of_users.email:
        print "True"
        new_user = User(email=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    
    else:
        print "WHOOPS******************"
        flash('Your email address is already in use.')
        return redirect('/register')

    # query db for username attr
    # if not in db, add to db

    # if in db, redirect to /login 
@app.route('/login')
def login_screen():
    """Go to login page."""

    return render_template("/login.html")


@app.route("/login", methods=["POST"])
def login():
    
    username = request.form.get('username')
    password = request.form.get('password')        

    # query db for username
    user = User.query.filter_by(email=username).first()
    print user.password
    # if username is not db, redirect w/ flashed message
    if password == user.password:
        return redirect('/homepage.html')
    # if username in db,
        # check if pw == user.password
            # if yes, then go to home page w/ flashed message, logged in
            # if not redirect to login page that password incorrect
    # if password == username + "_secret":
    #     id = username.split('user')[1]
    #     user = User(id)
    #     login_user(user)
    #     return redirect(request.args.get("next"))
    # else:
    #     return abort(401)
    else:
        pass
        # return something   


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
