import os
import sys
from random import randrange
from typing import List, Union

from dotenv import load_dotenv

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from pyngrok import ngrok

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from supabase import Client, create_client

from llama_index.llms.clarifai import Clarifai
from llama_index.llms import ChatMessage

# Load environment variables from the .env file
load_dotenv()

os.environ["CLARIFAI_PAT"] = os.getenv("CLARIFAI_PAT") #you can replace with your PAT or use mine

""" We need to pass the 'Bot User OAuth Token' """
# slack_token = os.environ.get('SLACK_BOT_TOKEN')
slack_token = os.getenv("SLACK_TOKEN")
client = WebClient(token=slack_token)

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

try:
# Posting a message in #random channel
    response = client.chat_postMessage(channel="meetings", text="Testingaaa \n line 2")
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

except SlackApiError as e:
    assert e.response["error"]
    print("slack bot error")

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/transcription")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    data = contents.decode("utf-8")
    print(contents.decode("utf-8"))
    try:
        # send to clarifai with prompt to summarize it the transcript
        # llm_model = Clarifai(model_url="https://clarifai.com/openai/chat-completion/models/gpt-4-turbo")
        # summary = llm_model.complete(prompt=f'''
        #             Please generate a concise summary of the following Zoom meeting transcription, in this format. Instead of new lines, put the literal characters '\n' without the quotes for formatting:

        #             Highlighting the key takeaways, major discussion points, and relevant speakers. The summary should follow the format below:

        #             Takeaways:
        #             - [List the main takeaways or actionable items discussed during the meeting]

        #             Summary:
        #             [Provide a brief summary of the meeting's main topics and discussions, capturing the essence of the conversation]

        #             Speakers:
        #             - [List the speakers' names along with their notable contributions or comments]

        #             Additional Notes:
        #             [Include any noteworthy information, decisions, or action items that the team should be aware of]

        #             This summary will serve as a valuable reference for both meeting participants and those who missed the meeting, helping everyone stay informed and aligned on important matters. Please ensure clarity, brevity, and accuracy in the summary.

        #             Transcription: {data}
        #             ''')
        # print(summary)
        # supabase.table("transcripts").insert({"transcript": data, "summary": summary}).execute()
        # client.chat_postMessage(channel="meetings", text=summary)

        return JSONResponse(
            content={"message": "Transcript summarized with gpt-4-turbo and saved to supabase"},
            status_code=200,
        )
    except Exception as e:
        return JSONResponse(
            content={"message": "Error printing file contents"}, status_code=500
        )

@app.post("/dailysummary")
def daily_summary():
    print("DAILY \SUMMARY")
    # response = client.conversations_info(channel="random")
    response = client.conversations_list()
    print(response["channels"])

    client.chat_postMessage(channel="meetings", text="DIE\nDIE")
    return JSONResponse(content="Line 1'\n'Line 2", status_code=200)

