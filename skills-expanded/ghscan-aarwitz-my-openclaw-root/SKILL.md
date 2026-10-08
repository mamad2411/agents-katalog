---
name: codex-execution-harness
description: Deterministic coding-execution router for implementation-first workflows with inspection, minimal edits, and explicit validation evidence.
metadata: {"clawdbot":{"emoji":"🧰"}}
---

# Codex Execution Harness Router (Lean + Deterministic)

Default for coding/devops requests is execution-first behavior.
Use domain skills before ad hoc shell when a specialized path exists.

## Operation Table

| Operation | Deterministic Action | Fail-Closed Rule |
|---|---|---|
| Scope lock | restate target outcome in one sentence | if scope unclear, stop before edits |
| Context gather | inspect files with fast reads/search | no blind edits |
| Minimal implementation | smallest safe patch per file | avoid unrelated churn |
| Validation | run at least one targeted check per change type | if check fails, do not claim success |
| Evidence report | summarize changes + command outcomes + next step | no assumption-based completion |

## Tooling Priority

1. task orchestration skills
2. repo/auth skills
3. runtime/config domain skills
4. shell for glue, probes, and validation

## Hard Rules

- No file edits before reading target files.
- No success claim without validation output.
- No broad refactors for narrow requests.
- No destructive commands unless explicitly approved.

## Output Contract

Return in this order:
1. outcome summary
2. concrete file/tool changes
3. validation evidence (pass/fail)
4. single next best action

## On-Demand Deep Reference

- `workspace/skills/codex-execution-harness/REFERENCE_FULL.md`
