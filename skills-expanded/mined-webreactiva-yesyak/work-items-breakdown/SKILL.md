---
name: work-items-breakdown
description: Converts a spec or an implementation plan into work items for the user's tracker, with the granularity, fields and links the user needs. The tracker can be GitHub or GitLab issues, Jira or Azure DevOps work items, Linear issues, or a plain task list. Use it whenever the user asks to create issues, tickets, tasks, stories, epics, a backlog or a board from a spec or plan, or asks "how do we split this work for the team".
---

# Work items breakdown

Creating items in a shared tracker is visible to other people. Always show a preview and get a clear yes before you create anything.

## 1. Ask what the user needs

Ask these questions in one round (with recommended options first), unless the answers are already clear:

| Question | Typical options |
| --- | --- |
| Where do the items go? | GitHub issues (`gh`), GitLab issues (`glab`), Jira, Azure DevOps (`az boards`), Linear, a task list that the project keeps in git (the task file it already has, otherwise `docs/<slug>-tasks.md`) |
| What granularity? | One item per plan step (Recommended when a plan exists), one per acceptance criterion, one epic with child tasks |
| Which fields? | Labels, milestone, assignee, estimate, parent or epic, iteration |
| Do items link to each other? | Dependencies from the plan order, parent/child |

Check which tools are available (`gh auth status`, `glab auth status`, `az account show`, MCP servers). If none works, produce a markdown file and say how to import it.

## 2. Build each item

For a local markdown list, write one table: title, criteria ids, depends on, labels. Use the full item below only for an external tracker.

```markdown
Title: <feature slug>: <step or capability in the imperative>

## Context
One or two sentences. Link to docs/<slug>-spec.md and docs/<slug>-plan.md.

## Acceptance criteria
- AC-15 Order cancelled before shipping: Given … When … Then …

## Definition of done
- Tests for the criteria pass in the full suite.
- Docs and ADRs updated.
- Manual check: <from the plan>

## Depends on
- <item titles or ids>
```

- Write items in the document language of `simplified-technical-language`.
- Add a label or tag with the feature slug.
- In an external tracker, copy the criteria text, not only the ids. People read it outside the repository.

## 3. Preview and confirm

Show a table of all items (title, criteria, depends on, labels) and the command or API you will use. Ask for confirmation. Apply the user's changes and show the table again if they change anything.

## 4. Create and record

- Create items in dependency order so you can link real ids.
- For an external tracker, save the mapping to `.scratchpad/<slug>/work-items.md`: item id or URL, title, criteria, plan step. A task list in the repo is its own record: commit it with the plan, never only in `.scratchpad/`.
- Report the links. If a creation fails, list it with the error; do not retry blindly.
