---
name: skill-memory-update
description: Persist durable project, service, task, agent, and QC learnings after meaningful workflow events.
category: workflow
---

# Skill: Memory Update

Use after task completion, bug discovery, decisions, or scope changes.

Always read and refresh `.maestro/knowledge/index.yaml` so future agents can select relevant memory without rereading the whole project knowledge base.

## Store

```text
architecture decisions
service/API/schema changes
test policy changes
bug root cause patterns
QC blocker rules
generated coder scope updates
user-approved workflow exceptions
actionable user feedback from .maestro/memory/project/feedback/inbox.md
promoted reusable learnings into feedback/patterns.md and feedback/anti-patterns.md
```

## Do not store

```text
secrets
raw tokens
passwords
long logs
temporary noise
low-confidence guesses without confidence marker
```

## Reuse and convention memory updates

After a task, update project memory when implementation or QC reveals reusable knowledge:

- New reusable asset introduced.
- Existing reusable asset changed.
- Reuse rule added or corrected.
- Coding convention discovered or changed.
- Business/technical flow clarified.
- Anti-pattern identified from bug or review.

Update only durable knowledge. Do not store speculative patterns without confidence.

## Feedback intake loop

When user/team reports AI mistakes or omissions:

1. Capture raw feedback in `.maestro/memory/project/feedback/inbox.md`.
2. For coding errors, require `root_cause`, `prevention_rule`, `regression_check`, and `recurrence_key`.
3. During `/sync-memory`, triage feedback:
   - recurring mistakes -> `feedback/anti-patterns.md`
   - validated fixes/best practices -> `feedback/patterns.md`
4. Record `source_artifact`, `source_bug` when available, and `confidence` in memory updates.
5. Mark processed inbox entries as `promoted` or `closed`.
6. Refresh `.maestro/knowledge/index.yaml` or record why it did not change.
