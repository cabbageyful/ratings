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
    current_user = User.query.filter_by(email=username).first()
    
    if current_user is None:    # email address is already in database
        print "True"
        new_user = User(email=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/login')   
    
    else:                      # email entered was found in database
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
    print user.user_id
    # if username is not db, redirect w/ flashed message
    if password == user.password:
        flash('You are logged in.')
        session['user'] = username
        return render_template("ind_user.html", user=user)  # redirect to their user page instead

    else:
        flash('Login Information is Wrong')
        return redirect('/login')
  

@app.route('/', methods=["POST"])
def logout():

    #if logout key pressed
    del session['user']
    flash("You are now logged out")
    return redirect('/')


@app.route('/users')
def user_list():
    """Show list of users."""

    users=User.query.all()
    return render_template("user_list.html",users=users)


@app.route('/users/<int:user_id>')
def get_indivdual_user(user_id):
    """See info page for an individual user."""

    user = User.query.filter_by(user_id=user_id).first()

    return render_template("ind_user.html", user=user)

@app.route('/movies')
def movie_list():
    """Show list of movies."""

    movies = Movie.query.order_by(Movie.title).all()

    return render_template("movies.html", movies=movies)

@app.route('/movies/<int:movie_id>')
def get_movie(movie_id):
    """See info page for an individual user."""

    movie = Movie.query.filter_by(movie_id=movie_id).first()

    movie_year = movie.released_at.strftime("%B %d, %Y")

    return render_template("ind_movie.html", movie=movie, movie_year=movie_year)


@app.route('/movies/<int:movie_id>', methods=["POST"])
def new_rating():
    """allow user to input rating for movie when LOGGED IN"""

    new_score = request.form.get("add-rating")
    print new_score
    if session['user']:
        # rating = rating = Rating(user_id=user_id, 
                      # movie_id=movie_id,
                      # score=score)add info to ratings table - user id, value from dropdown, & movie id
        # db.session.add(rating)
        # db.session.commit()
        flash('Thanks for your rating! It\'s really important to us.')
        return redirect('/movies')  # redirect to their user page instead

    else:
        flash("You are not logged in. Please log in or register to rate movie")
        return redirect('/login')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
