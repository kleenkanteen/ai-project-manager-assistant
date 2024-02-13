import os
import sys
from random import randrange
from typing import List, Union
from datetime import date

from dotenv import load_dotenv
from fastapi import FastAPI, File, Request, UploadFile, Path
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from pyngrok import ngrok
import os
import weaviate
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from supabase import Client, create_client
import shutil
import nest_asyncio
import json

nest_asyncio.apply()

from llama_index.evaluation import generate_question_context_pairs
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.node_parser import SimpleNodeParser
from llama_index.evaluation import generate_question_context_pairs
from llama_index.evaluation import RetrieverEvaluator
from llama_index.llms import OpenAI
from llama_index.llms.clarifai import Clarifai
from llama_index.llms import ChatMessage
from datetime import datetime
from datetime import datetime, timedelta, timezone

# Get the current date and time
current_date_time = datetime.now()
current_date = current_date_time.date()




# Load environment variables from the .env file
load_dotenv()

os.environ["CLARIFAI_PAT"] = os.getenv("CLARIFAI_PAT") #you can replace with your PAT or use mine

""" We need to pass the 'Bot User OAuth Token' """
# slack_token = os.environ.get('SLACK_BOT_TOKEN')
slack_token = os.getenv("SLACK_TOKEN")
client = WebClient(token=slack_token)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)


# try:
# Posting a message in #random channel
    # response = client.chat_postMessage(channel="meetings", text="Testingaaa \n line 2")
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

def search_and_query(text):
    documents = SimpleDirectoryReader("./Data").load_data()
    llm = OpenAI(model="gpt-4")
    node_parser = SimpleNodeParser.from_defaults(chunk_size=512)
    nodes = node_parser.get_nodes_from_documents(documents)
    vector_index = VectorStoreIndex(nodes)
    query_engine = vector_index.as_query_engine()
    response_vector = query_engine.query(f"{text}")
    return str(response_vector.response)

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
    print(type(data))
    try:
        # send to clarifai with prompt to summarize it the transcript
        llm_model = Clarifai(model_url="https://clarifai.com/openai/chat-completion/models/gpt-4-turbo")
        summary = llm_model.complete(prompt=f'''
            Please generate a concise summary of the following Zoom meeting transcription, in this format. Instead of new lines, put the literal 
            characters '\n' without the quotes for formatting:

            Highlighting the key takeaways, major discussion points, and relevant speakers. The summary should follow the format below:

            Topic: [Main topic of the meeting]

            Speakers:
            - [List the speakers' names along with their notable contributions or comments]

            Summary:
            - [Provide a brief summary of the meeting's main topics and discussions, capturing the essence of the conversation]

            Transcription: {data}
            ''')
        summary = (str(summary))
        supabase.table("transcripts").insert({"transcript": data, "summary": summary}).execute()
        client.chat_postMessage(channel="meetings", text=summary)

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
    today = date.today()
    today_start = today.isoformat() + "T00:00:00Z"
    today_end = today.isoformat() + "T23:59:59Z"
    response = supabase.table("transcripts").select('*').execute()
    print("HAHAHAHAHA")
    # response = supabase.table("transcripts").select().filter("created_at", "gte", today_start).filter("created_at", "lte", today_end).execute()
    summaries = response.data
    print(summaries)
    summaries_string = "\n\n".join([summary['summary'] for summary in summaries])
    full_message = "*Daily meeting summaries*\n\n" + summaries_string
    client.chat_postMessage(channel="meetings", text=full_message)
    return JSONResponse(content="Summaries posted to Slack", status_code=200)
    # response = client.conversations_info(channel="random")
    # response = client.conversations_list()
    # print(response["channels"])


@app.post('/meeting_ids')
def metting_id():
    response = supabase.table("transcripts").select('id','summary').execute()
    

    #ids = response['id']
    return JSONResponse(content={'Response': str(response)}, status_code=200)

@app.post("/dailysummary/rag/{title}")
def daily_summary(data: dict, title: str = Path(..., title="The title of the daily summary")):
    messages = data.get("messages", [])
    user_message = next((msg["content"] for msg in messages if msg["role"] == "user"), None)
    response = supabase.table("transcripts").select('*').eq('id', title).execute()
    dat = response.data[0]['transcript']
    directory_path = './Data'
    os.makedirs(directory_path, exist_ok=True)
    file_path = os.path.join(directory_path, 'example.txt')
    text_string = str(dat)
    with open(file_path, 'w') as file:
        file.write(text_string)  
    out = search_and_query(user_message)
    print(out)
    return JSONResponse(content={"title": f"{out}"}, status_code=200)