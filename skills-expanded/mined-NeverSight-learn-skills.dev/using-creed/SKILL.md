---
name: using-creed
description: "Use when starting any conversation in a Creed-enabled workspace — install/detect Creed skills, then route to the right skill by scenario. Read this before creative, test, debug, or ship work."
---

# Using Creed

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, ignore this skill.
</SUBAGENT-STOP>

## When to use this skill

- Session start in a Creed workspace
- Unsure which Creed skill applies
- First use / companion skills may be missing
- Before creative, test, debug, or ship work — pick the right skill first

## Quick Start (install)

Companion skills are required — `using-creed` alone is not enough:

```bash
npx skills add Gusen1453/creed
```

## Detect install

Required skills: `grill`, `solid`, `write-plan`, `tdd`, `test-design`, `debug`, `review`, `commit-and-push`.

If any are missing from the workspace skill list: **stop and ask the user to run the install command above** before doing the work. Do not invent Creed workflows from memory.

## How to use

1. Match the task to a skill in the map below.
2. Announce `Using <skill> to …`, read that skill, follow it.
3. If it has a checklist, one todo per item.
4. When several apply, follow the default flow:

```
using-creed
  → grill → solid → write-plan
  → tdd (+ test-design)
  → debug? → review → commit-and-push
```

## Skill map (scenarios)

| Situation | Skill |
|-----------|--------|
| New feature / behavior change / architecture / "grill me" / brainstorm — before any code | **grill** |
| Module boundaries, dependency direction, API shape, tests need many mocks | **solid** |
| Approved design or clear requirements → break multi-step work into tasks | **write-plan** |
| Writing production code (feature / bugfix / refactor) | **tdd** |
| Writing or reviewing tests: worth testing? unit vs integration? what to assert / mock? | **test-design** |
| Bug, test/CI failure, unexpected behavior, or about to claim "fixed" | **debug** |
| Finished a task slice / before opening or updating a PR | **review** |
| User asks to commit / push / open a PR (PR needs a Test plan) | **commit-and-push** |

Common pairings:

- **tdd + test-design** — tdd is the rhythm (test first, watch it fail); test-design decides what to feed, assert, and mock. Use both when implementing.
- **debug → tdd** — bug fixes: root cause with evidence first, then a failing regression test.
- **grill + solid** — apply solid during grill's architecture/interface sections.

## Checklist

- [ ] Companion Creed skills installed (else → Quick Start)
- [ ] Relevant Creed skill identified (or consciously N/A)
- [ ] Skill read/followed; announced
