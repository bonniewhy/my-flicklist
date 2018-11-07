from flask import Flask, request

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

# A form for adding new movies
add_form = """
    <form action="/add" method="POST">
        <label for="new-movie">
            I want to add
            <input type="text" id="new-movie" name="new-movie" />
            to my watchlist.
        </label>
        <input type="submit" value="Add It!" />
    </form>
"""

# TODO ---
# Create the HTML for the form below so the user can check off a movie from
# their watchlist when they've watched it.
# Name the action for the form "/crossoff" and make it's method "POST".

# A form for crossing off watched movies.
crossoff_form = """
    <form action="/crossoff" method="POST">
        <label for="crossed-off-movie">
            I want to cross off
            <select name="crossed-off-movie" id="crossed-off-movie">
                <option value="Heathers">Heathers</option>
                <option value="Death Becomes Her">Death Becomes Her</option>
                <option value="Heartbreakers">Heartbreakers</option>
                <option value="Jackie Brown">Jackie Brown</option>
                <option value="She-Devil">She-Devil</option>
            </select>
            from my watchlist.
        </label>
        <input type="submit" value="Cross It Off!" />
    </form>
"""

# TODO ---
# Finish filling in the function below so that the user will see a message like
# "Star Wars has been crossed off your watchlist".
# And create a route above the function definition to recieve and handle the
# request from your crossoff_form.

@app.route("/crossoff", methods=['POST'])
def crossoff_movie():
    crossed_off_movie = request.form['crossed-off-movie']

    crossed_off_movie_element = "<strike>" + crossed_off_movie + "</strike>"
    sentence = crossed_off_movie_element + " has been crossed off your watchlist."
    content = page_header + "<p>" + sentence + "</p>" + page_footer

    return content

# TODO ---
# Modify the crossoff_form above to use a dropdown (<select>) instead of an
# input text field (<input type="text" />)

@app.route("/add", methods=['POST'])
def add_movie():
    new_movie = request.form['new-movie']

    # Build response content
    new_movie_element = "<strong>" + new_movie + "</strong>"
    sentence = new_movie_element + " has been added to your watchlist!"
    content = page_header + "<p>" + sentence + "</p>" + page_footer

    return content

@app.route("/")
def index():
    edit_header = "<h2>Edit My Watchlist</h2>"

    # Build the response string.
    content = page_header + edit_header + add_form + crossoff_form + page_footer

    return content

if __name__ == "__main__":
    app.run()