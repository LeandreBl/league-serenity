#!/usr/bin/env python3

import torch
import time
from TTS.api import TTS

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC").to(device)

start = time.time()
tts.tts(text="That mate your flamed deserved it.")
stop = time.time()

print(f"Generated audio in {stop - start:.2f} seconds")
