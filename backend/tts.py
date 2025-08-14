from kokoro import KPipeline
import numpy as np
from queue import Queue
import json

with open('config.json', 'r') as f:
    config = json.load(f)

pipeline = KPipeline(lang_code='a')
audio_queue = Queue()

async def speak(text, broadcast_audio=False):
    generator = pipeline(text, voice=config['tts_voice'])
    for _, _, audio in generator:
        chunk = audio.astype(np.float32)
        audio_queue.put(chunk)
    
    while not audio_queue.empty():
        chunk = audio_queue.get()
        if broadcast_audio:
            # Broadcast chunk for frontend playback/viz
            await broadcast("audio_chunk", audio_chunk=chunk.tobytes())
        # Backend fallback playback (optional, toggle if needed)
        # sd.play(chunk, samplerate=24000)
        # sd.wait()
