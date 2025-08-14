import asyncio
import websockets
import ollama
import json
from memory import store_memory, retrieve_relevant_memory
from tts import generate_audio_chunks  # Updated import
from stt import listen
from prompts import system_prompt

connected_clients = set()

async def broadcast(state, data=None, audio_chunk=None):
    message = {"state": state, "data": data}
    if audio_chunk is not None:
        message["audio_chunk"] = audio_chunk.tolist()  # Send as list for JSON
    msg_json = json.dumps(message)
    for client in list(connected_clients):
        try:
            await client.send(msg_json)
        except:
            connected_clients.remove(client)

def generate_response(user_input):
    memory = retrieve_relevant_memory(user_input)
    
    prompt = system_prompt
    if memory:
        prompt += f"\nRelevant past context:\n{memory}\n"
    
    prompt += f"\nUser: {user_input}\nElysia:"
    
    response = ollama.generate(model="elysia:latest", prompt=prompt)['response']
    return response

async def handle_interaction():
    await broadcast("idle")
    while True:
        await broadcast("listening")
        user_input = listen()
        if user_input:
            if user_input.lower() in ["exit", "quit", "bye"]:
                await broadcast("idle", {"response": "Goodbye!"})
                for chunk in generate_audio_chunks("Goodbye!"):
                    await broadcast("audio_chunk", audio_chunk=chunk)
                break
            
            await broadcast("thinking")
            response = generate_response(user_input)
            print(f"Elysia: {response}")
            await broadcast("speaking", {"response": response})
            for chunk in generate_audio_chunks(response):
                await broadcast("audio_chunk", audio_chunk=chunk)
            
            store_memory(user_input, response)

async def websocket_handler(websocket, path=None):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            if data.get("action") == "start":
                await handle_interaction()
    finally:
        connected_clients.remove(websocket)

async def main():
    server = await websockets.serve(websocket_handler, "localhost", 8000)
    print("Hello, I'm Elysia. Ready to chat?")
    await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
