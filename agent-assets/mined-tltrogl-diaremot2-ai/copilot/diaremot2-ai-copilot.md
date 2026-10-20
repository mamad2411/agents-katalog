# Copilot Instructions for DiaRemot AI Agents

## Project Overview
DiaRemot is a CPU-only, multi-stage speech intelligence pipeline for long-form audio (1–3 hours). It produces diarized transcripts with per-segment affect, emotion, intent, sound event, and paralinguistic analysis. All inference is CPU-only, ONNX-preferred, with PyTorch fallback.

## Architecture & Workflow
- **Pipeline:** 11 canonical stages (see `src/diaremot/pipeline/stages/__init__.py::PIPELINE_STAGES`). Each stage is modular and must not be skipped unless explicitly disabled.
- **Model Strategy:**
  - **ONNXRuntime** for all models (VAD, SED, embeddings, emotion, intent) is preferred.
  - **PyTorch fallback** for model inference if ONNX is missing (never for preprocessing).
  - **ASR:** CTranslate2 (faster-whisper tiny.en, int8 quantization).
  - **Paralinguistics:** Praat-Parselmouth (voice quality, prosody).
- **Preprocessing:** Only `librosa`, `scipy`, `numpy`, and `soundfile` are allowed. Never use PyTorch for preprocessing.
- **Outputs:**
  - Main: `diarized_transcript_with_emotion.csv` (39 columns, see `src/diaremot/pipeline/outputs.py::SEGMENT_COLUMNS`)
  - Others: `segments.jsonl`, `speakers_summary.csv`, `summary.html`, `speaker_registry.json`, etc.

## Key Conventions
- **Environment:**
  - All models must be loaded from `DIAREMOT_MODEL_DIR` (set via env var).
  - Use only CPU execution; never use GPU providers.
  - Required env vars: `DIAREMOT_MODEL_DIR`, `HF_HOME`, `HUGGINGFACE_HUB_CACHE`, `TRANSFORMERS_CACHE`, `TORCH_HOME`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `NUMEXPR_MAX_THREADS`, `TOKENIZERS_PARALLELISM=false`.
- **Model Integration:**
  - Always implement ONNX inference first; add PyTorch fallback for robustness.
  - If both are missing, log a warning and disable the stage gracefully.
  - Never break or rename CLI entry points (`python -m diaremot.cli`, etc.).
- **Testing & Verification:**
  - Use `ruff`, `pytest`, and `mypy` for linting, testing, and type checks.
  - Run full pipeline on sample audio (`python -m diaremot.cli run --input data/sample.wav --outdir outputs/`).
  - Never fabricate logs or results; only report what actually ran.
- **Schema:**
  - The 39-column CSV schema is contractually fixed. Do not change without a migration plan.
- **Adaptive VAD:**
  - VAD parameters are auto-tuned for soft speech (see README/AGENTS.md for values).

## Examples & References
- See `AGENTS.md` for detailed agent workflow and ONNX/PyTorch integration patterns.
- See `README.md` for install, environment, and CLI usage.
- See `src/diaremot/pipeline/outputs.py` for output schema.

## Patterns to Follow
- Prefer ONNXRuntime for all inference; fallback to PyTorch only if ONNX is missing.
- Use only `librosa`, `scipy`, `numpy` for audio preprocessing.
- Always validate ONNX outputs against reference PyTorch/HF implementations.
- Log and handle missing assets gracefully; never crash the pipeline.

---
For any uncertainty, cite the relevant file and propose a diagnostic test. Do not guess at API signatures or behaviors.
