---
name: pet-companion
description: >
  Use this skill when the user wants to package a Codex pet success case as a
  public-safe cross-runtime workflow, export a runtime-neutral bundle, add a
  small companion viewer, or document adapter guidance for Claude Code, GitHub
  Copilot, OpenClaw, or Paperclip.
---

# pet-companion

Use this skill to turn a local pet workflow into a public-safe package.

## Core Goal

Keep three lanes separate:

1. native Codex pet package
2. runtime-neutral public bundle
3. runtime-specific adapter guidance

## Workflow

1. Inspect the local pet or companion source.
2. Strip private paths, private logs, and binary delivery artifacts.
3. Export or rewrite metadata into `runtime-adapters.json`.
4. Map runtime state names into the shared contract.
5. Add or update viewer examples.
6. Document runtime limits before claiming portability.
7. Verify with schemas, viewer checks, and the public safety scan.

## Required Evidence

- changed file paths
- example state file or manifest
- viewer or schema verification
- explicit unsupported areas

## Close Shape

```text
Package:
Runtime support:
Schemas:
Examples:
Checks:
Known limits:
```
