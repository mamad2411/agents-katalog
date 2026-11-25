---
name: model-publisher
description: Package trained checkpoints, generate model cards, and publish releases to Hugging Face Hub with optional GGUF export.
---

# Model Publisher

Use this skill to prepare and publish trained models for public or private distribution.

## Checkpoint Packaging

Convert training checkpoints to SafeTensors before publishing.
Validation requirements:

- verify tensor/key integrity after conversion
- preserve model config/tokenizer compatibility
- document source checkpoint and conversion command

## Model Card Generation

Auto-generate a model card (`README.md`) with at least:

- model overview and intended use
- architecture + tokenizer details
- training data summary and known limitations
- training/eval setup and headline metrics
- safety notes and out-of-scope usage

## Hugging Face Hub Publishing

Use `huggingface-cli` for authentication and push workflows.
Support:

- initial repository creation
- model + tokenizer artifact upload
- versioned updates for new checkpoints

## Optional GGUF Export

When requested, generate GGUF quantized variants for local inference.
Document quantization type, expected quality impact, and target runtime profile.

## Environment

Required:

- HF_TOKEN

## Release Outputs

1. `publish_manifest.json` (what was published + versions)
2. `README.md` (generated model card)
3. `release_notes.md` (changes since last version)
4. optional `gguf_manifest.json` (quantized artifacts)

## Preflight Validation

Before any publish operation, validate:

- `HF_TOKEN` is set and has write permissions.
- HF Hub API is reachable and token is valid (`huggingface-cli whoami`).
- Target repository exists or can be created under the authenticated account.

Report clear error if credentials are missing or invalid.
