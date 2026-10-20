---
name: retrospective-writer
description: "Writes honest retrospectives at end of each sprint and at task cycle completion. Used by retrospective-author subagent (fresh context) for unbiased assessment. Captures numbers, what went well, didn't go well, lessons, action items."
---

# Retrospective Writer

Пишет честные retrospectives - sprint и task cycle level.

## Когда применять

- Phase 5.7 sprint cycle (после reviews)
- Phase N+1 task cycle (financial macro retrospective)
- Через subagent `retrospective-author` (fresh context)

## Why fresh context

Retrospective должен be **honest assessment**:
- Не self-promotional
- Не defensive about issues
- Acknowledges failures honestly

Fresh context subagent reduces bias toward defending what он же сделал.

## Two types

### Sprint-level retrospective

After each sprint closes:
- Specific to that sprint
- Time variance
- Issues encountered
- Lessons applicable to remaining sprints в same cycle

### Task cycle retrospective

After all sprints complete (final wrap-up):
- Macro view across all sprints
- Trends across sprints
- Overall task cycle assessment
- Recommendations для future similar tasks

## Sprint retrospective structure

Saved to `.sprints/active/retrospective-sprint-{N}.md`:

```markdown
# Sprint {{N}} Retrospective

**Sprint name**: {{NAME}}
**Goal**: {{GOAL}}
**Author**: retrospective-author subagent (fresh context)
**Date**: {{DATE}}

## Numbers

| Metric | Value |
|--------|-------|
| Goal achieved | {{yes / partial / no}} |
| Estimated time | {{N}} min |
| Actual time | {{M}} min |
| Variance | {{±%}} |
| Tasks total | {{N}} |
| Tasks done | {{X}} |
| Tasks skipped | {{Y}} |
| Tasks failed | {{Z}} |

## Reviews summary

| Review | Verdict | Issues |
|--------|---------|--------|
| Internal SE | {{verdict}} | {{N}} findings |
| External Codex | {{verdict or N/A}} | {{N}} findings |

## What went well

{{Specific things, не generic platitudes}}

Examples GOOD:
- "context-investigator correctly identified Django ORM patterns - decomposition matched conventions"
- "Test-first hook caught 2 attempts to write code without tests - prevented quality issues"

Examples BAD (avoid):
- "Communication was good" (vague)
- "Got things done" (generic)

## What didn't go well

{{Honest issues, не euphemisms}}

Examples GOOD:
- "pydeps Python 3.13 incompatibility cost 5 minutes before fallback to madge"
- "Sprint goal underestimated - 18 minutes actual vs 15 estimated (+20%)"
- "HANDOFF.md update was forgotten initially, blocked by gate"

## Lessons learned

{{Actionable lessons}}

Examples GOOD:
- "Detect Python version в context-investigator before tool selection"
- "Cap sprint at 4 tasks if все Mх effort - 5 was too many"
- "Always run `/sprint:checkin` for HANDOFF update, не только после code work"

## Action items

{{Specific, owned tasks}}

- [ ] Update language-detector to check Python version (next cycle)
- [ ] Adjust sprint-planner heuristic for max tasks (configuration change)
- [ ] Add automated HANDOFF reminder в pre-tool-use-checkin hook (v0.2 work)

## For HANDOFF.md

{{2-3 sentence summary for HANDOFF}}

Sprint 1 completed audit phase architecture analysis. Key insight: pydeps 
incompatible with Python 3.13, switched to madge for JS analysis. 
Architecture findings: 3 HIGH severity issues identified.
```

## Task cycle retrospective structure

Saved to `.sprints/active/retrospective-task-cycle.md`:

```markdown
# Task Cycle Retrospective: {{TASK_NAME}}

**Started**: {{DATE_START}}
**Completed**: {{DATE_END}}
**Total duration**: {{DURATION}}
**Author**: retrospective-author subagent (fresh context)

## Cycle metrics

| Metric | Value |
|--------|-------|
| Sprints | {{N}} |
| Sprints passed | {{X}} |
| Sprints with issues | {{Y}} |
| Tasks total | {{M}} |
| Tasks done | {{P}} |
| Total time | {{ACTUAL}} |
| Estimated time | {{ESTIMATED}} |
| Variance | {{±%}} |

## Sprint-by-sprint summary

| Sprint | Goal achievement | Time variance | SE verdict | Codex verdict |
|--------|------------------|---------------|------------|---------------|
| 1 | {{achievement}} | {{±%}} | {{V}} | {{V}} |
| 2 | ... | ... | ... | ... |

## Cross-sprint trends

What patterns emerged across sprints?

- "Time estimates too optimistic in 3 of 4 sprints (avg +25%)"
- "context-investigator runs slower than expected - average 90s vs 60s estimate"
- "Test-first violations attempted в 2 sprints (both blocked successfully)"

## Major findings (across all sprints)

{{Aggregated findings от all SE reviews}}

## Recommendations для similar future tasks

{{What to do differently}}

- "Adjust time estimates +25% baseline для audit-type tasks"
- "Run quick context investigation pre-decomposition rather than within decomposition"
- "Consider mutation testing in deep mode только - too slow for standard"

## Action items

{{Cross-cycle improvements}}

- [ ] Update default config с adjusted time estimate baselines
- [ ] Add fast-path для re-runs (skip context investigation if cached)
- [ ] Document which depth modes use mutation testing

## Final HANDOFF.md update

{{Executive summary text для appending to HANDOFF.md}}

Full SDLC audit task completed успешно. 4 sprints all PASSED. 47 findings 
produced (3 BLOCKER, 8 CRITICAL, 15 HIGH, 16 MEDIUM, 5 LOW). HTML report 
available at .sprints/archive/2026-04-30-1432/report.html. Recommended 
next steps: address BLOCKER findings первый, then prioritize CRITICAL by 
business impact.
```

## Honesty self-check

Перед finalizing retrospective - subagent self-checks:

```python
def honesty_check(retrospective):
    checks = {
        'numbers_match_state': numbers_match_execution_log(retro.numbers, state),
        'issues_specific': not has_only_vague_issues(retro.issues),
        'lessons_actionable': all_lessons_have_actions(retro.lessons),
        'no_blame': not blames_external_factors_for_internal_issues(retro),
    }
    return checks
```

If self-check fails - revise retrospective, не release.

## Failure modes in retrospective writing

### Defensive retrospective

Pattern: Avoiding own mistakes, blaming external factors.

Example BAD:
- "Sprint took longer because tools were slow" (external blame)

Example GOOD:
- "Tool failures cost 5 min - should have version-checked first (internal lesson)"

### Generic platitudes

Pattern: "Things went well, learning happened" - no specifics.

Self-check flag: count specific references (file names, task IDs, specific events). If <5 - too generic.

### Over-positive

Pattern: Not acknowledging real issues.

Cross-check with: SE review findings, hook BLOCKs that occurred, time variance >20%. If retrospective says "all great" but data shows issues - flag.

## Output

Retrospective saved.
Action items added to:
- HANDOFF.md (action items для next cycle)
- `.sprints/active/_action-items.md` (tracker для cycle)

For task cycle retrospective: also generates HANDOFF.md executive summary.
