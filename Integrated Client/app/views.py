from app import app
from flask import render_template, request, flash, redirect, url_for
import requests
from urllib import parse

# Home page of the app. This is the page that the 
# user will see when they first visit the app
# The page prompts the user for either the name of 
# a review author or the number of stars for a review
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# (USES SERVICE 1: REVIEW SERVICE)
# This is the page that the user will see when they submit the form
# It checks the parameters passed and invokes the appropriate
# api endpoint and displays the results
# The results are a list of reviews that match the search criteria
# Each result will have a link on the movie title that will take
# the user to the movie details page
@app.route('/searchReview', methods=['POST'])
def searchReviews():
    results = []
    stars = request.form.get('movieStars')
    author = request.form.get('movieAuthor')
    if not author and not stars:
        flash('Please enter a search term.')
        return redirect(url_for('index'))
    elif author and stars:
        flash('Please enter only 1 term.')
        return redirect(url_for('index'))
    
    results = []
    if stars:
        stars = int(stars)
    if author:
        response = requests.get("http://127.0.0.1:9998/api/review/0/0/%s/0/0"%author)
        results = response.json()
    else:
        response = requests.get("http://127.0.0.1:9998/api/review/0/0/0/0/%d"%stars)
        results = response.json()

    print(results)
    for result in results:
        title = parse.quote(result['Movie'])
        result['link'] = "/movie?title=" + title
    return render_template('reviews.html', results=results)

# (USES SERVICE 2: MOVIE SERVICE)
# This is the page that the user will see when they click on a movie title
# It checks the parameters passed and invokes the appropriate
# api endpoint and displays the results
# The results are the details of the movie that was clicked on
# Each movie will have a link on the movie title or the director
# that will invoke the /picture route and display the picture
@app.route('/movie', methods=['GET'])
def movie():
    title = request.args.get('title')
    response = requests.get("http://127.0.0.1:9997/api/movies/title/%s"%title)
    movies = response.json()
    for movie in movies:
        title = parse.quote(movie['title'])
        d = parse.quote(movie['director'])
        movie['poster'] = "/picture?search=" + title
        movie['dPic'] = "picture?search=" + d
    return render_template('movies.html', results=movies)

# (USES SERVICE 3: BING IMAGE SEARCH SERVICE)
# This is the page that the user will see when they click on
# a movie title or director name. It checks the parameters passed
# and invokes the thirdparty api to get the picture and redirects
# to the image URL to display the image
@app.route('/picture', methods=['GET'])
def picture():
    search = request.args.get('search')
    url = "https://bing-image-search1.p.rapidapi.com/images/search"
    querystring = {"q":search,"count":"1","safeSearch":"moderate"}
    headers = {
        "X-RapidAPI-Key": "360e258801msh0b4172e9e4039b5p1b052fjsn69567fcb2512",
        "X-RapidAPI-Host": "bing-image-search1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    link = data['value'][0]['contentUrl']
    return redirect(link)