---
name: lawstu-exam-forecast
version: 1.0.0
description: Forecast likely exam issues from the syllabus, professor emphasis, and past exams — then build a timed self-simulation plan.
author: matrixx0070
tags: [law-student, exam-prep, forecasting, issue-spotting, simulation]
capabilities: []
---

## When to use

Reach for this in the two weeks before a final when you want to study *predictively* — concentrating on the doctrines most likely tested and how the professor likes to test them. The skill helps you infer the exam's shape from signals you supply (syllabus weight, in-class emphasis, released past exams) and sets up timed self-simulations.

**Not for:** obtaining actual exam questions or answers, or any breach of exam security. It forecasts from *legitimately available* signals and drills *you* under time — it does not predict the specific graded prompt or write answers for it. Not for building the outline (see `lawstu-outline-builder`) or generic bar drills (see `lawstu-bar-prep-questions`).

## Method

1. **Weight the syllabus.** Rank doctrines by class time spent — coverage roughly tracks testing. Decision point: a doctrine with heavy time but no obvious hypo is a sleeper issue; flag it.
2. **Read professor signals.** "This is heavily tested," repeated hypotheticals, and pet policy debates are tells. Note the exam *format* (issue-spotter, policy essay, short answer).
3. **Mine past exams** if released — recurring fact patterns, favored crossover issues, and question style.
4. **Map crossover issues.** Professors love hypos that braid two doctrines; list plausible pairings.
5. **Build a timed simulation plan.** Draft your own practice hypos in the professor's style, then write full IRAC answers on the clock.
6. **Self-score against your outline's rubric** and re-target weak doctrines.

## Example

Contracts professor spent three weeks on remedies and repeatedly hypothesized construction-contract breaches. Forecast: an issue-spotter braiding expectation damages with mitigation and a UCC/common-law choice-of-law wrinkle. You draft a matching hypo, write it in 60 minutes, and discover your mitigation analysis is thin — exactly what to shore up.

## Pitfalls

- Betting everything on one predicted issue; forecasts hedge, they don't gamble.
- Ignoring low-time doctrines that make cheap short-answer points.
- Practicing untimed, then blowing the clock on the real exam.
- Confusing "likely tested" with "known question" — never assume you have the actual prompt.

## Output format

```
Course | exam format | date
Doctrine forecast (ranked): doctrine | signal | confidence
Crossover pairings: [doctrine + doctrine]
Self-simulation plan:
  practice hypo (your draft, professor's style) | time budget
Post-sim scoring: weak doctrines → re-target
```

## Reference

- **IRAC / issue-spotting:** most law finals are issue-spotters graded on breadth plus two-sided application (`lawstu-irac-practice`).
- **Outline** supplies the rubric you self-score against (`lawstu-outline-builder`).
- **Bar framing:** predictive, timed practice mirrors MBE/essay conditioning (`lawstu-bar-prep-questions`).
