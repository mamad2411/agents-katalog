---
name: token-turbo
description: "Token reduction enforcement — max compression, minimal output, caveman mode. Always-on alongside caveman skill."
allowed-tools: Read, Bash
---

# Token Turbo — Always-On Token Reducer

## What It Does
Enforces maximum token efficiency on every response:
- Caveman compression (ultra-short outputs, bullet points only)
- No filler, no repetition, no hedging
- Max 150 words unless code
- Parallel batch all sub-tasks (fewer round-trips)

## Works With
- `caveman` skill — compression rules
- `compress` skill — context compression
- `compact-guard` — prevents context bloat
- CLAUDE.md Tier 0 routing — routes all sub-tasks to free models

## Always Active
Cannot be disabled. Runs on every prompt via skill-auto-activate.
