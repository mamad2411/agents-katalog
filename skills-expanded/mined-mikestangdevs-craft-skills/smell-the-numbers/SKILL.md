---
name: smell-the-numbers
description: "Use when code produces output someone will read — a report, metric, chart, or calculation — and a result is surprising, suspiciously clean, or just changed a lot. Implausible values (all zeros, a value past its physical limit, a metric that moved 40x) are root-caused at the source, never clamped, hidden, or smoothed in the display."
---

# Smell the Numbers

## The failure mode this fixes

The code runs, the page renders, the report generates — and the numbers are nonsense. A line carrying 1858% of its rated capacity. A formula panel showing all zeros. A `-0` in a financial summary. A KPI that moved 40x between runs of "the same" scenario. Agents (and tired humans) accept these because the *mechanism* worked: no exception, no red test, output produced. "It runs" gets mistaken for "it's right."

The worse version is the cosmetic fix: clamp the value, hide the row, round the -0, smooth the curve — make the output *look* plausible while the defect underneath keeps feeding everything else. That converts a visible bug into an invisible one.

This skill installs the domain-expert reflex: read the output the way someone who knows the territory would, flag everything that contradicts physical limits, business reality, or its own history — and treat each flag as a root-cause investigation, not a display problem.

## When to Use This Skill

- Output just changed significantly after a refactor, migration, or "no-behavior-change" cleanup
- A result is surprising in either direction — catastrophic where success was expected, or suspiciously perfect
- You see sentinel smells: zeros where work happened, -0, NaN leaking into display, values exceeding a hard limit, percentages outside [0,100], totals that don't sum
- A metric moved by an order of magnitude with no input change that explains it
- You're about to show the output to someone who will make a decision from it

**Don't use when:** the output has no ground truth to compare against and no internal consistency to violate (pure creative output). Don't let it become paralysis — the skill is a screen, not a proof of correctness for every digit.

## Instructions

### 1. Read the output as the skeptic, not the author

Before celebrating that output exists, actually read it. Ask the questions a domain reviewer would: Is this physically/financially/logically possible? Does it match the order of magnitude I'd estimate on a napkin? Is it consistent with the last known-good run? Do the parts sum to the whole?

### 2. Rank surprise as evidence

A surprising result has exactly three explanations, in descending likelihood: (1) a bug in the code, (2) a defect in the input data, (3) reality is genuinely surprising. Investigate in that order. "The strongest system in the fleet just failed the easiest scenario" is a bug report, not a finding — until the trace proves otherwise.

### 3. Trace one bad number all the way down

Pick the most implausible value and follow it backwards through the computation to the first place it goes wrong: the formula, the unit conversion, the field that was a calendar year where the math wanted a duration, the aggregation that double-counted. Fix at the source. One fully-traced number teaches you more than ten re-runs.

### 4. Never fix the display

If the investigation surfaces pressure to clamp, hide, filter, smooth, or reformat the bad value — that's the moment you're about to convert a loud bug into a silent one. The display gets fixed only after the underlying number is right. (Legitimate display issues exist — a -0 from float formatting *after* the value is verified correct — but earn that conclusion with the trace, don't assume it.)

### 5. Ask what else this poisoned

A wrong number rarely stays in its cell. The same broken conversion feeds the chart, the summary, the export, the downstream model. Once root-caused, sweep for every consumer of the defective path before declaring the incident closed.

## Output format

```
Output plausibility check: <what was reviewed>
Smells found: <list — value, why it's implausible (limit/history/consistency violated)>
Root cause: <the first wrong step in the chain, for each smell traced>
Classification: code bug / data defect / genuinely surprising (with proof)
Fix: <at-source fix; explicitly NOT a display change>
Blast radius: <other outputs fed by the same defect, checked>
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| "It runs" = "it's right" | accepting output because no exception fired. |
| Cosmetic correction | clamping, hiding, or smoothing the symptom; the dashboard heals, the model stays sick. |
| Surprise worship | writing a narrative for why the shocking result might be true, before checking whether it's a unit error. |
| Re-run roulette | running it again hoping for better numbers instead of tracing the bad one. |
| Celebrating the suspiciously clean | zero variance, perfect curves, and exact round totals are smells too. |

## Mental Model

> Every output number is a witness testifying about your code. When a witness says something impossible, you don't transcribe it neatly into the record — you cross-examine until you know why they said it.
