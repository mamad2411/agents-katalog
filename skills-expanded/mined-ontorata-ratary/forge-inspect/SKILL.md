---
name: forge-inspect
description: >-
  Gate review between blueprint tasks: spec compliance then code quality.
  Critical or constitutional issues block the next task.
---
# Forge Inspect

**Activates:** between `forge-execute` tasks (and before land).

## Two passes

### Pass 1 â€” Spec compliance

- Diff matches current blueprint task only
- ADR / phase requirements satisfied
- No forbidden patterns ([11-AI-RULES.md](../../docs-ai/governance/core/11-AI-RULES.md) Never create)
- **Inspection Pattern Ledger (Phase 8.8):** recall relevant ledger entries via MCP `search_memory` tag `inspection-pattern` or REST `/api/v1/inspection-patterns?path=â€¦` â€” use as prioritized checklist only; **constitutional blockers still come from spec**, not ledger alone

### Pass 2 â€” Code quality

- Layer boundaries (no transport in services)
- Matches [.ai/core/standards/02-CODING.md](../../docs-ai/governance/standards/02-CODING.md)
- Tests exist for behavior changes

## Severity

| Level | Action |
|-------|--------|
| **constitutional** | Block â€” fix before next task |
| **critical** | Block â€” fix before next task |
| **major** | Fix in current task if small; else add blueprint task |
| **minor** | Note; optional follow-up |

## Output

```markdown
## Inspect â€” Task N
- Spec: PASS / FAIL
- Quality: PASS / FAIL
- Blockers: (list or none)
```

Prompt cross-ref: `docs-ai/cross-cutting/agent-forge/workflow/prompts/review/code-review.md`

Optional: launch Bugbot subagent for large diffs when user requests.
