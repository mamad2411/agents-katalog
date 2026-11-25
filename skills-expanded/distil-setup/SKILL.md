---
name: distil-setup
description: >-
  Install distil and route an AI coding agent or SDK app through it to cut LLM token
  costs with certified, reversible context compression. Use when the user wants to set
  up distil, install distil-llm, reduce their agent/Claude Code/Codex/Gemini token spend,
  point a base_url at the distil proxy, or check how much distil has saved them.
---

# Set up distil

Distil is a certified, reversible LLM context compressor. The CLI is `distil`; the PyPI
package is `distil-llm` (the bare `distil` name was taken). Core is zero-dependency stdlib —
it runs anywhere. Follow these steps; only report numbers the commands actually print.

## 1. Install (isolated — never `pip install` system-wide)

Pick the first that's available:

```bash
pipx install distil-llm        # isolated CLI (preferred)
# or, zero-install:
uvx --from distil-llm distil bench
# or:
brew install dshakes/tap/distil
```

Verify: `distil --version` (should print `distil 1.0.0` or later).

## 2. See it work in seconds (offline, no API key)

```bash
distil bench    # certifies savings + decision-equivalence across 7 domains
```

## 3. Route real traffic through it — pick the user's situation

**Coding agent (Claude Code / Codex / Gemini CLI)** — wrap it, zero code change:
```bash
distil wrap --lossless-only -- claude     # subscription/OAuth-safe (ToS-safe, no tool injection)
distil wrap --expand -- claude            # PAYG: aggressive digest, model recovers detail on demand
```
`--lossless-only` is the safe default for subscription/OAuth sessions. Add `--verbatim` for
interactive sessions where the model should see content un-digested.

**Any SDK app (Python/TS/any language)** — point the client's `base_url` at the proxy:
```bash
distil proxy --upstream https://api.anthropic.com   # listens on 127.0.0.1:8788
```
Then set `base_url="http://127.0.0.1:8788"` (Anthropic) or `.../v1` (OpenAI-compatible). For
Gemini: `distil proxy --upstream https://generativelanguage.googleapis.com`.

**Org-wide, zero per-developer change** — run `distil proxy` as a sidecar and set
`ANTHROPIC_BASE_URL` / `OPENAI_BASE_URL` in managed settings or container env.

## 4. Prove the savings are real

```bash
distil leaderboard            # genuine cumulative savings from the local ledger
distil proxy --shadow 0.05    # then: distil shadow-stats — live decision-equivalence on real traffic
```

## Honest scope (tell the user this — it's the point)

The decision-equivalence guarantee is certified but **conditional on exchangeability** with
the calibration distribution, and when distil can't certify safety it **falls back to full
context** (never silently lossy). Aggressive *lossy* compression can cost end-to-end task
success — distil's *reversible*, relevance-gated tier is the one validated non-inferior to full
context on a real long-horizon agent. For an aggressive operating point, calibrate per
deployment: `distil calibrate` (fail-safe to full context).
