from flask import Flask, request, redirect
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True # Displays runtime errors in the browser, too.

page_header = """
<!DOCTYPE html>
<html>
    <head>
        <title>Flicklist</title>
    </head>
    <body>
        <h1>Flicklist</h1>
"""

page_footer = """
    </body>
</html>
"""

# A form for adding new movies.
add_form = """
    <form action="/add" method="POST">
        <label>
            I want to add
            <input type="text" name="new-movie" />
            to my watchlist.
        </label>
        <input type="submit" value="Add It!" />
    </form>
"""

def get_current_watchlist():
    # Returns user's current watchlist -- hard coded for now.
    return ["She-Devil", "Heartbreakers", "Heathers", "Death Becomes Her", "Jackie Brown"]

# A form for crossing off watched movies
# (First we build a dropdown fro the current watchlist items)
crossoff_options = ""
for movie in get_current_watchlist():
    crossoff_options += '<option value="{0}">{0}</option>'.format(movie)

crossoff_form = """
    <form action="/crossoff" method="POST">
        <label>
            I want to cross off
            <select name="crossed-off-movie" />
                {0}
            </select>
            from my watchlist.
        </label>
        <input type="submit" value="Cross It Off!" />
    </form>
""".format(crossoff_options)

# A list of movies that nobody should have to watch.
terrible_movies = [
    "Gigli",
    "Star Wars Episode 1: Attck of the Clones",
    "Paul Blart: Mall Cop 2",
    "Nine Lives",
    "Mission to Mars"
]

@app.route("/crossoff", methods=['POST'])
def crossoff_movie():
    crossed_off_movie = request.form['crossed-off-movie']

    if crossed_off_movie not in get_current_watchlist():
        # The user tried to cross off a movie that isn't in their list,
        # so we redirect back to the front page and tell them what went wrong.
        error = "'{0}' is not in your watchlist, so you can't cross it off!".format(crossed_off_movie)

        # Redirect to homepage, and include error as a query parameter in the URL
        return redirect("/?error=" + error)

    # If we didn't redirect by now, then all is well.
    crossed_off_movie_element = "<strike>" + crossed_off_movie + "</strike>"
    confirmation = crossed_off_movie_element + " has been crossed off your watchlist."
    content = page_header + "<p>" + confirmation + "</p>" + page_footer

    return content

@app.route("/add", methods=['POST'])
def add_movie():
    # TODO ---
    # 'Escape' the user's input so that if they typed HTML, it doesn't mess up
    # our site.
    new_movie = request.form['new-movie']
    new_movie_esc = cgi.escape(new_movie)

    # TODO ---
    # If the user type nothing at all, redirect and tell them the error.
    if new_movie == "":
        error = "Please enter a movie title!"
        return redirect("/?error=" + error)

    # TODO ---
    # If the user wants to add a terrible movie, redirect and tell them not to
    # add it because it sucks.

    if new_movie in terrible_movies:
        error = "Trust me, you do not want to add {0} to your watchlist.".format(new_movie)
        return redirect("/?error=" + error)

    # Build response content
    new_movie_element = "<strong>" + new_movie_esc + "</strong>"
    sentence = new_movie_element + " has been added to your watchlist."
    content = page_header + "<p>" + sentence + "</p>" + page_footer

    return content

@app.route("/")
def index():
    edit_header = "<h2>Edit My Watchlist</h2>"

    # If we have an error, make a <p> to display it.
    error = request.args.get("error")
    if error:
        error_esc = cgi.escape(error, quote=True)
        error_element = '<p class="error">' + error_esc + '</p>'
    else:
        error_element = ''

    # Combine all the pieces to build the content of our response.
    main_content = edit_header + add_form + crossoff_form + error_element

    # Build the response string.
    content = page_header + main_content + page_footer

    return content

if __name__ == "__main__":
    app.run()