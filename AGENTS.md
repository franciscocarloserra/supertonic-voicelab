# AGENTS.md — Supertonic VoiceLab

Vector arithmetic over Supertonic-3 voice packs. Three audiences: agents that **use** the voices, agents that **run** the lab, agents that **continue the research**.

## 1. Use a voice
* Packs: `new-voices/P00..P39.json`, native `voice_style` format (`style_ttl` 1×50×256, `style_dp` 1×8×16, every row unit L2-norm). Load with `TTS().get_voice_style_from_path(path)` or copy into a runtime's `voice_styles/`.
* Metadata + recipe per pack: `new-voices/index.json` (sorted by `utmos`; fields `sex`, `age`, `PQ`, `base`, `target`, `t`, `sliders`, `sample`, `pack`). Human table: `new-voices/README.md`.
* Samples: `samples/en/<id>.mp3`, one sentence (`params.json[sample_text]`), officials F1..F5/M1..M5 included.

## 2. Run the lab
```bash
pip install -r requirements.txt            # supertonic numpy soundfile; ffmpeg for mp3
export VOICELAB_MODEL_DIR=/path/to/supertonic-3   # optional; default = supertonic package cache (auto-download)
python panel/server.py                     # http://localhost:7894  (port: params.json[panel][port])
python -m voicelab.mix --base F1 --target M5 --t 0.75 --set gender=-1 mix_age=2 --out v.json --say "hi"
python scripts/gen_samples.py              # regenerates samples/en (skips existing files)
python scripts/screenshot.py               # docs/screenshot.png via playwright (channel=chrome)
```
* Panel endpoints: `GET /` UI, `POST /render {base,target,t,sliders,text,lang}` → wav + waveform + mel, `POST /pack` → downloadable JSON, `POST /save {name,...}` → `new-voices/custom/<name>.json`.
* `voicelab.lib`: `load_pack(name|path)`, `save_pack`, `renorm`, `add(pack, vec, scale)`, `morph(pack, target, t)`, `apply(base, sliders, target, t)`, `load_vec(name)`, `load_axes()`.
* Slider names = keys of `vectors/limits.json[slider_limits]`: `gender`, `speed_dp_only`, `mix_age`, `mix_arousal`, `mix_deep`, `mix_silky`, `mix_singsong`, `mix_shrill`, plus `ax0..ax9` (unlabeled ECAPA-Jacobian axes in `vectors/gradient_axes.npz`).
* Limits are per base (`F1`, `M1`) with `*` as the conservative fallback; `[0,0]` = any move breaks that base. Pair morph: `pair_t_max["A>B"]` is the max valid t for A→B; reverse direction unmeasured → t ≤ 1.
* Signs: `gender` + = more female. `speed_dp_only` + = faster. `mix_*` + = more of the label.
* Combined sliders: budget ~75 % of each limit with 2–4 active, 50 % with 8 (`params.json[panel][random]`).
* Always `renorm` after arithmetic. `lib.apply` does it.

## 3. Continue the research
Start with `results/STAGES.md` (stage table, findings, future strategies), then `results/STATUS.md` (chronological), `results/AXES.md` (validity criterion). Raw: `results/*.json`, `results/44_features.jsonl`.

### What was done (do not re-derive)
| # | experiment | result | where |
|---|---|---|---|
| 01–04 | gender / speed mean-difference vectors, combos | both work; speed is dp-only; `speed`(ttl+dp) shifts f0 | STATUS.md, 06_harmonics.md |
| 05 | PCA on 10 packs, ±3 | intelligible, unlabeled | STATUS.md |
| 06–07 | harmonics (pyin, HNR, voiced) + Whisper WER grid | ceilings: gender ±2 clean, +10 breathy; speed +4 max | 06_harmonics.md, 07_whisper.md |
| 08–09 | slot attention / slot swap | no per-row identity | STATUS.md |
| 10–15 | inversion PoC (torch replay, vocoder inversion, FM-loss inversion, multi-utterance) | NO-GO; FM loss discriminates speakers by 6 % vs ±20 % noise | STATUS.md, approach_mimocro.md, architecture.md |
| sweep it0/it2 | multilingual WER baseline; per-row break map | calibration = officials' ranges; rows inert | AXES.md |
| 20–22 | ECAPA-Jacobian axes + per-axis/per-base limits | 10 axes, break at scale 1–4; limits in `vectors/limits.json` | 20_grad.md, AXES.md |
| 23 | combined-slider budget | 75 % / 50 % rule | STAGES.md |
| 30–31 | audeering classifier PoC; classifier-gradient vectors | classifier OK (sex 10/10); gradients adversarial | 30_poc.md, 31_labels.md |
| 32 | Audiobox-Aesthetics on officials | PQ 7.68–8.10 → validity floor | 32_aes.md |
| 40–41 | extreme exploration (305 clips); pair table | hull 100 % valid; 47/48 pairs to t 1.5 | 41_pairs.md |
| 42–46 | label regression on mix weights (5 iters, 560 pts); Vox-Profile probe; pair label deltas | 6 usable labels (R² ≥ 0.4); textures husky/raspy/fry/nasal unaddressable | 42_regress.md, 43_vox.md, 45_refine_report.md, 46_pair_labels.md |
| 44, 47 | 40 packs generated; UTMOSv2 ranking | 40/44 valid; 6 above best official | 47_utmos.md, 44_features.jsonl |
| 50 | Mimocro perceptual-loss inversion (F1 from M1 init, 1500 iters) | not recovered, 94 % M1 | STAGES.md |

### Established facts
* Rows individually inert; only global directions matter. Audible subspace rank 209/256. All-zero pack is a valid voice.
* Loudness breaks first, then voicing, then WER (via tail hallucination). WER alone is a blind judge.
* Data-derived directions work; classifier gradients do not. Speed lives in `style_dp`.
* Validity = WER ≤ per-language baseline, and f0 / voiced / RMS dB / duration inside the officials' range + margin, on two phrases. Thresholds always derive from the officials' measured baseline. Keep it that way.

### Next steps, in order of cost/return (from STAGES.md)
1. Constrained inversion: optimize 10 official weights + slider values against ECAPA + f0 + age + sex + PQ inside the measured box. Valid by construction, seconds per candidate.
2. Same against a short real human wav: tells whether the officials' span reaches external identities.
3. Reverse-direction pair limits (b→a currently capped at t ≤ 1).
4. Response curves per slider per base (expected label value shown in the panel).
5. Mutual orthogonalization of `mix_*`; prosodic f0-std features; UTMOS as validity floor.

### Rebuilding the sensor stack
Not in this repo: the experiment scripts, their venvs, the audio.cpp analysis server. To reproduce the judge you need: a Whisper HTTP endpoint, speechbrain ECAPA, audeering wav2vec2 age/sex/emotion, Vox-Profile, UTMOSv2, Audiobox-Aesthetics, pyworld (not librosa pyin: 70 % of wall time). Budget every run (`budget_s`) and restart the synthesis server above a VRAM threshold.

## Rules
* All numeric knobs in `params.json`. Measured data in `vectors/limits.json` and `new-voices/index.json`. No hardcoded thresholds.
* Do not regenerate `samples/en/` or `new-voices/P*.json` unless asked; they are the published artefacts. Custom packs go to `new-voices/custom/` (gitignored).
* English for code and docs. Keep the panel dark and minimal.
