---
name: dio-dont-trust-your-memory-check-the-docs-first
description: Before stating external facts, check official docs or repo sources — not training memory.
disable-model-invocation: true
---

Training memory drifts. Wrong assumptions compound across turns. This is a **quick source check**, not full deep research.

## When this applies

External systems: CLIs, install flows, API behavior, registry or publish claims, version-specific flags, third-party tool behavior.

Skip for: code already in the workspace, pure opinion, or conversation recap macros.

## Process

1. **Name the claim** — one sentence you were about to assert.
2. **Verify** — `Read` in-repo docs or `WebFetch` / search official source once. Do not chain guesses.
3. **Answer with a label:**
   - **verified** — cite URL or file path (one line)
   - **unverified** — say what you tried; do not state as fact
   - **memory — not checked** — only if the user explicitly asked to skip lookup

## Output shape

Reply with **only**:

## claim
<what was at risk of being wrong>

## source check
<what was read or fetched, or "none — unverified">

## answer
<corrected statement, or honest "don't know yet">

## label
verified | unverified | memory — not checked

## Hard rules

- Do not invent CLI flags, install steps, or directory layouts from memory.
- If docs conflict with memory, docs win.
- For ledger-grade research with confidence scoring, use the `verasic-deep-research` skill instead.
