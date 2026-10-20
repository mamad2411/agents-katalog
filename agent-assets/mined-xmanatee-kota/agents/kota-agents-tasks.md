# Tasks

`data/tasks/*.md` is the active work queue. `data/tasks/archive/*.md` is
terminal history. There are no lifecycle subdirectories for open, blocked, or
in-progress work.

## Task contract

- The filename (without `.md`) is the task id.
- The first level-one heading is the title.
- Active frontmatter contains `status: open` or `status: blocked`, a `priority`
  from `p0` through `p3`, and an optional `depends_on` list.
- Archived frontmatter contains only `status: done` or `status: dropped`.
- Use `depends_on` for hard task predecessors. A task waiting on dependencies
  remains `open`; do not duplicate dependency waits as blocked preconditions.
- `blocked` is reserved for a concrete external precondition described in a
  `## Blocked on` section, such as an owner decision, an unavailable local
  capability, or operator-controlled evidence.
- Preserve owner wording, observed evidence, research provenance, and urgency
  in the body. Builders own implementation plans and judge completion using
  proportionate evidence.

There is no persisted `doing` state. A task is in progress only while an active
builder workflow run owns it; API and client projections derive that fact from
workflow state.

## Queue rules

- New rough ideas belong in `data/inbox/`.
- Before creating a task, scan active tasks and related inbox items for overlap.
- Prefer coherent, outcome-sized work over isolated mechanical cleanup.
- Authored priority orders otherwise actionable work. Dependencies and external
  blockers determine whether work can dispatch.
- Edit task Markdown directly with the normal editor or agent file tools.
  Prepare complete content before publication; related task edits belong in one
  change. Move terminal files to `archive/` and keep their status aligned.
- Do not restore tracking anchors or a separate backlog. If an initiative is
  decomposed, archive or drop its tracking task and let its child tasks carry
  the work.
- Before publishing task-data changes, run the task validator and confirm safe
  paths, unique ids, valid metadata, and valid dependency references.
