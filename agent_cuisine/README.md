---
title: AgentIA-Cuisine
emoji: 🍲
colorFrom: green
colorTo: orange
sdk: docker
app_file: app.py
pinned: false
---

# AgentIA-Cuisine

Cet agent FastAPI fournit des conseils et recettes de cuisine.

## Endpoint

- **POST /handle**  
  **Request**  
{ "query": "votre question cuisine" }


**Response**  
{
"answer": "texte de réponse",
"metadata": {}
}



## Déploiement

1. Sélectionnez **Docker → Blank** sur Hugging Face Spaces.  
2. Poussez ces fichiers :  
git add app.py requirements.txt Dockerfile README.md
git commit -m "Update AgentIA-Cuisine core files"
git push origin main --force


