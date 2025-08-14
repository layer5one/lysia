from kokoro import KPipeline
import sounddevice as sd
import numpy as np

pipeline = KPipeline(lang_code='a')  # American English

def speak(text):
    generator = pipeline(text, voice='af_heart')
    for _, _, audio in generator:
        # Audio is numpy array, play directly
        sd.play(audio.astype(np.float32), samplerate=24000)
        sd.wait()
