import random
import flask
from flask import Flask, url_for
from werkzeug.utils import redirect

#-------------------Завдання №2----------------------------
app = Flask(__name__)

movies = [
    {"id": 1, "title": "Harry Potter and the Chamber of Secrets", "Produced by": "David Heyman", "genre": "Fantasy"},
    {"id": 2, "title": "Spider-Man: No Way Home", "Produced by": "Kevin Feige and Amy Pascal", "genre": "Superhero"},
    {"id": 3, "title": "Karate Kid", "Produced by": "Jerry Weintraub, Will Smith, Jada Pinkett Smith, James Lassiter, Ken Stovitz", "genre": "Action"}
]

@app.route('/')
def home():
    return f"""Top 3 movies
            {movies[0]},
            {movies[1]},
            {movies[2]}"""

@app.route('/movie/<int:movie_id>/')
def movie_detail(movie_id):
    movie = next((movie for movie in movies if movie["id"] == movie_id), None)
    if movie:
        return f"Name: {movie['title']}, Produced by: {movie['Produced by']}, genre: {movie['genre']}"
    else:
        return "The movie was not found", 404

@app.route('/random')
def random_m():
    a = random.randint(0, len(movies))
    return redirect(url_for("movie_detail", movie_id=a))

if __name__ == '__main__':
    app.run(debug=True)