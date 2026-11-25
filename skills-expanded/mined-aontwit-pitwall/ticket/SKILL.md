---
name: ticket
description: Ticket — the tracker adapter of pitwall. Create / find / update the tracker task for each piece of work (plan work = subtask under the phase's parent task; review = merged) so work the PM didn't hand out, improvements you found yourself, and every task the agent loop does show up where the team scores it. Trackers are `clickup`, `github` (GitHub Issues) and `none` (no tasks, the PR is the record). Use when the user runs /pitwall:ticket, "สร้าง task", "เปิด task ใน sprint" — /pitwall:lap calls this skill itself · repo values live in .claude/agent-loop.md
user-invocable: true
---

# /pitwall:ticket — the tracker task for each piece of work

Read the `tracker` section of `.claude/agent-loop.md` first — its first row is `tracker: clickup | github | none` (no section = `none`) · the section numbers the playbooks cite (2–6) mean those sections of the adapter in use

## Tracker `none`

No tracker tasks: the PR is the record of the work · `/pitwall:ticket …` typed by the user → say "this repo has no tracker (profile `tracker: none`)" and stop (`/pitwall:ticket agent` too) · every call from the loop → do nothing, return

The sections from here to "GitHub adapter" are the `clickup` adapter (values from the profile: workspace / space / sprint folder, tag, QA, names) · `tracker: github` → section "GitHub adapter" at the end

Arguments:
- `/pitwall:ticket <subject + details>` = create a task in the current sprint with status `to do`
- `/pitwall:ticket agent <subject + details>` = create it and also put it in the loop's queue (it must pass the `/pitwall:queue` criteria)
- called from `/pitwall:lap` = find the task for that work; none → create it (sections 3–4) · update it per event (section 5)

Operations the playbooks call by name:

| Operation | clickup | github |
|---|---|---|
| Find open tasks (`/pitwall:queue`) | section 2 → `clickup_filter_tasks list_ids=[sprint]` with the profile's tag, status `to do`, assignee me or empty | open issues with the profile's agent label and no status label, assignee me or empty (GitHub adapter G2) |
| Read a parent with its subtasks (`/pitwall:lap` tracker sync) | `clickup_get_task include=["subtasks"]` | `gh api repos/{owner}/{repo}/issues/<n>/sub_issues` (G3) |
| Create / status / comment | sections 4–5 | G4–G5 |

## 1. Common values

| | |
|---|---|
| me | `clickup_resolve_assignees ["me"]` — use the numeric id, don't hardcode it |
| statuses the agent uses | `to do` · `in progress` · `review` · `pending` (blocked) — the stages after review (`rejected`, `wait to deploy`, `on prod` …) QA / PM move themselves |
| `review` means | merged into base, testable on dev (not just a PR opened) |
| tags | the repo tag **plus** one tag per server / game the work changes (the ones QA must test), both from the profile — a group / phase parent gets the repo tag only · work for every server gets every server tag · not sure which servers → read the diff / brief, never guess (no PR yet → repo tag only, add the server tags when the PR opens) · tags must already exist; never create a new one |

## 2. Find the current sprint

`clickup_get_workspace_hierarchy space_ids=[<space>] max_depth="2"` → in the profile's sprint folder, pick the list whose date range in its name covers today (`clickup_get_folder` does not return the list names — don't use it)
No list covers today → **never guess**: manual → ask the user · from the loop → skip the tracker step and write in the PR "No sprint list for today yet"

## 3. Names + structure (names from the profile — the way the team actually names things)

| Work | Structure |
|---|---|
| a plan row | a **subtask** under 1 parent task per phase |
| other work whose kind has a sprint group in the profile (bug, backend request …) | a **subtask** under that kind's group parent of **this** sprint, named per the profile (e.g. with an area prefix) |
| other work with no group in the profile | a standalone task in the sprint |
| work the profile marks "not tracked" | **no task** — say so in the report / PR ("not tracked in the sprint") |

Avoid duplicates: `clickup_filter_tasks list_ids=[sprint] include_closed=true` → a name that starts the same way (parent: phase or group name, child: `<prefix> <id> `) → use that one
The phase parent is not in this sprint (the phase spans sprints) → look in the previous sprint by the same name; found → use it, not found → only then create it · a group parent belongs to one sprint: not in this sprint → create it (section 4)

## 4. Create

