---
name: calibrate-first
description: Use when testing whether a trading signal, factor or backtest result is real. Trigger on "backtest", "factor", "IC", "does this signal work", "is this significant", "alpha", "edge", or any request to judge a quantitative trading result. Runs assay-lite so that the detection floor is measured before any result is read, every test is pre-registered, and "too small to see" is never reported as "no effect".
---

# Calibrate first

A result is only as good as the instrument that produced it. This skill makes the
instrument measure itself before it measures anything else.

**Where the tool is.** The commands below assume `assay_lite.py` is in the current
directory. If it isn't, and this skill was installed as a plugin, run the copy that
ships with the plugin: `uv run "${CLAUDE_PLUGIN_ROOT}/assay_lite.py" ...`. If neither
exists, ask the user to download `assay_lite.py` from
https://github.com/assaylabdesk-sudo/assay-lite. Don't rewrite it. Keep `--home`
pointed at a folder in the user's project, so the registry belongs to them and not
to the plugin cache.

## The four rules

1. **Run `floor` before interpreting any result.** Every dataset has a smallest
   effect it can see. Until that floor is measured for these prices and this
   horizon, a non-significant result means nothing either way.

   ```bash
   uv run assay_lite.py floor --prices prices.csv --horizon 1
   ```

2. **Never compare p with a conventional 0.05; the only bars are the ones the
   registry prints.** The bar is 0.05 divided by every trial ever charged in this
   registry, so the first trial's bar is 0.05 and every later one is stricter.
   Read it from `test` ("this trial (#N) faces") or `registry` ("bar for the last
   trial charged" and "the NEXT test will face" are two different bars; quote the
   one that matches the question). Do not quote a bar from memory: it changes every
   time a test runs.

3. **Trials are never refunded.** `test` writes the trial to the registry before
   it computes anything. Re-running the same signal, tweaking a parameter, or
   trying a second horizon is a new trial and tightens the bar. Do not suggest
   deleting registry lines, using a fresh `--home` to escape the count, or
   re-running until something passes. Each of those is p-hacking.

4. **Below the floor is UNDECIDABLE, not "no effect".** If `test` reports
   UNDECIDABLE, say: the effect, if any, is smaller than the floor IC this data
   can detect. Never write "the signal doesn't work" for an UNDECIDABLE result.

## Procedure

1. Check the inputs: prices as `date,asset,close`; signal as `date,asset,signal`,
   where the signal on a date is known at that date's close.
2. Run `breadth` once and state the effective number of independent bets next to
   the asset count.
3. Run `floor` for the exact prices file and horizon you will test.
4. Before running `test`, write down in one sentence what you expect and why.
   Then run `test` once.
5. Report the verdict line verbatim, with the IC, p, the bar it faced, the
   dispersion ratio and the scaled floor IC. Then explain it using the meanings
   below.

## What the verdicts mean

| verdict | meaning | say this, not that |
|---|---|---|
| PASS | p is below the registry bar | "cleared the multiple-testing bar", not "proven" or "profitable" |
| UNDECIDABLE | below the floor, or no floor measured | "too small for this data to see", not "doesn't work" |
| FAIL | the effect is at least floor-sized but too inconsistent to clear the bar | "large but unreliable", not "zero" |

## Limits to state when relevant

Cross-sectional, daily data, Spearman IC only. No transaction costs, so a PASS
says nothing about profitability after costs. Bonferroni is conservative when
trials are correlated.

## Why the floor is per-signal

The floor is calibrated with noise that is fresh every day. A signal with factor
structure (sector tilts, slow-moving ranks) has a more dispersed daily IC, so the
same mean IC is harder to detect. `test` prints the ratio of the signal's daily-IC
spread to the calibration noise and scales the floor up by it, never down. When
you report a result, quote the scaled floor, not the calibrated one, and mention
the ratio when it is above 1: it says the signal has fewer independent bets than
the asset count suggests. In `demo`, the sector tilt (redrawn every 63 days, no
planted effect) prints 1.79, and the two planted signals print 0.98 and 1.01.
