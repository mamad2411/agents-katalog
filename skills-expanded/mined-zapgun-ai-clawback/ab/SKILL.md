---
name: ab
description: Run a counterbalanced A/B knob block end to end and produce a report. Orchestrates the whole validation loop the other skills do piecemeal — for each arm it starts a clawback proxy with that arm's knobs and its OWN --state file (fresh SESSION KEY, no clawback-side carry-over), drives N turns of load through it (pty or replay driver), stops it, then analyzes the per-arm turn-logs and renders the charts. No cache-salt: production forwards none, so neither does the harness. Default block is A0 (passthrough baseline) vs A5 (recommended stack); the analyzer pools all passthrough turns into the baseline and compares each treatment arm against it, so the block must include A0 and may carry several treatment arms at once. Use this to run the full A/B runbook in one command. The pty driver spends real Anthropic tokens (one run per arm) — pin --model.
---

# clawback A/B knob block (end-to-end orchestrator)

Run `.skills/ab/scripts/ab_block.sh` from the project root. It is the single command
that ties the validation harness together: capture (separately, once) →
**this** (drive both arms + analyze + plot). It runs **one arm at a time**:

1. start a clawback proxy with the arm's knob set + its **own
   `--state` file** + a shared `--turn-log` (via `.skills/monitor`'s
   `run_monitor.sh --detach`);
2. drive `--turns N` of load through it (`--driver pty` = real claude via
   `.skills/drive`; `--driver replay` = HTTP fixture via `.skills/replay`);
3. stop the proxy;
4. repeat for the next arm;
5. analyze the shared turn-log (`.skills/bench`) and render charts
   (`.skills/plot`) into the `--out` directory.

## Cache hygiene WITHOUT a salt (production fidelity)

A knob A/B is only honest if it measures what **production** does, and
production forwards no salt. The harness used to prepend a per-arm
`--cache-salt` block to `system` to force each arm cold — but that salt
forced whole-body re-serialization and **zeroed within-arm cache warming**
(salted arms measured ~0% warm vs a pristine A0 at ~98%), measuring a
virtual system instead of the proxy. It is gone. Arms are
isolated three production-faithful ways instead:

1. **clawback-side**: each arm gets its **own `--state` file**, so no arm
   RESUMES a prior arm's persisted SESSION KEYs.
2. **Anthropic-side, byte-MUTATING arms**: a treatment arm that mutates
   forwarded bytes (strip-ephemeral, 1h-TTL, mobile) already gets a distinct
   **ANTHROPIC KEY**, so it cannot read a prior arm's warm entries.
3. **Anthropic-side, byte-IDENTICAL arms**: keep-alive-only forwards the
   same real-turn bytes as passthrough, so per-arm `--state` does **not**
   change the content-addressed ANTHROPIC KEY. Two **production-faithful**
   guards, neither of which deletes a turn: (a) the analyzer reports
   cold-starts in their own `"first"` gap bucket, so a carry-over-warmed
   open is never pooled into the warm-loop buckets it's compared within;
   and (b) `--cooldown-sec` spaces serial arms past Anthropic's 5-min cache
   TTL so each arm's opening turn is a **genuine cold-start** (counted,
   exactly as a production user pays it after an idle), not a fake-warm read
   of the prior arm's cache — set `~330` for a byte-identical-arm headline.
   The analyzer's `--warmup` discard (drop each arm's first N turns) stays
   an **opt-in diagnostic** (default `0`), *not* the standing guard: dropping
   opening turns also deletes legitimate production cold-start cost, so the
   default **counts** them.

This is driver-independent — the proxy forwards the arm's bytes the same way
regardless of how the turn was produced.

## How the analyzer pairs the arms

The proxy labels every turn `passthrough` or `treatment`; this script writes
one turn-log per arm and labels it into the analyzer as knobProfile `<arm>`.
The analyzer **pools all passthrough turns into the per-bucket baseline**,
then compares each *treatment* knobProfile against that baseline. So:

- The block **must include A0** (passthrough) for a savings % — it is the
  baseline every treatment arm is measured against.
- You can put **several treatment arms** in one block (e.g.
  `--arms "A0 A2 A5"`): each is labeled separately and compared against the
  shared A0 baseline in the same run.

