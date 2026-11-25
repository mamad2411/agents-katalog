---
name: simple-tasks
description: >
  Break a feature's spec and design into an ordered, dependency-aware task list
  (docs/<feature-name>/issues.json) — each task small enough for one implementation session. Use
  when the user wants to break down a feature, generate issues, create a work queue, or plan
  implementation steps. Triggers: "break this down", "create tasks", "generate issues", "task
  list", "work breakdown", "plan the work".
disable-model-invocation: true
---

# Simple Tasks — Break Down a Feature into an Ordered Task List

You are creating an ordered task list for a feature. Your job is to produce an `issues.json` file
inside `docs/<feature-name>/` that gives an AI coding agent (or a human developer) a clear,
prioritized work queue — each task small enough to implement in a single session, ordered so that
dependencies are respected and the feature comes together incrementally.

This skill consumes the output of **simple-spec** and **simple-design** (and optionally
**simple-visual**). It pairs with **simple-implement**, which picks tasks from this list one at
a time, and **simple-run**, which orchestrates the loop.

## Folder convention

All feature artifacts live in `docs/<feature-name>/`:

```
docs/
  index.json              ← feature manifest (created/updated by this skill)
  visual.md               ← from simple-visual (app-level, optional)
  <feature-name>/
    spec.md               ← from simple-spec
    spec/                 ← optional detail files (from simple-spec, if spec.md was split)
    design.md             ← from simple-design
    design/               ← optional detail files (from simple-design, if design.md was split)
    issues.json           ← THIS SKILL'S OUTPUT
    progress-log.md       ← created by simple-implement
```

The `<feature-name>` token is a short kebab-case identifier (e.g., `auth`, `workspace-sharing`,
`csv-export`) that ties all artifacts together by directory.

## Workflow

### 1. Gather context

Start by collecting all available planning documents **before** asking the user anything.

**Required inputs:**
- Read `docs/<feature-name>/spec.md` — this is your primary source for *what* to build, user
  stories, acceptance criteria, and edge cases.
- Read `docs/<feature-name>/design.md` — this tells you *how* to build it: architecture, data
  flow, interfaces, affected components, testing strategy.
- If `spec.md` or `design.md` indexes child detail files (a `spec/` or `design/` subfolder), read
  those too. They hold the page-level detail you need to size tasks accurately and to point each
  task at the right section.

**Optional inputs:**
- Read `docs/visual.md` if it exists — this is the app-level visual design system. UI/visual tasks need this context.
- Scan the codebase to understand its current state, conventions, and complexity. This helps
  you size tasks accurately and identify prerequisites.

**If inputs are missing:**
- If the user hasn't specified a feature name, check `docs/` for existing feature subdirectories
  and ask which one to break down. If there's only one, use it.
- If `spec.md` or `design.md` doesn't exist, tell the user and suggest running **simple-spec**
  or **simple-design** first. You can still proceed if the user provides enough context directly,
  but the output quality will be lower — say so explicitly.

### 2. Ask follow-up questions (only if needed)

After reading the planning docs, assess whether you have enough to produce a good breakdown.
Common gaps:

- **Granularity constraints:** Ask only if session limits or required review/rollout boundaries
  are unclear and would materially change the breakdown; otherwise use the sizing principles below.
- **Priority signals:** "The spec has 5 user stories — are any higher priority than others, or
  should I order by technical dependency only?"
- **Scope confirmation:** "The spec marks X as out-of-scope, but the design references it.
  Should I include it or flag it as a discrepancy?"
- **Testing expectations:** Clarify missing coverage or validation requirements; keep related
  tests with their implementation by default.

Keep it to one round of 1-4 focused questions. If you can make reasonable choices from the
planning docs, do so — you can note assumptions in the task descriptions.

### 3. Generate the task list

Read the template at `references/issues_template.json` in this skill's directory. Use it as the
structural guide for your output.
Its examples illustrate the schema, not required task boundaries: apply the sizing principles
below rather than automatically separating migrations, implementation, and tests.

**Required fields for every task:**

