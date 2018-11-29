from flask import request, redirect, render_template, session, flash
import cgi
from app import app, db
from models import User, Movie
from hashutils import check_pw_hash

# A list of movie names that nobody should have to watch.
terrible_movies = [
    "Gigli",
    "Star Wars Episode 1: Attack of the Clones",
    "Paul Blart: Mall Cop 2",
    "Nine Lives",
    "Starship Troopers"
]

def get_current_watchlist(current_user_id):
    return Movie.query.filter_by(watched = False, owner_id = current_user_id).all()

def get_watched_movies(current_user_id):
    return Movie.query.filter_by(watched = True, owner_id = current_user_id).all()

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = User.query.filter_by(email = email)

        if users.count() == 1:
            user = users.first()
            if check_pw_hash(password, user.pw_hash):
                session['user'] = user.email
                flash('Welcome back, ' + user.email + '!')
                return redirect("/")

        flash('Bad username or password... sorry. Try again!')
        return redirect("/login")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        if not is_email(email):
            flash('Zoinks!! "' + email + '" does not seem to be an actual email address. D:')
            return redirect('/register')

        email_db_count = User.query.filter_by(email = email).count()
        if email_db_count > 0:
            flash("Yikes! "' + email + '" is already taken by someone else.")
            return redirect('/register')

        if password != verify:
            flash("Passwords aren't the same!")
            return redirect('/register')

        user = User(email = email, password = password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.email
        return redirect("/")

    else:
        return render_template('register.html')

def is_email(string):
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present

@app.route("/logout", methods = ['POST'])
def logout():
    del session['user']
    return redirect("/")

@app.route("/rating-confirmation", methods = ['POST'])
def rate_movie():
    movie_id = request.form['movie_id']
    rating = request.form['rating']

    movie = Movie.query.get(movie_id)
    if movie not in get_watched_movies(logged_in_user().id):
        error = "'{0}' is not in your watched movies list, so you can't rate it!".format(movie)
        return redirect("/?erorr=" + error)

    movie.rating = rating
    db.session.add(movie)
    db.session.commit()
    return render_template('rating-confirmation.html', movie = movie, rating = rating)

@app.route("/ratings", methods = ['GET'])
def movie_ratings():
    return render_template('ratings.html', movies = get_watched_movies(logged_in_user().id))

@app.route("/crossoff", methods = ['POST'])
def crossedoff_movie():
    crossed_off_movie_id = request.form['crossed-off-movie']

    crossed_off_movie = Movie.query.get(crossed_off_movie_id)
    if not crossed_off_movie:
        return redirect("/?error=Attempt to watch a movie unknown to this database.")

    crossed_off_movie.watched = True
    db.session.add(crossed_off_movie)
    db.session.commit()
    return render_template('crossoff.html', crossed_off_movie = crossed_off_movie)

@app.route("/add", methods = ['POST'])
def add_movie():
    new_movie_name = request.form['new-movie']

    if (not new_movie_name) or (new_movie_name.strip() == ""):
        error = "Please specify the movie you want to add."
        return redirect("/?error=" + error)

    if new_movie_name in terrible_movies:
        error = "Trust me, you don't want to add '{0}' to your watchlist.".format(new_movie_name)
        return redirect("/?erorr=" + error)

    movie = Movie(new_movie_name, logged_in_user())
    db.session.add(movie)
    db.session.commit()
    return render_template('add-confirmation.html', movie = movie)

@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template('edit.html', watchlist = get_current_watchlist(logged_in_user().id), error = encoded_error and cgi.escape(encoded_error, quote = True))

def logged_in_user():
    owner = User.query.filter_by(email = session['user']).first()
    return owner

endpoints_without_login = ['login', 'register']

@app.before_request
def require_login():
    if not ('user' in session or request.endpoint in endpoints_without_login):
        return redirect("/register")

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'

if __name__ == "__main__":
    app.run()
