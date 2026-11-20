import argparse
import difflib
import json
import logging
import os
import re
import unicodedata

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# XTTS mispronounces gaming jargon and abbreviations (worst in French): the
# synthesized text is respelled phonetically, the displayed quote is unchanged.
PRONUNCIATIONS = {
    "en": {
        "L.P.": "L P",
        "Porofessor": "Poro-fessor",
        "winrate": "win rate",
        "Teemo": "Teemoh",
    },
    "fr": {
        "League of Legends": "Ligue ofe Légendes",
        "L.P.": "elle pé",
        "Teemo": "Timo",
        "Yasuo": "Yassouo",
        "Porofessor": "Poro-fessor",
        "winrate": "ouine-rète",
        "flash in": "flache inne",
        "Pick": "Pique",
        "Vayne": "Veine",
        "feeds": "fides",
        "flames": "flèmes",
        "flame": "flèmé",
        "mate": "mète",
        "memes": "mimes",
        "move": "mouve",
        "outplay": "aoute-plé",
        "ganks": "gannkes",
        "gap": "gape",
        "laner": "lèneur",
        "Zoom": "Zoume",
        "10": "dix",
    },
}


def tts_text(text, lang):
    for word, spoken in PRONUNCIATIONS.get(lang, {}).items():
        text = re.sub(rf"(?<!\w){re.escape(word)}(?!\w)", spoken, text)
    return text


def letters(text):
    text = unicodedata.normalize("NFD", text.lower())
    text = re.sub(r"[̀-ͯ]", "", text)
    return re.sub(r"[^a-z0-9]+", "", text)


def similarity(expected, heard):
    return difflib.SequenceMatcher(None, letters(expected), letters(heard), autojunk=False).ratio()


def soundpath_of(text, lang):
    soundpath = re.sub(r"[,.\s]+", "_", unicodedata.normalize("NFD", text)).lower()
    soundpath = re.sub(r"[̀-ͯ]", "", soundpath)
    soundpath = re.sub(r"[_.]+$", "", soundpath)
    return os.path.join(lang, f"{soundpath}.wav")


def generate(tts, whisper, text, lang, output_path, attempts, threshold):
    """XTTS sampling sometimes babbles, swallows words or trails off: synthesize
    several takes, transcribe each with Whisper and keep the most faithful one."""
    spoken = tts_text(text, lang)
    best = (-1.0, None)
    for attempt in range(attempts):
        wav = tts.tts(spoken, speaker_wav="./build/sample.mp3", language=lang, temperature=0.5, split_sentences=True)
        tmp = f"{output_path}.take.wav"
        tts.synthesizer.save_wav(wav, tmp)
        audio = librosa.resample(np.asarray(wav, dtype=np.float32), orig_sr=tts.synthesizer.output_sample_rate, target_sr=16000)
        segments, _ = whisper.transcribe(audio, language=lang, beam_size=5)
        heard = " ".join(s.text for s in segments).strip()
        score = max(similarity(text, heard), similarity(spoken, heard))
        logging.info(f"{output_path} take {attempt + 1}: {score:.2f} '{heard}'")
        if score > best[0]:
            best = (score, heard)
            os.replace(tmp, output_path)
        else:
            os.remove(tmp)
        if score >= threshold:
            break
    if best[0] < threshold:
        logging.warning(f"{output_path}: best take {best[0]:.2f} below {threshold}, listen to it: '{best[1]}'")


def main():
    parser = argparse.ArgumentParser(description="Generate audio files from a quotes JSON file.")
    parser.add_argument("--quotes-file", "-f", required=True, help="Path to the quote JSON file containing quotes.")
    parser.add_argument("--output-dir", "-o", required=True, help="Directory to save the generated audio files.")
    parser.add_argument("--clean", "-c", action="store_true", help="Clean the output directory and json file.")
    parser.add_argument("--only", nargs="*", default=[], help="Only (re)generate these soundpaths, e.g. fr/tu_es_heureux.wav.")
    parser.add_argument("--attempts", type=int, default=8, help="Maximum takes per quote.")
    parser.add_argument("--threshold", type=float, default=0.9, help="Whisper similarity accepting a take.")
    args = parser.parse_args()

    if not os.path.exists(args.quotes_file):
        raise FileNotFoundError(f"Quotes file {args.quotes_file} does not exist.")

    if not args.clean:
        global librosa, np
        import librosa
        import numpy as np
        import torch
        from faster_whisper import WhisperModel
        from TTS.api import TTS

        device = "cuda" if torch.cuda.is_available() else "cpu"
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        whisper = WhisperModel("small", device="cpu", compute_type="int8")

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

                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                generate(tts, whisper, text, lang, output_path, args.attempts, args.threshold)

            if args.clean:
                del quote["soundpaths"]

        f.seek(0)
        json.dump(quotes, f, indent=2, ensure_ascii=False)
        f.truncate()


if __name__ == "__main__":
    main()
