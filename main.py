from fastapi import FastAPI, WebSocket

from pydantic_models.chat_body import ChatBody
from services.llm_service import LLMService
from services.sort_source_service import SortSourceService
from services.search_service import SearchService

app= FastAPI()

searchSercive = SearchService() 
sort_source_service = SortSourceService()
llm_service = LLMService()  

@app.websocket("/ws/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data= await websocket.receive_json()
        print(data)
        query=data.get("query")
        search_results=searchSercive.web_search(query)
        sorted_results=sort_source_service.sort_source(query,search_results)    
        print(sorted_results)
        await websocket.send_json({
            'type':'search_results',
            'data':sorted_results   
        })

        print("Sending response")

        for chunk in llm_service.generate_response(query,sorted_results):   
            await websocket.send_json({
                'type':'content',
                'data':chunk
            })

    except:
        print("Unexpected error occurred")   
    finally:
        await websocket.close()

@app.post("/chat")
def chat_endpoint(body :ChatBody):
    search_results=searchSercive.web_search(body.query) 
    sorted_results=sort_source_service.sort_source(body.query,search_results)
    response=llm_service.generate_response(body.query,sorted_results)
    return response 