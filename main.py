from fastapi import FastAPI

from pydantic_models.chat_body import ChatBody
from services.search_service import SearchService

app= FastAPI()

searchSercive = SearchService() 

@app.post("/chat")
def chat_endpoint(body :ChatBody):
    search_results=searchSercive.web_search(body.query) 
    print(search_results)
    return body.query

