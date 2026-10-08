# Live Chord AI — Agent Rules

Rules for AI assistants working in this codebase to keep sessions efficient and within context limits.

## Project Files (Do Not Recreate)

| File | Purpose |
|------|---------|
| `app.py` | FastAPI server — single entry point, self-contained |
| `transformer_model.py` | Transformer architecture with math comments |
| `run_training.py` | Batched Chordonomicon training pipeline |
| `build_dataset.py` | Feature extraction only (deprecated, use run_training.py) |
| `train.py` | Standalone trainer (runs after build_dataset.py) |
| `static/index.html` | UI shell |
| `static/styles.css` | All styling including timeline + chord blocks |
| `static/script.js` | WebSocket, search, timeline playhead logic |

## Architecture Rules

- **Do NOT add new Python files** unless absolutely necessary — merge logic into existing files
- **Do NOT re-add deleted files**: CNN models (`.pkl`), training notebooks except `transformer_chord_recognition.ipynb`, `search_extract_chords.py`, `prep_transformer_data.py`
- `app.py` is the single server — no helper modules, no imports from deleted files
- The Transformer uses 24 chord classes: 12 major + 12 minor (no 7th, sus, aug, dim)

## Key Constants (must match across all files)

```python
SR              = 22050
HOP_LENGTH      = 512
SEQUENCE_LENGTH = 100   # frames per window
FEATURE_DIM     = 12    # chroma pitch classes
NUM_CHORD_CLASSES = 24
```

## Token Limit Rules

- **Always read existing file before editing** — never rewrite a file from scratch if it can be patched
- **Prefer multi_replace_file_content** over full rewrites for targeted edits
- **Do not re-explain** the full pipeline in every response — refer to this file
- **No Unicode box-drawing characters** in Python files — Windows codec errors (use ASCII `=`, `-`)
- When asked for a summary, keep it to the table + architecture section above

## Model State

- `transformer_chord_model.keras` — trained weights (may not exist yet until `run_training.py` completes)
- `app.py` gracefully falls back to Chroma template matching if model file is absent
- Training data: `X_dataset.npy` (N, 100, 12) and `y_dataset.npy` (N,)

## Common Commands

```bash
python app.py                           # start server
python run_training.py                  # synthetic training (~2-5 min, no downloads)
python run_training.py --samples 3000   # more data, slightly slower
python transformer_model.py <song.wav>  # test inference
```
