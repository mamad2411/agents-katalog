---
name: jsonl-stdout-batch-prediction-format
description: CLI emits one JSON object per line (path, prediction, score, overwrite_reason, status) so downstream tools (jq, grep, awk) can pipe directly.
category: cli
version: 1.0.0
version_origin: extracted
confidence: medium
tags: [magika, cli]
source_type: extracted-from-git
source_url: https://github.com/google/magika.git
source_ref: main
source_commit: 0a8cb9626bbf76c2194117d9830b23e9052a1548
source_project: magika
imported_at: 2026-04-18T00:00:00Z
---

# Jsonl Stdout Batch Prediction Format

**Trigger:** Building a CLI that processes many files and must compose with Unix text-processing pipelines.

## Steps

- Define a result struct with path, prediction.{dl, output, score, overwrite_reason}, status.
- Serialize each result to one compact JSON line (no pretty-printing); print exactly one line per input file.
- Add --jsonl as an explicit format flag; keep human-readable text as default.
- On errors, emit {"path":..., "status":"error", "error":"..."} as JSONL too — don't break the line-per-file invariant.
- Line-buffer stdout (BufWriter + flush, or set_line_buffer()) so streaming consumers see results immediately.
- Reserve stderr for progress and warnings; never mix progress lines into stdout.

## Counter / Caveats

- Paths with embedded newlines/control chars break naive line-by-line parsers; escape inside the JSON string.
- Field ordering in JSON is not guaranteed across serializers; if downstream relies on order, use ordered maps.
- JSONL is not Excel-friendly; users expecting CSV need a separate format.
- stdout buffering can delay tail-style consumers if you forget the explicit flush.

## Source

Extracted from `magika` (https://github.com/google/magika.git @ main).

Files of interest:
- `rust/cli/src/main.rs:102-128`
- `python/src/magika/cli/magika_client.py:70-71`
