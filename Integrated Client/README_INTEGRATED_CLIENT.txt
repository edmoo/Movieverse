To run the integrated client:
1. Make sure you are on a uni machine or using feng-linux
2. Start the movie service and the review service.
3. Do "module add anaconda3" in new terminal window (on the same machine as the servers)
4. Do "python3 -m venv int_client"
5. Do "source int_client/bin/activate"
6. Do "python3 -m pip install flask requests"
7. Do "python3 run.py"
8. Open a browser to https://127.0.0.1:9999 and follow onscreen instructions
9. Quit by doing Ctrl+C
10. To deactivate environment do "deactivate"

PURPOSE:
- You will be prompted to either search by review author or review star rating
- You will be then shown all reviews which match the search criteria (REVIEW SERVICE)
- You can click the movie title which to see the movie details (MOVIE SERVICE)
- You can click the movie title or director name to see a relevant image (3RD PARTY - BING IMAGE SEARCH)

NOTES:
- The services are accessed via the URL: http://127.0.0.1:999X/[...] Therefore,
  the client must be running on the same machine as the servers, X = [7,8,9]
- Creating a virtual environment in step 4 is optional, but recommended
