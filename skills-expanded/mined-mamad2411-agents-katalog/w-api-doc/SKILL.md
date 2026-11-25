---
description: Phase 5 helper for w-task — append/update module api.md with new API operations (GraphQL queries/mutations/subscriptions or REST endpoints) introduced or changed in the current task.
argument-hint: <task-slug>
allowed-tools: Bash, Read, Write, Edit
---

# w-api-doc

Persist API surface documentation per module. One `api.md` per module — sections
grouped by operation, kept current (not append-only) so future readers see the
real state of the API.

Reads `.claude/workflow.yaml`:
- `workflow.module_docs_root`
- `workflow.api_docs_filename` (default `api.md`)
- `project.schema_paths.graphql`

Input: `<state_root>/<task-slug>/impact.md` § GraphQL Schema Changes (or § REST
API Changes if applicable).

---

## Step 1 — Resolve path + scope

Read `state.yaml.module`.
Path: `<module_docs_root>/<NN>-<module>/<api_docs_filename>`

If `module_docs_root` or `api_docs_filename` is null: abort silently
("API doc persistence not configured").

If impact.md has no § GraphQL Schema Changes / § REST API Changes section
or those sections are empty: abort with "No API surface changes in this task."

---

## Step 2 — Parse operations from impact.md

For each operation listed, extract:
- **Name**: e.g. `signUp`, `sendMessage`, `getUserStreams`
- **Type**: query | mutation | subscription | REST endpoint
- **Auth**: required / public / role-scoped (look for `@Public()` / `@Roles()`)
- **Input**: DTO fields (from impact.md or referenced files)
- **Returns**: response type
- **Side effects**: queue jobs, pub/sub channels, cache writes — anything
  non-obvious from the signature

If impact.md doesn't have enough detail, read the actual schema/resolver file
(use `project.schema_paths.graphql` glob to locate).

---

## Step 3 — Read existing api.md

If file exists:
- Parse its current operation sections (heading is `### <OperationName>`).
- For each operation in this task:
  - If already exists → REPLACE that section's body with the new state.
  - If new → APPEND under the appropriate group (Queries / Mutations /
    Subscriptions / REST).

If file does not exist: create with template:
```markdown
# API — <module>

## Queries
## Mutations
## Subscriptions
## REST
```

(Delete empty groups before writing.)

---

## Step 4 — Write operation sections

Per operation template:

```markdown
### <OperationName>
- **Type:** <query|mutation|subscription|REST GET /path>
- **Auth:** <required | public | role: <role>>
- **Input:** <DTO type or inline field list>
  ```
  <inline schema snippet if useful>
  ```
- **Returns:** <output type>
- **Side effects / notes:**
  - <queue job emitted, if any>
  - <pub/sub channel published, if any>
  - <cache invalidation, if any>
  - <any non-obvious behaviour>

Last updated: <task-slug> (<YYYY-MM-DD>)
```

---

## Step 5 — Confirm

Print:
```
api.md updated: <path>
Operations added: <names>
Operations replaced: <names>

Review before /w-task advances Phase 5.
```
