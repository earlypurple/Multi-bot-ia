from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    query: str

@app.post("/handle")
async def handle_cuisine(q: Query):
    txt = q.query.lower()
    if "pâtes" in txt:
        return {
            "answer": "Recette pâtes : faire bouillir 8–10 min, égoutter, ajouter sauce tomate et parmesan.",
            "metadata": {}
        }
    return {
        "answer": f"Conseil cuisine pour : {q.query}",
        "metadata": {}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
