
import os
from slack_sdk import WebClient 
from slack_sdk.errors import SlackApiError 

""" We need to pass the 'Bot User OAuth Token' """
#slack_token = os.environ.get('SLACK_BOT_TOKEN')
slack_token="xoxb-6505923377716-6526528072016-EXQK9psScHfeGeAyKWCSVHdl"
print(f"{slack_token}")
# Creating an instance of the Webclient class
client = WebClient(token=slack_token)

try:
	# Posting a message in #random channel
	response = client.chat_postMessage(
    				channel="random",
    				text="Bot's first message")
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