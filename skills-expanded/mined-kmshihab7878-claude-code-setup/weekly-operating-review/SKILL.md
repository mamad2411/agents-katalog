---
name: weekly-operating-review
description: Friday weekly OS health pass. Runs /audit, then /level-up, then refreshes kb/wiki/_hot.md from current state. Single command instead of three. Logs the run. Does not build artifacts.
disable-model-invocation: true
---

# /weekly-operating-review — Friday Pulse

> The Friday weekly cadence in one skill. Adapted from AIS-OS weekly improvement loop.

## When to use
- Friday afternoon (or whenever your week ends)
- Weekly cadence, no exceptions for 90+ days

## When NOT to use
- Mid-week ("I'll just do a quick review") — defeats the trend
- Daily — that's `/daily-plan` + `/end-of-day-review`

## Inputs
- Last 7 days of `decisions/log.md`
- Last 7 days of `~/.claude/usage.jsonl` (if exists)
- Most recent `docs/audits/*.md`
- Current `context/Priorities.md`

## Outputs
- A new audit report (via `/audit`)
- A `/level-up` recommendation logged in `decisions/log.md`
- A refreshed `kb/wiki/_hot.md`
- One end-of-week entry in `decisions/log.md`

## Steps

### 1. Pre-flight
- `git status --short` — flag dirty state
- Read most recent audit; note total score
- Read most recent `/level-up` entry; note whether the recommended artifact was built

### 2. Run `/audit`
Invoke the `audit` skill. Capture: total score, top 3 gaps, recommended next action.

### 3. Run `/level-up`
Use the audit's top gap as the constraint. Walk the 5 questions. Land on one artifact.

### 4. Refresh `kb/wiki/_hot.md`

Re-derive each section:
- **This week's focus** ← `context/Priorities.md` "this week" + audit's top gap
- **Active decisions in play** ← `decisions/log.md` last 7 days, status `Active` or `Planned`
- **Open candidates from /level-up** ← `decisions/log.md` `Type: <skill|script|...>` entries with `Status: Planned` and not yet built
- **Hot wiki articles** ← inspect `kb/wiki/log.md` for articles touched in last 7 days; pick top 5 by relevance to focus
- **Active connections at risk** ← `connections.md` rows with `Status: auth pending|paused`
- **Leverage gap of the week** ← audit's top gap (one sentence)

Write the file. Update `last-updated:` to today.

### 5. Log the weekly review

```markdown
## YYYY-MM-DD — Weekly operating review

**Audit total:** X/100 (Δ from last: ±Y)
**Top gap:** <one line from audit>
**Level-up recommendation:** <artifact + why>
**Hot cache refreshed:** yes
**Status:** Reflective; no artifacts built this run.
**Follow-up:** Build the recommended artifact this coming week. Re-audit next Friday.
```

### 6. Output to user

Three-line summary:
- Score (with delta)
- Top gap
- Recommended artifact

That's it. The full reports are in their files.

## Hard rules

- **MUST NOT build** anything. This is reflection only.
- **MUST update** `_hot.md` even if score didn't change.
- **MUST log** even if no recommendation surfaced (a "stable, no recommendation" week is signal).
- **MUST flag** if last week's recommendation wasn't acted on.

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Last week's artifact wasn't built | Operator was busy / didn't agree / forgot | Don't re-recommend the same thing automatically. Ask: "Last week's recommendation was X. Still relevant?" |
| Audit and last audit are identical | Either nothing changed, or `/audit` is broken | Inspect `decisions/log.md` for movement. If real movement happened but score unchanged → rubric needs adjustment. |
| `_hot.md` ends up empty | Sources are empty (no decisions, no priorities, no audits) | This is real signal — the OS isn't being used. Surface this honestly. |

## Reference files
- `references/four-cs-framework.md` — what `/audit` measures
- `references/3ms-framework.md` — what `/level-up` thinks about
- `docs/CADENCE.md` — when this skill fires
- `docs/WIKI_LAYER.md` — what `_hot.md` is for

## Improvement loop
After each weekly review:
1. Did the operator act on the recommendation? If never → `/level-up` recommendations are wrong scope or wrong priority
2. Is the trend line going up? If flat for 4 weeks → either the OS plateau is real, or the rubric is mis-calibrated
3. Is `_hot.md` actually being read? If not → either reduce its size further, or stop maintaining it
