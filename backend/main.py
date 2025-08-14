import asyncio
import websockets
import ollama
from memory import store_memory, retrieve_relevant_memory
from tts import speak
from stt import listen
from prompts import system_prompt
import json

# WebSocket clients
connected_clients = set()

async def broadcast(state, data=None):
    message = json.dumps({"state": state, "data": data})
    for client in list(connected_clients):
        try:
            await client.send(message)
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
                speak("Goodbye!")
                await broadcast("idle", {"response": "Goodbye!"})
                break

            await broadcast("thinking")
            response = generate_response(user_input)
            print(f"Elysia: {response}")
            await broadcast("speaking", {"response": response})
            speak(response)

            store_memory(user_input, response)

async def websocket_handler(websocket, path):
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
    speak("Hello, I'm Elysia. Ready to chat?")
    await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
