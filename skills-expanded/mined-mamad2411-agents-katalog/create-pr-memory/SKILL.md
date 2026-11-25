---
name: create-pr-memory
description: Use when turning a pull request into an operational memory node. Enforces standardized field collection, preview confirmation, and automatic linking to existing business rules.
---

# Create PR Memory

## Overview

Create a `PRMemory` from the PR itself, not from a vague human recap.

Core rule: read the PR first, then synthesize the memory. Never persist without user confirmation.

## When to Use

- A PR was opened, merged, or reviewed and should become searchable memory
- You need durable recall of what a PR changed
- You need to capture changed files, touched areas, and linked work items

Do not use this for generic design decisions or business rules without a specific PR source.

## Required Fields (all mandatory before persisting)

| Field | Source | Description |
|-------|--------|-------------|
| `project` | User or context | Project identifier |
| `repo` | PR metadata | Repository name |
| `pr_number` | PR metadata | PR number |
| `title` | PR metadata | PR title |
| `summary` | Agent synthesis | What the PR does (not just the title restated) |
| `changed_files` | PR metadata | Full list of repo-relative paths |
| `areas` | Inferred from files | Practical labels: frontend, backend, auth, llm, etc. |
| `pr_url` | PR metadata | Full URL to the PR (REQUIRED) |
| `work_item_url` | PR metadata or user | Full URL to the linked card/ticket (REQUIRED) |
| `work_item_summary` | Card/ticket or user | Summary of the card, not the PR |
| `event_date` | PR metadata | ISO 8601 datetime of PR creation or merge |
| `authors` | PR metadata | List of PR authors |

Optional but recommended:

- `work_item_id`
- `work_item_provider`
- `branch`
- `status`
- `merged_at`

## Standardized Workflow

### Step 1: Collect Data Proactively

1. Read the PR from GitHub using `gh pr view` or equivalent.
2. Extract: title, status, branch, authors, changed files, pr_url, linked work item.
3. If the PR has a linked card/ticket, read it to get `work_item_url` and `work_item_summary`.
4. Infer `areas` from the file list.
5. Write an operational `summary` explaining what changed, system area, and intent.
6. Set `event_date` from PR creation or merge date.

### Step 2: Fill Gaps — Ask What You Cannot Find

If any required field is missing after proactive collection, ask the user with specific questions:

```text
Para criar a memória deste PR, preciso das seguintes informações que não consegui encontrar:
- Qual o link do card/ticket relacionado a este PR? (work_item_url)
- Qual o resumo do card? (work_item_summary)
```

Do NOT proceed until all required fields are populated. Do NOT persist with empty required fields.

### Step 3: Search for Related Nodes

Before persisting, search the memory graph for:

1. **Related business rules**: Use `memory.query` with `type=BusinessRule` and keywords from the PR summary and work item summary. Also search by modules/domain overlap.
2. **Related PR memories**: Search by file overlap, area overlap, or same work item.

Present candidates to the user:

```text
Encontrei nós potencialmente relacionados a este PR:

Regras de negócio:
- [memory_id] "Regra X" — motivo da relação

PRs relacionados:
- [repo]#[number] — motivo da relação

Deseja criar links entre este PR e algum desses nós? Se sim, quais e com qual tipo de relação (IMPLEMENTS, EVIDENCES, MODIFIES, RELATED_TO)?
```

If no strong candidate exists, say so and continue.

### Step 4: Preview Before Persisting

Show the complete JSON that will be sent to `memory.pr.create`:

```text
Preview da memória que será criada:

{
  "project": "...",
  "repo": "...",
  "pr_number": ...,
  "title": "...",
  "summary": "...",
  "changed_files": [...],
  "areas": [...],
  "pr_url": "...",
  "work_item_url": "...",
  "work_item_summary": "...",
  "event_date": "...",
  "authors": [...],
  "branch": "...",
  "status": "..."
}

Confirma a criação? (sim/não)
```

### Step 5: Persist and Link

1. Call `memory.pr.create` with all fields.
2. If the user confirmed links in Step 3, call `memory.pr.link_memory` for each confirmed relationship.

## Summary Rules

- The summary must explain what changed, not just restate the title.
- Mention system area and intent.
- Mention risk only if it is materially relevant.
- Keep the summary concise enough for retrieval.

Bad: `Updates proposal flow.`
Better: `Refactors proposal workflow to improve email thread handling and edit-state consistency in the frontend.`

## Changed Files Rules

- Always store the full changed-file list available at capture time.
- Preserve repo-relative paths.
- Do not reduce files to only "important" ones in the canonical payload.

## Area Inference

Use practical labels: `frontend`, `backend`, `auth`, `llm`, `reports`, `admin`, `email`.

Also set `touches_frontend` and `touches_backend` automatically based on areas.

## Common Mistakes

- Creating the memory from the PR title alone
- Omitting changed files
- Persisting without showing preview and getting confirmation
- Saving with empty `pr_url` or `work_item_url`
- Skipping the search for related business rules
- Not asking the user when required information is missing
