---
name: claim-trace
description: Cross-check every number in a paper, report, or README against the run artifacts it should have come from, and flag the ones with no source. Use before submitting or publishing anything containing results, after re-running experiments, when a results directory has been regenerated, and when asked to verify or audit reported figures. Runs scripts/trace_claims.py.
---

# claim-trace

Numbers in a paper drift from the runs that produced them. A figure gets updated, a table does not. An experiment is re-run and the abstract still quotes the old value. Checking by hand means holding a results tree and a manuscript in your head at once, which is exactly the job to hand to a script.

## Order of operations

```bash
python <skill>/scripts/trace_claims.py paper/main.tex --results results/2026-07-12
```

Start with the precise claims, they carry the most risk and the clearest signal:

```bash
python <skill>/scripts/trace_claims.py paper/main.tex --min-decimals 3
```

Then widen to `--min-decimals 2` and `--include-integers` if you want full coverage.

## Reading the three classes

**untraced** is the finding that matters. No artifact value rounds to this number at the precision it is written. It came from a run that is not in this directory, or it was typed by hand, or it is stale. Check every one.

**traced** means few enough artifact values match that the match is real provenance. The named files are where the number came from. This is the class you want your headline numbers in.

**ambiguous** means the number matched, but so did many other artifact values. A results tree holds tens of thousands of numbers, so at two decimal places something always rounds to whatever you name. A count of 2243 matching values is coincidence, not evidence.

Ambiguous is not a failure and does not fail the exit code. It means the check could not tell you anything, which is worth knowing.

## Making claims traceable

The reason so many numbers land in ambiguous is precision. `0.02` cannot be pinned to a source in a tree of forty thousand numbers. `0.0217` can.

Report enough significant figures that the number is unique to its run. This makes the paper more checkable for a reviewer for the same reason it makes it checkable here.

For a headline number, keep the path: name the artifact file in a comment next to the value, or in the table caption. A number whose source is written down never needs tracing again.

## Scope and limits

The script reads CSV, TSV, JSON, Markdown, text, log, and YAML artifacts. It does not open plots, notebooks, or binary formats, so a number that exists only inside a PNG will read as untraced.

Percents match both ways: `84.7%` traces to an artifact value of `84.7` or of `0.847`.

It checks that a number exists in the artifacts. It does not check that the number means what the sentence around it says. A value correctly copied into the wrong claim still passes.

Exit code is 1 when anything is untraced, so this works as a pre-submission gate.

## When numbers change

After re-running experiments, run this before touching the manuscript. The untraced list is the edit list, and it is usually much shorter than a full re-read of the paper.

Pair it with [docs-sync](../docs-sync/SKILL.md) when the same numbers appear in a README or results summary.
