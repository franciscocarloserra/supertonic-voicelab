# axes/ — gradient-derived voice axes + bounded dashboard (2026-09-03)

Status, full stage table, findings and future strategies: `STAGES.md` (2026-09-04). This file keeps the early (20–23) notes.

Goal: new, independent "mixing dimensions" for Supertonic-3 voice packs, each bounded to a range that does not break the baseline. Random search is the floor, not the method.

## Pipeline (numbered, each writes out/<NN>_*)
* `20_ecapa_grad.py` — Jacobian sketch: torch replay (inversion/inv_lib) -> 8 VF steps -> vocoder -> ECAPA embedding; backprop 16 random projections per (base, phrase, seed); SVD of all gradients in the W_value subspace (inversion/out/12_subspace.pt, rank 209). Out: `out/20_axes.npz` (10 orthonormal axes, 50x256 each), `20_grad.md`. 60 s.
* `21_eval_axes.py` — per axis and base and sign, scale grid [1,2,4,8,16], stop at first invalid. Score = ECAPA cos-distance at max valid scale. 10 random subspace directions as control. Renders ogg of the extremes. Latest completed: `out/21_20260903-125949` (axes complete, random controls partial).
* `22_eval_known.py` — same for the label-derived vectors `gender` and `speed_dp_only`. Latest: `out/22_20260903-125654`.
* `23_combined.py` — random combos of k sliders at fraction f of their own limit; valid% by (k,f), budget rule. NOT RUN yet (too slow, see perf).
* `panel_server.py` + `panel.html` — dashboard on 7893 (params.panel). One slider per axis + gender + speed_dp_only, range = per-base/per-sign max valid scale from the latest completed 21 and 22. Live render on slider move, save pack to `out/saved/`. Uses slot X9 only (runs use X0..X8).

## Validity criterion (sweep/sweeplib.validate, all thresholds from sweep/calib.json = 10 officials measured in sweep it0, widened by params.json[*].valid.margins)
WER <= per-language baseline (es: 0) | f0 inside officials' range +-15% | voiced >= officials' min - 0.05 | RMS dB inside officials' range +-3 dB | duration inside officials' per-phrase range +-15%. Must pass on BOTH phrases (sweep 3.5 s, final 7 s).

## Findings
* WER alone is blind to ttl: all-zero ttl still transcribes perfectly; only dp (speed) and absurd ttl scales break WER. Loudness, voiced and f0 are what bound timbre sliders.
* Single-row edits are inert (every one of the 50 rows rotated 90 deg: no change in WER, f0, voiced). Identity is distributed; only global directions matter.
* Gradient axes move ECAPA identity ~5x more per unit scale than random directions (scale 1: 0.26 vs 0.05) and f0 ~10x more, but hit the validity boundary at scale ~1-4 where random survives to 8-16. At the boundary both saturate (ECAPA 0.5-0.8).
* Identity-carrying rows: 28, 2, 23, 37, 49, 15, 17, 18. Not the high-attention rows of 08 (17, 25, 12, 20, 34).
* Recalibrated limits (full criterion, F1/M1): ax0 unusable (breaks at scale 1 both signs); others 1-2, a few reach 4 (ax2+, ax3-, ax8-). gender -4..+1 (f0 range caps +, loudness caps -). speed_dp_only -1..+2 (duration range).
* Loudness drifts strongly with gender (+2 -> -28.6 dB, -4 -> -20.5 dB vs officials -26.4..-23.1).

## Perf (measured) — fix before any further run
0.4 clips/s. Per candidate: 3 synth (0.1 s each), 2 Whisper (0.4 s each), 2 pyin (1.5 s + 3 s). pyin = ~70% of wall time. TODO: replace librosa.pyin with a fast f0 (pyworld, or pyin with frame 1024 / resolution 0.2), add `budget_s` per run with clean partial summary, and run a 20-clip perf probe before every sweep. Do not launch 23 before this.

## Env
`axes/venv` inherits torch from local-tts venv via .pth, adds speechbrain + torchaudio. ECAPA weights in `axes/ecapa_model`. Needs the analysis audiocpp server on 7890 (../start_server.sh) and Whisper on 6969.
