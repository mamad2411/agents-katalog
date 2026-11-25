---
name: omni-bench
description: Develop the omni-bench benchmark framework (ASR/STT + text generation) built on a producer/scorer split with an open JSON spec as SSOT. Use when working in an omni-bench checkout — changing the JSON schemas, the prepare/producer/scorer/diff pipeline, the adapter seams (Transcriber / Generator), datasets, fixtures, or the Swift producer SDK; or when running and validating benchmark artifacts. Encodes the schema-evolution rules, determinism invariants, commands, and repo gotchas that are easy to get wrong.
version: 1.0.1
---

# omni-bench development

Embeddable benchmark **framework**, not a model runner: hosts own inference via
adapter seams; omni-bench owns datasets, scoring, metrics, and the JSON spec.
North star: quality + speed **tied to specific hardware**; parity
(Python↔Swift, CUDA↔MLX) is a derived view. Primary consumer: a Swift host
wrapping in-process models (e.g. mlx-omni).

## Layout

- `schemas/*.schema.json` — **the SSOT** (open spec, JSON Schema draft 2020-12).
  Everything else follows it. Pinned `schema_version` (`0.1.0`, re-cut
  2026-07-04 — the pre-release 0.1.0/0.2.0 iterations are retired).
- `python/src/omni_bench/` — `core/` (prepare, producer, scorer, diff, validate,
  identity, hardware), `asr/` (normalizers, metrics, registry — the registry is
  the modality-agnostic task table despite the package name), `textgen/`
  (synthetic shared-prefix task), `models/` (**generated** — never hand-edit;
  regenerate with `just codegen-python`).
- `swift/` — producer SDK mirroring the Python producer (`Transcriber`,
  `Generator`, `Producer`, `ArtifactWriter`, JCS identity).
- `fixtures/` — committed goldens; each dir has a `generate.py` to regenerate.

## Pipeline & artifacts

`prepare → run → score → diff`:
manifest.json (+references.jsonl) → run-artifact.jsonl → result.json → parity-report.json.

- Producer never aborts: a failing sample becomes an `error` record.
- Scorer is the **trust anchor**: scoring exists only in Python, once. Never
  reimplement scoring in a host (measurer drift is the enemy this design kills).
- Identity is a JCS (RFC 8785) hash over a fixed subset (model, backend,
  hardware, os, task, dataset, run_profile.decode). Identity fields are
  host-declared and trusted — a bogus value silently breaks the parity join.

## Adapter seams (structural, no inheritance; Swift mirrors Python 1:1)

- ASR: `Transcriber.transcribe(audio, language, task) -> Transcript`.
- Text generation: `Generator.generate(prompt, task) -> Generation` +
  `reset_cache()`. All latency/token metrics (`ttft_s`, `prefill_s`,
  `prompt_tokens`, `generated_tokens`, `reused_tokens`, `cache_hit`, `decode_s`)
  are **host-reported** via `backend_native` — the seam is non-streaming, the
  producer cannot observe TTFT. The scorer derives the rates: `tok_per_s`
  (micro) and `prefill_tok_per_s` (cold samples only in cache mode — cache-free).
- Shared-prefix cold/warm scenario: `mode: "shared_prefix_cold_warm"` +
  per-sample `prefix_group`. Producer resets the cache at every group boundary;
  first sample after reset is `phase: "cold"`, rest `"warm"`; **nothing is
  warmup-discarded** — the scorer's `cache` block reports cold/warm medians and
  `ttft_speedup = cold / warm`. Built-in offline task: `textgen.shared_prefix.en.v1`.

## Schema evolution rules (bite hard)

- Objects are **closed** (`additionalProperties: false`) ⇒ ANY additive field is
  a breaking change ⇒ bump the minor `schema_version` **in lockstep across all
  schemas**, then update `SCHEMA_VERSION` in `core/{prepare,producer,scorer,diff}.py`,
  Swift `ArtifactWriter.writeHeader`, regenerate models AND all fixtures.
- After any schema change: `just codegen-python` (commit `models/`), rerun
  `fixtures/{scoring,parity,textgen}/generate.py`, hand-bump `fixtures/examples/*`
  and `fixtures/xlang/manifest.json`.
- Determinism is a hard invariant: `sort_keys` JSON, samples sorted by id,
  monotonic clocks, no timestamps in WAVs — `prepare` twice ⇒ identical hashes.
  Nothing under `omni_bench/` may use wall-clock or randomness in artifacts.

## Commands

```bash
just check                 # validate-schemas + pytest + swift test — run before commit
just codegen-python        # schemas -> pydantic models (stages *.schema.json to tmp)
uv run --project python pytest python/tests -q
cd swift && swift test
uv run --project python python -m omni_bench.cli prepare textgen.shared_prefix.en.v1  # offline, CI-safe
```

`just`/`uv` may live outside the default PATH (e.g. `/opt/homebrew/bin`).
Only `textgen.shared_prefix.en.v1` is downloads-free; the ASR tasks hit
HuggingFace — tests monkeypatch `get_task` instead.

## Gotchas

- datamodel-codegen parses EVERY file in its input dir — stage `*.schema.json`
  into a temp dir named `schemas` (the dir name lands in the generated header;
  keep it stable), which is why the justfile does exactly that.
- Required-nullable is the repo idiom (`"type": ["x", "null"]` + required):
  Swift writes explicit `NSNull()`, omission fails validation. `phase` is the
  exception (optional) so ASR artifacts keep their v1 shape.
- ASR hyp-identity in `diff` uses the language normalizer; text-generation uses
  NFC-exact comparison — deterministic decoding makes exact identity the gate.
- Hardware keys the identity: off macOS the collector can't see the accelerator;
  pass explicit `hardware={"soc": ..., "mem_gb": ...}` (producer warns otherwise).
- Keep contract docs in sync on any schema change: `schemas/README.md`,
  `docs/integration.md`, and the README CLI/task lists.
