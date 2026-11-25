---
name: plot
description: Render the tokens-saved chart from an analyzer output directory. Dependency-free SVG generator — reads summary.json + report.csv produced by benchmark/bin/analyze.js and emits TWO SVGs of the same cumulative billable-input story (passthrough baseline vs clawback, honest green/red shaded gap): tokens_saved.svg (labeled, titled "Token Efficiency", for on-screen) and tokens_saved.bg.svg (BARE 1200×630, lines + wedge only, no text — the share-card PNG background; without it the posted card has no chart lines). No cost/$/CI tables. Use after .skills/bench to produce the visuals that document the win.
---

# clawback chart renderer

Run `benchmark/bin/plot.js` from the project root. It reads an analyzer
**output directory** (the `--out` dir you gave `benchmark/bin/analyze.js`)
and writes TWO SVGs to a charts directory. No dependencies — pure Node + string
templating, so it runs anywhere clawback runs.

## Usage

```bash
node benchmark/bin/plot.js --in runs/smoke --out runs/smoke/charts
```

`--in` must contain `summary.json` and `report.csv` (run `.skills/bench`
first). The SVG is written to `--out`.

## Charts emitted

Both SVGs draw the **same** figure — **cumulative billable input tokens over
turns**, two lines (passthrough baseline vs clawback) with the gap between them
shaded. The shade is honest about direction: **green** when clawback's line ends
*below* passthrough (it spent fewer full-rate tokens — a real saving), **red**
when clawback ends *above* (it spent more — a regression we never hide). The
chart carries **no per-turn reclaim callout**; the report hero overlay owns that
figure now, so a chart copy would only collide with it.

- `tokens_saved.svg` — the **labeled, on-screen** chart: legend, axes, ticks,
  and the title **"Token Efficiency"**. This is what the report GUI shows.
- `tokens_saved.bg.svg` — the **BARE share-card background**: a 1200×630 white
  card with just the two lines + the filled wedge, **zero `<text>`**. The report
  GUI inlines this behind the scrim to build the downloadable / shareable PNG.
  **Missing it ⇒ the share PNG is a solid card with no chart lines.** (Backfill
  old runs that predate it with `.skills/finish --all`.)

One figure on purpose: the product story is "how many more tokens can you spend,
because clawback saves your quota" — not a dashboard of stats, and never a
dollar figure. **Billable input** = `input_tokens + cache_creation_input_tokens`
(the full-rate buckets); `cache_read` is the discounted reuse and is excluded.
Cost lives only in the analyzer's `report.md` appendix; it is never plotted.

## Honest-claim discipline

The win is conditional on idle gaps: on a tight loop the baseline caches well
too, so the gap trends to ~0 (no regression); it widens as gaps cross the
5-min / 60-min eviction boundaries. Read the chart by regime, never as one
context-free number.

## Reproducibility

The charts are a pure function of `summary.json` + `report.csv`; re-rendering
the same analyzer output yields byte-identical SVGs.
