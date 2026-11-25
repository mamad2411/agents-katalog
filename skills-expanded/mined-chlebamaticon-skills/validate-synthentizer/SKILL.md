---
name: validate-synthentizer
description: Synthesize challenged code and security review findings into the canonical JSON validation report. Use during a validation cycle after both reviews and challenges complete.
---

# Validate synthentizer

Read [the shared validation contract](../validate/validation-contract.md). The caller supplies `RUN_DIR` containing coordinator, reviewer, and challenge artifacts.

## Build the canonical report

Validate that every reviewer finding has exactly one corresponding challenge verdict. Start `synthesis.json` with the `change-summary` object using `changes.json`. Then include every upheld finding once and every reframed finding once using its revised content; exclude dismissed findings. Preserve source, ID, severity, evidence, and location. Sort final findings by severity (`blocking`, `important`, `minor`), then source, path, line, and ID so repeated runs have a stable order.

Write the array atomically. It must parse as JSON without markdown fences or commentary.

**Done when:** `synthesis.json` is valid JSON; every source finding is accounted for as upheld, dismissed, or reframed; and each non-dismissed finding appears exactly once in stable order.
