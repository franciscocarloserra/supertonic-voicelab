# STATUS (2026-09-03)

## Speed vector — CONFIRMED (objective)
`speed = mean(3 fastest) - mean(3 slowest)` by audio duration of the ES phrase. Fast set M3,F4,M4; slow set F1,M1,F3.
Duration for base 7.1s: scale -2 → 8.7s, -1 → 8.1s, +1 → 6.2s, +2 → 5.6s. Same for all 4 bases.
`speed_dp_only` gives identical durations → speed lives entirely in `style_dp`. Prefer `speed_dp_only` (leaves timbre untouched). Pending: user listens whether ±2 sounds natural vs. just using the `speed` request param.

## Gender vector — PENDING subjective eval
`gender = mean(F) - mean(M)` (norm ttl 1.54, dp 0.11). Projection separates classes cleanly (F: 0.27..0.70, M: -0.27..-0.92). Samples in `samples/02_gender/` at scales -2..+2 on F1,F5,M1,M2. Side effect: small duration drift (+2 → +2%).

## Next
* If gender is weak/noisy: PCA on the 10 packs, or per-row analysis (which of the 50 ttl rows carry gender).
* If a variant sounds good: `lib.save_pack(pack, '<dest>/<name>.json')` and add `voice_style_<name>` to the production spec.

## Harmonics (06) + Whisper WER (07) — 2026-09-03
* Whisper: 11/103 samples with WER>0.1, ALL in 04_combo at s≥+6 or g+6/g+10. Everything at |scale|≤4 (gender, speed, combos) and all PCA ±3 stays ≤0.1 WER (mostly 0).
* Speed +10/+100 destroys intelligibility (WER 0.5–0.9) — hard ceiling ~s+4 (≈4.5s for a 7s phrase, 1.55x). Beyond that, use request `speed`.
* Gender +10 alone: f0 med ~290Hz, voiced fraction drops 0.82→0.63, HNR still fine → timbre holds but voicing breaks (breathy). Gender ±2 keeps voiced/HNR; F5 even improves HNR (+2 → 12.5dB).
* `speed` (ttl+dp) at +2 drags f0 down to male range (F1 190→107Hz); `speed_dp_only` keeps f0 → always use dp-only for speed.
* Flatness > 0.13 == glitch flag (only s≥+6 samples); harm_band < 0.15 == breathy/noisy (M2, M1 base already low).
* Runtime: 06_harmonics ~1.5s/sample (pyin); 07 ~1s/sample with 2 workers.

## Context (2026-09-03)
Supertone discontinued Play / API / Voice Builder on 2026-08-31 (notice dated 2026-08-18); repo archived, no further model releases. Shift/Clear/Air moved to Antinode Audio. No hosted style encoder exists anymore → custom voices only via local inversion (see architecture.md, plan: FM-loss inversion with z1 from vocoder inversion or distilled latent encoder).

## Inversion PoC (inversion/, 2026-09-03, ~1h15 of 3h budget, GPU capped 2GB/~15% util) — NO-GO as designed
Pipeline: Mimocro OnnxModule replay (torch 2.11, local-tts venv). Scripts 10..15, outputs in inversion/out/, knobs in inversion/params.json.
* 10 torch==onnxruntime: PASS (max_abs ≤2e-3).
* 11 vocoder inversion (wav→latent from noise, multi-res STFT): FAIL, latent err 4.5×std. Without it there is no z1 for external audio.
* 12 effective subspace: rank 209/256 @99.9% energy. Minor.
* 13 single-utterance FM-loss inversion (F1 from its z1, warm F2): FAIL. FM 0.287 < true 0.391 but WER 1.28 (memorizes the latent), row_cos 0.94 < warm 0.956.
* 15 multi-utterance (4 phrases + holdout, lr 2e-3, prior 0.1): passes acceptance (WER 0) but row_cos 0.954 ≈ warm start; delta norm 0.53 → it is F2 with noise, not F1. f0 163 vs F1 190.
* Root cause: FM loss barely discriminates voices (F1 true 0.344 vs F2 0.365 on F1's own latents, 6%) while per-sample noise over (t,z0) is ±20%. Gradient toward identity is buried; low prior → memorization, high prior → no motion. Explains why Mimocro uses perceptual losses (ECAPA/mel) instead.
* What remains viable: vector arithmetic on the 10 official packs (validated), or perceptual-loss inversion à la Mimocro (slow, needs ECAPA + full sampling per step, and still needs z1 or a wav-domain loss).

## Sweep + gradient axes (2026-09-03, sweep/ and axes/)
* sweep/it0: multilingual WER baseline of the 10 officials (es 0, en 0, pt 0.125, fr 0.111; pt/fr misses are Whisper homophones). Calibration in sweep/calib.json: WER baseline, f0/voiced/RMS-dB/duration ranges per language.
* sweep/it2 (row break-map): every ttl row is inert alone -> per-row search abandoned.
* axes/20-22: 10 orthonormal identity axes from the ECAPA Jacobian, bounded per base/sign with the full baseline criterion; gender and speed bounded the same way. Dashboard on 7893. See axes/README.md.
* Open: axes/23 combined-slider budget (not run: pipeline too slow, pyin bottleneck). User has listened to nothing yet; the panel is the listening tool.
* Retraining the style encoder (paper: encoder trained jointly with text-to-latent, FM loss, 945 h / 2,576 speakers, 4x4090) estimated at 200-350 GPU-h (~100-500 USD cloud) + 3-5 weeks of work, no training code exists. Deferred until the axes approach is judged by ear.
