2nd place winner in the [lablabai AI hackathon](https://lablab.ai/event/nextgen-gpt-ai-hackathon) among 47 submissions. I hatched the idea and invited both team members. [Demo](https://lablab.ai/event/nextgen-gpt-ai-hackathon/jarvis/ai-project-manager-assistant)

API server for the project manager assistant slack bot.

First install the dependencies with `pip install -r requirements.txt`. Didn't use a virtual env cus it didn't work and I was running out of time xD.

First install the ngrok cli. ngrok allows you to expose a locally running server to the internet. ngrok does this through a "tunnel" it creates from the internet to the local port your server is running on. Any internet traffic is directed to that port. And vice versa. 

Download the executable from [here](https://ngrok.com/download) and in your terminal, `cd` to your project run `ngrok http 8000`. ngrok will direct requests to your local port 8000. This is the public URL for your server. Requests go like user -> this public url on ngrok's servers -> your local server on port 800. And responses go like server response -> ngrok tunnel on port 8000 -> user.

In another terminal, run the server with `uvicorn main:app --reload`. `uvicorn` is the web server that forwards the requests to our fastapi server. `main` is the name of our python file running fastapi, `main.py`. `--reload` means it will restart the server on code changes. The server will run on port 8000 by default. ngrok will listen to the requests on port 8000.

You put the url that ngrok gives you into the zapier webhook, post request url input.

Copy `.env.example` to `.env` and fill in the environment variables.

From api.slack.com, create a bot and get the bot token. Put it in the `SLACK_BOT_TOKEN` environment variable.

Next, go the "Slash Commands" section and create a command named /dailysummary. For the url, add the the ngrok url but append /dailysummary. This is the endpoint that is defined in `main.py`.
