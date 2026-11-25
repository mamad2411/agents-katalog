---
name: music-to-sheet
description: Convert a local MP3/WAV/FLAC/M4A/OGG song into timestamped chord notation and a quantized five-line percussion staff, render both as a responsive HTML report, and optionally publish it. Exports MusicXML, SVG, PDF, and MIDI. Use when the user asks for 音樂轉譜、音樂轉和弦、和弦譜、五線鼓譜、鼓譜、audio-to-chords, audio-to-drums, sheet HTML, or wants a song transcription uploaded as a web page.
compatibility: Linux host with the local music-transcriber systemd service, Docker, ffmpeg, curl, Python 3, Verovio, and Chrome/Chromium.
allowed-tools: bash read write
---

# Music to Sheet

Convert audio with the locally deployed models and create a shareable HTML score:

- Chords: Omnizart `chord_v1`
- Drums: ADTOF-PyTorch five-class model
- Engraving: MusicXML 4.0 rendered by open-source Verovio
- Output: chord timeline, five-line percussion staff, MusicXML/SVG/PDF/MIDI, JSON/CSV, and optional audio player

## Standard workflow

1. Confirm the input audio exists.
2. Choose a descriptive title. Preserve the user's supplied title verbatim.
3. Choose BPM:
   - Use a BPM supplied by the user or reliable metadata.
   - Otherwise use `95` as the renderer fallback and state that the grid tempo is estimated.
   - Never present quantization as exact if BPM has not been independently verified.
4. Run:

```bash
./scripts/music-to-sheet.sh /absolute/path/song.mp3 /absolute/path/output \
  --title "Song title" --bpm 95
```

5. Verify `index.html`, `drum-score.musicxml`, `drum-score.pdf`, `drum-score/page-01.svg`, `chords.json`, `chords.mid`, `drums.json`, and `drums.mid` exist and are non-empty.
6. Inspect the HTML locally before publishing. At minimum, confirm the title, chord timeline, five-line percussion staff, MusicXML/PDF/MIDI links, mobile viewport, and AI-transcription disclaimer render.
7. Publish only when requested:

```bash
./scripts/music-to-sheet.sh /absolute/path/song.mp3 /absolute/path/output \
  --title "Song title" --bpm 95 --upload
```

The upload uses the `upload-html` skill's timestamped path by default, preserving previous reports.

## Existing transcription artifacts

If models have already produced `chords.json` and `drums.json`, avoid rerunning inference:

```bash
python3 ./scripts/generate_drum_score.py \
  --drums /path/site/drums.json --output /path/site/drum-score.musicxml \
  --title "Song title" --bpm 95 --duration 120

/home/chihmin/src/music-transcriber/.venv-adtof/bin/python ./scripts/render_drum_score.py \
  --musicxml /path/site/drum-score.musicxml \
  --output-dir /path/site/drum-score --pdf /path/site/drum-score.pdf

python3 ./scripts/render_sheet.py \
  --chords /path/site/chords.json --drums /path/site/drums.json \
  --output /path/site/index.html --title "Song title" --bpm 95 \
  --audio-relative song.mp3
```

Copy the referenced audio and MIDI files beside `index.html` before upload.

## Verification

```bash
/home/chihmin/src/music-transcriber/.venv-adtof/bin/pytest -q tests/test_render_sheet.py
curl -fsS http://127.0.0.1:8789/health
```

Expected health status: `ready` with `omnizart-chord-v1` and `adtof-pytorch`.

## Interpretation guardrails

- These are model estimates, not human-verified engravings.
- ADTOF detects kick, snare, hi-hat, tom, and cymbal classes; it does not infer sticking or limbs.
- Synthetic percussion may be confused with other transient sounds.
- Omnizart may simplify extensions, inversions, slash chords, or altered harmony.
- The five-line score snaps detected events to the closest 16th note at the selected BPM.
- Cymbals and hi-hats use x noteheads; kick, snare, and tom use normal noteheads at conventional staff positions.
- MusicXML is the editable source; SVG and PDF are Verovio engravings generated from it.
- Always retain the disclaimer in generated HTML.
