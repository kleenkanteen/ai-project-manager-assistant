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
from broker import cloudamqp
import weaviate
from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
from supabase import Client, create_client
import shutil
import nest_asyncio
import json
import logging
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex,SimpleDirectoryReader,ServiceContext,PromptTemplate, Document
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.core.response.notebook_utils import display_response
from llama_index.llms.clarifai import Clarifai
from datetime import datetime, timedelta, timezone
from llama_index.core.node_parser import SimpleNodeParser
import weaviate

nest_asyncio.apply()




# Get the current date and time
current_date_time = datetime.now()
current_date = current_date_time.date()


# Load environment variables from the .env file
load_dotenv()


""" We need to pass the 'Bot User OAuth Token' """
# slack_token = os.environ.get('SLACK_BOT_TOKEN')
os.environ["CLARIFAI_PAT"] = os.getenv("CLARIFAI_PAT") #you can replace with your PAT or use mine
slack_token = os.getenv("SLACK_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
client = WebClient(token=slack_token)
supabase: Client = create_client(url, key)

auth_config = weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY)

cllient = weaviate.Client(
  url=WEAVIATE_URL,
  auth_client_secret=auth_config
)
rag_bot = App(token=os.environ.get("RAG_TOKEN"))


app = FastAPI()
import os

def search_and_query(text, ask):
    text_list = [text]
    documents = [Document(text=t) for t in text_list]
    parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=20)
    nodes = parser.get_nodes_from_documents(documents)
    vector_store = WeaviateVectorStore(weaviate_client=cllient)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    query_engine = index.as_query_engine(similarity_top_k=2)
    response = query_engine.query(ask)
    return response


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
    #response = supabase.table("transcripts").select('*').execute()
    print("HAHAHAHAHA")
    response = supabase.table("transcripts").select().filter("created_at", "gte", today_start).filter("created_at", "lte", today_end).execute()
    summaries = response.data
    print(summaries)
    summaries_string = "\n\n".join([summary['summary'] for summary in summaries])
    full_message = "*Daily meeting summaries*\n\n" + summaries_string
    print(full_message)
    client.chat_postMessage(channel="meetings", text=full_message)
    return JSONResponse(content="Summaries posted to Slack", status_code=200)


@rag_bot.message("")
def message_hello(message, say):
    response = supabase.table("transcripts").select('transcript').execute()
    summaries_dated = response.data
    text_string = str(summaries_dated) 
    out = search_and_query(text_string, message['text'])
    say(str(out))
    

if __name__== "__main__":
    
    tasks = [
        SocketModeHandler(rag_bot, os.environ.get("RAG_SOCKET_TOKEN")).start(),
        uvicorn.run(app, host="0.0.0.0", port=8000)
    ]

    # Run both tasks concurrently
    asyncio.run(asyncio.gather(*tasks))

