---
name: writing-plans
description: "Compatibility entrypoint for turning an approved MEDIUM/LARGE design into executable tasks. The Specification Writer workflow owns the canonical SDD planning contract."
---

# Writing Plans Compatibility Entry

Keep this skill name for routing compatibility, but follow `core-workflow-contract` and `specification-writer-workflow` as the only process owners.

## Required Files

- Write MEDIUM/LARGE work to `spec/<feature>/requirements.md`, `design.md`, and `tasks.md`.
- Link active work to `memories/repo/current-workstreams.md`; update `spec/INDEX.md` and `memories/repo/INDEX.md` when their rows change.
- Use `target-spec-bootstrap/references/templates.md` as the detailed template source. Do not invent another directory or standalone active plan.

## Minimum `tasks.md` Shape

Every task must name the responsible agent lane and independent reviewer lanes, not only the work description:

```markdown
## Progress Ledger

| Task ID | Status | Owner | Reviewer | Last updated | Verification | Evidence | Next action | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | READY | Developer | Technical Architect, QA | unknown | not_run | none | Start task | none |

### T-001: <short imperative title>
- Requirement refs: <FR IDs>
- Design refs: <DD IDs>
- Owner lane: technical-architect | developer | frontend-designer | root-cause-fixer | specification-writer
- Reviewer lanes: <developer, technical-architect, qa, security, frontend>
- Files involved / write set: <explicit paths or surfaces>
- Dependencies / parallel group / parallel ready: <IDs, group, true|false with reason>
- Acceptance checks: <observable outcomes>
- RED check: <failing test or reproducible check; N/A requires reason>
- Verification command: <command or evidence path>
- Ready artifacts: <changed files, test/review evidence, state updates>
- Stop conditions: <failure, missing context, conflict, or scope expansion>
```

Status values are `READY | IN_PROGRESS | DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | NEEDS_USER_INPUT | BLOCKED`. Update the ledger and `current-workstreams.md` whenever task or verification state changes. Reject placeholders, unresolved design choices, and chat-only progress.

This is the minimum output contract, not an SDD tutorial. Role workflows own reasoning and implementation behavior.
