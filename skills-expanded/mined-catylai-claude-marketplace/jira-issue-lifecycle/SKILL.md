---
name: jira-issue-lifecycle
description: "Runs the Jira calls for pre-work-gate and tracker-discipline: fetch, create, assign, move, comment on and close issues via Atlassian's MCP server, REST or a pasted issue. Use when starting, pausing or ending Jira work. Not for searches (use jira-jql); not for parents (use epic-and-parent-hygiene)."
license: MIT
---

# Issue Lifecycle on Jira

`issue-tracker-core` owns the rules: `pre-work-gate` (the four properties and the summary line)
and `tracker-discipline` (the seven states, dedupe, parenting and the comment templates). This
skill supplies the Jira calls for them, plus the Jira facts that change how the rules apply:
status categories, resolutions, and transitions that differ per workflow.

## Access

Use the first path that works, and say once which one you are on.

1. **Atlassian Rovo MCP server**, as a claude.ai connector or added in Claude Code. It acts as
   the signed-in user and needs no token in the shell. Tool names, `cloudId` and the calling
   rules: [references/atlassian-mcp.md](references/atlassian-mcp.md).
2. **REST API v3 with an API token**, Claude Code only:
   [references/rest-v3.md](references/rest-v3.md). Each block there reads `JIRA_SITE`,
   `JIRA_EMAIL` and `JIRA_API_TOKEN` itself.
3. **A pasted issue**, when neither is available (a web session without the connector, a denied
   tool, no token). Ask for the key, summary, status, resolution, assignee, parent and its
   status, description, and any comment that set or changed scope. Run the same checks with
   `Source: pasted`, and print every write (transition, assignment, comment) for the user to
   apply in Jira; none of it is recorded until they confirm.

If an MCP call fails on sign-in, ask the user to reconnect and move to the next path rather
than retrying.

## Configure the project

The core reads the `## Issue tracker` section of the project's `CLAUDE.md` (template:
`references/tracker-config.md` in `issue-tracker-core:tracker-discipline`). For Jira, fill it as:

| Setting | Jira value |
| --- | --- |
| Tracker | `jira-tracker` |
| Project | The project key, and the site host when there is more than one site |
| Ticket pattern | `<PROJECT_KEY>-[0-9]+`, for example `PROJ-[0-9]+` |
| Intake state | The status a new issue lands in (read one back after creating it) |
| Parent mechanism | `parent` field; name the level-1 type, usually Epic (see `epic-and-parent-hygiene`) |
| Top-level items | The highest hierarchy level in use, and who approves a new one |

The core's default pattern `[A-Z][A-Z0-9]+-[0-9]+` already matches Jira keys, but it also
matches another project's keys or a branch such as `docs/RFC-2119-alignment`. The project key
in the row avoids that.

## Map the workflow onto the seven states

Jira has no fixed states: each project's workflow defines statuses, and every status belongs to
one of three categories, `new`, `indeterminate` or `done`. Read the project's statuses and
resolutions once (MCP: ask `discover` for the project's statuses and resolutions; REST:
`GET /rest/api/3/project/<KEY>/statuses` and `GET /rest/api/3/resolution`), then write the
core's Status mapping table
(`tracker-discipline` rule 2, Map, do not extend). Jira-specific points:

- **`done` and `declined` share the `done` category.** The resolution tells them apart, so record
  both halves: `done | Done + resolution Done`, `declined | Done + resolution Won't Do`.
- **No review status:** carry `in-review` as `In Progress + linked PR`, as the core suggests.
- **No parked status:** carry `parked` as an unresolved issue in a `new`-category status with a
  `parked` label and a comment naming the revisit condition. A `done`-category status would make
  it count as finished in every rollup.
- Adding a status is a workflow edit for a Jira admin, not something to do from here.

<example>
Workflow statuses: Backlog (new), Selected for Development (new), In Progress (indeterminate),
Code Review (indeterminate), Done (done). Resolutions: Done, Won't Do, Duplicate.

| Core state | Tracker |
|---|---|
| backlog | Backlog |
| ready | Selected for Development |
| in-progress | In Progress |
| in-review | Code Review |
| done | Done + resolution Done |
| parked | Backlog + label `parked` + revisit comment |
| declined | Done + resolution Won't Do (or Duplicate, with a link to the original) |
</example>

## Gate calls

`pre-work-gate` finds the key (branch, message, session) with the `Ticket pattern` row. Then:

1. **Fetch** the issue (MCP `getJiraIssue`; REST section 3). You need summary, status name and
   category, resolution, assignee, issue type, and the parent with its status. Not found or not
   visible means `Exists` fails: ask which issue the work belongs to rather than creating one to
   pass the gate.
2. **Read the comments**, every page. A scope decision often lives in a comment rather than the
   description (REST section 4 prints them as text and says whether the thread is complete).
