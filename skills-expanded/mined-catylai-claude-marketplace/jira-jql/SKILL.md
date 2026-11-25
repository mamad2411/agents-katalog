---
name: jira-jql
description: "Writes and runs JQL sweeps against Jira. Use when finding issues, auditing a backlog, checking for duplicates before filing, or listing live parents. Not for moving or commenting on an issue (use jira-issue-lifecycle); not for choosing or repairing a parent (use epic-and-parent-hygiene)."
disallowed-tools: Write, Edit, NotebookEdit
license: MIT
---

# JQL on Jira

Every read in this plugin is a JQL query: the dedupe check, the candidate-parent shortlist, the
orphan sweep and each triage pass. This skill owns the expressions and how to report their
results. It only reads; what to do with a row belongs to `jira-issue-lifecycle` and
`epic-and-parent-hygiene`.

## Access

1. **Atlassian MCP server:** `searchJiraIssuesUsingJql(cloudId, jql, fields, maxResults)`, paging
   with the `nextPageToken` it returns. See
   [../jira-issue-lifecycle/references/atlassian-mcp.md](../jira-issue-lifecycle/references/atlassian-mcp.md).
2. **REST, Claude Code only:** `/rest/api/3/search/jql`. The paging loop in section 9 of
   [../jira-issue-lifecycle/references/rest-v3.md](../jira-issue-lifecycle/references/rest-v3.md)
   runs any query below and reports whether the sweep was complete.
3. **Neither:** print the JQL for the user to paste into Jira's issue search (advanced mode), and
   work from the results they paste back. Report the sweep as run by the user.

## Writing the query

Placeholders in `<ANGLE_BRACKETS>` come from the project, never from an example:

- `<PROJECT_KEY>`: from the `## Issue tracker` section.
- `<LEVEL_1_TYPES>`: the issue types at hierarchy level 1 (usually just `Epic`), read from the
  project's issue-type metadata as `epic-and-parent-hygiene` describes. Type names are
  configurable, so a query that hardcodes `Epic` silently misses a project whose level-1 type is
  called something else.
- `<NOT_PARKED>`: the clause that drops parked issues, from the Status mapping. For a parked
  status, `status NOT IN ("On Hold")`. For a parked label, `(labels IS EMPTY OR labels NOT IN
  (parked))`; a bare `labels NOT IN (parked)` also drops every unlabelled issue.

Rules that change the result set:

- **Liveness is `statusCategory != Done`, never `status != Done`.** The name filter drops only
  the status literally called Done and lets every other terminal status through. The category
  filter still keeps parked statuses in `To Do` or `In Progress`, so exclude those by name too.
- **`!=` excludes empty fields.** `assignee != currentUser()` skips unassigned issues; add
  `OR assignee IS EMPTY` when you mean them. Test absence with `IS EMPTY`, never `= null`.
- **`~` matches indexed words, not substrings.** `summary ~ "time"` does not find "timeout";
  use `"time*"` for a prefix and expect stemming.
- **Parenthesise every `OR` inside an `AND`**, and always scope by `project` and `ORDER BY`, so a
  sweep is bounded and reproducible.
- **`issueFunction` and similar come from third-party apps.** On a site without the app they are
  a syntax error; use two queries instead.
- History clauses (`status CHANGED TO … BEFORE -30d`, `WAS`) are slower but find work that
  started and stalled.

## Reporting results

- **Zero rows is ambiguous.** A misspelled status, a renamed status or a wrong project key all
  return an empty, successful result. Before calling a sweep clean, drop the narrowest clause
  and confirm the scope returns something.
- **The search has no `total`.** Report counts as "N issues across all pages", or, when paging
  stopped early, "at least N". A row count equal to `maxResults` is the page size, not the
  population. For an estimate, REST offers an approximate-count endpoint; quote it as approximate.

<example>
The stale in-progress sweep returns nothing. Before reporting, run
`project = PROJ AND statusCategory = "In Progress"` alone: it returns 12 issues, so the scope is
live and the `updated < -14d` clause really matched nothing. Report: "No in-progress issue has
gone 14 days without an update (12 in progress, all read)."
</example>

