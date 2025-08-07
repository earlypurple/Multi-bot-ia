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
        "cuisine": os.getenv("AGENT_CUISINE_URL", "https://earlypurple-agent-cuisine.hf.space/handle"),
        "tradeur": os.getenv("AGENT_TRADEUR_URL", "https://earlypurple-agent-tradeur.hf.space/handle"),
        "cannabis": os.getenv("AGENT_CANNABIS_URL", "https://earlypurple-agent-cannabis.hf.space/handle"),
        "geo": os.getenv("AGENT_GEO_URL", "https://earlypurple-agent-geo.hf.space/handle"),
        "med": os.getenv("AGENT_MED_URL", "https://earlypurple-agent-med.hf.space/handle")
    }
    
    url = agent_urls.get(agent_name)
    if not url:
        raise HTTPException(status_code=400, detail=f"Agent '{agent_name}' not found")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json={"query": query})
            response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
            return response.json()
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=f"Error while calling agent: {exc}")

@app.post("/ask")
async def orchestrate(q: Query):
    try:
        # Router la requête
        route = router(Hub(query=q.query))
        result = await call_agent(route, q.query)
        return {"route": route, "result": result}
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
