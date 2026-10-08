---
name: python-mcp-server-build
description: >-
  Use when building or debugging Python MCP servers.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [mcp, fastmcp, python, server, sqlite, fts5, otio, whisper, testing]
    triggers:
      - build an mcp server
      - fastmcp
      - mcp server in python
      - mcp tool testing
      - otio export
      - whisper word timestamps
      - fts5 search
    related_skills: [building-mcp-servers, mcp-server-wiring, mcp-endpoint-testing]
---

# Python MCP Server Build

Verified gotchas for building Python MCP servers with the official `mcp` SDK
(FastMCP). Every item below was hit and fixed during a real build; all
verified by execution.

## FastMCP API: pin mcp>=1.2,<2.0

`mcp` **2.x removed `mcp.server.fastmcp` entirely** (FastMCP moved to a
separate package). `from mcp.server.fastmcp import FastMCP` raises
`ModuleNotFoundError` on mcp 2.0. Pin in pyproject.toml:

```toml
dependencies = ["mcp>=1.2.0,<2.0"]
```

Verify with `uv pip list | grep -i mcp` before assuming the import works.

## Testing tools in-process: list results = one content block per element

`await mcp.call_tool(name, kwargs)` on FastMCP 1.x serializes a tool's Python
`list` return into **one `TextContent` block per list element**. Reading only
`content[0].text` silently returns the FIRST item's JSON — `len(json.loads())`
then reports that dict's key count (e.g. "8 hits" from one 8-column row),
which masquerades as a search-duplication bug for hours. Always parse every
block:

```python
async def call(tool_name, **kwargs):
    result = await mcp.call_tool(tool_name, kwargs)
    if isinstance(result, tuple):
        content, is_error = result
        if isinstance(content, list):
            parts = []
            for c in content:
                t = getattr(c, "text", "") or ""
                parts.append(json.loads(t) if t.startswith(("{", "[")) else t)
            return parts[0] if len(parts) == 1 else parts
        return str(content)
    return result
```

## SQLite FTS5 external-content tables are NOT auto-populated

`CREATE VIRTUAL TABLE t USING fts5(text, content='segments', content_rowid='id')`
starts EMPTY and stays empty without triggers. Add AFTER INSERT/DELETE/UPDATE
triggers on the content table, plus `INSERT INTO t(t) VALUES('rebuild')` on
every DB init (idempotent; heals rows written before triggers existed).
Search queries JOIN `fts f ON s.id = f.rowid`. Symptom of a missing trigger:
index table count is 0 while content rows exist, or stale rows that never
get deleted.

## OpenTimelineIO: Windows wheel ships ONLY core adapters

The `opentimelineio` pip wheel (0.18.x) includes just `otio_json`, `otioz`,
`otiod`. The NLE adapters (`fcp7_xml` for Premiere, `fcpxml`, `cmx_3600` EDL)
are **absent** — `write_to_file(..., adapter_name='fcp7_xml')` fails with
"Could not find plugin". Don't fight it: write minimal exporters with stdlib
`xml.etree` (FCP7 xmeml, FCPXML 1.9, CMX3600 EDL are small, well-documented
formats). Keep OTIO only for the DaVinci Resolve path (`otio_json`, imported
natively by Resolve).

Other OTIO trap: `otio.schema.Clip()` takes `media_reference=` (SINGULAR),
not `media_references=[...]` — the list form raises "incompatible constructor
arguments".

## faster-whisper word tokens carry leading spaces

Word timestamps come back as `' um,'` / `' So,'` — leading space + trailing
punctuation. Exact-match logic (filler-word removal, keyword tagging) must
normalize BOTH ends: `w["word"].strip(" .,!?;:'\"").lower()`. Also: multi-word
fillers ("you know", "sort of") arrive as separate tokens, so single-token
matching misses them by design — document that as a known limitation.

## Multicam/audio sync: correlate the ENERGY ENVELOPE, not the waveform

Raw cross-correlation on periodic content (sine tones, hum) rings badly — a
true 3.5s delay was detected as 64.6s. Fix: `abs()` the decimated signal,
smooth with a ~25ms moving average, then FFT cross-correlate the envelope.
Also fold FFT indices into signed lags (`idx if idx <= nfft//2 else idx - nfft`)
or the wrap-around half of the array reads as a huge bogus offset.

Deterministic sync test media: `ffmpeg -af "adelay=3500|3500"` bakes a known
offset; use incommensurate AM LFOs in `aevalsrc` so the envelope is unique:
`0.8*sin(2*PI*440*t)*(0.5+0.3*sin(2*PI*0.5*t)+0.2*sin(2*PI*0.37*t))`.

## uv sync extras are EXCLUSIVE

`uv sync --extra ml` run after `uv sync --extra dev` REMOVES the dev extras
from the venv → baffling partial-environment failures (tests run fine, lazy
imports inside them fail). Always sync BOTH: `uv sync --extra ml --extra dev`.

## PyPI name gotchas

- PySceneDetect installs as `scenedetect`, not `pyscenedetect` — wrong name
  fails resolution with "not found in the package registry".
- Edge TTS for generating real speech test fixtures:
  `uv run --with edge-tts python -m edge_tts --voice en-US-GuyNeural --text "..." --write-media out.mp3`.

## Workflow that worked (scaffold → verify loop)

1. `uv sync` core deps first; heavy ML (torch, whisper, CLIP) as an optional
   extra, lazy-imported inside the functions that use it — the server
   registers tools instantly without loading gigabytes of weights.
2. Unit tests for pure logic (cut planning, exporters, sync math) with
   synthetic fixtures — no ML needed.
3. A stdio smoke test that boots the real server and drives it through
   `ClientSession` (tools listed + a real call round-trip).
4. THEN the ML path on generated real-ish media (TTS speech), asserting exact
   counts before trusting the pipeline.
