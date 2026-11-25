---
name: backlog-hygiene-github
description: "Keeps a GitHub backlog truthful: status labels or issue types, milestones, sub-issue parents, blocked-by links, triage and orphan sweeps. Use when triaging, setting up labels, parenting an issue or auditing a backlog. Not for one issue's work (use issue-lifecycle-github) or boards (use projects-v2)."
allowed-tools: Bash(gh auth status), Bash(gh issue view *), Bash(gh issue list *), Bash(gh label list *)
license: MIT
---

# Backlog Hygiene on GitHub

`issue-tracker-core:tracker-discipline` owns the seven states, rule 2 ("Map, do not extend"), the
dedupe rule and the parenting rules. This skill supplies the GitHub carriers for them and the
sweeps that catch drift. Access (gh, GitHub MCP tools, or pasted data) works as described in
`issue-lifecycle-github`. Reads are pre-approved; every edit asks first.

Shell variables do not survive between Bash calls, so write numbers literally. The sub-issue and
type flags need a recent `gh`; if `gh issue edit --help` lacks `--parent`, use
[references/sub-issues-rest.md](references/sub-issues-rest.md).

## Carrying the seven states

GitHub natively records only `open` and `closed` with a reason, so `done` and `declined` are
native and the other five are carried by `status:` labels or a Projects v2 field. The recommended
Status mapping for the project's `## Issue tracker` section is in `issue-lifecycle-github`'s
`references/issue-tracker-section.md`.

Invariants the sweeps below check:

- Every open issue carries exactly one `status:` label. Closed issues need none; the close reason
  is the state.
- Blocked is a facet, not an eighth state (rule 2). Record it as a native blocked-by link
  (`gh issue edit 123 --add-blocked-by 118`) on an issue that is `ready` or `parked`. A repo may add
  a plain `blocked` label as a filter; `status:blocked` would break the one-status-label invariant.
- GitHub enforces none of this. An issue can carry three `status:` labels and every view renders
  them, which is why the sweeps exist.

| Namespace | Answers | Per issue |
|---|---|---|
| `status:` | Where in the lifecycle | Exactly one while open |
| `type:` | What kind of work (only without native issue types) | Exactly one |
| `priority:` | How urgent | Zero or one |
| `area:` | Which part of the system | Zero or more |

Setup, rename and delete commands: [references/labels.md](references/labels.md).

### Issue types or `type:` labels

Check whether the organization defines issue types:

```bash
gh api repos/{owner}/{repo}/issue-types --jq '.[].name'
```

If it returns names, set the native type (`gh issue edit 123 --type Bug`, or `type:"Bug"` in
search) and skip `type:` labels; two carriers for one fact will disagree. An empty result (for
example a personal-account repository) means `type:` labels. A native type such as `Epic` also
makes a clean marker for top-level items.

### Labels or a board field

Labels suit a single repository whose state must be visible without project access and queryable
with `gh issue list --search`. A Projects v2 single-select Status field suits work spanning
repositories, boards the team actually reads, or a repo where the conflict sweep keeps finding
hits, because a single-select holds exactly one value. Running both is allowed if the Status
mapping names which one is authoritative. Board calls: `projects-v2`.

## Parenting

The Parent mechanism row says what counts: `sub-issue`, `milestone`, or both. The shortlist is a
query run every time (tracker-discipline § Parenting).

Candidate sub-issue parents, live only:

```bash
gh issue list --state open --search 'type:"Epic" -label:"status:parked"' --json number,title --limit 20
```

Use `label:epic` (or the repo's top-level marker) when there are no issue types.

Candidate milestones. `gh api` turns `-f` fields into a POST unless `--method GET` is given:

```bash
gh api --method GET repos/{owner}/{repo}/milestones -f state=open -f sort=due_on -f direction=asc \
  --jq '.[] | "\(.number)\t\(.title)\tdue \(.due_on // "none" | .[0:10])\topen \(.open_issues)"'
```

Set, move and read parents:

| Task | Command |
|---|---|
| Set or move a parent | `gh issue edit 124 --parent 40` (replaces any existing parent) |
| Add children from the parent | `gh issue edit 40 --add-sub-issue 124,125` |
| Detach | `gh issue edit 124 --remove-parent` |
| Milestone | `gh issue edit 124 --milestone "<title>"`, or `--remove-milestone` |
| Read a child's parent | `gh issue view 124 --json parent` (includes the parent's `state`) |
| Read a parent's children | `gh issue view 40 --json subIssues,subIssuesSummary` |

A parent is live when it is open and not `status:parked`. Read it back after setting it, because
GitHub accepts a closed parent without complaint.

## Triage sweep

Each query reads open issues only. When the number of results equals `--limit`, the sweep saw a
truncated backlog: raise the limit and say so.

| Finds | Query |
|---|---|
| No labels at all | `gh issue list --state open --search "no:label" --limit 200 --json number,title` |
| In progress, unassigned | `gh issue list --state open --search 'no:assignee label:"status:in-progress"' --json number,title` |
| In review, no linked PR | `gh issue list --state open --search 'label:"status:in-review" -linked:pr' --json number,title` |
| In progress, untouched | `gh issue list --state open --search 'label:"status:in-progress" updated:<YYYY-MM-DD' --json number,title,updatedAt` with a literal cutoff date |

