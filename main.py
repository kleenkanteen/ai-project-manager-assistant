from typing import Union
from fastapi import FastAPI

import os
from slack_sdk import WebClient 
from slack_sdk.errors import SlackApiError 

""" We need to pass the 'Bot User OAuth Token' """
#slack_token = os.environ.get('SLACK_BOT_TOKEN')
slack_token="xoxb-6505923377716-6497481574726-g1uu7VHP0qwwHgXL68O15GsF"
print(f"{slack_token}")
# Creating an instance of the Webclient class
client = WebClient(token=slack_token)

try:
	# Posting a message in #random channel
	response = client.chat_postMessage(
    				channel="random",
    				text="Testing")
	print('Done 1')
	# Sending a message to a particular user
	response = client.chat_postEphemeral(
                    channel="random", 
                    text="Hello U06ETJNQX6E", 
                    user="U06ETJNQX6E")
	print('Done 2')
	# Get basic information of the channel where our Bot has access 
	response = client.conversations_info(
                    channel="random")
	print('Done 3')
	# Get a list of conversations
	response = client.conversations_list()
	print(response["channels"])
	
except SlackApiError as e:
	assert e.response["error"]

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}