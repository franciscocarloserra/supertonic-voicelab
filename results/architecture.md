# Supertonic 3 architecture — style path (read from ONNX + tts.json, 2026-09-03)

Pipeline: text_ids → **duration_predictor** (style_dp) → **text_encoder** (style_ttl) → text_emb → **vector_estimator** (flow matching, N steps, style_ttl) → latent (144ch) → **vocoder** → wav 44.1k.

## style_ttl (1, 50, 256) = 50 Global-Style-Token VALUES
* Text encoder (`speech_prompted_text_encoder`, 2 cross-attn layers, 2 heads, 256 units):
  * query = text features (W_query 256x256)
  * **key = learned constant** `tts.ttl.style_encoder.style_token_layer.style_key` (1,50,256), tiled over batch (W_key 256x256)
  * **value = style_ttl** (W_value 256x256). This is the ONLY entry point of the voice pack.
* Vector estimator: 24 `main_blocks`; style cross-attn in blocks 5, 11, 17, 23 only. Same scheme: key = const style_key (concat with `uncond_masker.style_key_special_token` for classifier-free guidance), value = style_ttl (concat with `style_value_special_token`). Query from latent (W_query 512→256).
* Consequence: **attention weights over the 50 slots depend only on text/latent and the fixed keys, never on the pack.** Slot i has a fixed role; the pack only decides *what* is injected in that role. Rows are unit-norm because the (unreleased) style encoder produced them via attention pooling (`style_token_layer`: 50 prototypes, 2 heads, over a 6-layer ConvNeXt on 24-dim compressed mel chunks).
* style_ttl output of a voice = 50 × (256-d) pooled descriptors of the reference audio. No global speaker vector anywhere.

## style_dp (1, 8, 16) = 128-d flat conditioning
Reshape to (1,128), concat with text features → Gemm layers (MLP + convs). Pure duration prior → speed/rhythm only (confirmed: speed lives 100% in dp).

## Missing piece
`style_encoder` (mel → 50 tokens) weights are not in the public ONNX; only its config is in tts.json. Voice Builder (the hosted encoder) shut down 2026-08-31; repo archived. Cloning ⇒ inversion (Mimocro) or re-training a style encoder (no data).

## Paper confirmation (SupertonicTTS, arXiv 2503.23108, `refs/`)
* Reference encoder = NANSY++ *timbre token block*: linear(144→d) + 6 ConvNeXt + 2 attention layers; **50 learnable query vectors** attend over the reference latent → 50 "reference values" (= our `style_ttl` rows; d=128 in paper, 256 in Supertonic 3).
* **Reference key = 50 learnable vectors in the text encoder, reused as keys in the VF estimator** (matches `style_key` const in ONNX). Values = reference values. Text encoder: 2 cross-attn layers; VF estimator: RefCondBlock ×4.
* Reference encoder input is the **speech autoencoder latent** (24ch, temporally compressed ×6 → 144ch @ ~14Hz), not mel. The public ONNX ships only the latent *decoder* (vocoder). Latent encoder and reference encoder are not shipped.
* CFG: p_uncond=0.05, uncond conditions replaced by learnable params (`style_*_special_token`).
* Duration predictor: reference embedding = stack of 2 cross-attn pooling (our `style_dp` 8×16) concatenated with utterance-level text embedding → linear → scalar duration.
* Training data (paper, v1): LJSpeech, VCTK, Hi-Fi TTS, LibriTTS; 945h, 2576 EN speakers.
