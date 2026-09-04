# results/

Outputs and conclusions of the experiments that produced the voices and sliders (2026-09-02 → 04). Start with **STAGES.md** (stage table, findings, future strategies), then STATUS.md (chronological log).

| file | content |
|---|---|
| `STAGES.md` | stage table 20–50, findings on the style space, labeled slider quality (R²), UTMOS ranking, inversion result, future strategies |
| `STATUS.md` | chronological status: speed/gender vectors, harmonics + WER sweeps, inversion PoC (no-go), gradient axes |
| `AXES.md` | ECAPA-Jacobian axes pipeline, validity criterion, per-axis limits |
| `LESSONS.md`, `architecture.md`, `approach_mimocro.md` | notes on the model architecture and the inversion approach |
| `06_harmonics.md`, `07_whisper.md` | harmonics / Whisper WER sweeps over gender, speed, PCA scales |
| `20_grad.md`, `30_poc.md`, `31_labels.md`, `32_aes.md`, `41_pairs.md`, `42_regress.md`, `43_vox.md`, `45_refine_report.md`, `46_pair_labels.md`, `47_utmos.md` | per-stage reports |
| `41_pairs.json`, `47_utmos.json`, `44_features.jsonl` | raw: pair extrapolation limits, UTMOS ranking, per-pack features (f0, voiced, RMS, age, sex, PQ, Vox-Profile scores, recipe) |

Negative results worth knowing before extending: classifier-gradient directions are adversarial; single-row edits are inert; flow-matching-loss inversion from audio does not recover identity; textures husky/raspy/fry/nasal are not addressable in this TTS.
