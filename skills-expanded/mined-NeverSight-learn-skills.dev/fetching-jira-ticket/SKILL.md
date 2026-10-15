---
name: fetching-jira-ticket
description: >
  Retrieve ALL information from a Jira ticket (description, comments, subtasks,
  attachments metadata, labels, sprint, status, assignee, reporter, etc.) and
  persist it as a single Markdown file. Use when the user says "fetch ticket",
  "retrieve Jira", "pull ticket info", "get ticket details", or provides a Jira
  ticket URL or key like PROJECT-1234. This skill ONLY retrieves — it never
  modifies the ticket or starts implementation.
allowed-tools:
  - mcp__jira__*
  - Read
  - Write
  - Grep
---

# Fetching Jira Ticket

## Purpose

Extract every available field from a Jira ticket and its subtasks, then write a
comprehensive Markdown snapshot to `docs/`. This file becomes the single source
of truth for all downstream skills (planning, subtask creation, execution).

## Inputs

| Input        | Source              | Required | Example                                                     |
| ------------ | ------------------- | -------- | ----------------------------------------------------------- |
| `TICKET_KEY` | User / `$ARGUMENTS` | Yes      | `JNS-6065`                                                  |
| `JIRA_URL`   | User (optional)     | No       | `https://vukaheavyindustries.atlassian.net/browse/JNS-6065` |

If the user provides a full URL, extract the ticket key from it.

## Output

A Markdown file at:

```
docs/<TICKET_KEY>.md
```

## Retrieval Checklist

You MUST retrieve **all** of the following. If a field is empty or unavailable,
write `_None_` — never silently omit it.

### Core fields

- Ticket key & URL
- Summary / title
- Status, Resolution
- Type (Story, Bug, Task, Epic, ...)
- Priority
- Labels, Components
- Fix Version(s), Affects Version(s)
- Sprint / Board
- Epic link (if any)
- Assignee, Reporter
- Created date, Updated date, Due date

### Rich content

- **Description** — full body, preserve formatting
- **Acceptance criteria** — if present as a custom field or within description
- **Comments** — every comment, with author and timestamp, in chronological order
- **Attachments** — list filenames, types, and sizes (do not download binary files)

### Subtasks & linked issues

For **each subtask** and **each linked issue**:

1. Retrieve its key, summary, status, assignee, and type.
2. Retrieve its full description.
3. Retrieve all its comments (author + timestamp + body).
4. Note the link type (e.g., "is blocked by", "relates to").

### Custom fields

Retrieve any non-empty custom fields visible on the ticket and list them under a
`## Custom Fields` section.

## Document Template

Write the file using this structure:

```markdown
# <TICKET_KEY>: <Summary>

> Retrieved on: <YYYY-MM-DD HH:MM UTC>

## Metadata

| Field           | Value |
| --------------- | ----- |
| Status          | ...   |
| Type            | ...   |
| Priority        | ...   |
| Assignee        | ...   |
| Reporter        | ...   |
| Labels          | ...   |
| Components      | ...   |
| Sprint          | ...   |
| Epic            | ...   |
| Fix Version     | ...   |
| Affects Version | ...   |
| Created         | ...   |
| Updated         | ...   |
| Due Date        | ...   |

## Description

<full description body>

## Acceptance Criteria

<if present>

## Comments

### Comment 1 — <Author> (<YYYY-MM-DD HH:MM>)

<body>

### Comment 2 — ...

## Subtasks

### <SUBTASK_KEY>: <Summary>

- **Status:** ...
- **Assignee:** ...
- **Type:** ...

#### Description

<body>

#### Comments

##### Comment 1 — <Author> (<date>)

<body>

### <next subtask...>

## Linked Issues

### <LINK_TYPE>: <ISSUE_KEY> — <Summary>

- **Status:** ...
- **Type:** ...

#### Description

<body>

#### Comments

...

## Attachments

| Filename | Type | Size |
| -------- | ---- | ---- |

## Custom Fields

| Field Name | Value |
| ---------- | ----- |
| ...        | ...   |
```

## Execution Rules

1. **Retrieve only.** Do NOT modify the Jira ticket. Do NOT start implementation.
   Do NOT create branches, write code, or propose solutions.
2. **Be exhaustive.** If the Jira MCP tool paginates results (e.g., comments),
   fetch every page.
3. **Preserve fidelity.** Keep original formatting, code blocks, and links from
   the description and comments.
4. **Create `docs/` if missing.** Run `mkdir -p docs` before writing.
5. **Confirm completion.** After writing the file, tell the user:
   - The file path written.
   - A short summary: ticket title, status, number of comments, number of
     subtasks retrieved.
   - Remind the user that this is retrieval only — no action has been taken.

## Validation

After writing the file, re-read it and verify:

- [ ] Every section from the template is present (even if marked `_None_`).
- [ ] Subtask count matches what Jira reported.
- [ ] Comment count per item matches what Jira reported.

If anything is missing, fetch the missing data and update the file before
reporting completion.
