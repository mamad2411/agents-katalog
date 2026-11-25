---
name: paired
description: Paired shadow-capture — one real claude session that captures the no-clawback baseline AND applies the armed knobs at the same time. This is the "shadow mode" knob for baseline capture: instead of forfeiting the optimizations for the measurement window (a plain passthrough baseline), the tee fans every turn to TWO unmodified clawback instances — PRIMARY (armed, default A5, streamed back to claude) and SHADOW (A0 passthrough, consumed for usage then discarded). Because both arms bill the SAME request bytes under the same turn, the analyzer pairs them turn-for-turn (pairBillableByPairSeq / bootstrapPairedDiff) for a tight turn-matched reclaim CI — not two free-running sessions that diverge. COSTS ~2x your Anthropic quota (every turn billed twice); the script REFUSES to run without --ack-2x. Use when you want a turn-matched A/B from a single live session.
---

# clawback paired shadow-capture (turn-matched baseline + armed in one session)

Run `.skills/scripts/run_paired.sh` from the project root. It answers a specific
problem with the plain `.skills/ab` block: two arms driven as two separate
`claude` sessions **diverge** after the first sampled token (different turns,
different counts — 342 vs 352 in the 75-min Haiku run), so turn *k* of A0 is
not the counterfactual of turn *k* of A5. The paired tee removes that: one
session, fanned to both arms, so every turn has an exact partner.

```
claude ──▶ tee ──┬─▶ clawback PRIMARY (armed, default A5) ─▶ Anthropic   (streamed back to claude)
                 └─▶ clawback SHADOW  (A0 passthrough)     ─▶ Anthropic   (usage tapped, discarded)
```

The SHADOW arm captures the **no-clawback baseline** while the PRIMARY arm
**applies (and serves claude) the armed knobs** — that is the knob this skill
adds: a baseline capture that does *not* forfeit the optimizations.

## The ~2x cost, and the switch

Shadow mode sends every billable turn to **both** arms, so it bills your
Anthropic quota **~2x** for the run. That is the price of an exact paired
measurement, and it is unavoidable by construction. So:

- `.skills/scripts/run_paired.sh` **refuses to start without `--ack-2x`** and prints
  the warning. Passing `--ack-2x` is the deliberate opt-in.
- It forwards `--ack-2x` to `benchmark/bin/tee.js`, which has the same guard
  (the tee refuses non-interactively without it, and prompts on a TTY).

Never run this for a long headline window without budgeting the doubled spend
against your own limits — the very quota clawback exists to stretch.

## Why the arms can't contaminate each other

- The two arms' forwarded bytes **already differ** — the PRIMARY (e.g. A5)
  strips the per-request `cch` and/or rewrites the TTL, while the SHADOW A0
  keeps the bytes pristine — so their **ANTHROPIC KEYs** differ and neither
  can warm the other's prompt cache. No salt needed, and none is used:
  production forwards no salt, so the harness must not either (a
  system-prepended salt forced whole-body re-serialization that zeroed
  within-arm cache warming — the confound we removed).
- The **SHADOW** is `--passthrough`, so A0 stays byte-transparent — the honest
  baseline that measures exactly what production sends.
- Each instance gets its **own `--state` file**, so neither resumes the
  other's persisted SESSION KEYs (the clawback-side carry-over guard).

Both instances are pre-seeded with one inert session so a fresh proxy does not
auto-arm a baseline capture that would force the opening ~5 turns to
passthrough (which would contaminate exactly the turns we want measured).

## How the analyzer pairs the arms

The tee writes one NDJSON record per arm per turn, both stamped with the same
internal `pairSeq` (a tee-only counter — it is **never** put on the wire: no
header, query param, or body field is added to either upstream request). The
outputs are named `A0.ndjson` (shadow) and `<primary-arm>.ndjson` (e.g.
`A5.ndjson`) so `analyze.js` labels them by basename with no `--label`. The
analyzer's paired path groups by `pairSeq`, computes `mean(base − treat)` over
matched pairs, and reports a paired-bootstrap 95% CI that is tighter than the
unpaired two-sample CI when the arms co-vary (they do — same fixture/cch/tools
per pair). The reclaim total is the **exact sum of per-pair deltas**, not a
projection.

