To run movie_server.py:
1. Make sure you are on uni machine or using feng-linux
2. do "module add anaconda3"
3. do "python3 -m venv mov_server"
4. do "source mov_server/bin/activate"
5. do "python3 -m pip install flask flask_mysqldb flask_restful"
6. do "python3 movie_server.py"
7. Quit the server by doing Ctrl+C
8. To deactivate environment do "deactivate"

API Routes: (ALL RETURN JSON)
BASE_URL: 127.0.0.1:9997
1. /api/movies
	- GET: lists all movies
	- DELETE: deletes all movies and resets id incrementing to 1 
2. /api/movie/<int:movie_id>
	- GET: returns movie data
	- DELETE: removes movie from db
3. /api/movies/<string:field>/<string:value>
	- GET: queries database 
		i.e. /api/movies/genre/Action returns all Action movies
		or /api/movies/title/Avatar returns all movies with title Avatar
4. /api/movie/<int:movie_id>/<string:title>/<int:year>/<string:genre>/<string:director>
	- PUT: puts movie entry into database (id field is ignored), returns movie id
	- POST: updates the fields for movie specified with id

NOTES:
- The service makes use of the database setup in class which can only
  be accessed with a University IP (hence Step 1)
- The service uses port 9997 so make sure that port is free on your machine
- Creating a virtual environment in step 3 is optional but recommended
