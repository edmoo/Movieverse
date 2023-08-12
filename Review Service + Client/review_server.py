from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_mysqldb import MySQL
from functools import wraps

app = Flask(__name__)
api = Api(app)

app.config['MYSQL_HOST'] = 'comp3211-mariadb.mariadb.database.azure.com'
app.config['MYSQL_USER'] = 'sc20em'
app.config['MYSQL_PASSWORD'] = 'sc20emsc20em'
app.config['MYSQL_DB'] = 'sc20em'
mysql = MySQL(app)

#Checks if database exists and creates it if not
def createDb(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            cur = mysql.connection.cursor()
            #Id increments by 1 each time a new review is added
            cur.execute("CREATE TABLE IF NOT EXISTS reviews (id INT AUTO_INCREMENT PRIMARY KEY, movie VARCHAR(255), author VARCHAR(255), review VARCHAR(255), stars VARCHAR(255))")
            mysql.connection.commit()
            cur.close()
            return f(*args, **kwargs)
        except Exception as e:
            return {'Error': str(e)}, 500

    return wrapper

#Contains all get,post,put and delete methods
class Review(Resource):
    @createDb
    #Searches database for a review and returns said review(s)
    def get(self, rev_id, rev_movie, rev_author, rev_review, rev_stars):
        #if all values are left as 0 it returns all reviews
        if 0==rev_id==rev_stars and '0'==rev_movie==rev_author==rev_review:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM reviews")
            reviews = cursor.fetchall()
            data = []
            for review in reviews:
                content = {'id': review[0], 'Movie': review[1], 'Author': review[2], 'Review': review[3], 'Stars': review[4]}
                data.append(content)
            return data, 200

        #If any value isnt 0, it goes through each value one by one and searches for reviews based on the first filled in value e.g. movie
        elif rev_movie != '0':
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM reviews WHERE movie = '%s'"%rev_movie)
            reviews = cursor.fetchall()
            data = []
            for review in reviews:
                content = {'id': review[0], 'Movie': review[1], 'Author': review[2], 'Review': review[3], 'Stars': review[4]}
                data.append(content)
            return data, 200    
        
        elif rev_author != '0':
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM reviews WHERE author = '%s'"%rev_author)
            reviews = cursor.fetchall()
            data = []
            for review in reviews:
                content = {'id': review[0], 'Movie': review[1], 'Author': review[2], 'Review': review[3], 'Stars': review[4]}
                data.append(content)
            return data, 200  

        elif rev_stars != 0:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM reviews WHERE stars = %d"%rev_stars)
            reviews = cursor.fetchall()
            data = []
            for review in reviews:
                content = {'id': review[0], 'Movie': review[1], 'Author': review[2], 'Review': review[3], 'Stars': review[4]}
                data.append(content)
            return data, 200  

        #Checks id last
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM reviews WHERE id = %d"%rev_id)
        rev = cur.fetchone()
        cur.close()
        if rev is None:
            return {'message' : 'Error 404, review not found'}, 404
        rev_format = {'id': rev[0], 'movie' : rev[1], 'author' : rev[2], 'review' : rev[3], 'stars' : rev[4]}
        return rev_format, 200
    
    @createDb
    #Commit a new review to the database
    def put(self, rev_id, rev_movie, rev_author, rev_review, rev_stars):
        #Makes sure no values are none
        if None in (rev_id, rev_movie, rev_author, rev_review, rev_stars):
            return {'message':'Missing args'}, 404
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO reviews (movie, author, review, stars) VALUES ('%s','%s','%s','%d')"%(rev_movie, rev_author, rev_review, rev_stars))
        #Increments id
        rev_id = mysql.connection.insert_id()
        mysql.connection.commit()
        cur.close()
        return {'message': 'Review Posted','id':rev_id},200

    @createDb
    #Edits a review
    def post(self, rev_id, rev_movie, rev_author, rev_review, rev_stars):
        if None in (rev_id, rev_movie, rev_author, rev_review, rev_stars):
            return {'message':'Missing args'}, 400
        cur = mysql.connection.cursor()
        #Review changed is based on id given
        cur.execute("SELECT * FROM reviews WHERE id = %d"%rev_id)
        revRep = cur.fetchone()
        if revRep is None:
            return {'message':'Review not found'}, 404
        cur.execute("UPDATE reviews SET movie = '%s', author = '%s', review = '%s', stars = '%d' WHERE id = %d" %(rev_movie, rev_author, rev_review, rev_stars, rev_id))
        mysql.connection.commit()
        cur.close()
        return 200

    @createDb
    #Deletes a review(s)
    def delete(self, rev_id, rev_movie, rev_author, rev_review, rev_stars):
        #If everything is left as 0 it deletes all reviews
        if(0==rev_id==rev_stars and '0'==rev_movie==rev_author==rev_review):
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM reviews")
            rev = cur.fetchall()
            if rev is None:
                return {'message' : 'There are no reviews'}, 404
            cur.execute("DELETE FROM reviews")
            cur.execute("ALTER TABLE reviews AUTO_INCREMENT = 1")
            mysql.connection.commit()
            print("commit")
            cur.close()
            return {'message': 'All Reviews Deleted'}, 200
        #Otherwise searches for review based on id given and deletes it
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM reviews WHERE id = %d"%rev_id)
        rev = cur.fetchone()
        if rev is None:
            return {'message' : 'Error 404, review not found'}, 404
        cur.execute("DELETE FROM reviews WHERE id = %d" %rev_id)
        mysql.connection.commit()
        cur.close()
        return {'message': 'Review deleted'}, 200


#Only one url, ignores variables that arent required in given method
api.add_resource(Review, '/api/review/<int:rev_id>/<string:rev_movie>/<string:rev_author>/<string:rev_review>/<int:rev_stars>')

if __name__ == '__main__':
    app.run(port=9998, debug=True)