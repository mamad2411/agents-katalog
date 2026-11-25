---
name: rekordbox-audio-analysis
description: Local ML audio analysis for a DJ library — discogs-effnet 1280-dim embeddings, mood/danceability heads, fast segment sampling, plain-TensorFlow inference. Use when audio features, embeddings, mood tags, or similarity are needed.
---

# Local audio analysis with MTG models

Hosted audio-features APIs are gone; local models are better anyway because you
keep the raw **1280-dim embedding**, which powers everything downstream
(clustering, similarity, Matching, visualization) without ever re-reading audio.

Reference implementation: `scripts/analyze_fast.py` (embeddings + mood) and
`scripts/essentia_features.py` (BPM/key). Models (free, from
https://essentia.upf.edu/models.html — don't redistribute, license is CC BY-NC-SA):
`discogs-effnet-bs64-1` + the `*-discogs-effnet-1` heads
(mood_happy/sad/aggressive/relaxed/party, danceability).

## Key engineering facts

- **You do not need the essentia C++ build for the ML models.** essentia has no
  arm64 pip wheel, and its TensorFlow linkage is broken on modern TF — but the
  models are ordinary TF graphs. `pip install tensorflow` runs them natively.
  You only need essentia's `TensorflowInputMusiCNN` mel frontend (or a faithful
  reimplementation) to match the expected input.
- **Decode is the bottleneck, not inference** (~1.8 s/track full-file). Sample
  **6 × 15-second segments spread 5%–90%** through the track (catches
  build-ups AND drops), decode with ffmpeg, average the outputs.
- Parallelize across performance cores; cap TF threads at 1/worker.
  Throughput ≈ 5.5 tracks/sec on an M1 Pro → a full library in under 80 min.
- **Store the embedding** as a float32 blob in SQLite alongside the head
  outputs. Tables: `embedding(rb_id, vec)` + `feature(rb_id, source, name, value)`.
- Audio files must be mounted (external drives!); metadata enrichment doesn't
  need them, audio analysis does.
- Incremental always: skip tracks that already have an embedding.

## Turning scores into tags

Check the DISTRIBUTION before tagging: several heads saturate (danceability,
party, RMS energy all ≈ 1.0 for electronic libraries — useless). The
well-spread ones were `mood_aggressive` and `mood_relaxed`.

- **Energy axis**: quartiles of mood_aggressive → warmup / groovy / driving / peak.
- **Vibe axis**: rule combos over heads (happy/chill/dark/euphoric/hypnotic/
  melancholic/feelgood) — see `scripts/ingest_tags.py` for thresholds.

## For custom genre vocabularies (future direction)

effnet's genre head is a fixed 400-style Discogs taxonomy. For arbitrary
DJ-vocabulary labels ("peak-time melodic techno"), use a CLAP-style zero-shot
model (e.g. LAION-CLAP) over the same stored audio/embeddings.