The fragmentation table is **empty** on a tee run by design: the tee sees only
the pre-clawback body and cannot know what each instance forwarded after its
own rewrites, so it omits `systemStableKey`/`sessionKey` rather than fake them.
Fragmentation is measured separately by the standalone A0-vs-A5 block
(`.skills/ab`) and the static inspector (`.skills/inspect`).

## Usage

```bash
# short L0 paired smoke on Haiku (8 turns, both arms => ~16 turns billed):
.skills/scripts/run_paired.sh --ack-2x --profile L0 --turns 8 \
  --model claude-haiku-4-5-20251001

# headline L0 paired run, 75-min wall clock, Haiku:
.skills/scripts/run_paired.sh --ack-2x --profile L0 --max-sec 4500 \
  --model claude-haiku-4-5-20251001 --out runs/paired-haiku-L0

# pair a different armed stack against the baseline (e.g. strip-ephemeral only):
.skills/scripts/run_paired.sh --ack-2x --primary-arm A4 --profile L0 --turns 50 \
  --model claude-haiku-4-5-20251001
```

## Options

- `--primary-arm A1..A5` — armed stack the PRIMARY applies (default `A5`).
  `A0` is rejected (both arms passthrough is meaningless).
- `--profile L0|L1|L2|L3|L4` — inter-turn gap regime (default `L0`).
- `--gap-sec N` — fixed inter-turn gap; overrides `--profile`'s range.
- `--max-sec N` — cap the run by wall clock (e.g. `4500` = 75 min); `--turns`
  becomes an upper safety bound.
- `--turns N` — turns to drive (default `8`; ≥200 for a headline; remember
  each turn bills **twice**).
- `--model ID` — pin claude's model (cost control; e.g.
  `claude-haiku-4-5-20251001`).
- `--effort low|medium|high|xhigh|max` — pin claude's reasoning level
  (`claude --effort`). Resizes the cached thinking blocks, so it shifts the
  cache economics. Haiku has no effort control; `xhigh` is Opus 4.7/4.8 only.
- `--prompts PATH` — pty prompt file (default `benchmark/prompts/coding.txt`).
- `--settle-sec N` / `--confirm-sec N` — pty quiescence / submit-confirm
  windows (bump `--confirm-sec` for slower models, e.g. Opus).
- `--host` / `--listen-port` / `--primary-port` / `--shadow-port` — bind
  host and the three ports (default `127.0.0.1`, `8788` / `8790` / `8791`).
  Point claude (the driver does) at `--listen-port`.
- `--out DIR` — output dir (default `runs/paired-<timestamp>`).
- `--ack-2x` — acknowledge the ~2x token cost (**required** to run).
- `--no-plot` — skip chart rendering.

## Outputs

In the `--out` directory:

- `A0.ndjson` — SHADOW (baseline) turn-log, the authoritative paired record.
- `<primary-arm>.ndjson` (e.g. `A5.ndjson`) — PRIMARY (armed) paired record.
- `instance.A0.ndjson` / `instance.<arm>.ndjson` — each clawback instance's
  OWN `--turn-log`, a cross-check (their numbers should agree with the tee's).
- `proxy.primary.log` / `proxy.shadow.log` / `tee.log` — process logs.
- `state.primary.json` / `state.shadow.json` — each instance's seeded state.
- `report.md`, `report.csv`, `summary.json`, `manifest.json` — analyzer
  outputs; the turn-matched reclaim headline is at the top of `report.md`.
- `charts/` — the four §9 charts (`.skills/plot`).

Read the headline with `sed -n '1,40p' <out>/report.md`.

## Where this sits

`.skills/ab` runs arms **serially as separate sessions** (good for many arms
and fragmentation, with each arm isolated by its own `--state` file + natural
ANTHROPIC-KEY divergence). **This** skill runs **two arms concurrently off one
session** for an exact turn-matched pair (good for a tight reclaim CI), at ~2x
cost. Both call `.skills/{drive,bench,plot}` for the
load, analysis, and charts. Capture a fixture once with `.skills/capture` if
you also want a replay arm (this skill is pty-only — it drives real claude).
```
