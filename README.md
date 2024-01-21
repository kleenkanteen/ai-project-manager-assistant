API server for the project manager assistant slack bot.

First install the dependencies with `pip install -r requirements.txt`. Not using virtual environment.

You also have to intall the ngrok cli. ngrok allows you to expose a web server running on your local machine to the internet. Just download the executable from [here](https://ngrok.com/download) and run it with `./ngrok http 8000`. This will expose the server running on port 8000 to the internet. You will get a url that you can use to send requests to your local server.

Then run the server with `server.py`. The server will run on port 8000 by default.
