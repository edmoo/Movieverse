import requests
import time

# gets all movies and prints them formatted onscreen
# also times the response from the server to use in 
# the report
def get_all():
    api_url = "http://127.0.0.1:9997/api/movies"
    start = time.time()
    response = requests.get(api_url)
    end = time.time()
    print("Response time: %fs" %(end-start))
    movies = response.json()
    print("\nID: TITLE | YEAR | GENRE | DIRECTOR")
    for movie in movies:
        print("%d: %s | %s | %s | %s"%(movie['id'], movie['title'], movie['year'], movie['genre'], movie['director']))
    quit_question()

# prompts the user for which field they want to search by
# then gets the search term and calls the appropriate 
# call from the server. It prints the returned 
# results formatted on screen
# Also times the response from the server to use in
# the report
def search_movie():
    istr = input("How would you like to search? [id/title/year/genre/director/b]: ")
    # goes back to the main menu
    if istr.strip().lower() == "b":
        print("")
        return
    # search by id has a different api endpoint
    elif istr.strip().lower() == "id":
        i = int(input("What is the id? [id]: "))
        api_url = "http://127.0.0.1:9997/api/movie/%d" %i
        start = time.time()
        response = requests.get(api_url)
        end = time.time()
        print("Response time: %fs" %(end-start))
        movie = response.json()
        if response.status_code == 404:
            print("Movie not found")
        else:
            print("%d: %s | %s | %s | %s"%(movie['id'], movie['title'], movie['year'], movie['genre'], movie['director']))
    # all other searches use the same api endpoint but with different parameters
    elif istr.strip().lower() == "title":
        title = input("What is the title? [title]: ")
        title = title.strip().replace(" ", "%20")
        api_url = "http://127.0.0.1:9997/api/movies/title/%s" %title
        start = time.time()
        response = requests.get(api_url)
        end = time.time()
        print("Response time: %fs" %(end-start))
        movies = response.json()
        if response.status_code == 404:
            print("Movie not found")
        else:
            print("\nID: TITLE | YEAR | GENRE | DIRECTOR")
            for movie in movies:
                print("%d: %s | %s | %s | %s"%(movie['id'], movie['title'], movie['year'], movie['genre'], movie['director']))
    elif istr.strip().lower() == "year":
        year = input("What is the year? [year]: ")
        year = int(year.strip())
        api_url = "http://127.0.0.1:9997/api/movies/year/%d" %year
        start = time.time()
        response = requests.get(api_url)
        end = time.time()
        print("Response time: %fs" %(end-start))
        movies = response.json()
        if response.status_code == 404:
            print("Movie not found")
        else:
            print("\nID: TITLE | YEAR | GENRE | DIRECTOR")
            for movie in movies:
                print("%d: %s | %s | %s | %s"%(movie['id'], movie['title'], movie['year'], movie['genre'], movie['director']))
    elif istr.strip().lower() == "genre":
        genre = input("What is the genre? [genre]: ")
        genre = genre.strip().replace(" ", "%20")
        api_url = "http://127.0.0.1:9997/api/movies/genre/%s" %genre
        start = time.time()
        response = requests.get(api_url)
        end = time.time()
        print("Response time: %fs" %(end-start))
        movies = response.json()
        if response.status_code == 404:
            print("Movie not found")
        else:
            print("\nID: TITLE | YEAR | GENRE | DIRECTOR")
            for movie in movies:
                print("%d: %s | %s | %s | %s"%(movie['id'], movie['title'], movie['year'], movie['genre'], movie['director']))
    elif istr.strip().lower() == "director":
        director = input("What is the director? [director]: ")
        director = director.strip().replace(" ", "%20")
        api_url = "http://127.0.0.1:9997/api/movies/director/%s" %director
        start = time.time()
        response = requests.get(api_url)
        end = time.time()
        print("Response time: %fs" %(end-start))
        movies = response.json()
        if response.status_code == 404:
            print("Movie not found")
        else:
            print("\nID: TITLE | YEAR | GENRE | DIRECTOR")
            for movie in movies:
                print("%d: %s | %s | %s | %s"%(movie['id'], movie['title'], movie['year'], movie['genre'], movie['director']))
    else:
        print("Invalid input")
        search_movie()
        return
    quit_question()

# promps the user to enter all movie details
# then sends a post request to the server to add
# the movie to the database
# Also times the response from the server to use in
# the report
def add_movie():
    title = input("Title: ")
    year = input("Year: ")
    genre = input("Genre: ")
    director = input("Director: ")
    title = title.strip().replace(" ", "%20")
    genre = genre.strip().replace(" ", "%20")
    director = director.strip().replace(" ", "%20")
    year = int(year.strip())
    api_url = "http://127.0.0.1:9997/api/movie/0/%s/%d/%s/%s" %(title, year, genre, director)
    start = time.time()
    response = requests.put(api_url)
    end = time.time()
    print("Response time: %fs" %(end-start))
    if response.status_code == 201:
        print("Movie added")
        movie_id = response.json()['id']
        api_url = "http://127.0.0.1:9997/api/movie/%d" %movie_id
        response = requests.get(api_url)
        movie = response.json()
        print("%d: %s | %s | %s | %s"%(movie['id'], movie['title'], movie['year'], movie['genre'], movie['director']))
    else:
        print("Something went wrong")
    quit_question()

