---
name: abogen
description: "EPUB/PDF/teks → audiobook MP3 lokal dengan TTS (Kokoro/supertonic), sinkron caption. Web UI :8808, CLI, PyQt. | EN: audiobook text to speech tts epub pdf mp3 narration listen"
version: 1.0.0
category: creative-producer
lang: id
---

# AboGen — Text → Audiobook Lokal

## Jalankan
- `abogen-web` — web UI Flask di http://localhost:8808 (paling gampang)
- `abogen-cli` — mode CLI
- `abogen` / `abogen-pyqt` — TUI / GUI desktop

## Catatan
- TTS 100% lokal (Kokoro + supertonic + espeak) — tanpa API key, tanpa cloud.
- Input: EPUB, PDF (via pymupdf), TXT/Markdown. Output: MP3 + caption sinkron.
- Model TTS di-download saat pertama pakai (beberapa ratus MB, sekali saja).
- Alternatif TTS cepat tanpa model: `media-forge tts "teks" out.wav` (suara macOS).
