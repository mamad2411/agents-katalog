---
name: model-config-min-json-compact-format
description: Distribute model config as compact JSON (config.min.json) alongside the .onnx file so package size stays small and parsing is universal.
category: data
version: 1.0.0
version_origin: extracted
confidence: high
tags: [magika, data]
source_type: extracted-from-git
source_url: https://github.com/google/magika.git
source_ref: main
source_commit: 0a8cb9626bbf76c2194117d9830b23e9052a1548
source_project: magika
imported_at: 2026-04-18T00:00:00Z
---

# Model Config Min Json Compact Format

**Trigger:** Distributing an ML model with metadata that must be parsable from every language without a custom binary format.

## Steps

- Author the canonical config in pretty JSON (full whitespace) for readability.
- Generate config.min.json via jq -c or json.dump(separators=(',', ':')).
- Ship .min.json next to model.onnx; keep the pretty version in source control for review.
- Add a config_version field so you can evolve the schema without breaking old loaders.
- Validate strictly at load time: required fields present, value ranges correct, fail fast on unknown fields if you want strict mode.
- Test the config parser in every binding to catch JSON quirk drift early.

## Counter / Caveats

- Minified JSON is unreadable for debugging; always keep a pretty source-of-truth.
- Schema changes need version bumps and migration notes.
- Threshold arrays of 300+ floats inflate the file; consider a sparse representation.
- Binary formats (protobuf, msgpack) win on size but lose universal portability.

## Source

Extracted from `magika` (https://github.com/google/magika.git @ main).

Files of interest:
- `assets/models/standard_v3_3/config.min.json`
- `rust/lib/src/config.rs`
- `go/magika/config.go:10-31`
