from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_mysqldb import MySQL
from functools import wraps

app = Flask(__name__)
api = Api(app)

# Database configuration
app.config['MYSQL_HOST'] = 'comp3211-mariadb.mariadb.database.azure.com'
app.config['MYSQL_USER'] = 'sc20cah'
app.config['MYSQL_PASSWORD'] = 'c8#ae89R'
app.config['MYSQL_DB'] = 'sc20cah'
mysql = MySQL(app)

# Runs at the start of each request
# Checks if the database table exists/ can connect to database
# If not, creates the table or returns error if unable to connect
def check_db(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            cur = mysql.connection.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS movies (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), year VARCHAR(255), genre VARCHAR(255), director VARCHAR(255))")
            mysql.connection.commit()
            cur.close()
            return f(*args, **kwargs)
        except Exception as e:
            return {'error': str(e)}, 500

    return wrapper

# Get a specific movie or delete it from the database
# movie specified by unique id
class Movie(Resource):
    @check_db
    def get(self, movie_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM movies WHERE `id` = %d" %movie_id)
        movie = cursor.fetchone()
        cursor.close()
        # If movie exists, return it else return error
        if movie is None:
            return {'message': 'Movie not found'}, 404
        content = {'id': movie[0], 'title': movie[1], 'year': movie[2], 'genre': movie[3], 'director': movie[4]}
        return content, 200

    @check_db
    def delete(self, movie_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM movies WHERE id = %d" %movie_id)
        movie = cursor.fetchone()
        # If movie exists, delete it else return error
        if movie is None:
            return {'message': 'Movie not found'}, 404
        cursor.execute("DELETE FROM movies WHERE id = %d" %movie_id)
        mysql.connection.commit()
        cursor.close()
        return {'message': 'Movie deleted'}, 200

# Put the movie data into the database
# or update existing movie data
class MoviePutPost(Resource):
    @check_db
    def put(self, movie_id, title, year, genre, director):
        # if input data is empty, return error
        if title is None or year is None or genre is None or director is None:
            return {'message': 'Missing arguments'}, 400
        cursor = mysql.connection.cursor()
        # add to database
        cursor.execute("INSERT INTO movies (title, year, genre, director) VALUES ('%s', %d, '%s', '%s')" %(title, year, genre, director))
        movie_id = mysql.connection.insert_id()
        mysql.connection.commit()
        cursor.close()
        return {'message': 'Movie added', 'id': movie_id}, 201

    @check_db
    def post(self, movie_id, title, year, genre, director):
        # if input data is empty, return error
        if title is None or year is None or genre is None or director is None:
            return {'message': 'Missing arguments'}, 400
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM movies WHERE `id` = %d" %movie_id)
        movie = cursor.fetchone()
        # if movie does not exist, return error
        if movie is None:
            return {'message': 'Movie not found'}, 404
        cursor.execute("UPDATE movies SET title = '%s', year = %d, genre = '%s', director = '%s' WHERE `id` = %d" %(title, year, genre, director, movie_id))
        mysql.connection.commit()
        cursor.close()
        return {'message': 'Movie updated', 'id': movie_id}, 200

# Gets all movies or deletes all movies
class MoviesAll(Resource):
    @check_db
    def get(self):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM movies")
        movies = cursor.fetchall()
        json_data = []
        # Convert to JSON
        for movie in movies:
            content = {'id': movie[0], 'title': movie[1], 'year': movie[2], 'genre': movie[3], 'director': movie[4]}
            json_data.append(content)
        return json_data, 200

    @check_db
    def delete(self):
        # Deletes all and resets ID auto increment to 1
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM movies")
        cursor.execute("ALTER TABLE movies AUTO_INCREMENT = 1")
        mysql.connection.commit()
        cursor.close()
        return {'message': 'All movies deleted'}, 200

# Searches the database by value in specified column/field
class MovieSearch(Resource):
    @check_db
    def get(self, field, value):
        #if invalid field
        if field not in ['title', 'year', 'genre', 'director']:
            return {'message': 'Invalid search field'}, 400
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM movies WHERE `%s` = '%s'" % (field, value))
        movies = cursor.fetchall()
        # if no movies found
        if movies is None:
            return {'message': 'Movie not found'}, 404
        json_data = []
        # if movies found loop through each and reformat into json
        for movie in movies:
            content = {'id': movie[0], 'title': movie[1], 'year': movie[2], 'genre': movie[3], 'director': movie[4]}
            json_data.append(content)
        return json_data, 200

# Binds each class to a URL format
api.add_resource(MovieSearch, '/api/movies/<string:field>/<string:value>')
api.add_resource(MoviesAll, '/api/movies')
api.add_resource(Movie, '/api/movie/<int:movie_id>')
api.add_resource(MoviePutPost, '/api/movie/<int:movie_id>/<string:title>/<int:year>/<string:genre>/<string:director>')

# Runs the app on port 9997
if __name__ == '__main__':
    app.run(port=9997, debug=True)