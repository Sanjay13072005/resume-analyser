from sentence_transformers import SentenceTransformer, util
import json
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

# Load job roles
with open(r"C:\Users\Sanjay B\OneDrive\Pictures\resume_analyzer\data\keyword_roles.json", "r") as f:
    roles = json.load(f)

def suggest_roles(resume_text, top_n=3):
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    similarities = []
    for role, desc in roles.items():
        desc_embedding = model.encode(desc, convert_to_tensor=True)
        score = util.cos_sim(resume_embedding, desc_embedding).item()
        similarities.append((role, score))
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [role for role, score in similarities[:top_n]]
