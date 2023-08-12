To run movie_client.py:
1. Make sure you are on a uni machine or using feng-linux
2. Start the server (See README_SERVER.txt)
3. Do "module add anaconda3" in new terminal window (on the same machine as server)
4. Do "python3 -m venv mov_client"
5. Do "source mov_client/bin/activate"
6. Do "python3 -m pip install requests"
7. Do "python3 movie_client.py"
8. Follow On-screen instructions for the command-line client
9. Quit client using on-screen option
10. To deactivate environment do "deactivate"

NOTES:
- The service is accessed via the URL: http://127.0.0.1:9997/[...] Therefore,
  the client must be running on the same machine as the server
- Creating a virtual environment in step 4 is optional, but recommended
