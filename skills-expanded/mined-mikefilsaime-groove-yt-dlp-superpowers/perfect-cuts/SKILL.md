---
name: perfect-cuts
description: Turn a raw talking-head recording into a frame-perfect edited timeline - retakes removed, false starts caught, zero gap space. Drops a care package with Premiere/Resolve XML, MP4, EDL, SRT, Remotion launcher files, and a cut log. Use when the user drops a raw clip and asks to "perfect cut this", "clean cut this", "gling this", "cut the retakes out", "rough cut this footage", or invokes /perfect-cuts.
---

# Perfect Cuts

Gling-killer: transcript decides **which take wins**, waveform decides **the exact frame to cut**. One run drops a care package with every useful format — minimal decisions for the user.

Proven on real footage 2026-06-10 (v1→v5 iteration). The locked rules were learned from frames the user flagged — don't soften them.

## The three locked rules (the product — never soften these)

1. **Hard threshold in, soft threshold out.** Clip START = first frame voice crosses **-30dB** (breaths and mouth noise live below it — a -38dB start grabs the inhale and reads as 2-4 dead frames; the user flagged exactly this). Clip END = where speech drops below **-38dB** (word tails are quiet; -30dB clips them). These exact values are frame-verified on reference footage and are ALWAYS tried first; the script falls back to per-clip calibration only if they produce a degenerate map (it says so when it happens).
2. **Zero pad in, one frame out.** in_frame = `floor(onset × fps)` — no safety pad; 0.12s of "safety" pad was flagged as "2-4 frames too long." out_frame = `ceil(end × fps) + 1`.
3. **Intra-sentence silence ≥ 0.25s = suspect false start.** Whisper MERGES restarts into one clean sentence (it deduplicates the repeated words), so the transcript alone hides them. The speech map splits blocks at ≥0.25s silences — when one "sentence" spans two blocks, assume the first block is an aborted attempt unless its text clearly continues into the next. Prefer the later attempt.

## Workflow

### 0. Setup check (run silently before anything)

```bash
which ffmpeg ffprobe || echo MISSING-FFMPEG
ls "$HOME/GitHub/Marketing Assets and Skills/.venv-whisperx/bin/whisperx" 2>/dev/null || \
ls "$HOME/Library/Python/3.9/bin/whisperx" 2>/dev/null || \
ls ~/.buttercut/venv/bin/whisperx 2>/dev/null || \
ls ~/.perfect-cuts/venv/bin/whisperx 2>/dev/null || \
which whisperx || echo MISSING-WHISPERX
```

Set `$WHISPERX` to whichever binary was found. If anything is missing, tell the user what's needed and offer to install (consent first — it's ~3GB):

