## Introduction

A slack bot for project managers. Instantly send meeting summaries in a channel right after a zoom meeting. And see a summary of all your daily meetings with a simple /dailysummary command.

Presentation: https://vimeo.com/905384625

Demo: Join this slack channel and type /dailysummary to test that command: https://join.slack.com/t/assistanthackathonhq/shared_invite/zt-2b5ggtnj5-3B0EOu3Z_mHlAuozLuvbIg

You won't be able to do a meeting and get the transcriptions for it. You'll have to download the desktop app from fathom.video, link it to your zoom account, and then create a 2 piece Zapier integration that sends Fathom's meeting transcript to my FastAPI server.

## Tech Stack
- FastAPI (Python web server)
- GPT-4 turbo to generate summaries from meeting transcription.
- Supabase (hosted postgres instance)
- Fathom for zoom bot + Zapier integration to send the video transcription to our FastAPI server
- ngrok to host the server publicly

## Developement Guide

This repo is the API server that serves the slack bot and Zapier webhook.

1. First install the dependencies with `pip install -r requirements.txt`. Not using virtual environment because I had issues on windows for it.
2. You have to set up a slack bot. Sign in to api.slack.com. Create a bot. Install it to your workspace and give it access to the #meetings channel. Add the bot's api key to `.env`.
3. Set up a supabase project and fill in the url as well as the service key in `.env`.
4. Sign in to clarifai.com and get your account's api key to put into `.env`.
5. Install ngrok from [here](https://ngrok.com/download). ngrok allows you to expose a local port to the internet. The local port you will expose is the port your web server is running on. Type `ngrok http 8000`. This will expose port 8000 to the internet. You will get a url that others can use to access your server.
6. In a new terminal, run the FastAPI server with `uvicorn main:app --reload`. `uvicorn` is the web server that forwards the requests to our FastAPI server. `main` is the name of our entry point file, `main.py`. `--reload` means it will restart the server on code changes. The server will run on port 8000 by default.
7. You then put the ngrok url into the zapier post webhook's url in the action panel. Test that part and it should work.
8. In api.slack.com, create the /dailysummary command. Use the ngrok url when setting it up.

Start a zoom meeting with at least 2 participants and talk for at least 1 minute. Make sure Fathom's bot is there and recording. When the meeting ends, you will see the slack bot write the summary in the #meeting channel. Type /dailysummary and all summaries of the day will also be written.