<example>
The orphan sweep's REST loop ends with `=== INCOMPLETE: stopped after 20 pages and 2000 issues`.
Report "at least 2000 open issues checked; the sweep did not finish", list the orphans found so
far, and offer to rerun with a narrower scope (one component, or `created >= -180d`).
</example>

## Sweeps

**Dedupe before filing** (`tracker-discipline` § Dedupe before creating). Search on the symptom
in two or three phrasings, not on the summary you were about to write:

```
project = <PROJECT_KEY> AND statusCategory != Done
  AND text ~ "<symptom phrase>"
ORDER BY updated DESC
```

That covers live and parked issues, because a parked issue never sits in the `done` category
(see the mapping in `jira-issue-lifecycle`).

For a suspected regression, run it again without the status clause to find the `done` issue it
undoes. Record the result as `NEW`, `DUPLICATE → <KEY>` or `UNCHECKED` (the search could not run).

**Untriaged**, oldest first because those are the ones triage keeps skipping:

```
project = <PROJECT_KEY> AND statusCategory = "To Do" AND assignee IS EMPTY AND labels IS EMPTY
ORDER BY created ASC
```

**Claims to be started, nobody on it.** Every row is a state that is not true:

```
project = <PROJECT_KEY> AND statusCategory = "In Progress" AND assignee IS EMPTY
ORDER BY updated DESC
```

**Stale in progress.** Each row is either blocked work that belongs back in `ready` or `parked`
(`tracker-discipline`), or finished work nobody transitioned:

```
project = <PROJECT_KEY> AND statusCategory = "In Progress" AND updated < -14d
ORDER BY updated ASC
```

**Closed with no reason.** A `done`-category issue without a resolution cannot be told apart
from abandoned work:

```
project = <PROJECT_KEY> AND statusCategory = Done AND resolution IS EMPTY
ORDER BY resolved DESC
```

**Everything about one key**, for "why is this code here":

```
project = <PROJECT_KEY> AND (issuekey = <KEY> OR parent = <KEY> OR text ~ "<KEY>")
ORDER BY created ASC
```

**Live parents** (the `tracker-discipline` shortlist and full set; `epic-and-parent-hygiene`
decides which to use):

```
project = <PROJECT_KEY> AND issuetype IN (<LEVEL_1_TYPES>)
  AND statusCategory != Done AND <NOT_PARKED>
ORDER BY updated DESC
```

Add `AND updated >= -90d`, or the project's current-bucket label, fix version or component, for
the shortlist.

## Orphan sweep

An orphan is a live issue below the top level with no parent, a dead parent, or a parent that
no longer exists (`tracker-discipline` § Parenting).

**No parent:**

```
project = <PROJECT_KEY> AND statusCategory != Done
  AND issuetype NOT IN (<LEVEL_1_TYPES>, <HIGHER_LEVEL_TYPES>)
  AND parent IS EMPTY
ORDER BY created DESC
```

Leave out `<HIGHER_LEVEL_TYPES>` when the project has nothing above level 1. Sub-tasks always
have a parent, so they never appear here.

**Dead parent.** JQL cannot filter on the parent's status, so fetch live issues that have a
parent, with the `parent` field, and check each parent's status in the result:

```
project = <PROJECT_KEY> AND statusCategory != Done AND parent IS NOT EMPTY
ORDER BY updated DESC
```

A row whose parent is in the `done` category, or in a parked or declined status, is an orphan.
The REST loop prints `parent=<KEY>(<category>)` on every row for this. If a result omits the
parent's status, read that parent directly.

**Parent no longer exists:** shows as an error when reading the parent key, not as a row. Treat
it the same way.

Hand every orphan to `epic-and-parent-hygiene` for the repair; a sweep that only lists orphans
has not fixed any.

## Boards and sprints

Sprint clauses depend on boards. `sprint in openSprints()` means open on any board, which in a
project with two boards is rarely the question; scope by the board's sprint instead. Board ids
come from the board endpoint (REST section 10) and differ per site.

## Verify

For every sweep you report:

- the query ran with a `project` scope and an `ORDER BY`;
- an empty result was checked by widening the query;
- the count is labelled complete, "at least N", or approximate;
- the JQL itself is in the report, so the user can rerun it.
