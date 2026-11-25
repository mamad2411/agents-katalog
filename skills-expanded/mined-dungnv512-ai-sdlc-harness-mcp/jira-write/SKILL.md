---
name: jira-write
description: Wraps the Jira WRITE scripts (create, update, transition, comment, link) with a mandatory dry-run-then-confirm gate. Use whenever the user wants to create a Jira issue, update fields, change status, add/update a comment, or link two issues. Always previews the exact payload and sends nothing until the user explicitly confirms.
---

# Jira Write Skill

**This is the highest-risk skill in this repo.** Every other skill here is
read-only or writes to a local file the author can `git diff`/revert. This
one, once confirmed, makes a live write against the team's real Jira board
— a board other people are looking at. Follow the gate below exactly; do
not shortcut it because a request "seems simple."

This is a NEW skill (no mother-repo prior art) wrapping the write scripts
from task #3's fetch-layer port:

| Operation | Script | Endpoint |
|---|---|---|
| Create issue | `bin/create-jira-issue.sh` | `POST /rest/api/3/issue` |
| Update issue (incl. reassign — see below) | `bin/update-jira-issue.sh` | `PUT /rest/api/3/issue/{key}` |
| Transition (change status) | `bin/transition-jira-issue.sh` | `POST /rest/api/3/issue/{key}/transitions` |
| Add a comment | `bin/add-jira-comment.sh` | `POST /rest/api/3/issue/{key}/comment` |
| Update an existing comment | `bin/update-jira-comment.sh` | `PUT /rest/api/3/issue/{key}/comment/{id}` |
| Link two issues | `bin/link-jira-issues.sh` | `POST /rest/api/3/issueLink` |

**No standalone assign or delete script exists in this repo's `bin/`, and
neither should be added:**
- **Reassigning an existing issue** is not a separate operation — Jira's
  update endpoint accepts `fields.assignee.id` like any other field, so
  "assign SN-41 to Minh" is a **update** (`bin/update-jira-issue.sh` with
  `{"fields": {"assignee": {"id": "<accountId>"}}}`), not a missing
  capability. Assignment at creation time uses `create-jira-issue.sh`'s
  `JIRA_ASSIGNEE_ID`.
- **There is no delete script, and none may be added.** Org policy forbids
  deleting Jira issues. If a user asks to delete an issue, say plainly that
  this skill has no delete path by design and point them at transitioning
  the issue to a terminal status (e.g. "Won't Do") instead.
  `.claude/settings.json` backs this with an explicit
  `Bash(*delete-jira-issue.sh*)` entry in `permissions.deny` — a standing
  guard against the script being copied back in from the mother repo
  later, not just an absence this skill happens to rely on today.

## The gate: dry-run is the default, confirmation is mandatory

Every invocation of this skill goes through three steps, in order, every
time — there is no "just send it" shortcut:

### Step 1 — Build the payload with `json.dump`, never string-templating

