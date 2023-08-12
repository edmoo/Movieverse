Running review_server.py:
1.Run the following commands:
"module add anaconda3"
"python3 -m venv review_server"
"source review_server/bin/activate"
"python3 -m pip install flask flask_mysqldb flask_restful"
"python3 review_server.py"
2.Once quit, deactivate the environment with "deactivate"

Route:
http://127.0.0.1:9998/api/review/<int:rev_id>/<string:rev_movie>/<string:rev_author>/<string:rev_review>/<int:rev_stars>
	-GET: Leave all values as 0 to get all
		To search for specific value, replace any variable in URL with value and the first none 0 in the URL will be searched for
	-PUT: Populate every value to publish a new review (id is ignored, can leave as 0)
	-POST: Populate every value to replace a review with the same id
	-DELETE: Leave all values as 0 to delete all
		   To delete a specific review, replace rev_id with id to be deleted
	
0 is counted as an empty value
"python3 -m venv review_server" is optional



Running review_client.py:
1.Start review_server.py
2.Run the following in terminal:
"module add anaconda3"
"python3 -m venv review_client"
"source review_client/bin/activate"
"python3 -m pip install requests"
"python3 review_client.py"
3. Use program as instructed
4.Once done, quit the program through the menu and deactivate using "deactivate" in terminal

The service URL is http://127.0.0.1:9998/api/review/<int:rev_id>/<string:rev_movie>/<string:rev_author>/<string:rev_review>/<int:rev_stars>
Client must be on same machine as the server
"python3 -m venv review_client" is optional