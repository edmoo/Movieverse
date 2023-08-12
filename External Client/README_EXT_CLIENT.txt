To run external_client.py:
1. Make sure you are on a uni machine or using feng-linux
2. Start the server (See README_SERVER.txt)
3. Do "module add anaconda3" in new terminal window (on the same machine as server)
4. Do "python3 -m venv ext_client"
5. Do "source ext_client/bin/activate"
6. Do "python3 -m pip install requests"
7. Do "python3 external_client.py"
8. Follow On-screen instructions for the command-line client
9. Quit client using on-screen option
10. To deactivate environment do "deactivate"

NOTES:
- The web service used is 'Bing Image Search' and has a limit of 1000 requests per month
- Creating a virtual environment in step 4 is optional, but recommended
