---
name: agentic-video-editing
description: Use when building FOSS video-editing MCP servers.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [video, mcp, ffmpeg, whisper, otio, editing, agentic, nle]
    triggers:
      - video editing mcp
      - selects mcp
      - agentic editing
      - multicam sync
      - filler removal
      - transcription pipeline
      - video search
      - premiere export
      - davinci resolve
    related_skills: [building-mcp-servers, voice-memo-transcription, youtube]
---

# Agentic Video Editing (FOSS stack)

Build local-first, agent-controllable video editing tools — the open-source
answer to commercial products like Cutback's Selects MCP. Reference
implementation: `pmb2/open-selects-mcp` (private, MIT).

## Capability → library map

| Capability | FOSS library | Notes |
|---|---|---|
| Transcription + word timestamps | faster-whisper | `word_timestamps=True, vad_filter=True`; words drive all cutting |
| Speaker diarization | pyannote.audio 3.1 | gated HF model needs token; community path works; overlay onto segments by max overlap |
| Scene detection | PySceneDetect | PyPI name is **`scenedetect`**, NOT `pyscenedetect` |
| Visual search | open_clip ViT-B/32 (laion2b) | frame sampling at ~0.5fps, cosine over stored embeddings |
| Transcript search | SQLite FTS5 | virtual table + `MATCH`; phrase-OR the query tokens |
| Multicam sync | numpy FFT cross-correlation | correlate ENERGY ENVELOPE (abs + 25ms moving avg), not raw waveform |
| Silence/filler removal | word timestamps → cut plan | non-destructive: store planned cuts, render on request |
| Selects reels / batch shorts | SQLite query → timeline → ffmpeg | keep clips+paths+timecodes in SQLite |
| Premiere/FCP/Resolve export | FCP7 XML / FCPXML 1.9 / OTIO / EDL | stdlib XML writers; OTIO only for Resolve |

## The critical techniques

### Multicam sync: correlate the envelope, not the wave
Raw cross-correlation of periodic content (pure tones, hum) rings — the peak
lands at a random period multiple. Fix: take `abs()` of the decimated signal,
smooth with a 25ms moving average, then FFT cross-correlate. Envelope shape
(speech/music amplitude modulation) is unique per time position.
- Fold the FFT index into a **signed lag**: `lag = idx if idx <= nfft//2 else idx - nfft`.
- Sign convention (verified empirically): a clip that STARTS LATER gets a
  NEGATIVE alignment offset (its media is shifted earlier on the timeline).
- Parabolic interpolation around the peak for sub-sample precision.
- Test with synthetic media whose audio has AM at incommensurate LFO rates
  (e.g. `0.5+0.3*sin(2π*0.5t)+0.2*sin(2π*0.37t)`) and a known `adelay` offset.

### Filler/silence removal from word timestamps
Silence cut = gap between consecutive word ends/starts > threshold, minus keep
padding (~80ms) so speech never sounds clipped. Filler cut = word span ± pad,
then merge overlapping intervals. Store as cut plans (clip, kind, start, end,
label) — never destructively edit the source.

**Whisper tokens carry leading spaces** (`' um,'`) — normalize with
`token.strip(" .,!?;:'\"()").lower()` before matching, or fillers never match.
**Filler matching must be longest-first phrase matching over consecutive
tokens** (`you know` beats `you`; each token belongs to at most one
occurrence), not a per-token set lookup. Compute `removed_seconds` from the
MERGED intervals, not the sum of padded word spans (overlaps double-count).

### Visual search pitfalls
CLIP text→frame cosine: normalize BOTH sides; guard zero vectors with
`np.divide(..., where=denominators>0)` so no NaNs. Dedupe near-duplicate
frames temporally (min gap ~1.5s) or one static scene floods the results.
Verified pattern: 8s red→blue synthetic clip, query "a solid red screen"
must rank t∈[0,2s), "a solid blue screen" must rank t∈[4,6s). Pure-color
scores run ~0.33 — low absolute values are normal for CLIP on flat colors;
the RELATIVE ordering is what matters.

### NLE export without heavy deps
OTIO's **Windows wheel ships only core adapters** (`otio_json`, `otioz`,
`otiod`) — fcp7_xml/fcpxml/cmx_3600 are missing. Don't fight it: write minimal
exporters with stdlib `xml.etree` (FCP7/xmeml for Premiere, FCPXML 1.9 for
Final Cut), keep OTIO JSON for DaVinci Resolve (imports natively), and a
plain-text CMX3600 EDL. Timecode: `HH:MM:SS:FF` at 24fps base.

## MCP server build notes
- Pin `mcp>=1.2.0,<2.0` — SDK 2.x REMOVED `mcp.server.fastmcp` (FastMCP moved
  out). Verify the import after `uv sync`, don't trust `pip list`.
- FastMCP 1.x `call_tool` returns `(content, is_error)`; a LIST return value
  becomes ONE TextContent block PER ITEM — `content[0].text` is only the
  first element. Parse each block separately and join, or a single-hit result
  silently reads as a dict and `len()` lies (8 columns ≠ 8 hits).
- Heavy ML deps go in `[project.optional-dependencies] ml = [...]` with lazy
  imports inside each step — server registers tools in seconds without
  downloading gigabytes of weights. `uv sync --extra ml` DROPS the dev extra;
  re-sync `--extra ml --extra dev` or pytest runs in a partial env.
- FTS5 with `content='segments'` needs AFTER INSERT/DELETE/UPDATE triggers on
  the content table (external-content tables don't auto-sync) plus a
  `INSERT INTO segments_fts(segments_fts) VALUES('rebuild')` on Store init so
  pre-trigger rows become searchable. `analyze_footage` must accept + reuse an
  existing `clip_id` or words land on an orphan clip.
- Verify with: unit tests for pure logic (cut plans, exporters, embedding
  ranker) + one stdio smoke test (`StdioServerParameters` + `mcp.client.stdio.stdio_client` +
  `ClientSession`, then initialize/list_tools/call 2-3 tools).
- **Wiring into Hermes**: `hermes mcp add NAME --command <abs venv python> --args -m <module> --stdio --env KEY=VALUE ...`
  — no `cwd` support in Hermes MCP config, so use absolute venv python + env
  vars for DB/workdir. The enable prompt (`Enable all N tools? [Y/n]`) hangs
  in non-interactive shells; run it in a PTY and send `Y` then a CR. Verify
  with `hermes mcp test NAME`; tools appear as `mcp_<server>_<tool>` after a
  new session.

## Verification workflow
1. Generate synthetic test media with ffmpeg (two angles, one with `adelay`)
2. Unit-test the DSP and cut planning with deterministic fixtures
3. Protocol-level smoke test over real stdio
4. Export every format and assert file content (xmeml/fcpxml markers)
5. Run `uv run pytest` and the functional script before committing

## References
- `references/selects-capability-map.md` — full Selects MCP capability analysis
  and FOSS alternatives evaluated (Jumper, Eddie AI, TwelveLabs, Video Jungle).
