---
name: end-of-day-review
description: Evening reflection loop. Records what changed today, what skills worked, what failed, what context was missing. Proposes updates to skills/references/wiki/connections. Logs a one-line entry in decisions/log.md. Does not build anything.
disable-model-invocation: true
---

# /end-of-day-review — Evening Loop

> Last skill of the working day. Captures the small lessons before they evaporate overnight.

## When to use
- End of the working day, before stepping away
- After a notable session (incident, breakthrough, pivot)

## When NOT to use
- Mid-task
- More than once per day
- When the day was 100% admin / non-OS work — the entry would be empty

## Inputs
- `git log --oneline` since last review (if last review timestamp is available, use it; otherwise last 24h)
- Tool calls from `~/.claude/usage.jsonl` last 24h
- `~/.claude/audit.log` and `audit-mcp.log` last 24h (warns / blocks?)
- Operator's memory of the day

## Outputs
- Five-line summary in chat:
  - **What changed:** commits, ships, conversations resolved
  - **Skills used:** which ones, did they work?
  - **What broke:** failures, surprises, friction
  - **Context gap:** which file would have helped if filled?
  - **Tomorrow's hint:** one-line carry-forward for tomorrow's `/daily-plan`
- One-line entry in `decisions/log.md` with same date

## Hard rules
- **MUST be terse.** Five lines, not five paragraphs.
- **MUST capture failures honestly.** Not "what went well" — what went *wrong*.
- **MUST NOT propose** more than one improvement candidate. (That's `/level-up`'s job for the week.)
- **MUST flag** if the day produced no commits AND no entries in `decisions/log.md` AND no `usage.jsonl` activity — the OS wasn't used.

## Steps

1. **Pull signals:**
   - `git log --oneline -20` — what shipped
   - `tail -200 ~/.claude/usage.jsonl | python3 -c "..."` — count tool calls
   - Check `~/.claude/audit.log` for any WARN / BLOCK entries

2. **Ask the operator:** "Anything notable from today I wouldn't see in git or logs?" — capture in their words.

3. **Synthesize the five lines.**

4. **Carry-forward:** the "tomorrow's hint" feeds `/daily-plan` tomorrow morning. Make it actionable, not vague.

5. **Append to `decisions/log.md`:**
   ```markdown
   ## YYYY-MM-DD — End of day: <one-line summary>
   - What changed: ...
   - What broke: ...
   - Context gap: ...
   - Tomorrow: ...
   ```

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| No commits, no tool calls, no operator input | Day was off the OS | Log a single line: "Off-OS day, no review needed" |
| Same context gap surfaces 3 days running | A specific reference / skill is genuinely missing | Promote to `/level-up` candidate next Friday |
| Operator says "nothing notable" but tool log shows heavy activity | Auto-pilot day | Surface this — heavy activity without notable outcomes is a signal |
| Long failure list | Bad day, or systematic friction | If long for 3+ days → escalate to `/level-up` early; don't wait for Friday |

## Reference files
- `context/Priorities.md` — for "did today match priorities?"
- `decisions/log.md` — where the entry lands
- `~/.claude/usage.jsonl` — tool call signals
- `~/.claude/audit.log` — warning / block signals

## Improvement loop
After each run:
1. Did the carry-forward hint actually steer tomorrow's plan? If never → hint quality is bad
2. Did the same context gap surface in multiple end-of-day reviews? If yes → it's a real candidate, escalate
3. Did the operator skip more than 2 reviews per week? If yes → either the loop is too heavy, or the OS isn't being used (both are signal)
