import argparse
import json
import logging
import os
import re
import unicodedata
import urllib.request
import wave

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ElevenLabs instant clone of build/sample.mp3 (voice "league-serenity").
VOICE_ID = "7k53hL4G30o4usRJMDzN"
MODEL_ID = "eleven_multilingual_v2"
SAMPLE_RATE = 24000
# A calm, soft, slow therapist: steady delivery, no added style, slowest speed.
VOICE_SETTINGS = {"stability": 0.8, "similarity_boost": 0.75, "style": 0.0, "speed": 0.7}


def soundpath_of(text, lang):
    soundpath = re.sub(r"[,.\s]+", "_", unicodedata.normalize("NFD", text)).lower()
    soundpath = re.sub(r"[̀-ͯ]", "", soundpath)
    soundpath = re.sub(r"[_.]+$", "", soundpath)
    return os.path.join(lang, f"{soundpath}.wav")


def generate(key, voice, text, output_path):
    request = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=pcm_{SAMPLE_RATE}",
        data=json.dumps({"text": text, "model_id": MODEL_ID, "voice_settings": VOICE_SETTINGS}).encode(),
        headers={"xi-api-key": key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request) as response:
        pcm = response.read()
    with wave.open(output_path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(pcm)


def main():
    parser = argparse.ArgumentParser(description="Generate audio files from a quotes JSON file with ElevenLabs.")
    parser.add_argument("--quotes-file", "-f", required=True, help="Path to the quote JSON file containing quotes.")
    parser.add_argument("--output-dir", "-o", required=True, help="Directory to save the generated audio files.")
    parser.add_argument("--clean", "-c", action="store_true", help="Clean the output directory and json file.")
    parser.add_argument("--only", nargs="*", default=[], help="Only (re)generate these soundpaths, e.g. fr/tu_es_heureux.wav.")
    parser.add_argument("--voice", default=VOICE_ID, help="ElevenLabs voice id.")
    args = parser.parse_args()

    key = os.environ.get("ELEVENLABS_API_KEY")
    if not args.clean and not key:
        raise SystemExit("ELEVENLABS_API_KEY is not set.")

    with open(args.quotes_file, "r+", encoding="utf-8") as f:
        quotes = json.load(f)

        for quote in quotes:
            for lang, text in quote["languages"].items():
                quote.setdefault("soundpaths", {})[lang] = soundpath_of(text, lang)
                output_path = os.path.join(args.output_dir, quote["soundpaths"][lang])

                if args.clean:
                    if os.path.exists(output_path):
                        logging.info(f"Removing {output_path}")
                        os.remove(output_path)
                    continue
                if args.only and quote["soundpaths"][lang] not in args.only:
                    continue

                # "spoken": the text said, respelled where the voice mispronounces
                # anglicisms; "languages" stays the text displayed.
                spoken = quote.get("spoken", {}).get(lang, text)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                logging.info(f"{output_path}: '{spoken}'")
                generate(key, args.voice, spoken, output_path)

            if args.clean:
                del quote["soundpaths"]

        f.seek(0)
        json.dump(quotes, f, indent=2, ensure_ascii=False)
        f.truncate()


if __name__ == "__main__":
    main()
