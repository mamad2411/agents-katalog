---
name: qa-exploratory-charter
version: 1.0.0
description: Design a time-boxed exploratory-testing charter with a clear mission, tours, and heuristics to find bugs scripted tests miss.
author: matrixx0070
tags: [qa, exploratory, charter, heuristics, tours]
capabilities: []
---

## When to use

When you want to find defects that scripted cases won't — usability gaps, edge interactions, "what happens if I..." bugs — under a focused mission and a timebox. A charter turns open-ended poking into disciplined, reportable exploration. Best for new features, gnarly areas, or pre-release confidence beyond the regression suite.

**Not for:** verifying a specific known requirement (write a test case), regression checks (see qa-regression-suite), or aimless clicking with no mission. Exploration without a charter is just clicking around; the charter is what makes it accountable.

## Method

1. **Write the mission** — one sentence naming target + purpose: "Explore the file-upload flow to discover failures in size, type, and network-interruption handling." Narrow enough to finish in one timebox.
2. **Set the timebox** — typically 60-90 minutes. Decision point: if the area is too big for one box, split into multiple charters rather than sprawling.
3. **Pick tours** to structure coverage: *Feature tour* (every control once), *Money tour* (anything touching value/transactions), *Landmark tour* (key screens in odd orders), *Antisocial tour* (invalid/hostile inputs), *Interruption tour* (kill network, background the app, double-submit).
4. **Load heuristics** to trigger ideas: boundaries (0, 1, max, max+1, negative, empty), CRUD consistency, "goldilocks" (too big/small/just right), consistency with rules and history.
5. **Explore and log continuously** — note bugs, questions, and new charter ideas as you go. Decision point: if you find a rich bug seam, spawn a follow-up charter instead of blowing the current timebox.
6. **Debrief:** summarize coverage, bugs found, areas not reached, and confidence.

## Example

```
Charter: Explore discount-code entry to find validation and stacking failures. Timebox 60m.
Tours: Money tour (totals), Antisocial tour (malformed codes).
Heuristics: boundaries (empty, 100-char code), stacking (2 codes), casing (LOWERcase).
Findings: BUG code field trims to 8 chars silently; QUESTION should stacked codes cap at cart total?
Not reached: gift-card interaction. Confidence: medium.
```

## Pitfalls

- **Mission too broad** — "test the app" can't be covered or debriefed; scope to one flow.
- **No notes** — you find a bug, forget the steps, can't reproduce. Log as you go.
- **Blowing the timebox** — chasing one bug for 3 hours; spawn a follow-up charter instead.
- **No debrief** — exploration with no summary teaches the team nothing about coverage or confidence.

## Output format

```
Charter mission: <target + purpose, one sentence>
Timebox: <minutes>   Tester: <name>
Tours: <feature/money/landmark/antisocial/interruption>
Heuristics to apply: <boundaries, CRUD, consistency, goldilocks...>
--- Session notes ---
Bugs found: <ref + one-line>
Questions raised: <open items for dev/PM>
New charter ideas: <follow-ups>
Areas not reached: <coverage gaps>
Confidence: <low/medium/high> + why
```