- **ffmpeg** (any standard build): macOS `brew install ffmpeg` · Windows `winget install ffmpeg` · Linux distro package.
- **WhisperX** — needs Python 3.10–3.12 (NOT 3.13+; whisperx 3.4.2 won't resolve):
  ```bash
  # macOS (Windows: install Python 3.12 from python.org or `winget install Python.Python.3.12`,
  # then use %USERPROFILE%\.perfect-cuts\venv and venv\Scripts\ paths)
  brew install python@3.12        # if no 3.10-3.12 present
  python3.12 -m venv ~/.perfect-cuts/venv
  ~/.perfect-cuts/venv/bin/pip install 'whisperx==3.4.2' 'pyannote-audio==3.4.0' 'torch==2.8.0' 'torchaudio==2.8.0'
  ```
  Versions are PINNED — a known-good combo. torch ≥2.9 breaks pyannote (torchaudio dropped `AudioMetaData`); pyannote ≥4 breaks whisperx 3.4.2 (`use_auth_token` removed). Never let pip upgrade them.

### 1. Intake — ONE AskUserQuestion call, then no more questions

Required: **the clip path** (usually arrives with the request; include in the call only if missing).

- **Q1 — Script:** "Did you film from a script?" → **Exact script** (paste it or give a path) / **Rough script** (wrote one, ad-libbed wording) / **Freestyled** (no script).
- **Q2 — MP4:** "Include a rendered MP4 in the package?" → **Yes (default)** / **No, timeline files only**. (The MP4 is the only large/slow artifact — everything else is KB-sized and always included.)
- **Q3 — Save location:** "Where should the package go?" → **Downloads (default)** / **Next to the source clip** / custom.

That's the whole interview. Language is auto-detected by WhisperX. Thresholds are auto-calibrated. No filler-word removal — surgically cutting "ums" mid-flow forces jump cuts that damage more than they fix; retakes and false starts already catch the garbage.

### 2. Transcribe

```bash
TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1 "$WHISPERX" "<video>" \
  --model small --language en --compute_type float32 --device cpu \
  --output_format json --output_dir /tmp/perfect-cuts
```

- Env var required (torch ≥2.6 weights_only default breaks pyannote's VAD load).
- `--compute_type float32` required on CPU.
- Always quote paths — OBS filenames contain spaces.
- `--language en` is the DEFAULT — never omit it for auto-detect; mis-detection silently produces a garbage transcript and every cut decision inherits it. Only change the code if the user says the footage isn't English.
- ~1 min per 2 min of footage; if clip >5 min, run in background and say so.
- Output: `/tmp/perfect-cuts/<stem>.json`.

### 3. Build the speech map

```bash
python3 "<skill dir>/scripts/speech_map.py" "<video>" "/tmp/perfect-cuts/<stem>.json" --out /tmp/perfect-cuts/map.json
```

(`<skill dir>` = the folder containing this SKILL.md — shown in the skill invocation context. All `scripts/` references in this file are relative to it; never assume an install location.)

The script ALWAYS tries the locked -30dB/-38dB first — the first printed line confirms which thresholds were used. Only if the locked values produce a degenerate map (one giant block, or speech shredded into confetti — bad mic, untreated room) does it fall back to measuring the speaker's level and deriving thresholds, and it announces that loudly. If you see the rescue-calibration line, tell the user their audio is unusual and the cut deserves extra scrutiny.

Sanity-check the printed blocks: they should read like sentences with believable boundaries. If they don't, investigate (music bed, two speakers, clipped audio) before cutting — never push a suspicious map through the editorial pass.

### 4. Editorial pass (the judgment step — this is yours)

**This step IS the product.** Everything before it is plumbing and everything after it is packaging — if time or attention is constrained, it comes out of the packaging, never out of this pass. Work the block list line by line; do not skim.

Read the block list and decide which blocks survive:

- **Retakes** (same/near-same line repeated): keep ONE. Default to the LAST take — but if an earlier take flows grammatically into the following content, that one wins. Read the words, don't count takes.
- **False starts**: drop the fragment, keep the complete delivery.
- **Mid-sentence restarts**: cut at the restart point — the block boundary is already there.
- **Sound checks, throat clears, dead air, direction-to-camera ("okay let me redo that")**: drop.
- **Merging blocks:** consecutive blocks with `gap_after` < 0.6s forming one continuous thought may merge into a single clip (first block's onset → last block's end). When in doubt, keep separate clips.
- **Whisper merge trap (rule 3):** transcript sentence spans two blocks → first block is probably an aborted attempt.

**With a script (exact or rough):**
- Match blocks to script lines — the script is the intent; takes are attempts at it. Keep the take closest to the script (exact mode) or the latest fluent take (rough mode).
- Fix Whisper mishears in clip `text` using script wording (never edit the whisper JSON — it's the timing source of truth).
- **Coverage check:** any script line with NO matching block = never cleanly delivered. Flag prominently — that's a reshoot warning, most valuable BEFORE the set is torn down.
- Script order wins when takes were filmed out of order.

### 5. Compute frames + build cuts.json

`/tmp/perfect-cuts/cuts.json`:

```json
{
  "source": "<abs video path>", "fps": <map>, "width": ..., "height": ...,
  "samplerate": ..., "source_duration": <map>,
  "sequence_name": "<stem> perfect cut",
  "output": "<set per exporter>",
  "clips": [{"in_frame": floor(onset*fps), "out_frame": ceil(end*fps)+1, "text": "<spoken words>"}, ...]
}
```

Use each kept block's `onset` (NOT `start`) for in, `end` for out. Always include `text` (script-corrected if available) — SRT and the preview player need it.

### 6. Drop the care package

Create `<save location>/<stem> perfect cut (C)/`. Filenames are purpose-first and numbered by importance — a non-technical user should know what each file is for without opening it:

| File in package | Tool | |
|---|---|---|
| `README (C).txt` | you write it (template: `scripts/readme_template.txt`) | Explains every file in plain words. Fill in nothing — it's generic. |
| `1 WATCH - final video (C).mp4` | `render_mp4.py cuts.json <out>` | Only if user said yes. Frame-accurate single-pass re-encode. |
| `2 EDIT - Premiere + Resolve (C).xml` | `export_fcp7.py cuts.json` | Premiere: File→Import. Resolve: File→Import Timeline. |
| `3 REVIVE - cut decisions (C).csv` | you write it (format below) | The revival sheet. |
| `4 OPEN IN REMOTION - Mac (C).command` | `cp scripts/open-in-remotion-mac.command` + `chmod +x` | Double-click → Remotion Studio. |
| `5 OPEN IN REMOTION - Windows (C).bat` | `cp scripts/open-in-remotion-windows.bat` | Same, for Windows. Ship BOTH — packages migrate across machines. |
| `6 CAPTIONS (C).srt` | `export_srt.py cuts.json <out>` | Captions on the EDITED timeline. Pairs with the MP4 for CapCut. |
| `7 AVID + LEGACY (C).edl` | `export_edl.py cuts.json <out>` | CMX3600. |
| `cut data (C).json` | copy cuts.json from /tmp | Machine-readable cut points — powers the Remotion launchers + automation. |
| `_remotion-launcher (C).mjs` | `cp scripts/_remotion-launcher.mjs` | Shared engine behind both launchers. Self-contained: embeds the whole Remotion project template, needs only Node on the target machine — works even where the skill isn't installed. Falls back to a video dropped into the package folder when the original source path is gone. |

No HTML preview — browser video seeking can't be gapless, and a preview with gaps undermines the product (removed 2026-06-12 after the user saw stutter; the MP4 is the preview). CapCut has no timeline-import format; CapCut users use the MP4 + SRT (say so matter-of-factly if asked).

When the package is complete, **open the folder for the user**: `open "<package dir>"` (macOS).

**Cut log format** — every block, kept AND cut, with the reason:

```csv
block,status,source_in,source_out,timeline_position,text,reason
6,KEPT,00:00:16:11,00:00:19:14,1,"Canada has joined the AI arms race,",take 4 of 4 — flows into next line
2,CUT,00:00:05:04,00:00:07:18,,"Canada just joined the AI arms race.",retake 1 of 4
26,CUT,00:01:28:07,00:01:29:06,,"and that $200",false start — restarted at block 27
```

Timecodes at source fps. Any cut line can be revived — "revive block 26" re-inserts it at its natural position: edit cuts.json, re-run the exporters into the same folder. Never redo transcription.

### 7. Report

- Package path (folder is already open on their screen), raw → edited duration.
- **Lead with the MP4:** "watch `1 WATCH - final video` first."
- What was cut, one tight list: retakes ×N, false starts ×N, dead air total.
- **Script coverage warnings first** if any line never got a clean take.
- Point at `3 REVIVE - cut decisions (C).csv` for revivals.
- If the user flags a wrong cut: fix that single block decision in cuts.json and re-run exporters. Never redo the pipeline.

## Sharp edges (learned the hard way)

- `ffmpeg` inside a shell `while read` loop eats stdin — always `-nostdin`.
- Never stream-copy (`-c copy`) concat of separately encoded segments — timestamps glitch, frames freeze. `render_mp4.py` does it right (single filter_complex, one re-encode).
- Source fps comes from ffprobe — never assume 30. NTSC rates (23.976/29.97/59.94) are handled by the exporter; all frame math uses the real rate.
- Whisper word timestamps are fine for WHICH words exist, unreliable (±0.3s, pads ends) for WHERE to cut. Never cut on Whisper times.
- Whisper merges restarted sentences — the waveform blocks are the truth about how speech actually flowed.
- The XML, EDL, and Remotion launchers all reference the ORIGINAL source clip — if the user moves or renames it, those break (the launcher's fallback: drop the raw clip into the package folder). The MP4 is the only standalone-forever artifact; the README says all this.
- No browser-based preview, ever — HTML5 video seeking has per-seek latency, so segment-skip playback always stutters at cut points. It was tried and removed; don't re-add it.