Every one: `clickup_create_task` list_id=current sprint, **assignees=[<id of me>], never empty**, tags per section 1 → `clickup_get_task` to confirm me is on it and the tags are there (not there → the assignee rule in section 5)
- **phase parent task**: status `in progress` · description in the profile's tracker language · Why (the plan's goal + the phase) / What (link to the phase file, 1 subtask = 1 row = 1 PR) / Done when (all subtasks merged + QA per the phase's combined DoD)
- **group parent task**: status `in progress` · Why (the team groups this kind of work per sprint) / What (subtask = 1 item, the name format from the profile) / Done when (every subtask at `review` or later)
- **subtask**: `parent=<parent id>`, status `in progress` (loop) · manual work under a group parent: `to do` — parent already in `review` → parent back to `in progress` + comment (in the profile's tracker language) "Added <subtask> — back to in progress until everything is merged"
- **standalone task**: status manual `to do` · loop `in progress`

Description of a subtask / standalone task (body in the profile's tracker language):

```markdown
## Why
<problem / opportunity — for work you found yourself, say where you found it (code, user, metric)>

## What
<short scope + main files · plan work: link the row in the phase file instead of copying it>

## Done when
- <checkable criteria — level A/B/C of `/pitwall:gauge`>
```

No points / estimate — the team scores it at sprint review · manual: not enough information to write "Done when" → ask the user 1 question before creating

## 5. Updates along the way (called by the loop) — short team-style comment, no tables (the Verify table / size live in the PR)

Comment templates below are in English; write them in the profile's tracker language.

| Event | subtask / standalone task | parent task |
|---|---|---|
| PR opened | **keep `in progress`** + server tags the diff changes that the task lacks (`clickup_add_tag_to_task`, section 1) + 1-line comment `PR #<n> opened (waiting for merge) — <what it does> · no testing needed yet` → store `prCommentId` in state | don't touch |
| PR merged (sync at the start of a `/pitwall:lap` round) | → `review` + ✅ on the PR comment: the API has no reactions, so use `clickup_update_comment` to prepend `✅ merged <YYYY-MM-DD> — ` to the existing text | see the next row |
| the parent has **≥ 1** subtask and **every one** is in `review` or later | — | → `review` + comment to QA: `merged to <base>: PR #a, #b · <effect on users / regression scope> · please test on dev: <level C steps from the PR> [@<QA>](#user_mention#<id>)` |
| PR closed without merge | keep `in progress` + comment the reason + report to the user | don't touch |
| park | → `pending` + 1–2 line comment with the reason / question | don't touch |

- **Changing status: `clickup_update_task` sends only `task_id` + `status`** — never send `assignees` in the same call (the tool replaces the whole list)
- **Assignee rule (after every create or status change):** there must be ≥ 1 assignee and me must be one — me missing → `clickup_update_task assignees=[<everyone already there> + me]` (never remove anyone, including QA)

## 6. `/pitwall:ticket agent`

Create per section 4 (status `to do`), then check the `/pitwall:queue` criteria — pass → add to `queue` in state: `{ "id": "t-<task id>", "source": "tracker", "trackerId": "<task id>", "playbook": null }` · fail → say which criteria failed (the task stays in the sprint for a human to do)

## Report

Task link + sprint + status + (if any) whether it was added to the loop's queue — in the profile's user language

## Never

- Never touch other people's tasks (without me) **except** tasks the agent created itself (in state / subtasks of a parent in `parents`), to which you may add me back · never change priority / points · assignee: you may only add me
- Never create a task outside the profile's sprint folder; never create a new tag / list; never delete a task
- Never move to `rejected` / `accepted` / `wait to deploy` / `on prod` / `complete`

## GitHub adapter (`tracker: github`)

GitHub Issues as the tracker, through `gh` (no MCP needed) · values from the profile's `tracker` section: the agent label, the three status labels, QA login, milestone mode · `{owner}/{repo}` = the repo's origin · section numbers G2–G6 stand in for 2–6 above

### G1. Common values

| | |
|---|---|
| me | `gh api user -q .login` — use the login, don't hardcode it · assign with `--add-assignee @me` |
| status | carried by labels from the profile, never by closing: `to do` = open with no status label · `in progress` / `review` / `pending` = the profile's label for each · move with `gh issue edit <n> --add-label "<new>" --remove-label "<old>"` (one call, so the issue never shows two statuses) |
| `review` means | merged into base, testable on dev — **people close the issue** after QA, the agent never does |
| labels | every label the profile names must already exist (`gh label list --json name`) — missing → never create it: manual → tell the user which · loop → skip that label and write "label `<name>` missing" in the PR |
| PR link | the PR body says `Refs #<n>` — **never** `Closes` / `Fixes` / `Resolves #<n>`: those close the issue on merge and skip QA |

### G2. Find open tasks + the current milestone

Open tasks (`/pitwall:queue`): `gh issue list --state open --label "<agent label>" --assignee @me --json number,title,labels,body` and again with `--search "no:assignee"` in place of `--assignee @me` → drop issues carrying any status label · the issue body must have a checkable "Done when" (queue criterion 1) · an issue created seconds ago can be missing from the list (GitHub indexes it with a short delay) — an empty result right after a create → list once more before deciding there is nothing

Milestone (profile `milestone: current | none`): `none` → issues get no milestone · `current` → `gh api "repos/{owner}/{repo}/milestones?state=open" --jq '.[] | {number,title,due_on}'` → the open milestone with the earliest `due_on` on or after today · none matches → **never guess**: manual → ask the user · from the loop → create without a milestone and write in the PR "No milestone for today yet"

### G3. Names + structure

| Work | Structure |
|---|---|
| a plan row | a **sub-issue** under 1 parent issue per phase |
| other work / improvements you found yourself | a standalone issue |

Avoid duplicates: `gh issue list --state all --search "<prefix> in:title" --json number,title,state` (parent: the phase name, child: `<prefix> <id> `) → a title that starts the same way → use that one · a parent spans milestones, so search it without a milestone filter
Read a parent's sub-issues: `gh api repos/{owner}/{repo}/issues/<parent>/sub_issues --jq '.[] | {number, state, labels: [.labels[].name], assignees: [.assignees[].login]}'`

### G4. Create

Every one: `gh issue create --title "<name>" --body-file <file> --assignee @me --label "<agent label>"` (+ `--label "<in progress label>"` when the loop starts it, + `--milestone "<title>"` per G2 except for a parent) → the command prints the URL; the number is its last segment
- **phase parent issue**: label `in progress` · body in the profile's tracker language: Why (the plan's goal + the phase) / What (link to the phase file, 1 sub-issue = 1 row = 1 PR) / Done when (all sub-issues merged + QA per the phase's combined DoD)
- **sub-issue**: create it, then attach it by the issue **id** (not the number): `gh api -X POST repos/{owner}/{repo}/issues/<parent>/sub_issues -F sub_issue_id=$(gh api repos/{owner}/{repo}/issues/<n> -q .id)` — parent already labelled `review` → move it back to `in progress` + comment (tracker language) "Added #<n> — back to in progress until everything is merged"
- **standalone issue**: manual → no status label (`to do`) · loop → `in progress`

Body: the same Why / What / Done when template as section 4 · no estimate

### G5. Updates along the way (called by the loop)

| Event | sub-issue / standalone issue | parent issue |
|---|---|---|
| PR opened | **keep `in progress`** + 1-line comment `PR #<pr> opened (waiting for merge) — <what it does> · no testing needed yet` via `gh issue comment <n> --body-file <file>` → the printed URL ends in `#issuecomment-<id>` → store that id as `prCommentId` | don't touch |
| PR merged (sync at the start of a `/pitwall:lap` round) | → `review` + prepend `✅ merged <YYYY-MM-DD> — ` to the PR comment: `gh api repos/{owner}/{repo}/issues/comments/<prCommentId> -q .body`, then `gh api -X PATCH repos/{owner}/{repo}/issues/comments/<prCommentId> -f body="<new text>"` | see the next row |
| the parent has **≥ 1** sub-issue and **every one** is labelled `review` or closed | — | → `review` + comment to QA: `merged to <base>: PR #a, #b · <effect on users / regression scope> · please test on dev: <level C steps from the PR> @<QA login>` |
| PR closed without merge | keep `in progress` + comment the reason + report to the user | don't touch |
| park | → `pending` + 1–2 line comment with the reason / question | don't touch |

Assignee rule (after every create or status change): `gh issue view <n> --json assignees` — me missing → `gh issue edit <n> --add-assignee @me` (never `--remove-assignee`)

### G6. `/pitwall:ticket agent`

Create per G4 (no status label), then check the `/pitwall:queue` criteria — pass → `queue` += `{ "id": "t-<number>", "source": "tracker", "trackerId": "<number>", "playbook": null }` · fail → say which criteria failed

### Never (github)

- Never close, reopen, lock, transfer or delete an issue · never create or delete a label or milestone · never edit labels other than the profile's status labels and agent label
- Never touch issues without me **except** issues the agent created (state / sub-issues of a parent in `parents`), to which you may add me back · assignees: only `--add-assignee @me`
