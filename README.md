API server for the project manager assistant slack bot.

First install the dependencies with `pip install -r requirements.txt`. Not using virtual environment.

You also have to intall the ngrok cli. ngrok allows you to expose a local port to the internet. The local port is the port your web server is serving. Just download the executable from [here](https://ngrok.com/download) and run it with `ngrok http 8000`. This will expose the server running on port 8000 to the internet. You will get a url that you can use to send requests to your local server.

In a new terminal, run the server with `uvicorn main:app --reload`. `uvicorn` is the web server that forwards the requests to our fastapi server. `main` is the name of our fastapi entry point file, `main.py`. `--reload` means it will restart the server on code changes. The server will run on port 8000 by default. ngrok will listen to the requests on port 8000 and forward them to your local server.

You put the url that ngrok gives you into the zapier post webhook url in the action panel.

run the code. 

lines 72 to 94 are problematic. sending the trnascript to clarifai and getting the response back is not working. but everything else is.



To run Rag for your Meetings you have to run first postman and go to endpoint ./meeting_ids (Example:- http://127.0.0.1:8000/meeting_ids) 

After that you will get your meeting id with summary of each meetings 

Now you have to change endpoint to ./dailysummary/rag/{id}  (Example :- http://127.0.0.1:8000/dailysummary/rag/17) and send post request with below Json type

```json
{
    "model": "gpt-4",
    "response_format": {"type": "json_object"},
    "messages": [
        {
            "role": "system",
            "content": "You are helpful Assistant who is knowldgeable about meetings and their information about it",
            "topic": "seller"
        },
        {
            "role": "user",
            "content": "What is meeting about?"
        }
    ]
}
```

Now you can change content of user to ask any question about meetings

