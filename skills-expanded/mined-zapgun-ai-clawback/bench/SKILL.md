---
name: bench
description: Analyze clawback turn-logs (NDJSON) to compare treatment vs passthrough arms. Produces report.md, report.csv, summary.json, manifest.json. Headline is billable input tokens reclaimed per turn (full-rate quota saved, no pricing) with a bootstrap 95% CI; per-turn $ and hit-rate are a demoted cost appendix, all stratified by inter-turn gap bucket. Use after the operator has collected counter-balanced windows.
---

# clawback benchmark analyzer

Analyze per-turn NDJSON logs emitted by a running clawback proxy.

## Usage

```bash
node benchmark/bin/analyze.js --out runs/report-$(date +%s) <turn-log-path>...
```

Inputs may be individual `.ndjson` files or directories containing them.
Each record's `arm` field determines whether it counts as treatment,
passthrough, or `treatment-ping` (keep-alive overhead).

## Inputs

Turn-logs are produced by clawback when started with `--turn-log <path>`:

```bash
clawback --turn-log ./runs/turns.ndjson ...          # treatment
clawback --turn-log ./runs/turns.ndjson --passthrough ...   # baseline
```

Both arms write to the same file — arm label is embedded per record.

## Outputs

Written to the `--out` directory:

- `report.md` — leads with the **billable input tokens reclaimed vs
  passthrough** headline (per-turn rate + bootstrap CI; full-rate quota
  clawback keeps off your bill — no pricing). The `$`/turn cost detail is
  a demoted appendix below it. Then two diagnostic sections:
  - **Prefix fragmentation** — distinct clawback SESSION KEYs seen per
    stable system prefix, per knobProfile. `1` = one logical context maps
    to one Anthropic cache key (ideal); `>1` (flagged ⚠️) means the same
    context was split across keys, each cold-starting Anthropic's cache —
    strip-ephemeral collapses this toward 1. This is the headline finding
    on hot loops where passthrough fragments but the stack does not.
  - **Keep-alive ping coverage** — share of turns preceded by ≥1
    `treatment-ping` during the gap, plus mean pings/turn. High coverage
    on a >5-min gap bucket alongside a high hit rate is keep-alive
    keeping the cache warm (the 15-min warmth test). Renders
    only when the log carries ping records.
- `report.csv` — turn-level rows for downstream plotting. Includes
  `pingsSincePrevTurn` and `msSinceLastPing` per turn (ping coverage),
  alongside `gapMs`/`gapBucket` and the priced `usd_estimate`.
- `summary.json` — machine-readable aggregates; the top-level `tokens`
  block is the headline (baseline vs treatment billable totals + mean
  per-turn, `reclaimedPerTurn` + CI, `pctLessPerTurn`,
  `reclaimedTotalIsProjected`). The `prefixFragmentation` array carries
  the per-prefix key counts, and each arm stratum carries
  `meanPingsSincePrevTurn` + `pingCoverageShare`.
- `manifest.json` — input file list, pricing hash, clawback version,
  wall-clock coverage per arm.

All gap, ping-coverage, and fragmentation metrics are derived
analyzer-side from the existing turn-log fields (`ts`, `sessionKey`,
`systemStableKey`, and the `treatment-ping` records) — no proxy change
is needed to collect them.

## Reproducibility

Bootstrap CIs use a seeded PRNG; rerunning on the same inputs yields
byte-identical reports (ignoring `generatedAt` timestamps).

## When to use

- After an operator has run treatment/passthrough windows (≥ 200 turns
  per arm, ideally across multiple days).
- To generate the `report.md` that's committed alongside the study.
- To regenerate historical reports when pricing updates (use the
  pricing-hash field in `manifest.json` to detect drift).