# promps the user to enter the id of the movie they want to update
# then gets the updated details from the user
# then sends a post request to the server to update
# the movie in the database
# Also times the response from the server to use in
# the report
def update_movie():
    istr = input("What is the id of the movie? [id/b]: ")
    if istr.strip().lower() == "b":
        print("")
        return
    else:
        i = int(istr)
        api_url = "http://127.0.0.1:9997/api/movie/%d" %i
        response = requests.get(api_url)
        movie = response.json()
        if response.status_code == 404:
            print("Movie not found")
            update_movie()
            return
        else:
            print("%d: %s | %s | %s | %s"%(movie['id'], movie['title'], movie['year'], movie['genre'], movie['director']))
            i2 = input("Would you like to update this movie? [y/n]: ")
            if i2.strip().lower() == "n":
                update_movie()
                return
            elif i2.strip().lower() == "y":
                title = input("Updated Title: ")
                year = input("Updated Year: ")
                genre = input("Updated Genre: ")
                director = input("Updated Director: ")
                title = title.strip().replace(" ", "%20")
                genre = genre.strip().replace(" ", "%20")
                director = director.strip().replace(" ", "%20")
                year = int(year.strip())
                api_url = "http://127.0.0.1:9997/api/movie/%d/%s/%d/%s/%s" %(i, title, year, genre, director)
                start = time.time()
                response = requests.post(api_url)
                end = time.time()
                print("Response time: %fs" %(end-start))
                if response.status_code == 200:
                    print("Movie updated")
                else:
                    print("Something went wrong")
            else:
                print("Invalid input")
                update_movie()
                return
    quit_question()

# promps the user to enter the id of the movie they want to delete
# then sends a delete request to the server to delete
# the movie from the database
# Also times the response from the server to use in
# the report
def delete_movie():
    istr = input("What is the id of the movie? [id/b]: ")
    if istr.strip().lower() == "b":
        print("")
        return
    else:
        i = int(istr)
        api_url = "http://127.0.0.1:9997/api/movie/%d" %i
        response = requests.get(api_url)
        movie = response.json()
        if response.status_code == 404:
            print("Movie not found")
            delete_movie()
            return
        else:
            print("%d: %s | %s | %s | %s"%(movie['id'], movie['title'], movie['year'], movie['genre'], movie['director']))
            confirm = input("Are you sure you want to delete this movie? [y/n]: ")
            if confirm.strip().lower() == "y":
                start = time.time()
                response = requests.delete(api_url)
                end = time.time()
                print("Response time: %fs" %(end-start))
                if response.status_code == 200:
                    print("Movie deleted")
                else:
                    print("Something went wrong")
            else:
                if confirm.strip().lower() != "n":
                    print("Invalid Input!")
                delete_movie()
                return

    quit_question()

# double checks the user wants to perform the action
# then calls the appropriate endpoint
# Also times the response from the server to use in
# the report
def delete_all():
    confirm = input("Are you sure you want to delete all movies? [y/n]: ")
    if confirm.strip().lower() == "y":
        api_url = "http://127.0.0.1:9997/api/movies"
        start = time.time()
        response = requests.delete(api_url)
        end = time.time()
        print("Response time: %fs" %(end-start))
        if response.status_code == 200:
            print("All movies deleted")
        else:
            print("Something went wrong")
    elif confirm.strip().lower() != "n":
        print("Invalid Input!")
        delete_all()
        return
    quit_question()

# Runs at the end of each selection
# Asks user if they want to quit or continue 
def quit_question():
    i2 = input("\nWould you like to exit? [y/n]: ")
    print("")
    if i2.strip().lower() == "y":
        exit()
    elif i2.strip().lower() != "n":
        print("Invalid input")
        quit_question()

# Main body of the program (Main Menu)
print("Welcome to the movie database!\n")
while True:
    # gives the user a list of options
    print("What would you like to do?")
    print("1. List all movies")
    print("2. Search for a movie")
    print("3. Add a movie")
    print("4. Update a movie")
    print("5. Delete a movie")
    print("6. Delete all movies")
    print("7. Quit\n")
    # gets the user's selection
    istr = input("Please select from the list above: ")
    i = int(istr)
    # calls the appropriate function based on the user's selection
    try:
        if i == 1:
            get_all()
        elif i == 2:
            search_movie()
        elif i == 3:
            add_movie()
        elif i == 4:
            update_movie()
        elif i == 5:
            delete_movie()
        elif i == 6:
            delete_all()
        elif i == 7:
            exit()
        else:
            print("Unrecognised option! Please try again.\n")
    # catches any connection errors and quits the program
    # as the server is not running therefore no need to continue
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print("Connection error! Quitting.\n")
        exit()