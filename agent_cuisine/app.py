from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    query: str

recipes = {
    "pâtes": "Recette pâtes : faire bouillir 8–10 min, égoutter, ajouter sauce tomate et parmesan.",
    "pizza": "Recette pizza : préparer la pâte, étaler la sauce tomate, ajouter du fromage et des garnitures, cuire au four à 220°C pendant 15-20 minutes.",
    "salade": "Recette salade : mélanger de la laitue, des tomates, des concombres et des oignons. Ajouter une vinaigrette à base d'huile d'olive et de vinaigre."
}

@app.post("/handle")
async def handle_cuisine(q: Query):
    txt = q.query.lower()
    for recipe, instructions in recipes.items():
        if recipe in txt:
            return {
                "answer": instructions,
                "metadata": {}
            }
    return {
        "answer": f"Désolé, je n'ai pas de recette pour : {q.query}. Essayez 'pâtes', 'pizza' or 'salade'.",
        "metadata": {}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
