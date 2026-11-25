---
name: vstack-scorecard
description: Turn vstack diagnose reports into a per-agent or per-fleet scorecard with letter grades, render it for humans, and compare two scorecards over time to catch regressions. Use to answer "is this agent fleet getting better or worse?" and to gate CI on agent-behavior quality.
---

# /vstack-scorecard

The reporting + regression-tracking skill. Individual patterns and `/vstack-diagnose` tell you what's wrong *right now*; this skill aggregates findings into a graded scorecard and tracks it across runs so you can prove the trend — and fail a build when behavior regresses.

## When to invoke

- "Grade this agent / fleet."
- "Are we getting better or worse over time?"
- "Set up a CI gate on agent behavior."
- After a batch of `/vstack-diagnose` runs, to roll them into one readout.
- Before/after a model upgrade, prompt rewrite, or framework swap, to quantify the delta.

If the user wants to diagnose a single trace, use `/vstack-diagnose`. If they want drift detection on raw pattern metrics (not graded), use `/vstack-baseline`. This skill is specifically about **letter-graded scorecards and regression gating**.

## Preflight

The scorecard is computed from one or more **diagnose reports** (the JSON that `/vstack-diagnose` / `vstack_diagnose` / `vstack-diagnose` produces). Surface:

- One or more saved report JSONs (a single run, or a batch across many traces).
- An identity to score against: `--agent-id` (one agent) or `--fleet-id` (a group).
- For trend tracking: the *previous* scorecard JSON to compare against.

If the user has no saved reports yet, run `/vstack-diagnose` first and save its JSON (`vstack-diagnose --trace … --json > report.json`), then come back here.

## Workflow

### Step 1 — Compute the scorecard

```bash
vstack-scorecard compute \
  --reports reports.json \          # a JSON list of DiagnoseReport(s), or {"reports": [...]}
  --agent-id booking-agent \        # or --fleet-id checkout-crew
  --title "Booking agent — week 24" \
  --out scorecard.json
```

The scorecard assigns letter grades **per dimension** (reasoning, coordination, trust, workload, culture) and **overall** — not per pattern. Individual patterns appear as per-pattern severity contributions (High / Med / Low counts + a score delta) that feed the dimension scores. Omit `--out` to print to stdout.

### Step 2 — Render it for a human

```bash
vstack-scorecard render scorecard.json --format markdown   # text | markdown | html
```

Use `markdown` for a PR comment or doc, `html` for a dashboard, `text` for a terminal readout.

### Step 3 — Compare against the last scorecard (trend + regressions)

```bash
vstack-scorecard compare baseline.json current.json --format markdown
```

To gate CI on it, add the failure thresholds — the command exits non-zero when a blocking regression is detected:

```bash
vstack-scorecard compare baseline.json current.json \
  --fail-on-regression \
  --fail-grade C \              # fail if overall grade drops to/below C
  --fail-score 10.0            # fail if the score drops by more than 10 points
```

### Step 4 — Synthesize

```
## Scorecard — <agent/fleet id>

**Overall grade:** <grade> (<score>/100)

**By dimension:** (worst three first)
- <dimension>: <grade> — <one-line reason>
- …

**Trend vs. <baseline date>:** <improved / held / regressed>, Δscore = <delta>
- Regressions: <dimension: grade A→C> (if any)
- Wins: <dimension: grade C→A> (if any)

**Verdict:** <one sentence — ship / hold / investigate>
**If gating CI:** the `compare --fail-on-regression` step exited <0 = pass | non-zero = blocked>.
```

Cap at ~300 words. Attach the scorecard + comparison JSON in a collapsible block.

## Failure modes

- **Reports JSON is a single object, not a list.** `compute` accepts either a bare list or `{"reports": [...]}`. If the user has one report, wrap it in a list.
- **No baseline scorecard exists yet.** First run establishes the baseline; tell the user there's nothing to compare against and to re-run after the next batch. Save this scorecard as the baseline.
- **`compare` flags a regression the user disagrees with.** Surface the per-dimension deltas verbatim — the grade drop is mechanical, not a judgment. The user decides whether the regression is acceptable; offer to re-baseline if it's an intended trade-off.
- **Reports came from `--client none` (deterministic only).** Every dimension is still graded, but dimensions that lean on LLM-detected patterns will have no findings to penalize them, so they score artificially high (A+ by default). Read deterministic-only scorecards as "no structural findings", not "verified healthy".

## Composition

- Upstream: `/vstack-diagnose` (produces the reports this skill grades), or a batch job that saved many reports.
- Downstream: nothing automatic. A regression routes the user back to `/vstack-diagnose` / `/vstack-post-incident` on the offending trace.
- Compose with: `/vstack-baseline` (raw-metric drift) for a fuller monitoring story — scorecards grade, baselines detect metric drift; together they cover both "what grade" and "what moved".

## What you don't do here

- Don't grade a single trace and call it a fleet verdict. One report is a snapshot; trends need batches.
- Don't set `--fail-on-regression` in CI without telling the user it will block merges — make the gating opt-in and explicit.
- Don't editorialize the grade. The scorecard is mechanical; present the number and the deltas, then let the user decide what's acceptable.
