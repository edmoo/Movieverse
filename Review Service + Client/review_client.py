import time
import requests

#Gets all reviews
def printAll():
    #Time before request
    start = time.time()
    response = requests.get("http://127.0.0.1:9998/api/review/0/0/0/0/0")
    #Time after request
    end = time.time()
    #Calculates resonse time and prints it
    overall = end-start
    print("Time elapsed: %f seconds"%overall)
    reviews = response.json()
    print("\n[id] - [Movie] - [Author] - [Review] - [Stars]")
    for review in reviews:
        print("%d | %s | %s | %s | %s"%(review['id'], review['Movie'], review['Author'], review['Review'], review['Stars']))

#Gets reviews for specific movie
def movieSearch(mov):
    start = time.time()
    response = requests.get("http://127.0.0.1:9998/api/review/0/%s/0/0/0"%mov)
    end = time.time()
    overall = end-start
    print("Time elapsed: %f seconds"%overall)
    reviews = response.json()
    print("\n[id] - [Movie] - [Author] - [Review] - [Stars]")
    for review in reviews:
        print("%d - %s - %s - %s - %s"%(review['id'], review['Movie'], review['Author'], review['Review'], review['Stars']))

#Gets reviews for specific author
def authorSearch(inp):
    start = time.time()
    response = requests.get("http://127.0.0.1:9998/api/review/0/0/%s/0/0"%inp)
    end = time.time()
    overall = end-start
    print("Time elapsed: %f seconds"%overall)
    reviews = response.json()
    print("\n[id] - [Movie] - [Author] - [Review] - [Stars]")
    for review in reviews:
        print("%d - %s - %s - %s - %s"%(review['id'], review['Movie'], review['Author'], review['Review'], review['Stars']))

#Gets reviews that give a movie a specific star rating
def starSearch(inp):
    try:
        inp = int(inp)
        if(inp<1 or inp>5):
            print("Stars must be between 1 and 5")
            return
    except ValueError:
        print("Not an integer")
        return
    start = time.time()
    response = requests.get("http://127.0.0.1:9998/api/review/0/0/0/0/%d"%inp)
    end = time.time()
    overall = end-start
    print("Time elapsed: %f seconds"%overall)
    reviews = response.json()
    print("\n[id] - [Movie] - [Author] - [Review] - [Stars]")
    for review in reviews:
        print("%d - %s - %s - %s - %s"%(review['id'], review['Movie'], review['Author'], review['Review'], review['Stars']))

#Commits a new review to the database (PUT NOT POST)
def postReview(mov, auth, rev, stars):
    try:
        stars = int(stars)
        if(stars<1 or stars>5):
            print("Stars must be between 1 and 5")
            return
    except ValueError:
        print("Stars not an integer")
        return
    start = time.time()
    response = requests.put("http://127.0.0.1:9998/api/review/0/%s/%s/%s/%d"%(mov,auth,rev,stars))
    end = time.time()
    overall = end-start
    print("Time elapsed: %f seconds"%overall)
    resp = response.json()
    print(resp)

#Deletes a review with given id
def deleteReview(id):
    try:
        id = int(id)
    except ValueError:
        print("Id must be an integer")
        return
    if id == 0:
        print("Id must be greater than 0")
        return
    start = time.time()
    response = requests.delete("http://127.0.0.1:9998/api/review/%d/0/0/0/0"%id)
    end = time.time()
    overall = end-start
    print("Time elapsed: %f seconds"%overall)    
    print(response)

#Deletes all reviews in database
def deleteAll():
    start = time.time()
    response = requests.delete("http://127.0.0.1:9998/api/review/0/0/0/0/0")
    end = time.time()
    overall = end-start
    print("Time elapsed: %f seconds"%overall)    
    print(response)

#Edits review with given id
def editReview(inp, mov, auth, rev, stars):
    if '0'==mov==auth==rev:
        print("Values cannot equal 0")
        return
    try:
        inp = int(inp)
        stars = int(stars)
        if(stars>5 or stars<1):
            print("Stars must be between 1 and 5")
            return
        if(inp==0):
            print("Id cannot be 0")
            return
    except ValueError:
        print("Id and Stars must be an integer")
        return
    start = time.time()
    response = requests.post("http://127.0.0.1:9998/api/review/%d/%s/%s/%s/%d"%(inp,mov,auth,rev,stars))
    end = time.time()
    overall = end-start
    print("Time elapsed: %f seconds"%overall)    
    print(response)
    

print("Entering the review zone...\n")
loop = True
#Loops until user selects 9
while loop:
    #Text based interface
    print("\n1 - View All Reviews")
    print("2 - Search for Review")
    print("3 - Publish Review")
    print("4 - Delete Review")
    print("5 - Delete All")
    print("6 - Edit review")
    print("9 - Exit")

    x = input()
    try:
        if x == '1':
            printAll()
        elif x == '2':
            print("\n\n1 - Search By Movie")
            print("2 - Search By Author")
            print("3 - Search By Stars")
            x = input()
            if x == '1':
                print("\nEnter movie: ")
                mov = input()
                movieSearch(mov)
            elif x == '2':
                print("\nEnter author: ")
                inp = input()
                authorSearch(inp)
            elif x == '3':
                print("\nEnter stars: ")
                inp = input()
                starSearch(inp)
        elif x == '3':
            print("\nEnter Movie: ")
            mov = input()
            print("Enter Author: ")
            auth = input()
            print("Enter Review: ")
            rev = input()
            print("Enter Stars: ")
            stars = input()
            #Server ignores 0's so it cannot be input
            if 0==stars or '0'==mov or '0'==auth or '0'==rev:
                print("Cannot contain 0")
            else:
                postReview(mov, auth, rev, stars)
        elif x == '4':
            print("\nEnter id: ")
            id = input()
            deleteReview(id)
        elif x == '5':
            deleteAll()
        elif x == '6':
            print("Enter id: ")
            inp = input()
            print("Enter movie: ")
            mov = input()
            print("Enter author: ")
            auth = input()
            print("Enter new review: ")
            rev = input()
            print("Enter new stars: ")
            stars = input()
            if 0==inp or 0== stars or '0'==mov or '0'==auth or '0'==rev:
                print("Cannot equal 0")
            else:
                editReview(inp,mov,auth,rev,stars)
        elif x == '9':
            #Exits
            loop = False
    except(requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print("Error")
        exit()
