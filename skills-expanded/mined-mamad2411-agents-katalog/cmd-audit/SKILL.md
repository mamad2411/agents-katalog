---
name: cmd-audit
description: Command — Quality-check your recent WORK (today's code, a feature, a file) via the auditor agent. For health-check of the Claude Code config itself (agents, commands, hooks), use /system-audit instead.
---

Delegate a quality review to the auditor agent.

## Steps

### Step 1: Determine scope

If the user provided a specific scope (file, task, or area):

- Use that as the audit target

If no scope provided:

- Default to recent work — read `git diff` / `git log` and `.claude/memory.md` for context

### Step 2: Select audit tier

| Tier | When                                          | Depth                                           |
| ---- | --------------------------------------------- | ----------------------------------------------- |
| T1   | Quick sanity pass                             | Scan for obvious issues, 2-3 min                |
| T2   | After completing a feature or multi-step task | Check completeness, consistency, side effects   |
| T3   | Weekly review, after major changes            | Full regression check, knowledge-base sweep     |
| T4   | Monthly or after system changes               | Deep infrastructure audit, cross-file coherence |

Default to T2 for explicit `/audit` calls.

### Step 3: Delegate to auditor

Spawn the auditor agent with the appropriate tier and scope:

```
Agent(auditor): [Tier] audit of [scope].

Context:
- [Brief description of what was done]
- [Key files involved]

Check for:
1. Completeness — were all requirements met?
2. Consistency — do changes align with existing patterns?
3. Side effects — did changes break anything downstream?
4. Knowledge — are there learnings to promote or nominate?

Report findings as PASS/WARN/FAIL with specific file:line references.
```

### Step 4: Process results

- **PASS**: Note success and any suggestions
- **WARN**: Log warnings to `.claude/logs/incident-log.md`
- **FAIL**: Log failures to `.claude/logs/incident-log.md` and report the corrective actions needed to the user

### Step 5: Update logs

Append audit results to `.claude/logs/audit-trail.md` under a new section:

```markdown
## Audit — HH:MM (T[tier])

- Result: [PASS/WARN/FAIL]
- Findings: [bullets]
- Actions: [corrective actions needed]
```

## Arguments

`[scope]`
