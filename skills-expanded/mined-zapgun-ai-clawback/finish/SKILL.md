---
name: finish
description: Turn a benchmark turn-log (or an already-analyzed run dir) into a report the GUI shows right away — runs analyze + plot so summary.json + report.csv AND charts/tokens_saved.svg + charts/tokens_saved.bg.svg all exist. The bare .bg.svg is the share-card PNG background; without it the downloaded/posted card has no chart lines. Also backfills old runs (--all) that predate the .bg.svg output. Use after a manual analyze, or to repair runs whose share PNG renders as a solid card. Pass --card to also bake the share-card PNG to disk (opt-in, best-effort).
---

# clawback finish-run (report generation for the GUI)

Run `.skills/finish/scripts/finish_run.sh` from the project root. It produces the exact files
the report server serves for a run, so the run appears complete in the GUI with
a share PNG that actually carries the chart.

A run is GUI-complete when its directory under the report root (config.reportDir,
default `./runs`) holds:

- `summary.json` + `report.csv` — analyzer output (the hero figures + CSV).
- `charts/tokens_saved.svg` — the labeled on-screen chart.
- `charts/tokens_saved.bg.svg` — the BARE share-card background. The report
  GUI inlines this behind the scrim to make the downloadable / shareable PNG.
  **Missing it ⇒ the PNG is a solid card with no chart lines.**

`run_paired.sh` and `ab_block.sh` already run analyze + plot at the end of a
complete (both-arm) run, so a normal benchmark is finished automatically. Reach
for this skill for a manual analyze, a single-step re-plot, or a backfill.

## Usage

```bash
# Analyze fresh turn-logs into a run dir, then plot both SVGs:
.skills/finish/scripts/finish_run.sh runs/my-run runs/A0.ndjson runs/A5.ndjson

# Re-plot a run that already has summary.json + report.csv (adds .bg.svg):
.skills/finish/scripts/finish_run.sh runs/my-run

# Backfill EVERY run under the root that's missing its bare background:
.skills/finish/scripts/finish_run.sh --all
.skills/finish/scripts/finish_run.sh --all --root runs

# Also bake the social share card to disk (opt-in; PNG is best-effort):
.skills/finish/scripts/finish_run.sh runs/my-run --card
.skills/finish/scripts/finish_run.sh --all --card
```

## Backfill is safe and idempotent

Re-plot is a pure function of `summary.json` + `report.csv`: it never
re-spends tokens, never re-reads turn-logs, and `--all` skips any run that
already has `charts/tokens_saved.bg.svg`. So running `--all` repeatedly only
fills the gaps and is byte-identical for runs already complete.

## Bake the social share card (`--card`, opt-in)

By default `finish_run.sh` stops at the SVGs. The share PNG is rendered on
demand, client-side, when someone hits **Download/Share** in the report GUI —
so the pipeline never hard-depends on a headless browser, and the browser is
the faithful renderer. Pass `--card` to *also* bake `charts/share_card.{svg,png}`
to disk right now, for posting a card without opening the GUI:

```bash
.skills/finish/scripts/finish_run.sh runs/my-run --card     # one run
.skills/finish/scripts/finish_run.sh --all --card           # every run missing a PNG
```

`--card` delegates to `.skills/scripts/preview_card.sh`, which walks a best-effort
raster ladder — headless Chrome (faithful 1200×630) → macOS `sips` (degraded:
drops the text blur, so the headline is bedded on a scrim) → SVG-only no-op when
neither is present. A missing rasterizer leaves `share_card.svg` and skips the
PNG; it never fails the run. The `--all --card` backfill skips runs that already
have `share_card.png`, staying as cheap and idempotent as the re-plot backfill.
The same `--card` flag is on `run_paired.sh` and `ab_block.sh`, baking the card
at the tail of a full both-arm run.

## When a run can't be finished

`--all` skips (with a note, without aborting) any directory lacking
`summary.json` + `report.csv` — e.g. an aborted run, or one whose analyzer
output was never written. Analyze it first (supply its turn-logs as extra
arguments) and the plot step follows automatically.