Labelled but with no `status:` label (these look triaged and are not):

```bash
gh issue list --state open --limit 1000 --json number,title,labels \
  --jq '.[] | select([.labels[].name | select(startswith("status:"))] | length == 0) | "#\(.number)\t\(.title)"'
```

Each triage decision records the type, the status, and the parent or why there is none. Anything
not moving to `ready` gets a comment saying why, since the issue is the durable record. Apply a
decision in one command:

```bash
gh issue edit 88 --type Bug --add-label "status:ready,priority:p1,area:ingestion" --parent 40
```

A decline closes the issue with a reason (`gh issue close 87 --reason "not planned" --comment
"<why>"`). Before a batch loop over a query's output, run the query alone and read it.

### Conflicting status labels

```bash
gh issue list --state open --limit 1000 --json number,title,labels \
  --jq '.[] | {number, title, s: [.labels[].name | select(startswith("status:"))]} | select(.s | length > 1) | "#\(.number)\t\(.s | join(" + "))\t\(.title)"'
```

Empty output passes. Repair needs judgement: read the issue (`gh issue view 88 --comments`),
decide which claim is true, then remove the others in one `gh issue edit`.

## Orphan and dead-parent sweep

One call covers the whole open backlog, with the parent's state included:

```bash
gh issue list --state open --limit 1000 --json number,title,milestone,parent --jq '
  "read \(length) open issues",
  (.[] | select(.parent == null and .milestone == null) | "orphan\t#\(.number)\t\(.title)"),
  (.[] | select(.parent != null and .parent.state != "OPEN") | "dead-parent\t#\(.number)\tparent #\(.parent.number)\t\(.title)")'
```

- When the Parent mechanism is `sub-issue` only, drop `and .milestone == null`.
- If "read N" equals the limit, raise `--limit` and rerun.
- A parent that is open but `status:parked` is also dead. Compare the parent numbers with
  `gh issue list --state open --label "status:parked" --json number --jq '.[].number'`.

Older `gh` without the `parent` field: the REST list carries `parent_issue_url` and filters
milestones server-side, paginating the whole backlog:

```bash
gh api --method GET --paginate repos/{owner}/{repo}/issues -f state=open -f milestone=none \
  --jq '.[] | select(.pull_request == null and .parent_issue_url == null) | "#\(.number)\t\(.title)"'
```

Each orphan gets a decision now, with the user:

| Decision | Action |
|---|---|
| Part of a larger piece of work | `gh issue edit <n> --parent <p>` after the user agrees |
| Belongs to an iteration | `gh issue edit <n> --milestone "<title>"` |
| Genuinely top level | Needs the user's explicit approval (Top-level items row); say so in a comment |
| Should not be done | `gh issue close <n> --reason "not planned" --comment "<why>"` |

### Parents whose children are all closed

```bash
gh issue list --state open --limit 1000 --json number,title,subIssuesSummary \
  --jq '.[] | select(.subIssuesSummary.total > 0 and .subIssuesSummary.completed == .subIssuesSummary.total) | "#\(.number)\t\(.title)"'
```

For each hit, either close the parent as `completed` or add the remaining work as a child. The
reverse (a closed parent with open children) shows up as `dead-parent` above.

## Without gh

GitHub MCP tools: `list_issues` (filter by `state` and `labels`; page with `after`),
`search_issues`, `issue_read` (`get_sub_issues` and `get_parent`, paged with `page`/`perPage` up to
100), `sub_issue_write` (`add` with `replace_parent`, `remove`; it takes the child's database `id`
from `issue_read`), `issue_write` `update` (its `labels` replaces the whole set) and
`list_issue_types`. The label tools sit in the server's non-default `labels` toolset. There are no
milestone or dependency tools; print those `gh` commands for the user.

With no tool at all, ask for an export (the output of the `gh issue list --json` queries above, or
a pasted list), run the same checks on it, and print the fixes as commands for the user to run.

## Examples

<example>
Untriaged #214 "Search shows stale results after reindex"; the org has issue types.
Decision: `--type Bug`, `status:ready`, parent #40 "Search reliability" from the shortlist. Propose
it with the reason, and after the user agrees run `gh issue edit 214 --type Bug --add-label
"status:ready" --parent 40`, then read #214 back.
</example>

<example>
The orphan sweep prints `dead-parent #212 parent #20`; #20 was closed as completed last month.
#212 is an orphan wearing a badge. Run the shortlist, propose #31 (the live platform epic), and
after agreement run `gh issue edit 212 --parent 31`. Read back that the parent's state is OPEN.
</example>

<example>
The conflict sweep prints `#88 status:ready + status:in-progress`. The comments show the assignee
posted a start comment two days ago. Keep `in-progress`: `gh issue edit 88 --remove-label
"status:ready"`. If the comments showed nothing since the last triage, ask the assignee instead of
guessing.
</example>

## Verify

- The conflict sweep prints nothing.
- The orphan sweep's "read N" is below the limit, and every `orphan` or `dead-parent` line was
  fixed or reported to the user with the decision still open.
- Every changed issue was read back (`gh issue view <n> --json labels,parent,milestone,issueType`),
  and a set type actually stuck; without push access GitHub drops a type change silently.
