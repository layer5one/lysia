from kokoro import KPipeline
import numpy as np
import torch
import json
import os

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

pipeline = KPipeline(lang_code='a')

def generate_audio_chunks(text):
    generator = pipeline(text, voice=config['tts_voice'])
    for _, _, audio in generator:
        if isinstance(audio, torch.Tensor):
            audio = audio.cpu().numpy()
        chunk = audio.astype(np.float32)
        yield chunk
