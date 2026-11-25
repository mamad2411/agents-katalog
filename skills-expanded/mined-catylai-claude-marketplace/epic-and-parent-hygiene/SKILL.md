---
name: epic-and-parent-hygiene
description: "Sets, verifies and audits Jira parents (epics and higher levels) via the parent field. Use when parenting a new issue, when an issue has no parent or a dead one, or when auditing epics. Not for general JQL sweeps (use jira-jql); not for transitions or comments (use jira-issue-lifecycle)."
license: MIT
---

# Epic and Parent Hygiene on Jira

`tracker-discipline` § Parenting owns the rules: every non-top-level item has a live parent,
the candidate list is a query run every time (shortlist, then full set), a new top-level item
needs the user's approval, the parent goes in the create call, and an orphan is fixed when found.
This skill supplies the Jira mechanics. Calls go through the Atlassian MCP server, REST, or a
pasted issue, as in `jira-issue-lifecycle` § Access.

## One field: `parent`

Jira links every level of its hierarchy through the `parent` field: a sub-task to its standard
issue, a story, task or bug to its epic, and an epic to any level above it. This holds for
company-managed and team-managed projects alike. The old Epic Link and Parent Link custom fields
are gone from the API (dates in
[../jira-issue-lifecycle/references/platform-changes.md](../jira-issue-lifecycle/references/platform-changes.md)),
so write `parent` and nothing else. If a team's saved filters or automation still name
`Epic Link`, tell them; fixing those is their admin's job.

## Find the hierarchy levels

Issue-type names are configurable, so read the levels rather than assuming "Epic":

- MCP: `listJiraProjectIssueTypesMetadata` with the project key (through the execute tool).
- REST: `GET /rest/api/3/issue/createmeta/<PROJECT_KEY>/issuetypes` (section 2 of
  [../jira-issue-lifecycle/references/rest-v3.md](../jira-issue-lifecycle/references/rest-v3.md)).

Each type has a `hierarchyLevel`: `-1` sub-task, `0` standard, `1` epic level, `2` and up for
any levels an organisation added above epics. A type named "Epic Task" at level 0 is a standard
issue. Record the level-1 type names (for `<LEVEL_1_TYPES>` in `jira-jql`) and the highest level
in the `Parent mechanism` and `Top-level items` rows of the `## Issue tracker` section. When
levels above 1 exist, the top-level approval rule applies to the highest level, not to epics.

## Choose a parent

1. Run the dedupe check and decide whether the item is top level (`tracker-discipline`).
2. **Shortlist:** the live-parents query in `jira-jql` with `updated >= -90d` or the project's
   current-bucket label, fix version or component. Present five to ten, or propose one with
   the reason.
3. **Full set:** the same query without the narrowing clause, only when nothing on the shortlist
   fits. If nothing fits there either, ask whether a new top-level item is warranted, and wait.
4. For a sub-task, the parent is the standard issue it belongs to, not an epic.

An issue link (`relates to`, `blocks`) to an epic is not a parent. It does not roll up and does
not satisfy the rule; check `fields.parent`, not the link list.

## Set and verify a parent

- **At creation:** put `parent` in the create call (`createJiraIssue` takes `parent` as a key;
  REST section 5).
- **On an existing issue:** MCP `editJiraIssue` with the parent key; REST section 8.
- **Read back:** the parent key is the one you set and its status category is not `done`, and
  its status is not the mapped `parked` or `declined` one. Jira accepts a dead parent without
  an error, so the read-back is the only check.

Moving a sub-task to another parent is not accepted as a plain edit on every site. If the edit
is rejected, or the read-back shows the old parent, tell the user: the options are Jira's Move
operation in the UI or recreating the sub-task under the right parent.

## Repair orphans

`jira-jql` finds them. Repair each row when found:

| Finding | Repair |
| --- | --- |
| No parent, not top level | Choose a parent (above) and set it. |
| Parent `done`, parked or declined | Re-parent to a live parent. |
| Parent key does not resolve | It was deleted or moved to another project; re-parent. |
| Genuinely top level | Leave it and add a comment saying why it is top level. |
| Should not be done at all | Close it as `declined` with a reason (`jira-issue-lifecycle`). |

<example>
An audit finds PROJ-311 "Add CSV export" with no parent, and PROJ-312 whose parent PROJ-20 is
Done. The shortlist returns PROJ-45 "Reporting Q3" (In Progress) and PROJ-51 "Platform upkeep"
(To Do). Propose PROJ-45 for both, since both are reporting features; after the user agrees,
set it and read both back to confirm parent PROJ-45 with category `indeterminate`.
</example>

<example>
PROJ-88 has no parent but carries a "relates to" link to epic PROJ-40. The link does not count.
Propose PROJ-40 as the parent (the link shows the reporter's intent), set `parent` after the user
agrees, and leave the link in place.
</example>

## Audit parents

**Open epic, no live children.** For each open level-1 issue:

```
project = <PROJECT_KEY> AND parent = <EPIC_KEY> AND statusCategory != Done
```

An empty result means either the epic is finished and nobody closed it, or remaining work was
never filed as a child. Read the epic and ask which: close it with the finished resolution, or
file the remainder as children so the state stops lying.

**Closed epic, live children.** The dead-parent sweep in `jira-jql` finds these. Repair is one of
two: reopen the epic because its work is not finished, or re-parent the open children to a live
parent. Pick one per epic, with the user.

An epic's progress bar counts only the children it has, so 100% says nothing about work never
filed under it.

## Verify

- Every issue you parented reads back with the intended parent key.
- That parent's status category is not `done`, and it is not in a parked or declined status.
- For an audit, report each finding with its repair (done, proposed, or declined by the user)
  and the JQL used, so the sweep can be rerun.
