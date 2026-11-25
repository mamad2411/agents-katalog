---
name: inspect
description: Statically inspect prompt-cache breakpoints in a captured /v1/messages body or a clawback --state file, with ZERO token spend and no API calls. Answers "where are the cache_control breakpoints, and which ephemeral tokens (cch / date / <env>) sit inside which cached prefixes?" — i.e. what a single mutation cold-starts. Use it to SEE why strip-ephemeral matters (cch precedes the earliest breakpoint, so it cold-starts every cached prefix every request) before spending tokens on a dynamic probe. Read-only and safe to run against a live benchmark.
---

# clawback cache-breakpoint inspector

Run `.skills/inspect/scripts/inspect_breakpoints.sh [PATH] [--json]` from the project root.

With no `PATH`, it inspects the most recently modified `runs/*/state*.json`.
This is read-only — it touches only files already on disk, never the running
proxy — so it is safe to run while a benchmark is in flight.

```bash
# inspect the newest run's captured state
.skills/inspect/scripts/inspect_breakpoints.sh

# inspect a specific captured body or fixture
.skills/inspect/scripts/inspect_breakpoints.sh benchmark/fixtures/ccode.json

# machine-readable model for tooling
.skills/inspect/scripts/inspect_breakpoints.sh runs/l2-haiku/state.A0.json --json
```

## What it reports

A cache-ordered segment table (`tools -> system -> messages`), each row marked
with its `cache_control` breakpoint (and TTL) and any ephemeral token it
carries, followed by a verdict centered on `cch` (the per-request rotator).

Worked example, from a real Claude Code v2.1.145 body:

```
  33    20               system[0] "x-anthropic-billing-header: cch=..."   <-- cch
  34    14  BREAK 1h    system[1] "You are Claude Code, ..."
  35  7304  BREAK 1h    system[2] " You are an interactive agent ..."   <-- iso-date

VERDICT:
  cch sits BEFORE the earliest breakpoint (pos 34). Every cached prefix
  includes it, so a new cch per request cold-starts 2/2 prefixes ... No
  breakpoint isolates tools or anything ahead of cch, so nothing survives.
```

## Why static is enough (and the limit of "static")

Anthropic caches the **cumulative** prefix up to each breakpoint by exact
match. So a token at cache-order position P invalidates every breakpoint at
position >= P when it rotates. That single fact characterizes the whole
structure: you do **not** need a 2^N probe to know what cold-starts. The
inspector reads the breakpoint placement straight out of the captured body and
applies that rule. This replaces, rather than approximates, an exhaustive
dynamic sweep; the one thing it can't prove (that Anthropic honors the
breakpoints as documented) is what the optional token-costing probe confirms.

## Input fidelity caveat

A **synthetic** (hand-authored) fixture may carry a tools breakpoint that
real Claude Code lacks, and no `cch` at all — so the inspector will
(correctly) report "no cch ... rotation driven only by date/env." That is a
property of the input, not a bug: only a body captured from a real session
(see `.skills/capture`) reproduces the genuine cch + breakpoint structure.
The shipped `benchmark/fixtures/ccode.json` is such a capture (sanitized of
personal data, structure intact), but it ages as Claude Code releases move —
inspect a fresh `--capture-body` dump or a live run's `state*.json` for a
verdict on the current build.

## Sensitivity

State files and captured bodies contain your system prompt and tool
definitions. Treat the inputs as sensitive; the inspector itself only prints
positions, token estimates, ~60-char segment labels, and short ephemeral
samples (e.g. `cch=f1b84`) — not full block contents.
