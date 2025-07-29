from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
import os
import httpx

class Query(BaseModel):
    query: str

class Hub(BaseModel):
    query: str
    result: str = ""

app = FastAPI()

# LangGraph pour routage
graph = StateGraph(Hub)

@graph.add_node
def router(state):
    txt = state.query.lower()
    if "recette" in txt or "cuisine" in txt: 
        return "cuisine"
    elif "trade" in txt or "action" in txt or "bourse" in txt: 
        return "tradeur"
    elif "cannabis" in txt or "strain" in txt: 
        return "cannabis"
    elif "actu" in txt or "news" in txt or "géo" in txt: 
        return "geo"
    else: 
        return "med"

# Routes vers les agents spécialisés
async def call_agent(agent_name: str, query: str):
    agent_urls = {
        "cuisine": "https://earlypurple-agent-cuisine.hf.space/handle",
        "tradeur": "https://earlypurple-agent-tradeur.hf.space/handle", 
        "cannabis": "https://earlypurple-agent-cannabis.hf.space/handle",
        "geo": "https://earlypurple-agent-geo.hf.space/handle",
        "med": "https://earlypurple-agent-med.hf.space/handle"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(agent_urls[agent_name], 
                                   json={"query": query})
        return response.json()

@app.post("/ask")
async def orchestrate(q: Query):
    # Router la requête
    route = router(Hub(query=q.query))
    result = await call_agent(route, q.query)
    return {"route": route, "result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
