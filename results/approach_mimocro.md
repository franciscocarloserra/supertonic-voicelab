# Mimocro/supertonic-voice-cloning — review

Source: https://github.com/Mimocro/supertonic-voice-cloning (README, fetched 2026-09-03).

## What it does
Gradient-based **inversion**: given reference audio, optimize a Supertonic voice style (`style_ttl`, `style_dp`) so the synthesized output matches the reference. Replays the ONNX graphs as native PyTorch ops (`utils/onnx_torch.py`) so waveform-level losses backprop into the style tensors.

## Method
* Warm-start from a preset voice JSON; optimizes deltas `delta_ttl`, `delta_dp` **on the per-row normalized manifold** (matches our finding: rows are unit norm).
* Optimizer: Adam or Muon, up to 60k iterations, bf16 autocast, CUDA.
* Loss: ECAPA speaker-embedding cosine (identity) + soft-DTW log-mel vs reference + soft-DTW on vocoder latents + duration anchor to reference length + silence barrier + optional L2 prior.
* Inputs: reference wav (optional noisereduce / vocal extraction), Whisper for transcript, Supertonic ONNX weights, preset JSON.
* Scripts: `src/invert.py` (loop), `src/download_assets.py`, `src/synth_onnx.py`, `probe_bank.py` (64-phrase probe bank).

## Constraints
≥6 GB VRAM, batch ≥2 (reference + probe), CUDA only. Author calls it "half-sloppy … somehow works".

## Relation to this project
* Complementary: we do label-driven arithmetic (cheap, no reference audio); Mimocro does reference-driven optimization (expensive, arbitrary target).
* Reusable pieces: the differentiable ONNX→torch replay could give a **gradient on our vectors** (e.g. optimize a single scalar along `gender` towards a target speaker embedding) — the "directed optimization" path that kokoro STATUS lists as top open item.
* Confirms the row-normalization constraint independently.