## Usage

```bash
# short L0 no-regression smoke, baseline vs recommended stack, on Haiku:
.skills/ab/scripts/ab_block.sh --profile L0 --turns 8 --driver pty \
  --model claude-haiku-4-5-20251001

# headline L2 (5-30 min gaps) block, >=200 turns/arm for a reportable %:
.skills/ab/scripts/ab_block.sh --profile L2 --turns 200 --driver pty \
  --model claude-haiku-4-5-20251001 --out runs/L2-headline

# clean HTTP replay arm (needs a CLAWBACK_OAUTH_TOKEN bearer + a captured
# fixture; never an API key):
CLAWBACK_OAUTH_TOKEN=… .skills/ab/scripts/ab_block.sh --profile L2 --turns 200 \
  --driver replay --fixture benchmark/fixtures/ccode.json

# keep-alive warmth test: does A1 stay warm across a 15-min idle on the
# native 5m TTL?
CLAWBACK_OAUTH_TOKEN=… .skills/ab/scripts/ab_block.sh --driver replay \
  --arms "A1 A0" --gap-sec 900 --turns 5 --out runs/keepalive-15m
```

## Arms

- `A0` passthrough baseline (forces all knobs off)
- `A1` keep-alive only
- `A2` 1h-TTL only (nested-cache-control rewrite on — the moat)
- `A3` 1h-TTL + keep-alive
- `A4` strip-ephemeral only
- `A5` recommended stack (keep-alive + 1h-TTL + strip-ephemeral)

Each arm's knobs are set **explicitly** on the proxy command, not inherited
from DEFAULTS, so the arm is the arm regardless of the operator's global
`CLAWBACK.md`.

## Options

- `--profile L0|L1|L2|L3|L4` — inter-turn gap regime (default `L0`).
- `--gap-sec N` — fixed inter-turn gap in seconds; overrides `--profile`'s
  jittered range (forwarded to both drivers). For a precise idle, e.g. the
  15-min keep-alive warmth test above.
- `--turns N` — turns per arm (default `8`; analyzer marks savings
  `insufficient` below 30/arm; target ≥200 for a reportable %).
- `--arms "A0 A5"` — space-separated arm list (default `"A0 A5"`).
- `--driver pty|replay` — load driver (default `pty`).
- `--model ID` — pin claude's model for the pty driver (cost control).
- `--fixture PATH` — replay fixture (default `benchmark/fixtures/ccode.json`).
- `--prompts PATH` — pty prompt file (default `benchmark/prompts/coding.txt`).
- `--settle-sec N` — pty quiescence threshold (default `8`).
- `--host`, `--port` — proxy bind (default `127.0.0.1:8787`).
- `--out DIR` — output dir (default `runs/ab-<timestamp>`).
- `--no-plot` — skip chart rendering.

## Spends real tokens

`--driver pty` runs the real `claude` binary once per arm against your own
Anthropic limits. Keep `--turns` small and pin `--model` (e.g.
`claude-haiku-4-5-20251001`) for plumbing / no-regression runs; reserve a
larger, default-model run for the headline numbers. `--driver replay` also
spends tokens but forwards a `CLAWBACK_OAUTH_TOKEN` bearer (never an API key)
and is cheaper to script.

## Outputs

In the `--out` directory:

- `turns.<arm>.ndjson` — one turn-log per arm (labeled into the analyzer as
  knobProfile `<arm>`; the passthrough arm pools into the baseline).
- `proxy.<arm>.log` — each arm's proxy stdout+stderr.
- `state.<arm>.json` — each arm's own proxy state file, so a restart never
  resumes the previous arm's persisted SESSION KEYs (the clawback-side
  carry-over guard described above).
- `report.md`, `report.csv`, `summary.json`, `manifest.json` — the analyzer
  outputs (`.skills/bench`).
- `charts/` — the four §9 marketing charts (`.skills/plot`).

Read the headline with `sed -n '1,40p' <out>/report.md`.

## Where this sits

Capture a fixture once with `.skills/capture`. This skill is the runner;
`.skills/{drive,replay}` are the load arms it calls, `.skills/bench` is the
analyzer, `.skills/plot` is the chart renderer. To run an arm by hand
instead, see those skills.
