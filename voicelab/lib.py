import json, os, time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
PARAMS = json.load(open(ROOT / "params.json"))
LIMITS = json.load(open(ROOT / PARAMS["limits_file"]))


def model_dir():
    """Supertonic-3 model dir: env override > params.model_dir > supertonic package cache (auto-downloaded on first TTS())."""
    d = os.environ.get(PARAMS["model_dir_env"]) or PARAMS["model_dir"]
    if d: return Path(d)
    from supertonic.loader import get_cache_dir
    return get_cache_dir()


def official_dir():
    return Path(PARAMS["official_styles_dir"]) if PARAMS["official_styles_dir"] else model_dir() / "voice_styles"


def official_names():
    return sorted(p.stem for p in official_dir().glob("*.json"))


def load_pack(name_or_path):
    """'F1' -> official pack; 'P23' -> new-voices pack; anything ending in .json -> that file."""
    s = str(name_or_path)
    if s.endswith(".json"): p = Path(s)
    elif (ROOT / PARAMS["new_voices_dir"] / f"{s}.json").exists(): p = ROOT / PARAMS["new_voices_dir"] / f"{s}.json"
    else: p = official_dir() / f"{s}.json"
    d = json.load(open(p))
    return {"ttl": np.array(d["style_ttl"]["data"], dtype=np.float32),
            "dp": np.array(d["style_dp"]["data"], dtype=np.float32), "_raw": d}


def save_pack(pack, path, source="voicelab"):
    """Writes the pack in the native Supertonic voice_style JSON format (loadable by supertonic and audio.cpp)."""
    d = json.loads(json.dumps(load_pack(official_names()[0])["_raw"]))
    d["style_ttl"]["data"] = pack["ttl"].astype(np.float32).tolist()
    d["style_dp"]["data"] = pack["dp"].astype(np.float32).tolist()
    d["metadata"] = {"source_file": source, "extracted_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    json.dump(d, open(path, "w"))


def renorm(pack):
    """Native packs have every row (ttl 50x256, dp 8x16) at unit L2 norm. Re-project after arithmetic."""
    out = {}
    for k in ("ttl", "dp"):
        a = pack[k]; n = np.linalg.norm(a, axis=-1, keepdims=True); n[n == 0] = 1
        out[k] = (a / n).astype(np.float32)
    return out


def load_vec(name):
    z = np.load(ROOT / PARAMS["vectors_dir"] / f"{name}.npz"); return {"ttl": z["ttl"], "dp": z["dp"]}


def load_axes():
    return np.load(ROOT / PARAMS["vectors_dir"] / "gradient_axes.npz")["axes"]


def add(pack, vec, scale):
    return {"ttl": pack["ttl"] + scale * vec["ttl"], "dp": pack["dp"] + scale * vec["dp"]}


def morph(pack, target, t):
    """base + t*(target-base) on ttl (t>1 extrapolates); dp copied from target past the midpoint."""
    return {"ttl": pack["ttl"] + t * (target["ttl"] - pack["ttl"]), "dp": target["dp"].copy() if t >= 0.5 else pack["dp"].copy()}


def apply(base, sliders=None, target=None, t=0.0):
    """Recipe -> pack. sliders: {'gender': -1.5, 'mix_age': 2, 'ax3': -1, ...}."""
    pack = load_pack(base)
    if target and t: pack = morph(pack, load_pack(target), float(t))
    axes = None
    for n, s in (sliders or {}).items():
        if not s: continue
        if n.startswith("ax"):
            axes = load_axes() if axes is None else axes
            pack = {"ttl": pack["ttl"] + float(s) * axes[int(n[2:])][None], "dp": pack["dp"]}
        else:
            pack = add(pack, load_vec(n), float(s))
    return renorm(pack) if PARAMS["panel"]["renorm_rows"] else pack
