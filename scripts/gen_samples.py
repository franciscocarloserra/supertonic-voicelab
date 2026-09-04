"""Render one sample per voice (officials + new-voices) with the official supertonic package. Text/lang/format in params.json."""
import subprocess, sys, io
from pathlib import Path
import soundfile as sf
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from voicelab import lib
from supertonic import TTS

P = lib.PARAMS; out = lib.ROOT / P["samples_dir"]; out.mkdir(parents=True, exist_ok=True)
tts = TTS(model_dir=lib.model_dir())
names = lib.official_names() + sorted(p.stem for p in (lib.ROOT / P["new_voices_dir"]).glob("*.json"))
for n in names:
    dst = out / f"{n}.{P['sample_format']}"
    if dst.exists(): continue
    path = (lib.ROOT / P["new_voices_dir"] / f"{n}.json") if n.startswith("P") else lib.official_dir() / f"{n}.json"
    wav, dur = tts.synthesize(P["sample_text"], voice_style=tts.get_voice_style_from_path(path), lang=P["sample_lang"])
    buf = io.BytesIO(); sf.write(buf, wav[0], tts.sample_rate, format="WAV", subtype="PCM_16")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", "pipe:0", "-b:a", P["sample_bitrate"], str(dst)], input=buf.getvalue(), check=True)
    print(n, round(float(dur[0]), 2), "s", flush=True)
