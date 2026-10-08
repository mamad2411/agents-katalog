---
name: qwen-mtp-gguf-release
description: Repository-level wrapper for the canonical Qwen MTP or nextn GGUF release workflow. Use when Codex needs to prepare, validate, convert, quantize, smoke-test, or optionally release Qwen-family GGUF artifacts from this repository while preserving the canonical implementation under qwen-mtp-gguf/.
---

# Qwen MTP GGUF Release

Use this as a lightweight repository wrapper. The canonical implementation lives under `qwen-mtp-gguf/`.

## Required Reading

Read these files before running or changing the workflow:

- `qwen-mtp-gguf/SKILL.md`
- `qwen-mtp-gguf/README.md`

Load the reference files inside `qwen-mtp-gguf/references/` only when the task touches sizing, extraction, conversion, troubleshooting, or agent packaging.

## Operating Rules

- Reuse `qwen-mtp-gguf/scripts/` rather than copying conversion logic.
- Run the canonical pipeline with `--preflight-only` before any conversion or model download.
- Treat disk shortages, model-config mismatches, missing tools, and missing token access as blockers.
- Keep examples public-safe with placeholders for model IDs, local paths, output repos, and tokens.
- Keep Hugging Face upload disabled unless the user explicitly authorizes upload for that run.
- Keep cleanup disabled unless confirmed uploads are verified.
- Never publish or upload artifacts merely because GitHub sync was approved.

## Canonical Flow

1. Inspect requested target model, MTP source model, output mode, quant formats, and available machine resources.
2. Run the canonical preflight command from `qwen-mtp-gguf/SKILL.md`.
3. Review `preflight_report.md` and stop on hard blockers.
4. Run the full canonical pipeline only after the user accepts the launch plan and safety gates.
5. Smoke-test outputs before any upload.
6. Upload only when separately authorized, then clean up only after successful upload confirmation.
