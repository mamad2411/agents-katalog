---
name: Hugging Face Hub
skill_id: huggingface-hub
description: Guides model, dataset, and space workflows around Hugging Face Hub with explicit auth, artifact, and cache assumptions.
version: 1.0.0
source_kind: elephant-builtin
aliases: ["hugging face hub", "hf hub", "huggingface"]
trigger_phrases: ["download this model from hugging face", "inspect this hf repo", "publish to hugging face hub"]
keywords: ["huggingface", "hub", "model", "dataset", "repo", "auth", "cache"]
category: mlops
---

# Hugging Face Hub

Use this built-in skill when the user is working with model repos, datasets, cards, or publishing flows on Hugging Face Hub.

## Core rules

- Confirm the exact repo id, artifact type, and auth posture before acting.
- Distinguish local cache state from remote hub state.
- Inspect model cards, licenses, and file sizes before large pulls or pushes.
- Keep publish steps explicit and reversible.

## Default workflow

1. Verify the target repo or dataset identifier.
2. Check auth, access level, and local storage implications.
3. Inspect metadata, artifact layout, and intended use.
4. Pull, publish, or mirror only the artifacts the task actually needs.

## Guardrails

- Do not assume a repo is public, local, or already cached without verification.
- Do not hide large downloads or publishes behind vague progress language.
- Do not ignore license or model-card constraints.
