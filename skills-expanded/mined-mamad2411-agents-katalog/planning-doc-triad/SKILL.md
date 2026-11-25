---
name: planning-doc-triad
description: "Maintain project planning with three distinct documents: a big-picture roadmap, a near-term TODO list, and one active detailed plan. Use this skill when the user wants to create, clean up, or reset repository planning docs such as a roadmap, TODO file, or active plan, or when those roles are blurred across existing files. Do not use it for generic requests for priorities, next steps, or an implementation plan unless the user is explicitly asking to update or establish planning documents."
---

# Planning Doc Triad

Use three planning documents with non-overlapping roles.
If the repo already has canonical files for these roles, reuse them.
If it does not, default to:

- `docs/roadmap.md`: strategic direction and phased sequencing
- `TODO.md`: near-term actionable queue
- `PLAN.md`: one active detailed plan for the current job

This structure separates strategy, near-term execution, and active working context.
Treat it as a hierarchy:

- roadmap sets direction
- todo holds the near-term candidate queue
- plan expands the one todo item currently being executed

## When To Apply It

Apply this skill when:

- roadmap items are mixed with implementation tasks
- there is no clear "what next" list
- multiple plan files keep going stale
- detailed planning is happening only in chat history
- priorities are hard to infer from the current docs

Use it both for new repos and for cleaning up an existing planning system.

## Core Rules

### Roadmap doc

Use the roadmap for:

- product or technical direction
- phases or milestones
- intentional deferrals
- sequencing across multiple chunks of work

Do not use the roadmap for:

- session-level checklists
- fine-grained task breakdowns
- ephemeral notes

If the repo already has a canonical roadmap file, reuse it.
Otherwise default to `docs/roadmap.md`.

### Todo doc

Use the todo file for:

- near-term candidate work
- active or next-up work
- unrelated items that could reasonably be worked on soon
- small actionable items
- ordered execution priority

Keep it:

- short
- concrete
- easy to scan

Do not turn it into a strategy memo or a storage place for distant ideas.
Do not expand a todo item into a detailed execution document until it becomes the active job.

If the repo already has a canonical todo file, reuse it.
Otherwise default to `TODO.md`.

### Active plan doc

Use the plan file for:

- one active initiative
- the one todo item currently being executed
- one detailed job breakdown
- current scope, non-goals, steps, and open questions

Keep one clearly active detailed plan file.
If the repo already has a canonical current-plan location, reuse it instead of adding another root-level plan file.
When a todo item becomes the current job, expand it here instead of turning `TODO.md` into prose.
Rewrite the active plan freely as the current job changes.
Do not preserve stale plan history in multiple competing active plan files.

## Setup Workflow

When introducing this methodology to a repo:

1. Check whether the repo already has a roadmap, todo list, or plan docs.
2. Reuse existing files when they already match the intended role.
3. If the repo has no established convention for a missing role, create the missing files in these default locations:
   - `docs/roadmap.md`
   - `TODO.md`
   - `PLAN.md`
4. Remove overlap so each file has one clear job.
5. Move durable decisions into canonical docs such as architecture or product docs.

## Maintenance Workflow

When updating planning docs during normal work:

1. Keep the roadmap file focused on strategic direction, milestones, and sequencing.
2. Keep the todo file as the ordered near-term queue derived from that direction.
3. When one todo item becomes the current job and needs detail, expand it into the active plan file.
4. During execution, update the active plan as scope, steps, or open questions change.
5. After execution, remove completed items from the todo file, add any new follow-up tasks there, and rewrite the active plan for the next job.
6. If the plan produced durable decisions, persist them outside the active plan file.

## Writing Standards

- Keep all three files concise.
- Lead with what matters now.
- Use direct, concrete wording.
- Prefer ordering over categorization unless categories materially help.
- Avoid repeating the same item across files.

## Recommended File Shapes

### `docs/roadmap.md`

Prefer this structure:

- purpose or current recommendation
- phases or milestones
- likely deliverables per phase

### `TODO.md`

Prefer this structure:

- one short rule line
- `## Next Up`
- a flat ordered list of near-term candidate tasks

### `PLAN.md`

Prefer this structure:

- current job promoted from `TODO.md`
- goal
- in scope
- out of scope
- work plan
- open questions
- exit criteria

## Anti-Patterns

Avoid these failure modes:

- turning the roadmap into a backlog
- turning the todo file into a strategy memo
- keeping several plan files for parallel jobs without a clear active one
- leaving the active plan file as stale history after the job changes
- storing important product decisions only in the active plan file

## Output

When applying this methodology, produce:

- the updated files, or the new files that were actually needed
- a short explanation of what each file now owns
- the current next actions
