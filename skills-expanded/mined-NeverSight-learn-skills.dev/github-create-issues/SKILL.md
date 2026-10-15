---
name: github-create-issues
description: >-
  Create GitHub Issues from a github_backlog_input.json (the output of
  classify-github-issues) via the bundled create_github_issues.py script. Always
  shows a visual dry-run table first and only creates real issues after the user
  explicitly approves. Use this whenever there is a github_backlog_input.json or
  any file of items to file in GitHub, or when the user says "create these GitHub
  issues", "file the backlog", "push these to GitHub", or "create the issues".
  This is the step that actually writes to the repo, so prefer it over hand-rolling
  API calls. After creating, it writes github_backlog_result.json for
  github-writeback-tracking.
effort: max
---

<!-- generated: third-party requirements -->
> **Requires:** `pip install requests` — this skill's scripts import `requests`.

# github-create-issues

Take a `github_backlog_input.json` and create the issues in GitHub by driving
the bundled `create_github_issues.py`. The script creates the milestone and labels
if needed, creates each issue, then creates a tracking issue with a task list
linking them all.

Creating issues is effectively un-undoable (close is manual; notifications already
fired). So this skill is built around a hard gate: **visual dry-run always, real
run only on an explicit "yes".**

For the exact JSON shapes see `references/data-contracts.md`.

## Prerequisites

- **Auth** — `gh auth login` once (the script reads `gh auth token`). Or set
  `$env:GH_TOKEN`. See the `github-auth` skill.
- **Owner/repo** — set `$env:GH_OWNER` / `$env:GH_REPO`, or include `owner` /
  `repo` in the JSON. Env vars override the JSON.
- **Python + requests + openpyxl** — run the setup checker if unsure:
  `powershell -ExecutionPolicy Bypass -File "${CLAUDE_SKILL_DIR}/scripts/setup_check_github.ps1"`

## Step 1 — VISUAL DRY-RUN (creates nothing)

GitHub Issues has no `validateOnly` API. Instead: read `github_backlog_input.json`
and render a formatted table for the user to review before any API call.

Present:

```
 # | Key    | Title                              | Labels               | Assignee
---|--------|------------------------------------|----------------------|---------
 1 | row-1  | Portal label "Auto" should show... | bug, P1, size:S      | —
 2 | row-2  | Add rate limiting to API           | enhancement, P2, ... | pon
...
Milestone: Audit Wave 1
Tracking issue: yes (created last, links all above)
Total: 2 issues
```

> **GATE — stop here.** Do not proceed until the user has explicitly approved the
> list (e.g. "create them", "go ahead", "yes").

If the user requests changes, update `github_backlog_input.json` and re-render the
table. The table is free — re-rendering costs nothing.

## Step 2 — REAL RUN (only after explicit approval)

```powershell
$env:GH_OWNER = "Cartagena365"
$env:GH_REPO  = "GlassHull"
python "${CLAUDE_SKILL_DIR}/scripts/create_github_issues.py" `
  --input  "<workdir>/github_backlog_input.json" `
  --output "<workdir>/github_backlog_result.json"
```

The script prints one line per created issue (`key X -> #N <url>`) and a final
`tracking issue -> #N <url>`. Then it writes `github_backlog_result.json`.

Relay the output to the user. Surface any failure clearly — a partial run is better
visible than silent.

## After creating — verify

Confirm the items landed. Check `github_backlog_result.json` — every item should
have a `number` and `url`. Items without a `number` failed; surface them to the user.

## Idempotency — don't double-create

`create_github_issues.py` is **not** idempotent: re-running on the same
`github_backlog_input.json` creates a second set of issues. After a successful run,
hand off to **github-writeback-tracking** to stamp `Issue #` / `Issue URL` back onto
source rows. Once a row carries an Issue #, treat it as done. To re-file a subset,
prune the input to only the un-filed `key`s first.
