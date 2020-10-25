from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv('PROJECT_API_KEY')

app = Flask(__name__)

@app.route('/')
def index():
    movie_name = request.args.get('search-box')
    if not movie_name:
        return render_template("/index.html")
    resp = requests.get(f'http://www.omdbapi.com/?i=tt3896198&apikey={API_KEY}&s={movie_name}&type=movie')
    resp_json = resp.json()
    if resp_json.get('Search') is None:
        return render_template("/index.html")
    results = resp_json['Search']
    ratings = {}
    for movie in results:
        imdb_id = movie['imdbID']
        movie_details = requests.get(f'http://www.omdbapi.com/?apikey={API_KEY}&i={imdb_id}').json()
        ratings[movie['Title']] = movie_details['imdbRating']
    return render_template(
        "/search.html",
        keywords=movie_name,
        results=results,
        ratings=ratings
    )

@app.route('/about.html')
def about():
    return render_template("/about.html")

if __name__ == '__main__':
    app.run(threaded=True, port=5000)