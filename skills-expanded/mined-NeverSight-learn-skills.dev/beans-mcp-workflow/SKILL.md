---
name: beans-mcp-workflow
description: Use this skill when the user needs to manage Beans work items in a Beans workspace—create, view, update, reopen, archive, query, or bulk-manage beans, edit `.beans` files/frontmatter, or manage parent/blocking relationships. Use it even when the user says tickets/issues/backlog instead of “beans.” Do not use it for generic GitHub issue workflows that are not backed by Beans.
---

# Beans MCP Skill

## When to Use

Use this skill whenever you need to:

- Create, view, edit, or delete beans (tasks, bugs, features, epics, milestones)
- Query, filter, sort, or search beans
- Bulk-create or bulk-assign beans to a parent
- Read or write bean markdown files under `.beans/`
- Generate Copilot workspace instructions from the live Beans context

Do **not** use this skill for:

- Generic GitHub Issues/Projects workflows unrelated to a Beans workspace
- One-off markdown editing outside `.beans/` records

---

## Available Tools

| Tool                   | Purpose                                         |
| ---------------------- | ----------------------------------------------- |
| `beans_init`           | Initialize Beans in a workspace                 |
| `beans_archive`        | Archive completed/scrapped beans                |
| `beans_view`           | View one or more beans by ID                    |
| `beans_create`         | Create one bean                                 |
| `beans_bulk_create`    | Create many beans                               |
| `beans_update`         | Update bean metadata/body                       |
| `beans_bulk_update`    | Update many beans                               |
| `beans_edit`           | Metadata-only update helper                     |
| `beans_reopen`         | Reopen a completed/scrapped bean                |
| `beans_complete_tasks` | Complete markdown checklist tasks in body       |
| `beans_delete`         | Delete one or more beans                        |
| `beans_query`          | Query/list/filter/sort/ready/graphql operations |
| `beans_bean_file`      | Read/create/edit/delete `.beans` files          |
| `beans_output`         | Read extension output logs                      |

---

## Default Workflow (Use This First)

When the user asks for bean work and intent is unclear, default to this sequence:

1. **Discover**: `beans_query` with `operation: "ready"` (or `refresh` if broad list needed)
2. **Inspect**: `beans_view` for the specific bean(s)
3. **Mutate**: `beans_update` (or bulk variants) with minimal required changes
4. **Body tasks**: `beans_complete_tasks` for checklist completion
5. **Close/archive**: `beans_update` to `completed`/`scrapped`, then `beans_archive` when appropriate

Use alternatives only when this default is insufficient.

---

## Field Reference

### Creating a bean (`beans_create`, `beans_bulk_create`)

| Field         | Required | Notes                                                        |
| ------------- | -------- | ------------------------------------------------------------ |
| `title`       | ✅       | String, max 1024 chars                                       |
| `type`        | ✅       | e.g. `task`, `bug`, `feature`, `epic`, `milestone`           |
| `status`      | —        | e.g. `todo`, `in-progress`, `draft`, `completed`, `scrapped` |
| `priority`    | —        | `critical`, `high`, `normal`, `low`, `deferred`              |
| `body`        | —        | Markdown body content                                        |
| `description` | —        | Deprecated alias for `body`; use `body` instead              |
| `parent`      | —        | Parent bean ID                                               |

### Updating a bean (`beans_update`, `beans_bulk_update`)

| Field         | Notes                                                                  |
| ------------- | ---------------------------------------------------------------------- |
| `beanId`      | Required — ID of bean to update                                        |
| `status`      | New status                                                             |
| `type`        | New type                                                               |
| `priority`    | New priority                                                           |
| `parent`      | Assign to a new parent                                                 |
| `clearParent` | Set `true` to detach from current parent                               |
| `blocking`    | Array of bean IDs this bean now blocks                                 |
| `blockedBy`   | Array of bean IDs this bean is blocked by                              |
| `body`        | Full body replacement (cannot combine with `bodyAppend`/`bodyReplace`) |
| `bodyAppend`  | Append text to the end of the body                                     |
| `bodyReplace` | Array of `{ old, new }` string substitutions in the body               |
| `ifMatch`     | Optimistic concurrency guard — pass the bean's `etag`                  |