Regardless of which operation, construct the JSON body with a throwaway
`python3 -c` (or heredoc) call that builds a Python `dict` and serializes
it with `json.dump`/`json.dumps` — the exact same technique every script in
`bin/` already uses internally for this reason: **`update-jira-issue.sh`
takes the caller's complete JSON body as passthrough** (no field-level
escaping happens at the script layer — that's correct for the script,
since it's a deliberately generic passthrough, but it means injection risk
lives entirely at this skill's layer, not the script's). A prior task in
this repo already found and fixed a real JSON injection caused by
string-templating model output directly into a JSON literal — do not
repeat it. Concretely: never do `BODY="{\"fields\": {\"summary\": \"$SUMMARY\"}}"`
(a summary containing `"` or `\` breaks or injects); always do:

```bash
python3 -c '
import json, sys
fields = {"summary": sys.argv[1]}
print(json.dumps({"fields": fields}, indent=2))
' "$SUMMARY"
```

This applies to every operation below, including the ones whose underlying
script (`create-jira-issue.sh`, `transition-jira-issue.sh`,
`add-jira-comment.sh`, `link-jira-issues.sh`) already builds its own JSON
internally via `json.dump` — build the SAME shape yourself first, for the
preview, so what you show the user in step 2 is provably what step 4 will
actually send (the script re-derives the identical body from the same
inputs; you are not duplicating logic, you are proving it in advance).

Payload shapes (mirror exactly what each script's own inline `json.dump`
call produces — see that script for the authoritative field list):

| Operation | Shape |
|---|---|
| Create | `{"fields": {"project": {"key": ...}, "issuetype": {"name": ...}, "summary": ..., ["description": ADF paragraph], ["assignee": {"id": ...}], ["priority": {"id": ...}], ["labels": [...]]}}` |
| Update | Whatever `fields`/other top-level keys the requested change needs — e.g. `{"fields": {"assignee": {"id": ...}}}` for a reassignment, `{"fields": {"summary": "..."}}` for a rename. Write it to a temp file and pass via `JIRA_UPDATE_FILE`, not `JIRA_UPDATE_BODY` — a file avoids shell-quoting the JSON content a second time. |
| Transition | `{"transition": {"id": ...} or {"name": ...}, ["fields": {"resolution": {"name": ...}}]}` |
| Add/update comment | `{"body": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": ...}]}, ...]}}` (one paragraph per newline for `update-jira-comment.sh`) |
| Link | `{"outwardIssue": {"key": ...}, "inwardIssue": {"key": ...}, "type": {"name": ...}}` |

### Step 2 — Print the dry run. Send nothing.

Show the user, verbatim:
1. Which script would run and with which env vars (values, not just names)
2. The exact JSON payload from step 1, pretty-printed
3. The exact endpoint/method it targets

**Do not invoke the actual `bin/*-jira-*.sh` write script yet. Do not make
any HTTP request.** This is the default behavior for every call to this
skill — there is no flag or phrasing that skips straight to a live call.

Example dry-run output:

```
DRY RUN — nothing has been sent to Jira.

Would run:
  JIRA_PROJECT_KEY=SN JIRA_ISSUE_TYPE=Task \
  JIRA_SUMMARY="Implement login screen" \
  JIRA_ASSIGNEE_ID=712020:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx \
  bash bin/create-jira-issue.sh

Payload (POST /rest/api/3/issue):
{
  "fields": {
    "project": {"key": "SN"},
    "issuetype": {"name": "Task"},
    "summary": "Implement login screen",
    "assignee": {"id": "712020:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"}
  }
}

Reply to confirm before this is sent live, or say what to change.
```

### Step 3 — Explicit confirmation, every time

Wait for an unambiguous affirmative reply to that specific dry run (e.g.
"yes, send it" / "confirmed" / "go ahead") in the conversation. A prior
general instruction to "just do the Jira stuff" earlier in the session
does NOT count as confirmation for this specific payload — every write
gets its own dry run and its own confirmation, because a payload built
from a misheard detail (wrong assignee, wrong issue key) is exactly the
failure this gate exists to catch before it's live. If the user changes
any input, restart at step 1 with the new value and show a new dry run —
do not patch the old preview and assume it's still been approved.

### Step 4 — Live call, only after confirmation

Only now, run the actual script with the same env vars shown in the dry
run:

```bash
JIRA_PROJECT_KEY=SN JIRA_ISSUE_TYPE=Task JIRA_SUMMARY="Implement login screen" \
JIRA_ASSIGNEE_ID=712020:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx \
bash bin/create-jira-issue.sh
```

This call is a genuine live write, and `.claude/settings.json` deliberately
does **not** put these six scripts in its Bash allowlist — invoking them
here will still prompt for the harness's own permission approval. That is
a second, independent gate on top of this skill's own confirmation step,
not a redundant annoyance: the in-conversation confirmation proves the
*payload* was reviewed; the permission prompt proves the *action* itself
was deliberate. Report back the script's own output (issue key / comment
id / "Linked X -> Y") verbatim — don't paraphrase a Jira key.

## Notes

- All six scripts already `unset AUTH` after their own `curl` call and
  write their raw JSON response under `${JIRA_OUT_DIR:-outputs/jira}/`
  (gitignored) — nothing about this skill changes that.
- `bin/get-jira-transitions.sh` (read-only, in `pull-jira`) is how you find
  the right `JIRA_TRANSITION_ID`/`JIRA_TRANSITION_NAME` before calling
  transition here — run it first if you don't already know the target
  transition.
- If a request would require a script that doesn't exist in this repo's
  `bin/` (delete, standalone assign, bulk edit, etc.), say so plainly
  rather than approximating it with a different write call.
