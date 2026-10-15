---
name: simple-tasks
description: >
  Break down a feature specification and technical design into an ordered list of implementable tasks
  (issues-<feature-name>.json) inside docs/<feature-name>/. Use this skill whenever the user wants to
  create a task list, break down a feature into issues, generate a work queue, plan implementation
  steps, or turn a spec + design into actionable tasks. Trigger on phrases like "break this down",
  "create tasks", "generate issues", "task list", "work breakdown", "what needs to be built",
  "plan the work", or any request that involves converting planning documents into an ordered set
  of implementable units.
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
    design.md             ← from simple-design
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

- **Granularity preference:** "The design describes 3 major components. Should each be one task,
  or should I break them into smaller units (e.g., data model, API, UI separately)?"
- **Priority signals:** "The spec has 5 user stories — are any higher priority than others, or
  should I order by technical dependency only?"
- **Scope confirmation:** "The spec marks X as out-of-scope, but the design references it.
  Should I include it or flag it as a discrepancy?"
- **Testing expectations:** "Should testing be a separate task per component, or bundled into
  each implementation task?"

Keep it to one round of 1-4 focused questions. If you can make reasonable choices from the
planning docs, do so — you can note assumptions in the task descriptions.

### 3. Generate the task list

Read the template at `references/issues_template.json` in this skill's directory. Use it as the
structural guide for your output.

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

- **Each task should be completable in one session.** If a task feels like it would take more
  than a few hours of focused work, break it into smaller pieces. An agent should be able to
  pick up a single task, implement it, verify it, and move on.

- **Tasks should be independently verifiable.** Each task's acceptance criteria should be
  testable without completing subsequent tasks. This means the feature builds up incrementally —
  each task leaves the codebase in a working state.

- **Reference the planning docs, don't duplicate them.** Task descriptions should point back to
  specific sections of the spec or design (e.g., "Implement the sharing permissions model
  described in design.md § Proposed storage changes"). Don't copy entire sections.

- **Include setup and testing tasks.** Don't skip the boring stuff: database migrations, config
  changes, test scaffolding, CI updates. These are tasks too and they often block other work.

- **Be specific about what "done" means.** "Implement the API endpoint" is vague. "Implement
  POST /api/workspaces/:id/share — validates input, creates sharing record, returns 201 with
  sharing details. Returns 409 if already shared with that user." is verifiable.

- **Map user stories to tasks, but don't force a 1:1 mapping.** A single user story might
  require multiple tasks (data model + API + UI). Multiple simple stories might be one task.
  The design document's "affected components" and "planned changes" sections are usually the
  best guide for task boundaries.

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

- This skill produces a **task breakdown**, not a spec or design. Focus on *what work units to
  do and in what order*, not on requirements (spec's job) or architecture (design's job). If you
  catch yourself writing user stories or proposing technical approaches, you've crossed into
  another skill's territory — reference the planning docs instead.
- The number of tasks should be proportional to the feature's complexity. A small feature might
  have 3-5 tasks. A large feature might have 15-25. Don't inflate or compress artificially.
- If the spec and design disagree on something, flag it as a discrepancy rather than silently
  picking one. The user needs to resolve it before implementation.
- All tasks start with `status: "todo"`. Only **simple-implement** changes task status.
- The `depends_on` field creates a DAG (directed acyclic graph). Don't create circular
  dependencies. If two tasks are truly co-dependent, merge them into one.
