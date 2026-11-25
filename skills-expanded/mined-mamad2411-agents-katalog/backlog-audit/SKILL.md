---
name: backlog-audit
description: "Audit a backlog against the requirement register and the delivery conventions. Use when the user asks whether the backlog is complete, traceable or trustworthy, wants to know if scope is covered, inherits a board they did not build, or before a milestone or client review. Writes nothing."
---

# Backlog Audit

Read the register and the board, report what is wrong, change nothing.

Writing nothing is the point. An audit that fixes as it goes reports a clean board and leaves nobody able to say what was wrong with it, and the finding is usually more valuable than the fix: a Feature holding one story is a grooming conversation, not a silent edit.

Read `docs/delivery/requirements.md`, `docs/agents/backlog-conventions.md` and `docs/agents/delivery-tracker.md`. Where the register is missing, say so and audit what can be audited: structure, readiness and the graph do not need it, and traceability is the only section that goes dark.

## The checks

Run all six. They are what you look for, not what you print: findings from every check land in the one severity-grouped report at the end, each item named once. Carry a count for every check and at most the ten worst items from each, with the remainder as a number.

### Traceability

- **Orphan requirements**: in the register, covered by no story. Contracted scope with nowhere to live. Every `Must` orphan is a finding on its own.
- **Gold-plating**: stories citing no requirement. Either the register is thin or the work is unbilled invention.
- **Phantom citations**: a story citing a requirement ID that is not in the register.

### Structure

- **Echoes**: a Feature holding one story that restates it. Report the pair side by side and let the titles make the case.
- **Thin Features**: fewer than three stories. Some are legitimately atomic; the count is the flag, not the verdict.
- **Fat Features**: more than seven.
- **Orphan items**: a story with no Feature, a Feature with no Epic.
- **Code collisions and gaps**: a hierarchy code used twice, or a number missing from a sequence, which usually means a deleted item that something still references.
- **Convention drift**: a title with no code, a Feature repeating its Epic's name, acceptance criteria sitting in the body.

### Readiness

- Stories with no acceptance criteria, or criteria not in `Given … when … then …` form.
- Stories with no estimate, or estimated above 8.
- Stories with fewer than the conventions' body sections.

### The graph

- **Cycles**. Report the ring.
- **Isolated stories**: no edges either way. Some are genuinely independent; a cluster of them means the graph was never swept.
- **Over-linking**: a story blocked by more than about five others is usually carrying edges that are sequencing preference rather than a gate.
- **Schedule violations**: a story scheduled at or before a blocker's sprint. The most actionable finding in the audit, because it is a plan that cannot execute as written.
- **External dependencies** past their needed-by date.

### Tags

- Tags outside the conventions' dimensions.
- A dimension with a suspiciously wide value set. Fifteen values where the conventions imply five usually means the same concept was named from several surfaces, which makes the dimension unqueryable.
- **Sprint drift**: a `Sprint:` tag disagreeing with the item's iteration field. Expected, since the tag is derived and the field is dragged; report the count and the fix rather than treating each as a defect.

### Schedule

- Sprints committed above the plan's velocity.
- Milestones whose carrying stories are not all scheduled before the milestone date.
- Stories in a closed sprint that are not Done.

## Report

One report, grouped by severity rather than by check, because what blocks delivery outranks what is untidy. Lead with a line per check: its name, its count, and `clean` where it is clean. Then the items:

1. **Blocking**: cycles, schedule violations, `Must` orphans, unready stories in the current sprint.
2. **Risk**: thin coverage, over-linked chains, external dependencies running late, milestones without full carrying sets.
3. **Hygiene**: convention drift, tag drift, missing estimates outside the committed scope.

Close with **where to rejoin the chain**, one line, because the finding list is only useful if it turns into a next action:

| Finding | Rejoin at |
|---|---|
| No register, or orphan requirements | `/ingest-requirements` |
| Missing coverage, wrong hierarchy | `/shape-backlog` |
| Echoes, thin Features, unready stories | `/groom-stories` |
| Cycles, isolated stories, missing edges | `/map-dependencies` |
| Schedule violations, milestone gaps | `/plan-release` |
| Overcommitted or stale current sprint | `/plan-sprint` |

## Done when

- All six checks ran, including the ones that came back clean, and the clean ones are named as clean.
- Findings are grouped by severity with specific items, not counts alone, and no item is reported twice.
- Every check contributed a count line, including the clean ones.
- The rejoin line is stated.
- Nothing on the board or on disk changed.
