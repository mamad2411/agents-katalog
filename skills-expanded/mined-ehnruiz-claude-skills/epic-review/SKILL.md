---
name: epic-review
description: Review a Jira epic (or the Jira Product Discovery idea it implements) against its own In Scope list - which items are done, partly done, not started, or have no evidence - then flag scope conflicts and stale statuses, and draft the In Scope list for the follow-on epic. Use this whenever the user is preparing for an epic review, quarter close-out, scope or refinement meeting, asks "what was completed on this epic", "what is left for Q2", "what should carry over", "prep me for the review of PROJ-1234", pastes a JPD idea or epic link with a meeting invite, or needs to fill in a cloned epic whose scope still says TBD.
---

# Epic review

Answer the question a quarter-close meeting asks: of what this epic promised, what is done,
what is left, and what goes into the next one. The answer comes from ticket evidence, item by
item, not from the epic's status field, which is usually stale.

**Requires:** the Atlassian MCP connector (`getJiraIssue`, `searchJiraIssuesUsingJql`,
`searchConfluence`, and `listJiraIssueComments` through `executeRead`). Read-only by default.
Companion skills: `ticket-write` files any missing work this review uncovers, `ticket-digest`
recaps it.

## Team defaults

The rules below are team-neutral. These values are examples. Read the real ones from the
user's `CLAUDE.md` or from the epic itself, and ask once when neither says:

| Setting | Example |
| --- | --- |
| Jira site / delivery project | `your-site.atlassian.net`, project `PROJ` |
| Discovery (JPD) project | `DISC`; ideas link to delivery epics with the **Polaris work item link** type (`implements` / `is implemented by`) |
| Epic summary shape | `T1 \| Q1FY27 \| Area \| Name (Phase n - ...)`; the next quarter's epic is usually a clone, linked with the **Cloners** type |
| Scope sections in descriptions | `### In Scope` and `### Out of Scope` under `## Requirements` |
| Docs home | Confluence, the team's space |

## Workflow

### 1. Resolve the anchor

The user may give a JPD idea URL (`.../polaris/projects/KEY/ideas/...?selectedIssue=KEY-13`),
an epic key, or a board link plus a meeting invite. Take the key from `selectedIssue` when it
is there. Fetch it with `getJiraIssue`, `view: "evidence"`, which also returns issue links.

- **JPD idea:** follow `is implemented by` links to the delivery epic(s). Keep the idea's
  roadmap and target-date fields; they say which quarter the review closes.
- **Epic:** follow `implements` back to the idea, if any, and `is cloned by` forward to the
  next-period epic.

You now have up to three records: **idea**, **epic**, **next epic**.

### 2. Collect

1. The epic's description, read for its In Scope and Out of Scope bullets. If the idea has
   its own lists, read those too; step 4 compares them.
2. Epic comments: `executeRead` with `name: "listJiraIssueComments"`. Earlier rounds of this
   same question often sit there ("which of these were not completed?"), with an answer from
   the epic owner.
3. Children of each epic, **one query per epic**: `parent = PROJ-1200`, fields `summary`,
   `status`, `assignee`. Query them separately; a single `parent in (...)` query does not
   reliably say which epic each row belongs to.
4. One sweep for related tickets outside the epics: the project's area prefix or label in
   the summary (`summary ~ "CHECKOUT"`, `labels = checkout`). Decision, assumption and open-question
   registers often live there as sub-tasks of an unparented task.
5. Optional: `searchConfluence` in the docs home for pages titled with the area name, for
   step 5's documentation question. Titles and last-modified dates are enough.

Do not fetch every ticket's description. Summaries and statuses carry the evidence.

### 3. Map each In Scope item to evidence

One row per In Scope bullet, in the epic's own order and wording (shortened if long). For
each, pick the tickets that deliver it and give one status:

| Mark | Meaning |
| --- | --- |
| ✅ Done | Every delivering ticket is Done |
| 🟡 Partial | Some done, or the rest are In Review / Working |
| ❌ Not started | Delivering tickets exist and are all To Do / Backlog, or the epic owner says so in a comment |
| ❓ No evidence | No ticket, comment or page shows this item; say so, do not guess |

A ticket already parented to the next epic counts as **moved**; say "moved to Q2" in the
evidence cell. Evidence is ticket keys plus status, under 20 words. Name the assignee only
when it matters (unassigned work on the critical path, or the owner is in the meeting).

### 4. Flag what the meeting must decide

At most five flags, most consequential first. Look for:

- **Scope conflicts:** the idea and the epic list the same item on different sides, or an
  item appears in both In and Out of Scope.
- **Status drift:** the epic says To Do while most children are Done, or the idea's target
  date has passed.
- **Unowned critical work:** the one remaining item is unassigned or in Backlog.
- **Open policy:** assumptions that contradict each other, or business decisions still
  open that the next phase depends on.
- **Empty successor:** the next epic's scope still reads TBD.

### 5. Draft the follow-on scope

A paste-ready In Scope list for the next epic, grouped:

1. **Carry over:** every ❌ and 🟡 item from step 3, with keys.
2. **Already parented** to the next epic, with keys.
3. **Candidates** the user's own role or the sweep in step 2 suggests. Mark these as
   proposals.

Then an Out of Scope list, starting from the current epic's. If the documentation home is
part of the outcomes, name the existing pages from step 2.5 and propose a hub structure in
one line per child page.

## Output contract

In this order, in chat:

1. One sentence naming the idea, epic and next epic with keys, and what the meeting must
   produce.
2. The step 3 table: `In Scope item | Status | Evidence`.
3. The step 4 flags, numbered.
4. The step 5 draft.
5. One line offering the write-back (below).

Budget: the whole output under 600 words, table included. Plain language; a ticket key is
the only identifier allowed outside the evidence column.

Example table rows (placeholder keys):

```
| Configure CI/CD pipelines | ❌ Not started | PROJ-1205 PR env Backlog; PROJ-1206 staging Backlog, unassigned, moved to Q2 |
| Locale routing foundation | ✅ Done | PROJ-1203 middleware Done; PROJ-1190 URL decision Done |
| Present to leadership to finalize | ❓ No evidence | No ticket or notes page |
```

## Writing back

This skill does not change Jira on its own. Writing the draft into the next epic happens
only when the user asks, and then:

1. `getJiraIssue` the next epic with `responseContentFormat: "html"` and keep its current
   description.
2. Replace only the `TBD` bullets under In Scope and Out of Scope, leaving Background and
   Stakeholders untouched.
3. `editJiraIssue` with `contentFormat: "html"` so links and mentions survive.
4. Quote the before and after to the user.

New work the review uncovered goes through `ticket-write`, one ticket at a time, after the
user confirms the list.
