---
name: retro
version: 1.0.0
standalone: true
description: Periodic cross-agent learning consolidation — review what worked, what didn't, propagate insights
uses:
  - core/memory
requires:
  tools: [curl]
  env: []
security:
  risk_level: read
  capabilities:
    - memory:read
    - memory:write
  requires_approval: false
---

# Retro — Cross-Agent Learning Consolidation

Periodic retrospective that reviews agent learnings, consolidates patterns,
and propagates high-value insights across agents. Run weekly or after
significant milestones.

**Standalone mode**: Works without agent-coordinator. Scans `.os/agents/*/memory/`
directly instead of using the coordinator API.

## When to Use

- Weekly scheduled consolidation
- After a sprint or milestone completion
- When learning propagation thresholds are met
- When you notice agents repeating the same mistakes

## Steps

### 1. Gather Agent Learnings

Scan each agent's L1 memory for recent learnings:

```bash
# Framework mode
curl -s "${AC_COORDINATOR_URL:-http://localhost:9889}/memory/recent?days=7"

# Standalone mode
find .os/agents/*/memory/ -name "*.md" -newer .os/retro-last-run 2>/dev/null
```

### 2. Categorize Findings

Group learnings into:
- **Patterns**: Recurring approaches that worked (promote to L2)
- **Anti-patterns**: Mistakes that keep happening (add to skill references)
- **Process gaps**: Where the workflow broke down (create issues)
- **Tool insights**: Better ways to use tools (update SKILL.md files)

### 3. Propagate High-Value Learnings

For each pattern with `applications >= 2` and `successes >= 1`:

```bash
# Framework mode — trigger propagation
curl -s -X POST "${AC_COORDINATOR_URL:-http://localhost:9889}/memory/${AGENT_ID}/consolidate"
```

For standalone mode, manually copy high-value learnings from
`.os/agents/{name}/memory/` to `.os/memory/shared/`.

### 4. Update Skill References

If a learning reveals a common mistake or pattern:
1. Identify the relevant skill
2. Add the pattern to that skill's `references/` directory
3. Example: review misses → add to `review/pr-review/references/common-misses.md`

### 5. Create Issues for Process Gaps

If the retro reveals systematic problems:
1. Create a GitHub issue describing the gap
2. Tag it with the relevant category
3. Prioritize based on frequency and impact

### 6. Record Retro Summary

Write a summary to `.os/retro/YYYY-MM-DD.md`:

```markdown
# Retro — {date}

## What Worked
- {pattern}: {evidence}

## What Didn't
- {anti-pattern}: {evidence}

## Actions
- [ ] {action item}

## Learnings Propagated
- {learning} → L2 shared memory
```

Touch `.os/retro-last-run` to mark the timestamp.

## Completion States

- **DONE**: Retro complete, learnings propagated, summary written
- **DONE_WITH_CONCERNS**: Retro complete but some propagation failed
- **BLOCKED**: Cannot access agent memories
- **NEEDS_CONTEXT**: Need clarification on which time period to review
