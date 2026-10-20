---
name: generated-enum-and-config-code-from-json-schema
description: Build-time code generator that reads a JSON content-type knowledge base and emits per-language type-safe enums + const TypeInfo structs (MIME type, group, extensions, is_text).
category: codegen
version: 1.0.0
version_origin: extracted
confidence: high
tags: [magika, codegen]
source_type: extracted-from-git
source_url: https://github.com/google/magika.git
source_ref: main
source_commit: 0a8cb9626bbf76c2194117d9830b23e9052a1548
source_project: magika
imported_at: 2026-04-18T00:00:00Z
---

# Generated Enum And Config Code From Json Schema

**Trigger:** You have a large dynamic schema (300+ entries) and need per-language type safety without hand-writing or hand-maintaining enums.

## Steps

- Create a generator binary (Rust here) that reads content_types_kb.min.json and config.min.json.
- Parse with serde; for each content type emit a const struct with label, mime_type, group, description, extensions, is_text.
- Generate enum variants per type; map labels to valid identifiers (CamelCase / snake_case, leading-digit prefix).
- Write generated code under a clearly-marked path (rust/lib/src/content.rs, python types/content_type_label.py) with a 'DO NOT EDIT' header.
- Use a deterministic ordering (BTreeMap) so regeneration is reproducible.
- Wire generation into the build pipeline (build.rs, setup.py hook, or dedicated generate.sh) and check generated files into git.

## Counter / Caveats

- Generator output must be deterministic; non-deterministic ordering breaks reproducible builds and noisy diffs.
- Schema drift (new fields, type changes) causes generator failures; version the schema and validate before generating.
- Large enums (300+ variants) slow Rust compile times; consider non_exhaustive and feature gates.
- IDE autocomplete fails until generation runs; document a clone-time setup script.

## Source

Extracted from `magika` (https://github.com/google/magika.git @ main).

Files of interest:
- `rust/gen/src/main.rs:23-100`
- `python/src/magika/types/content_type_label.py:19-30`
- `rust/lib/src/content.rs (generated)`
