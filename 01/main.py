from flask import Flask
import random

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    # Choose a movie by invoking our new function
    todays_movie = get_random_movie()
    tomorrows_movie = get_random_movie()

    # Build the response string
    content = "<h1>Movie of the Day</h1>"
    content += "<ul>"
    content += "<li>" + todays_movie + "</li>"
    content += "</ul>"

    # TODO -- Pick another random movie, and display it under
    # the heading "<h1>Tomorrow's Movie</h1>"

    if todays_movie == tomorrows_movie:
        tomorrows_movie = get_random_movie()
    
    if todays_movie != tomorrows_movie:
        content += "<h1>Tomorrow's Movie</h1>"
        content += "<ul>"
        content += "<li>" + tomorrows_movie + "</li>"
        content += "</ul>"

    return content

def get_random_movie():
    # TODO -- Make a list with at least 5 movie titles.
    movies = ["Heartbreakers", "Death Becomes Her", "Heathers", "Jackie Brown", "She-Devil"]
    # TODO -- Randomly choose one of the movies, and return it.
    random_movie = random.choice(movies)

    return random_movie

if __name__ == "__main__":
    app.run()