| Field                | Type            | Description                                              |
| -------------------- | --------------- | -------------------------------------------------------- |
| `id`                 | string          | `TASK-<feature>-001` format, zero-padded, sequential     |
| `type`               | string          | `"story"` \| `"bug"` \| `"task"` \| `"chore"`           |
| `title`              | string          | Short imperative summary (e.g., "Add sharing permissions model") |
| `description`        | string          | Concise but sufficient detail for an agent to implement  |
| `acceptance_criteria` | array of string | Success conditions — specific and verifiable             |
| `status`             | string          | Always `"todo"` when generated by this skill             |
| `priority`           | integer         | 1 = highest. Determines execution order                  |
| `depends_on`         | array of string | IDs of tasks that must complete first. Empty if none     |

**Optional fields** — add these when the project complexity warrants it:

- `estimated_effort`: `"small"` | `"medium"` | `"large"` — relative sizing
- `tags`: array of strings for categorization (e.g., `["backend", "database"]`)
- `notes`: string for context that doesn't fit elsewhere
- `blocked_reason`: string explaining why a task is blocked (used by simple-implement)
- `files_likely_affected`: array of file paths the task will probably touch

The agent is free to add other fields as needed for complex projects. The required fields are
the contract that **simple-implement** depends on.

**Key principles:**

- **Order by dependency, then by priority.** Tasks with no dependencies and high priority come
  first. Tasks that depend on others come after their dependencies. The `priority` field is the
  tiebreaker when dependencies are equal.

- **Size tasks around cohesive changes.** Each task should have a clear, independently
  verifiable outcome that an agent can implement and verify confidently in one session. Keep
  closely related implementation and tests together. Do not create separate tasks solely because
  changes touch different files or technical layers, but do not force an entire user story into
  one task. Split when work involves distinct outcomes, meaningful prerequisites, or too much
  scope for one session.

- **Tasks should be independently verifiable.** Each task's acceptance criteria should be
  testable without completing subsequent tasks. This means the feature builds up incrementally —
  each task leaves the codebase in a working state.

- **Reference the planning docs, don't duplicate them.** Task descriptions should point back to
  specific sections of the spec or design (e.g., "Implement the sharing permissions model
  described in design.md § Proposed storage changes", or a child file such as
  "design/permissions.md § Schema changes"). Don't copy entire sections.

- **Include necessary setup and testing work.** Account for database migrations, config changes,
  test scaffolding, and CI updates within the relevant task. Make them separate tasks when they
  are meaningful prerequisites or need independent validation or rollout.

- **Be specific about what "done" means.** "Implement the API endpoint" is vague. "Implement
  POST /api/workspaces/:id/share — validates input, creates sharing record, returns 201 with
  sharing details. Returns 409 if already shared with that user." is verifiable.

- **Map user stories to tasks, but don't force a 1:1 mapping.** A single user story might
  require multiple tasks; multiple simple stories might be one task. For example, sharing could
  have one task for storage, API, permission checks, and tests, and another for the sharing UI,
  API integration, and UI verification. Use the design's affected components and planned changes
  to identify scope, and the sizing principles above to choose task boundaries.

### 4. Save the output

- Save the task list to `docs/<feature-name>/issues.json`.
- Update (or create) `docs/index.json` at the project root. This is a lightweight manifest:

```json
{
  "features": {
    "<feature-name>": {
      "status": "tasks_ready",
      "path": "docs/<feature-name>/"
    }
  }
}
```

Valid feature statuses: `"planning"`, `"spec_ready"`, `"design_ready"`, `"tasks_ready"`,
`"in_progress"`, `"done"`.

- Tell the user the file path and give a brief summary: how many tasks, what the critical path
  looks like, and any assumptions you made.

### 5. Suggest next step

Let the user know the task list is ready for implementation. Mention that they can:

- Use **simple-implement** to work through tasks one at a time (manual control).
- Use **simple-run** to automatically loop through all tasks until the feature is complete.
- Review and adjust the task list before starting — reorder, split, merge, or remove tasks
  as needed. The JSON format makes this easy.

## Important notes

- This skill produces a **task breakdown**, not a spec or design — focus on *what work units to
  do and in what order*, not requirements or architecture. If you find yourself writing user
  stories or proposing technical approaches, reference the planning docs instead.
- Keep the task count proportional to complexity, with no target or minimum count. A small
  feature may need only one task; larger features should split at meaningful boundaries.
- If the spec and design disagree, flag it as a discrepancy for the user to resolve rather than
  silently picking one.
- All tasks start with `status: "todo"` — only **simple-implement** changes task status.
- `depends_on` forms a DAG — no circular dependencies. If two tasks are truly co-dependent,
  merge them into one.
