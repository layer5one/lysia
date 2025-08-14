import chromadb
from datetime import datetime
import ollama
import json
import os

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

client = chromadb.PersistentClient(path="./memory_db")
collection = client.get_or_create_collection(name="elysia_memory")
recent_memory = []  # In-memory list for last N turns

def store_memory(user_input, assistant_response):
    timestamp = datetime.now().isoformat()
    text = f"User: {user_input}\nElysia: {assistant_response}"
    embedding = ollama.embeddings(model="elysia:latest", prompt=text)['embedding']
    collection.add(documents=[text], embeddings=[embedding], ids=[timestamp], metadatas=[{"timestamp": timestamp}])
    
    recent_memory.append(text)
    if len(recent_memory) > config['recent_memory_limit']:
        recent_memory.pop(0)

def retrieve_relevant_memory(query, threshold=config['memory_threshold']):
    recent = "\n\n".join(recent_memory)  # Always include recent for fluidity
    
    embedding = ollama.embeddings(model="elysia:latest", prompt=query)['embedding']
    results = collection.query(query_embeddings=[embedding], n_results=3, include=["documents", "distances"])
    older = [doc for doc, dist in zip(results['documents'][0], results['distances'][0]) if (1 - dist) >= threshold]
    older_str = "\n\n".join(older) if older else ""
    
    memory = recent
    if older_str:
        memory += f"\n\nOlder relevant context:\n{older_str}"
    return memory if memory else None
