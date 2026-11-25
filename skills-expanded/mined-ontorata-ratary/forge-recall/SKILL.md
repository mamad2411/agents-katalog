---
name: forge-recall
description: >-
  Session start: Ratary context recovery + governance before any work.
  Use at the beginning of every chat or when resuming a task.
---
# Forge Recall

**Activates:** every session start (before design or code).

## Steps

1. **Ratary Context Recovery** â€” `search_memory` / handoff (when MCP available); **validate against repository**
2. Read [.ai/sessions/CURRENT.md](../../docs-ai/cross-cutting/sessions/CURRENT.md) â€” audit trail fallback only
3. Read [.ai/sync/README.md](../../docs-ai/cross-cutting/ratary-sync/README.md) if structural / memory questions
4. **New machine?** [.ai/bootstrap/MACHINE-SETUP.md](../../docs-ai/cross-cutting/bootstrap/MACHINE-SETUP.md) â€” repo first, Ratary after env
5. When Phase **8.8** ledger enabled: search `inspection-pattern` or scoped API recall
6. If user said "lanjut" / handoff: `handoff` tag or `get_memory_by_codename`
7. Read [SESSION-BOOTSTRAP.md](../../docs-ai/governance/core/SESSION-BOOTSTRAP.md)
8. Read [IMPLEMENTATION-COMPLETION-PROTOCOL.md](../../docs-ai/governance/core/IMPLEMENTATION-COMPLETION-PROTOCOL.md) when implementing
9. Read [GOVERNANCE-STATUS.md](../../docs-ai/governance/core/GOVERNANCE-STATUS.md) when structural
10. Restate task, constraints, Forge stages
11. Ask blocking questions only â€” do not implement yet

## Output

Short **Recall brief**: Ratary memory Â· repo validation Â· branch/commit Â· planned stages.

## Skip when

Read-only one-line questions with no repo impact.