---

## Archive and GraphQL Parity

### Archive completed work

Use `beans_archive` to archive completed/scrapped beans.

```json
{}
```

### Raw GraphQL queries/mutations

Use `beans_query` with `operation: "graphql"` for CLI parity with `beans query --json`.

```json
{
  "operation": "graphql",
  "graphql": "{ beans(filter: { type: [\"bug\"] }) { id title status } }"
}
```

With variables:

```json
{
  "operation": "graphql",
  "graphql": "query($q: String!) { beans(filter: { search: $q }) { id title } }",
  "variables": { "q": "authentication" }
}
```

---

## CLI-Aligned Workflow Guidance

- Prefer `beans_view` / `beans_query` over ad-hoc file parsing for bean state.
- Use `beans_bulk_create` / `beans_bulk_update` for batch parent/relationship updates.
- Use `beans_complete_tasks` for markdown checklist completion inside a bean body.
- Use `beans_archive` only after work is completed/scrapped and user intent is to archive.

### Gotchas (High-Value Corrections)

- `beans_update` rejects combining `body` with `bodyAppend`/`bodyReplace` in one request.
- `beans_delete` allows only `draft`/`scrapped` unless `force: true`.
- `beans_reopen` requires the current status to match `requiredCurrentStatus` (`completed` or `scrapped`).
- Omitting `beanId` produces a validation hint; prefer `beanId` (not `id`).
- For concurrent edits, pass `ifMatch` with the current bean `etag` from `beans_view`.

### Relationship semantics

- **Parent**: hierarchy (milestone → epic → feature → task/bug).
- **Blocking**: this bean blocks another bean.
- **BlockedBy**: this bean depends on another bean.

### Issue types

- `milestone`, `epic`, `bug`, `feature`, `task`

### Statuses

- `in-progress`, `todo`, `draft`, `completed`, `scrapped`

### Priorities

- `critical`, `high`, `normal`, `low`, `deferred`

### Body modification guidance

- Use `body` for full replacement.
- Use `bodyAppend` to append content.
- Use `bodyReplace` for exact replacements.
- Do **not** combine `body` with `bodyAppend`/`bodyReplace` in one request.

### Concurrency guidance

- Use `ifMatch` with a current `etag` from `beans_view` when concurrent edits are possible.

---

## Bulk Operations

### Bulk create under a shared parent

```json
{
  "beans": [
    { "title": "Design API schema", "type": "task" },
    { "title": "Implement endpoints", "type": "task" },
    { "title": "Write tests", "type": "task" }
  ],
  "parent": "feature-auth-42"
}
```

Each item can specify its own `parent` to override the top-level `parent`.

### Bulk re-assign existing beans to a parent

```json
{
  "beans": [
    { "beanId": "task-001", "status": "todo" },
    { "beanId": "task-002" },
    { "beanId": "task-003" }
  ],
  "parent": "epic-q2-roadmap"
}
```

---

## Querying

### Refresh (list all beans)

```json
{ "operation": "refresh" }
```

### Filter

```json
{
  "operation": "filter",
  "statuses": ["in-progress", "todo"],
  "types": ["bug", "feature"],
  "tags": ["auth"]
}
```

### Search

```json
{ "operation": "search", "search": "authentication", "includeClosed": false }
```

### Sort

```json
{ "operation": "sort", "mode": "updated" }
```

Modes: `status-priority-type-title` (default), `updated`, `created`, `id`

### Ready (actionable, unblocked beans)

```json
{ "operation": "ready" }
```

### LLM context — generate Copilot instructions

```json
{ "operation": "llm_context", "writeToWorkspaceInstructions": true }
```

Writes to `.github/instructions/beans-prime.instructions.md` when `writeToWorkspaceInstructions` is true.

---

## File Operations (`beans_bean_file`)

### Path rules

- Pass the filename **without** the `.beans/` prefix — it is resolved automatically.
- Both `foo.md` and `.beans/foo.md` are accepted; the leading `.beans/` is stripped.
- Use `update_frontmatter` to atomically update frontmatter fields without rewriting the body.

