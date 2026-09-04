# axes/ — stages, findings, future strategies (2026-09-03/04)

Goal: usable, **labeled, bounded** sliders over Supertonic-3 voice packs, validated programmatically (WER 0 + officials' ranges + margins), exposed in the panel (7893). Only the user listens/judges. All knobs in `params.json`; every threshold derives from the officials' measured baseline (`sweep/calib.json`) + explicit margin.

## Stages (script → output)
| # | Stage | Script | Output | Result |
|---|---|---|---|---|
| 20 | ECAPA-gradient axes (Jacobian SVD in audible subspace) | `20_ecapa_grad.py` | `out/20_axes.npz` | 10 axes, unlabeled, break at scale 1–4 |
| 21/22 | Per-axis/per-base scale limits | `21_eval_axes.py`, `22_eval_known.py` | `out/21_*`, `out/22_*` | limits feed the panel |
| 30 | Age/gender/emotion classifier PoC (audeering) | `30_poc_classify.py` | `out/30_poc.*` | gender 10/10 correct, age 22–40, ADV 0.38–0.65 |
| 31 | Classifier-gradient vectors | `31_label_grad.py` | `vectors/lbl_*.npz` | adversarial: label moves, voice breaks at scale 1 |
| 32 | Audiobox-aesthetics PQ on officials | `32_poc_aesthetics.py` | `out/32_aes.*` | PQ 7.68–8.10 → validity floor min−1.0 |
| 40 | Extreme exploration of the safe space (noise/pair/scale/dp/combo/mix3) | `40_explore.py` | `out/40/{clips.jsonl,map.md,listen/}` | 305 clips, see findings |
| 41 | Pair table (a→b extrapolation limits) | `41_pair_table.py` | `out/41_pairs.*` | 47/48 pairs valid at t=1.5, many to t=12 |
| 43 | Vox-Profile voice-quality PoC | `43_poc_vox.py` | `out/43_vox.*` | only deep/silky/singsong/shrill/flowing/loud vary |
| 44 | 40 synthetic packs via sliders | `44_gen_packs.py` | `out/44/{packs,features.jsonl,listen}` | 40/44 valid in 88 s |
| 45 | Iterative label regression on mix weights | `45_refine.py` | `out/45/{data.jsonl,dirs_iter*.json}`, `vectors/mix_*.npz` | 560 pts, 6 usable labels |
| 46 | Label deltas along pairs | `46_pair_labels.py` | `out/46_pair_labels.*` | dominant label per pair |
| 47 | UTMOSv2 ranking + direction | `47_utmos.py` | `out/47_utmos.*`, `vectors/mix_utmos.npz` | 6 gens beat best official |
| 50 | Mimocro gradient inversion sanity (F1 ref from M1 init) | `refs/mimocro` (patched) | `out/50_inv/` | not recovered, see findings |
| — | Panel | `panel_server.py`, `panel.html` | 7893 | bases: officials, gens (ranked), inv_* |

## Findings
**Space structure**
* Rows individually inert; only global directions matter. Audible subspace rank 209/256. All-zero pack is a valid voice.
* WER alone is blind to ttl; loudness breaks first, then voiced, then WER via tail hallucination. Real intelligibility loss is rare.
* Officials' hull: mix3 100 % valid. Pairs extrapolate to t=1.5 (47/48), many to t=12 but saturate beyond t≈3–4 after renorm. Noise: safe sigma 0.1–0.3, sounds dirty (PQ 5.3). Global row scale: up ×1.5–2, down ÷3. dp random directions valid to scale ≥2.
* Combined sliders: 75 % of individual limit with 2–4 active, 50 % with 8.

**Sensors** (`sensors.py`, ~120 ms/clip; UTMOS +1.3 s)
* Classifier **gradients** are adversarial (age/male break voicing at scale 1). **Data-derived** directions work (mean F−M, pairs, regression on mix weights).
* Vox-Profile textures husky/raspy/fry/nasal are always 0 on this TTS: not addressable.
* Analysis audiocpp (7890) balloons VRAM over thousands of requests (14 GB); `guard_vram()` restarts it above `refine.acpp_vram_restart_mb`.

**Labeled sliders** (45, iter 5, R² / Δ per unit; measured limits in `out/22_*-172555`)
* age 0.48 / 4.66 y · arousal 0.50 / 0.066 · deep 0.70 / 2.99 logit · silky 0.59 / 1.88 · singsong 0.50 / 3.21 · shrill 0.48 / 2.64.
* Not usable (R² < 0.4): flowing, loud, PQ, valence, f0, male (as regression; `gender` mean-difference vector works instead). utmos R² 0.28, +0.25 MOS/unit.
* UTMOS: officials 2.58 (F2) … 3.40 (M5, F1); gens P23 3.63, P35 3.51, P12 3.51 above best official.

**Inversion (50)**: 1500 iters, 652 ms/iter, ECAPA cos to F1 0.14→0.70, but result stays M1-like: audeering male 1.0, f0 129 Hz (F1 190), pack row-cos to F1 dropped 0.949→0.909, 94 % M1 + 30 % off-hull residual in officials' weight space. Identity loss alone is fooled; consistent with classifier-gradient finding. Checkpoints loadable in panel as `inv_*`.

## Future strategies (ordered by cost/return)
1. **Constrained inversion** (~1 h): optimize 10 official weights + mix_* slider values against ECAPA + f0 + age + gender + PQ jointly, box = measured limits. Valid by construction, seconds per candidate. Answers "knobs from a reference waveform" within what the model can do.
2. **Real-voice reference** (30 min after 1): same against a short human wav; tells whether the officials' span approximates external identities or only interpolates.
3. **Mimocro with extra losses / other init** (30 min/run): add f0 + audeering gender terms, or init from F2/F3. Low return if 1 works.
4. **Reverse-direction pair limits** (one explorer iteration, 5 min): toward slider currently falls back to t≤1 for unmeasured b→a.
5. **Response curves for top-R² sliders** (20 min): label vs slider position per base; show expected value in panel.
6. Not started: mutual orthogonalization of mix_* vectors, prosodic f0-std features, Vox-Profile emotion heads, CLAP prompts, UTMOS as validity floor.
