---
name: gro-growth-experiment
version: 1.0.0
description: Run the ICE prioritization and experiment-spec process to pick and fully specify the next growth test.
author: matrixx0070
tags: [growth, experimentation, ice, prioritization, process]
capabilities: []
---

## When to use

Use this when you have more growth ideas than capacity and need a disciplined way to choose *what to test next* and write a spec anyone can execute. Reach for it to run a weekly growth cadence, triage a backlog, or turn a vague idea into a runnable experiment.

**Not for:** the statistical design of a single test once chosen (use gro-ab-test-design for MDE/sample size), or diagnosing where the problem is (gro-funnel-analysis / gro-retention-analysis feed this with ideas). This is the *pipeline*, not the stats.

## Method

1. Frame every idea as an experiment tied to ONE funnel metric and grounded in an insight ("data shows X, so try Y"). Reject ideas with no metric or no rationale.
2. Score each with ICE (1–10): Impact (if it works, how big?), Confidence (evidence it will work), Ease (effort to build+run). Decision point: score independently, then discuss — anchoring on one dimension distorts the rest. ICE score = average of the three.
3. Rank by ICE, then sanity-check the top: does it target your current biggest constraint? Reorder if a high-ICE idea addresses a non-bottleneck.
4. For the chosen idea, write the spec: hypothesis, primary metric, variant description, success criteria, and owner. Hand statistical sizing to gro-ab-test-design.
5. Set a fixed review cadence (weekly). Decision point: cap concurrent experiments so results stay attributable and traffic isn't split too thin.
6. On completion, log the result and the *learning* regardless of win/lose. Feed learnings back into Confidence scores of related ideas — the system compounds.

## Example

Backlog: (A) social proof on signup — I8 C6 E9 = 7.7; (B) new pricing page — I9 C4 E3 = 5.3; (C) email drip — I5 C7 E8 = 6.7. Rank A > C > B. Biggest constraint is activation, and A targets signup activation — proceed with A. Spec it, size via gro-ab-test-design, review Friday. Log: A won +3pp; raise Confidence on related social-proof ideas.

## Pitfalls

- Scoring Impact optimistically for pet ideas; require an evidence link for Confidence.
- Running 12 tests at once so nothing is attributable and every surface is contaminated.
- Only logging winners — losses carry the highest-value learning and stop repeat mistakes.
- Prioritizing high-ICE ideas that don't touch the current bottleneck (busywork with good scores).

## Output format

```
Growth backlog — week of <date>
Idea            Impact  Conf  Ease  ICE   Constraint fit
A <idea>          8      6     9    7.7   yes/no
B <idea>          9      4     3    5.3   yes/no
...
Chosen: <idea> (ICE <>, targets <bottleneck>)
Spec:
  Hypothesis: <because insight, change will move metric>
  Metric:     <primary>
  Variant:    <description>
  Success:    <criterion>  | Owner: <name>
  Sizing:     via gro-ab-test-design
Review cadence: weekly | Concurrent cap: <N>
Log: <result + learning → confidence updates>
```
