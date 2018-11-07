from flask import Flask, request, redirect, render_template
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True # Displays runtime errors in the browser, too.

# A list of movies that nobody should have to watch.
terrible_movies = [
    "Gigli",
    "Star Wars Episode 1: Attack of the Clones",
    "Paul Blart: Mall Cop 2",
    "Nine Lives",
    "Mission to Mars"
]

def get_current_watchlist():
    # Returns user's current watchlist -- hard coded for now.
    return ["She-Devil", "Heathers", "Heartbreakers", "Death Becomes Her", "Jackie Brown"]
    # return []

@app.route("/crossoff", methods=['POST'])
def crossoff_movie():
    crossed_off_movie = request.form['crossed-off-movie']

    if crossed_off_movie not in get_current_watchlist():
        # The user tried to cross off a movie that isn't in their list,
        # so we redirect back to the front page and tell them what went wrong.
        error = "'{0}' is not in your watchlist, so you can't cross it off!".format(crossed_off_movie)

        # Redirect to homepage, and include error as a query parameter in the URL.
        return redirect("/?error=" + error)

    # If we didn't redirect by now, then all is well.
    return render_template('crossoff.html', crossed_off_movie = crossed_off_movie)

@app.route("/add", methods=['POST'])
def add_movie():
    # Look inside the request to figure out what the user typed.
    new_movie = request.form['new-movie']

    # If the user typed nothing at all, redirect and tell them the error.
    if (not new_movie) or (new_movie.strip() == ""):
        error = "Please specify the movie you want to add."
        return redirect("/?error=" + error)

    # If the user wants to add a terrible movie, redirect and tell them the error.
    if new_movie in terrible_movies:
        error = "Trust me, you don't want to add '{0}' to your watchlist.".format(new_movie)
        return redirect("/?error=" + error)

    # 'Escape' the user's input so that if they typed HTML, it doesn't mess up
    # our site.
    new_movie_escaped = cgi.escape(new_movie, quote = True)

    # TODO ---
    # Create a template called add-confirmation.html inside your templates directory
    # Use that template to render the confirmation message instead of this temparary message below.
    return render_template('add-confirmation.html', new_movie = new_movie)

# TODO ---
# Modify the edit.html file to display the watchlist in an unordered list with
# bullets in front of each movie.
# Put the list between "Flicklist" and "Edit My Watchlist" under this heading:
# <h2>My Watchlist</h2>

# TODO ---
# Change get_current_watchlist to return []. This simulates a user with an empty
# watchlist. Modify edit.html to make sense in such a situation:
#   -- First: Head the <h2>My Watchlist</h2> and it's unordered list.
#   -- Second: Hide the crossoff form, since there are no movies to cross off.
# Then you can change get_current_watchlist back to the list of hard-coded movies.

@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template("edit.html", watchlist = get_current_watchlist(), error = encoded_error and cgi.escape(encoded_error, quote = True))

if __name__ == "__main__":
    app.run()