3. **Check the properties** with Jira's specifics:
   - *Assigned:* an assignee is an `accountId`. Find one with `lookupJiraAccountId` or the
     assignable-user search; never guess or reuse one.
   - *Workable:* translate the status through the Status mapping. Without a mapping, ask; the
     category alone cannot tell `ready` from `backlog` or `in-review` from `in-progress`.
   - *Parented:* the parent's category is not `done` and its status is not the mapped `parked`
     or `declined` one. Details in `epic-and-parent-hygiene`.
4. **Print the core summary**, with `State: <core state> (<Jira status name>)`.

<example>
Branch `fix/PROJ-212-null-payload`. `getJiraIssue` returns status "Selected for Development"
(category `new`), no assignee, parent PROJ-40 In Progress.

```
[PROJ-212] Intake parser crashes on empty payload
State: ready (Selected for Development) · Assignee: unassigned · Parent: PROJ-40 · Source: tracker
Gate: FAIL: assigned
```

Offer to assign it to the user (their `accountId` from the lookup), then transition it to
In Progress and post the start comment, reading the issue back after each write.
</example>

## Create an issue

1. Run `tracker-discipline` § Dedupe before creating first; `jira-jql` has the query.
2. Pick the issue type from the project's metadata (`listJiraProjectIssueTypesMetadata`; REST
   createmeta), and read the required fields for that type. A create that fails naming
   `customfield_NNNNN` is missing one of those.
3. Create in one call with project, type, summary, description, assignee and `parent`
   (`tracker-discipline` § Parenting, step 5).
4. Read it back: note the key, the status it landed in, and that the parent is live.

## Transitions

Transition ids belong to a workflow and change when an admin edits it, so list them from the
issue in hand every time (`getTransitionsForJiraIssue`; REST section 6). The list holds only the
moves allowed from the current status. When the move you want is missing, the workflow does not
allow it from here: tell the user rather than chaining other transitions to get there.

A transition can carry a screen with required fields (often the resolution). The assignee is
often not on that screen, so assign in a separate call. A successful transition returns no
body, so read the status and resolution back.

## Comments

Use the three templates in `tracker-discipline` § Comment trail (start, handoff, finish) with
the state move each one explains. Through MCP, `addOrEditJiraIssueComment` takes Markdown.
Through REST, the body is Atlassian Document Format with one paragraph node per paragraph;
REST section 7 builds it. Keep comments unrestricted unless the content requires a role or
group restriction, because a restricted comment is invisible to everyone outside it.

## When the change merges

A Jira issue moves only when something moves it. Find out which of these the project uses, and
note it in the `## Issue tracker` section:

1. **An explicit transition** at finish, with the finish comment.
2. **A Jira automation rule**, for example on "pull request merged". An admin configures it.
3. **Smart Commits**, a Jira feature: a commit line such as `PROJ-123 #comment Fixed the retry
   bound` or `PROJ-123 #<transition-name>` acts on the issue when the commit reaches a connected
   repository. It works only when an admin has enabled Smart Commits on the source integration
   and the commit email matches a Jira user; confirm with the team before relying on it.

Branch names, commit scopes and PR titles carry the key per
`issue-tracker-core:branch-and-title-conventions`. Where a development integration (GitHub for
Jira, GitLab, Bitbucket) is installed, that key is what links the branch, commits and PR to the
issue. Jira has no closing keyword, so whichever option applies, read the issue back after merge.

## Close and reopen

Close with the transition and the resolution in the same call, so the issue never sits closed
without a reason: the finished resolution for `done`, the not-doing one for `declined`. Reopen
with the transition back and the resolution cleared; if the read-back still shows a resolution,
clear it with an edit and say so in a comment. REST section 6 has both calls.

<example>
PROJ-77 was closed as Done yesterday; the fix regressed. The team reopens it.
Transition PROJ-77 back to In Progress with the resolution cleared, read it back
(status In Progress, category `indeterminate`, resolution none), and comment: "Reopened: the
retry bound regressed in the 2.3 release. Next step: add a test for the 5-attempt limit."
</example>

## Failure paths

| Situation | Response |
| --- | --- |
| No MCP tools, no token, no paste yet | Ask the user to paste the issue (Access, path 3). |
| MCP sign-in expired | Ask for `/mcp` sign-in or a reconnect at claude.ai/customize/connectors; continue on the next path. |
| Permission denied on a write | Report which write and print it for the user to apply in Jira. |
| Transition not offered | Say the workflow does not allow it from the current status; ask how to proceed. |
| A write succeeded but the read-back shows no change | A parameter was dropped or wrong; check the schema or REST body and repeat once. |

## Verify

After every write, read the issue back and check:

- the status translates, through the Status mapping, to the core state you intended;
- the resolution is set for `done` and `declined` and empty for live states;
- the assignee is the intended `accountId`;
- the newest comment is the one you posted;
- a new or changed parent exists and is live.

From pasted data, print the same checklist for the user to confirm after they apply the change.
