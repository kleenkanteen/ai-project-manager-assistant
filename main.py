import os
import sys
from typing import Union, List

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from random import randrange
# Load environment variables from the .env file
load_dotenv()
MAX_RANDOM_USER_ID = 1_000_000_000
user_id = randrange(1, MAX_RANDOM_USER_ID)


""" We need to pass the 'Bot User OAuth Token' """
# slack_token = os.environ.get('SLACK_BOT_TOKEN')
slack_token = os.getenv('Slack_Token')
print(f"{slack_token}")
# Creating an instance of the Webclient class
client = WebClient(token=slack_token)

BASE_URL = "http://localhost:8000"
USE_NGROK = "True"
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_ANON_KEY')

supabase: Client = create_client(url, key)

def init_webhooks(base_url):
    # Update inbound traffic via APIs to use the public-facing ngrok URL
    pass


if USE_NGROK:
    # pyngrok should only ever be installed or initialized in a dev environment when this flag is set
    from pyngrok import ngrok

    # Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
    # when starting the server
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "8000"

    # Open a ngrok tunnel to the dev server
    # I commented this part out because you should run "ngrok http 8000" in a separate terminal
    # public_url = ngrok.connect(port).public_url
    # print("ngrok url:", public_url)
    # logger.info('ngrok tunnel "{}" -> "http://127.0.0.1:{}"'.format(public_url, port))

    # Update any base URLs or webhooks to use the public ngrok URL
    # commented out for now
    # BASE_URL = public_url
    # init_webhooks(public_url)


# try:
    # Posting a message in #random channel
    # response = client.chat_postMessage(channel="random", text="Testing")
    # print("Done 1")
    # Sending a message to a particular user
    # response = client.chat_postEphemeral(
    #     channel="random", text="Hello U06ETJNQX6E", user="U06ETJNQX6E"
    # )
    # print("Done 2")
    # Get basic information of the channel where our Bot has access
    # response = client.conversations_info(channel="random")
    # print("Done 3")
    # Get a list of conversations
    # response = client.conversations_list()
    # print(response["channels"])

# except SlackApiError as e:
#     assert e.response["error"]
#     print("slack bot error")

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# @app.post("/summary")
# def summary(request: Request):
#     body = request.body()
#     print("body", body)
#     # body = request.json()
#     # print("body", body)
#     # return JSONResponse(content=body, status_code=200)
#     return JSONResponse(content=body, status_code=200)

@app.post("/summary")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    data = (contents.decode('utf-8'))
    print(contents.decode('utf-8'))
    response = supabase.table('test').insert({'id': user_id, 'texxt': data}).execute()
    return JSONResponse(content={"message": "File contents printed successfully"}, status_code=200)