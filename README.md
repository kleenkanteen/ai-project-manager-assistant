API server for the project manager assistant slack bot.

First install the dependencies with `pip install -r requirements.txt`. Not using virtual environment.

You also have to intall the ngrok cli. ngrok allows you to expose a local port to the internet. The local port is the port your web server is serving. Just download the executable from [here](https://ngrok.com/download) and run it with `ngrok http 8000`. This will expose the server running on port 8000 to the internet. You will get a url that you can use to send requests to your local server.

In a new terminal, run the server with `uvicorn main:app --reload`. `uvicorn` is the web server that forwards the requests to our fastapi server. `main` is the name of our fastapi entry point file, `main.py`. `--reload` means it will restart the server on code changes. The server will run on port 8000 by default. ngrok will listen to the requests on port 8000 and forward them to your local server.

You put the url that ngrok gives you into the zapier post webhook url in the action panel.