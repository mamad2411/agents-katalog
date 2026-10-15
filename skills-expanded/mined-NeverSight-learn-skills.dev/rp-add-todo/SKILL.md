---
name: rp-add-todo
description: Capture an idea, task, or follow-up from the current conversation without losing flow — writes it to .planning/todos/ and updates STATE.md. Use this skill when the user mentions something they want to remember ("we should also...", "don't forget...", "add to the list..."), when execution uncovers work that doesn't belong in the current phase, when a decision surfaces a follow-up task, or when an idea comes up mid-session that shouldn't be forgotten but shouldn't derail the current work. Keeps ideas captured without derailing execution.
---

# Add Todo

Captures an idea or task without derailing the current work. The goal is "thought → captured → continue" in under 10 seconds. The todo lands in `.planning/todos/` where `rp-check-todos` can surface it later.

## What belongs here vs the task registry

| Use todo | Use task registry |
|----------|------------------|
| Idea that came up mid-execution | Work scoped to a phase |
| Follow-up for a future phase | Task with a known verify command |
| "We should look into X" | Concrete implementation step |
| Discovery during debugging | Anything with a dependency |
| Nice-to-have that shouldn't block current work | Anything on the critical path |

If it belongs in the current phase → add it to TASK-REGISTRY.md directly.  
If it's future work with no phase yet → this skill.

## Capture

Extract from the conversation:
- **What:** the actual idea or task (be specific — vague todos are useless)
- **Why:** why it matters (brief — one sentence max)
- **Area:** which part of the codebase or planning it relates to (infer from context)
- **Urgency:** blocking / high / normal / low

```bash
mkdir -p .planning/todos
```

Write `.planning/todos/<YYYY-MM-DD>-<slug>.md`:

```markdown
# Todo: <slug>

**Captured:** <date>
**Area:** <auth / data / ui / infra / planning / etc>
**Urgency:** normal

## What

<Specific description of the idea or task>

## Why

<Why it matters — one sentence>

## Context

<Any relevant context from the current session that won't be obvious later>

## Suggested next action

<What should happen with this — add to phase N, investigate, discuss, etc>
```

## Update STATE.md

Add a line to the cross-cutting queue if it's cross-cutting, or just note it in the next queue:

```markdown
| `open` | <todo summary> — see `.planning/todos/<slug>.md` |
```

## Confirm capture

```
Captured: <slug>

"<what>"

Area: <area> · Urgency: <urgency>
File: .planning/todos/<date>-<slug>.md

Continuing with current work.
```

Don't ask questions — capture what was said and continue. If it's ambiguous, capture the ambiguous version and note "clarify when reviewing todos."

## Deduplication

Before writing, check existing todos:

```bash
ls .planning/todos/ 2>/dev/null
```

If a similar todo exists, update it rather than creating a duplicate. Duplicates make todo review noisy.

## What rp-check-todos does with these

`rp-check-todos` reads `.planning/todos/*.md` and surfaces them with routing options:
- Work on it now (adds to current phase)
- Defer to next phase
- Create a new phase
- Discard (turns out not worth doing)

Todos are not permanent — they're staging. Every todo should eventually be acted on, deferred explicitly, or discarded. A growing unreviewed todo pile is a warning sign.