### `update_frontmatter` defaults

- Prefer `update_frontmatter` over `edit` when changing only metadata fields.
- Set nullable fields (`parent_id`, `tags`, `blocking_ids`, `blocked_by_ids`, `pr`, `branch`) to `null` to remove them.

```json
{ "operation": "read", "path": "task-abc--fix-login.md" }
```

```json
{
  "operation": "edit",
  "path": "task-abc--fix-login.md",
  "content": "---\ntitle: \"Fix login timeout\"\nstatus: in-progress\ntype: bug\n---\n\nBody here.\n"
}
```

```json
{
  "operation": "create",
  "path": "my-note.md",
  "content": "---\ntitle: \"My note\"\n---\nContent.\n",
  "overwrite": false
}
```

```json
{ "operation": "delete", "path": "old-note.md" }
```

```json
{
  "operation": "update_frontmatter",
  "path": "task-abc--fix-login.md",
  "fields": {
    "status": "in-progress",
    "pr": "123",
    "branch": "feature/cascade-status-and-skills-npm"
  }
}
```

### Frontmatter conventions

- `title` values are **always double-quoted** in frontmatter.
  - ✅ `title: "Fix login timeout"`
  - ❌ `title: Fix login timeout`
- Dates use ISO 8601: `2026-01-01T00:00:00Z`
- Standard fields: `title`, `status`, `type`, `priority`, `tags`, `parent_id`, `blocking_ids`, `blocked_by_ids`, `pr`, `branch`, `created_at`, `updated_at`

---

## Caching Behaviour

The server caches unfiltered `list` calls (no status/type/search filter) using a two-layer strategy:

1. **Burst TTL (5 s):** Repeated calls within 5 seconds return the in-memory cache instantly.
2. **Timestamp check:** After 5 s, a lightweight query fetches only `id + updatedAt` for all beans. If nothing has changed, the full cached result is returned without a full GraphQL round-trip.
3. **Mutations invalidate:** `create`, `update`, and `delete` always invalidate the cache immediately.

Filtered queries (status/type/search) are **never cached** and always hit the CLI.

---

## Common Patterns

### Create an epic with child tasks in one workflow

```jsonc
// Step 1 — create the parent epic
{ "title": "User Authentication", "type": "epic", "status": "todo", "priority": "high" }

// Step 2 — bulk create children under it
{
  "beans": [
    { "title": "Design auth schema", "type": "task" },
    { "title": "Implement JWT flow", "type": "task" },
    { "title": "Add refresh token support", "type": "task" },
    { "title": "Write integration tests", "type": "task" }
  ],
  "parent": "<epic-id-from-step-1>"
}
```

### Mark a task in-progress and add body notes

```json
{
  "beanId": "task-xyz",
  "status": "in-progress",
  "bodyAppend": "\n## Progress\n\n- [x] Schema designed\n- [ ] Implementation started\n"
}
```

### Reassign a group of tasks to a new epic

```json
{
  "beans": [{ "beanId": "task-001" }, { "beanId": "task-002" }, { "beanId": "task-003" }],
  "parent": "epic-new-parent"
}
```

---

## Trigger Guidance (Description Optimization)

This skill should trigger for prompts like:

- “Can you update this backlog item and link it to its blocker?”
- “Move these tasks under an epic and mark one in-progress.”
- “Edit the bean frontmatter and set PR/branch metadata.”

This skill should **not** trigger for prompts like:

- “Open a GitHub issue in repo X” (without Beans workspace context)
- “Update Jira ticket ABC-123” (external tracker)

---

## Evaluation Starter (Output Quality + Triggering)

Use `evals/evals.json` as the canonical test set and iterate in `iteration-N/` workspace folders.

- Start with 2–3 realistic prompts, then expand.
- Include both should-trigger and should-not-trigger cases.
- Add assertions after first outputs to avoid brittle checks.

Use this file layout:

- `evals/evals.json`
- optional fixtures under `evals/files/`

If you add scripts later, keep them non-interactive, expose `--help`, and emit structured output (JSON) on stdout.
