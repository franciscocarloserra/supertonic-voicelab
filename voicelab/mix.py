"""CLI: build a new voice pack from a base + sliders. Example:
  python -m voicelab.mix --base F1 --target M5 --t 0.75 --set gender=-1 mix_age=2 --out my_voice.json [--say "Hello" --wav out.wav]
Slider ranges validated per base are in vectors/limits.json (measured on F1/M1; '*' is the conservative fallback)."""
import argparse, json
from . import lib


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--base", required=True); a.add_argument("--target"); a.add_argument("--t", type=float, default=0.0)
    a.add_argument("--set", nargs="*", default=[], metavar="NAME=SCALE"); a.add_argument("--out", required=True)
    a.add_argument("--say"); a.add_argument("--wav"); a.add_argument("--lang", default=lib.PARAMS["sample_lang"])
    o = a.parse_args()
    sliders = {k: float(v) for k, v in (s.split("=") for s in o.set)}
    pack = lib.apply(o.base, sliders, o.target, o.t)
    lib.save_pack(pack, o.out, source=json.dumps({"base": o.base, "target": o.target, "t": o.t, "sliders": sliders}))
    print("wrote", o.out)
    if o.say:
        from supertonic import TTS
        tts = TTS(model_dir=lib.model_dir()); wav, _ = tts.synthesize(o.say, voice_style=tts.get_voice_style_from_path(o.out), lang=o.lang)
        tts.save_audio(wav, o.wav or o.out.replace(".json", ".wav")); print("wrote", o.wav or o.out.replace(".json", ".wav"))


if __name__ == "__main__": main()
