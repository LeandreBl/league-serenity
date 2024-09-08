import json
import os
import sys
import argparse
import unicodedata
import re
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

import torch
from TTS.api import TTS

device = "cuda" if torch.cuda.is_available() else "cpu"
args = sys.argv[1:]

argparse = argparse.ArgumentParser(description="Generate audio files from a quotes JSON file.")
argparse.add_argument(
    "--quotes-file",
    "-f",
    type=str,
    required=True,
    help="Path to the quote JSON file containing quotes.",
)
argparse.add_argument(
    "--output-dir",
    "-o",
    type=str,
    required=True,
    help="Directory to save the generated audio files.",
)
argparse.add_argument(
    "--clean",
    "-c",
    action="store_true",
    help="Clean the output directory and json file.",
)

args = argparse.parse_args(args)
if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

input_file = args.quotes_file
if not os.path.exists(input_file):
    raise FileNotFoundError(f"Quotes file {input_file} does not exist.")

if not args.clean:
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)

with open(input_file, "r+", encoding="utf-8") as f:
    quotes = json.load(f)

    for quote in quotes:
        for lang, text in quote["languages"].items():
            soundpath = re.sub(r'[,.\s]+', '_', unicodedata.normalize("NFD", text)).lower()
            soundpath = re.sub(r'[\u0300-\u036f]', '', soundpath)
            soundpath = re.sub(r'[_.]+$', '', soundpath)

            quote.setdefault("soundpaths", {})
            quote["soundpaths"][lang] =  os.path.join(lang, f"{soundpath}.wav")

            output_path = os.path.join(args.output_dir, quote["soundpaths"][lang])

            if args.clean:
                if os.path.exists(output_path):
                    logging.info(f"Removing {output_path}")
                    os.remove(output_path)
                continue

            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path))

            audio = tts.tts_to_file(text, file_path=output_path, speaker_wav="./build/sample.mp3", language=lang)
            logging.info(output_path)

        if args.clean:
            del quote["soundpaths"]

    f.seek(0)
    json.dump(quotes, f, indent=2, ensure_ascii=False)
    f.truncate()
    f.flush()
