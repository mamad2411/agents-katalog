---
name: context-optimizer
description: Optimize token usage and context management. Use when sessions feel slow, context is degraded, or you're running out of budget.
---

# Context Optimizer

Manage your context window and token budget effectively.

## Quick Diagnosis

1. Run `/context` to check current usage
2. If > 70% → compact now before it degrades
3. If > 90% → you're in the "dumb zone", compact immediately

## Optimization Strategies

### Immediate

| Action | Saves | When |
|--------|-------|------|
| `/compact` | 30-50% context | At task boundaries |
| Disable unused MCPs | ~5% per MCP | When switching domains |
| Use subagents for exploration | Keeps main context clean | Heavy search/read tasks |
| Fresh session via `/resume` | 100% reset | When starting unrelated work |

### Configuration

Set proactive auto-compaction:
```json
{
  "env": {
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "50"
  }
}
```

### MCP Audit

Keep <10 MCPs enabled, <80 tools total. Each MCP adds overhead to every request.

## Token Efficiency Rules (40-60% savings)

- No sycophantic openers ("Sure!", "Great question!")
- No closing fluff ("Let me know if you need anything!")
- No prompt restatement before answering
- Code first, explanation only if non-obvious
- Structured output (tables, bullets) over prose
- ASCII only: -- not em dashes

## One-Pass Coding

- Read all files first
- Understand test assertions before writing
- Write complete solution once
- Stop if green — never iterate more than twice on same failure

## Tool-Call Budgets

| Task | Max Calls |
|------|-----------|
| Quick fix | 20 |
| Medium feature | 40 |
| Large feature | 80 |

## Task Profiles

- **Coding**: code first, minimal explanation, simplest solution
- **Agent/Pipeline**: structured output only, no prose
- **Analysis**: finding first, tables over paragraphs

## When Context Is Degraded

Signs: Claude repeats itself, forgets earlier context, responses become generic.

Fix:
1. Manual `/compact`
2. If still bad: new session with `/resume`
3. For recurring issues: reduce CLAUDE.md size, disable MCPs

## Purpose
Reduce token use and context degradation in long sessions.

## Inputs
Current session state and size.

## Validation
- Context size reduced and the task still has what it needs.

## Example
```text
Summarise finished subtasks, drop tool dumps, keep the plan and open questions.
```

## Related skills
token-efficiency, memory-status

## When to use
Sessions feel slow, context is degraded, or budget is running out.
