import requests
import time

def download_image():
    # Ask user for their search term
    i = input("What is your search query? [query/b]: ")
    # quit if user enters b
    if i.strip().lower() == 'b':
        print("")
        return
    # Recall self if invalid input
    elif i.strip() is None:
        print("Invalid input")
        download_image()
        return
    # Create the API request
    url = "https://bing-image-search1.p.rapidapi.com/images/search"
    querystring = {"q":i.strip(),"count":"10","safeSearch":"moderate"}
    headers = {
        "X-RapidAPI-Key": "360e258801msh0b4172e9e4039b5p1b052fjsn69567fcb2512",
        "X-RapidAPI-Host": "bing-image-search1.p.rapidapi.com"
    }
    start = time.time()
    response = requests.request("GET", url, headers=headers, params=querystring)
    end = time.time()
    print("Response time: %fs" %(end-start))
    data = response.json()
    # Gets 10 results so loop through each result until valid image is found
    for result in data['value']:
        imgUrl = result['contentUrl']
        f1 = imgUrl.split('/')[-1] # get the last part of the url
        f2 = f1.split('?')[0]  # get filename
        f3 = f2.split('.')
        if len(f3) > 1: #has extension
            # Download the image binary data
            fname = f2
            print("Downloading image...")
            start = time.time()
            response = requests.get(imgUrl)
            end = time.time()
            print("Download time: %fs" %(end-start))
            if response.status_code != 200:
                print("Error downloading image")
                continue
            print("Saving image...")
            start = time.time()
            # save the image
            with open(fname, 'wb') as f:
                f.write(response.content)
            end = time.time()
            print("Save time: %fs" %(end-start))
            print("Image saved as %s" %fname)
            break
    
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

# Main body of the program
print("Welcome to the Bing Image Search Client!\n")
while True:
    # Ask user for input with options
    print("What would you like to do?")
    print("1. Download an Image")
    print("2. Quit\n")
    istr = input("Please select from the list above: ")
    i = int(istr)
    # Wrapped in try block to catch connection error
    try:
        if i == 1:
            download_image()
        elif i == 2:
            exit()
        else:
            print("Unrecognised option! Please try again.\n")
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print("Connection error! Quitting.\n")
        exit()