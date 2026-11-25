---
name: backlog-task
description: Writes backlog-md-py task records that scan cleanly — CLI-created files, a why/Ship/Constraints description shape, one acceptance criterion per Ship bullet, a single done source. Use when creating a backlog task or drafting or rewriting a task description or acceptance criteria; not for closing, claiming, or reassigning tasks, and not for stores other than backlog-md-py.
license: MIT
spec_hash: 355b7ec32838
metadata:
  version: "1.0.0"
---

# Backlog Task

Task files fail two ways: a dense paragraph buries the deliverables, and the
done-definition drifts out of the acceptance criteria. The shape prevents the
first; the AC rule pins the second.

## Create the task

1. Create it with the CLI, never by hand:
   `uvx --from backlog-md-py backlog-py task create "<title>" --no-dod-defaults`.
   The CLI assigns the id and writes the marker structure; report the assigned
   id.
1. Fill the description inside the markers with the shape below.
1. Add one acceptance criterion per Ship bullet (`--ac`, repeatable), and give
   each verification command its own criterion.
1. Verify: the task appears on the board (`backlog-py board`, or the
   `task_board` MCP tool where wired) with the full description.

## The description shape

```text
<why — one or two sentences, facts only>

Ship:

- <deliverable>

Constraints:

- <constraint>

<decision record — one sentence, dated, when a decision exists>
```

- **Why** states the facts that make the work exist. Keep out argument and
  history.
- **Ship** lists the deliverables, one per bullet. A sentence that fits no
  bullet is context, not a deliverable; move it to Why or cut it.
- **Constraints** states how the work must happen: boundaries, standards,
  owners.
- **Decision record** appears only when a decision was made; one sentence with
  the date, for example "Agreed with the maintainer 2026-10-26: shape-first
  over tooling."

## The AC rule

Every Ship bullet gets an acceptance criterion. A verification command gets
its own criterion. The AC block is the single done source: the DOD section
stays empty unless the store's convention fills it, and the description
carries no restatement of the ACs.

## Edit, not reformat

The marker frame (`SECTION`, `AC:BEGIN`, `DOD:BEGIN` comments) and the
`- [ ] #N` checklist format are the store's contract; backlog-py parses them.
Edit prose only inside the markers. After editing a task file by hand, run
the board and confirm the text survived before calling the edit done.

## Repository rules

The store is generic; the rules around it are not. Read the repo's steering
docs (AGENTS.md, ai-rules) when the task touches them, and carry the rules it
names into the task's Constraints. Common examples:

- every referenced skill is declared in the repo's `agents.toml` in the same
  change that first references it
- mise task names cannot contain colons; use hyphens
- ambiguity is marked, not resolved: record it with a safe default and an
  owner
