import chromadb
from datetime import datetime
import ollama

client = chromadb.PersistentClient(path="../memory_db")
collection = client.get_or_create_collection(name="elysia_memory")

def store_memory(user_input, assistant_response):
    timestamp = datetime.now().isoformat()
    text = f"User: {user_input}\nElysia: {assistant_response}"
    embedding = ollama.embeddings(model="elysia:latest", prompt=text)['embedding']
    collection.add(documents=[text], embeddings=[embedding], ids=[timestamp], metadatas=[{"timestamp": timestamp}])

def retrieve_relevant_memory(query, threshold=0.7):
    embedding = ollama.embeddings(model="elysia:latest", prompt=query)['embedding']
    results = collection.query(query_embeddings=[embedding], n_results=3, include=["documents", "distances"])
    relevant = [doc for doc, dist in zip(results['documents'][0], results['distances'][0]) if (1 - dist) >= threshold]
    return "\n\n".join(relevant) if relevant else None
