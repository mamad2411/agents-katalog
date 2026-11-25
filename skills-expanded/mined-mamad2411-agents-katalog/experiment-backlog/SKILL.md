---
name: experiment-backlog
description: Generates a growth experiment backlog from the brief's evidence, ICE-scores it honestly, and designs the top five as minimum-viable tests with decision rules written before launch. Use when plenty is being done but nothing is being learned.
argument-hint: "[the metric to move + anything already tried]"
---

# Experiment Backlog — fewer bets, ranked, decided in advance

Most "testing" is activity wearing a lab coat. An experiment is only real once three things are written down before it runs: the hypothesis with its because, the smallest test that could falsify it, and the decision rule that fires when the result lands. This skill produces those — ranked, owned, and deliberately few.

## Inputs
- The metric to move, plus anything already tried and how it went: $ARGUMENTS
- From `marketing-brief.md` if present: numbers that matter (north star and drivers), channels & funnel with stage conversion numbers, top pains, objections & beliefs, and past learnings. The weakest funnel stage is the best hypothesis generator.

## Do this
1. **Anchor on the target metric** and find the weakest link feeding it in the brief's funnel numbers. Experiments aimed at the constraint beat experiments aimed at whatever is fashionable this month.
2. **Generate 15–20 candidates,** each written as: "We believe [change] will move [metric] because [observation or research]." No because, no backlog entry — a hunch gets upgraded by finding its evidence or gets cut.
3. **ICE-score honestly and show the table:**
   - **Impact** — how far the target metric moves if this wins.
   - **Confidence** — what evidence says it will. Enthusiasm scores a 1.
   - **Ease** — time and cost to a readable result.
   Sort by score. Note where two experiments would contaminate each other's read.
4. **Design the top five as minimum-viable tests:** the smallest version that produces a believable signal, what stays constant, the single success metric, and the rough sample or duration that signal needs — sanity maths, not false precision. Low-volume businesses read sales conversations and close rates, not dashboards.
5. **Write the decision rule for each before it runs:** "If X by [date or sample], scale it by doing Y. If not, kill it and start the next." No extending a test because the result hurt.
6. **Set the operating cadence:** how many run at once (one or two — parallel tests on the same audience muddy each other), the owner per test, and the weekly readout inside `/marketing:weekly-review`.

## Output
The full scored backlog table, then the top five as test cards — hypothesis, minimum-viable design, success metric, sample or duration, decision rule, owner, start date. Log the five live cards in `marketing-brief.md` (create a Learnings & experiments section if none exists) so every future session knows what is in flight.

## Rules
- Evidence over invention: confidence scores come from the brief or past results, never from how much the team likes the idea.
- One variable per test. Two changes that win together teach you nothing you can reuse.
- A test without a pre-written decision rule is a diary entry.
- Killing experiments is the system working. The backlog exists so stopping one thing never feels like stopping.
- Dead experiments get written down too. A kill nobody recorded is an experiment somebody reruns next quarter.
