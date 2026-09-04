# Lessons (2026-09-03) — what the day bought, what it did not

## Learned (verified, reusable)
1. Voice pack anatomy: `style_ttl` = 50 unit-norm rows consumed only as cross-attention VALUES against fixed learned keys; `style_dp` = 128-d duration prior. Roles per slot are fixed by the model, not by the pack. (architecture.md)
2. Vector arithmetic works and is safe inside |scale| ≤ 4 with per-row renorm. Gender (mean F − mean M) shifts f0 without breaking voicing; speed lives 100% in `style_dp` (use `speed_dp_only`). Whisper WER + flatness/voiced/HNR are a sufficient automatic acceptance test. (STATUS.md, 06/07)
3. Row-cosine to an official pack is NOT a quality signal: 0.94 can be unintelligible and 0.954 can be a different voice. Only synthesis + Whisper + acoustic metrics decide.
4. FM-loss inversion is a dead end for identity: F1-true vs F2 differ 6% on F1's own latents, per-sample noise ±20%. Low prior memorizes, high prior stalls. Any inversion needs a perceptual identity metric in the loop (speaker embedding), i.e. full synthesis per step. Saved ~3 days of building the "elegant" pipeline.
5. Vocoder is not invertible by naive gradient from noise; external audio has no route to z1 without a latent encoder. This, not the optimizer, is the real blocker for cloning on Supertonic 3.
6. Infra that stays: dedicated audiocpp_server on 7890 with hot-reload slots X0..X9 (no restart to try a pack), panel 7891, torch replay of the 4 ONNX graphs validated to 2e-3.

## Not learned / open
* Whether gender ±2 sounds good (needs user ear; samples in samples/02_gender).
* Semantics of PCA components 2..4 and per-slot roles (09_slot_swap written, not run).
* Whether CMA-ES over PCA coords with ECAPA objective + Whisper barrier reaches a target voice (next experiment if cloning is still wanted; needs a speaker encoder installed).

## Verdict
Not wasted: the arithmetic path is production-usable today and the inversion path was falsified in 1h15 of GPU instead of days. The over-built part was the inversion scaffolding (10-15), kept for reference only.
