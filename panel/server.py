"""Slider panel. GET / -> UI; POST /render {base,target,t,sliders,text,lang} -> wav; POST /save {name,...} -> new-voices/custom/<name>.json.
Backend: the official `supertonic` package (CPU/ONNX). Knobs: params.json[panel]."""
import json, sys, io, base64
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np, soundfile as sf
from voicelab import lib
from supertonic import TTS

HERE = Path(__file__).resolve().parent; P = lib.PARAMS; PN = P["panel"]
tts = TTS(model_dir=lib.model_dir())
NEW = sorted(p.stem for p in (lib.ROOT / P["new_voices_dir"]).glob("*.json"))
RANK = {r["id"]: r for r in json.load(open(lib.ROOT / "results" / "47_utmos.json"))} if (lib.ROOT / "results" / "47_utmos.json").exists() else {}
RECIPE = {json.loads(l)["id"]: json.loads(l) for l in open(lib.ROOT / "results" / "44_features.jsonl")} if (lib.ROOT / "results" / "44_features.jsonl").exists() else {}
def mel_db(w, sr, sp):
    """numpy mel spectrogram in dB relative to the clip max, mels x frames. No librosa dependency."""
    n, h = sp["n_fft"], sp["hop"]; win = np.hanning(n).astype(np.float32); pad = np.pad(w, n // 2)
    frames = np.lib.stride_tricks.sliding_window_view(pad, n)[::h] * win; S = np.abs(np.fft.rfft(frames, axis=1)) ** 2
    mel = lambda f: 2595 * np.log10(1 + f / 700); imel = lambda m: 700 * (10 ** (m / 2595) - 1)
    pts = imel(np.linspace(mel(0), mel(sp["fmax_hz"]), sp["n_mels"] + 2)); freqs = np.fft.rfftfreq(n, 1 / sr)
    lo, c, hi = pts[:-2, None], pts[1:-1, None], pts[2:, None]
    fb = np.maximum(0, np.minimum((freqs - lo) / (c - lo), (hi - freqs) / (hi - c))).astype(np.float32)
    m = 10 * np.log10(np.maximum(S @ fb.T, 1e-10)); return (m - m.max()).T
def cfg():
    return {"officials": lib.official_names(), "new": [{"id": n, "utmos": RANK.get(n, {}).get("utmos"), "age": RANK.get(n, {}).get("age"), "origin": RECIPE.get(n, {}).get("base")} for n in NEW],
            "sliders": list(lib.LIMITS["slider_limits"]), "limits": lib.LIMITS["slider_limits"], "axes": P["gradient_axes"], "pairs": lib.LIMITS["pair_t_max"], "random": PN["random"],
            "text": P["sample_text"], "lang": P["sample_lang"], **{k: PN[k] for k in ("slider_step", "debounce_ms", "pair_step", "default_base")}}
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        html = open(HERE / "panel.html").read().replace("__CFG__", json.dumps(cfg()))
        self.send_response(200); self.send_header("content-type", "text/html"); self.end_headers(); self.wfile.write(html.encode())
    def do_POST(self):
        q = json.loads(self.rfile.read(int(self.headers["content-length"])))
        pack = lib.apply(q["base"], q.get("sliders"), q.get("target"), q.get("t", 0))
        if self.path == "/pack":
            tmp = HERE / ".render.json"; lib.save_pack(pack, tmp, source=json.dumps(q)); body = open(tmp, "rb").read()
            self.send_response(200); self.send_header("content-type", "application/json"); self.send_header("content-disposition", f"attachment; filename={q.get('name') or 'voice'}.json"); self.end_headers(); self.wfile.write(body); return
        if self.path == "/save":
            dst = lib.ROOT / P["new_voices_dir"] / "custom" / f"{q['name']}.json"; lib.save_pack(pack, dst, source=json.dumps(q)); body = json.dumps({"path": str(dst.relative_to(lib.ROOT))}).encode()
        else:
            tmp = HERE / ".render.json"; lib.save_pack(pack, tmp)
            wav, dur = tts.synthesize(q["text"], voice_style=tts.get_voice_style_from_path(tmp), lang=q["lang"]); w = wav[0].astype(np.float32)
            buf = io.BytesIO(); sf.write(buf, w, tts.sample_rate, format="WAV", subtype="PCM_16")
            n = PN["wave_px"]; seg = np.array_split(w, n); wave = np.stack([[s.min() for s in seg], [s.max() for s in seg]], 1).ravel()
            sp = PN["spec"]; m = mel_db(w, tts.sample_rate, sp)
            spec = np.clip((m - sp["db_floor"]) / (sp["db_ceil"] - sp["db_floor"]), 0, 1).T  # frames x mels
            body = json.dumps({"spec": (spec * 255).astype(np.uint8).tobytes().hex(), "spec_shape": list(spec.shape), "wav": base64.b64encode(buf.getvalue()).decode(), "dur_s": float(dur[0]), "rms_db": round(20 * float(np.log10(np.sqrt((w ** 2).mean()) + 1e-9)), 1), "wave": (np.clip(wave * 127, -127, 127).astype(np.int8).tobytes().hex())}).encode()
        self.send_response(200); self.send_header("content-type", "application/json"); self.end_headers(); self.wfile.write(body)
if __name__ == "__main__":
    print(f"panel http://localhost:{PN['port']}"); HTTPServer(("127.0.0.1", PN["port"]), H).serve_forever()
