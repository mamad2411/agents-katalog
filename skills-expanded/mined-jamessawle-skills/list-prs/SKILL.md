---
name: list-prs
description: Use this skill whenever someone asks about open pull requests, PR status, or wants to know what PRs need attention. This skill queries GitHub and classifies every open PR by readiness (ready/waiting/blocked/draft), CI pass/fail, review approval state, merge conflicts, unresolved review threads, and staleness — producing a structured table that plain gh commands cannot. Trigger this skill for any request involving "open PRs", "PR status", "what needs review", "what's ready to merge", "stale PRs", "my PRs", or checking on pull requests across one or many repos. Even if the request sounds simple, this skill adds enrichment that a raw gh pr list cannot provide.
license: MIT
compatibility: Requires GitHub CLI (gh) authenticated with sufficient repo access
allowed-tools: Bash
argument-hint: "[owner/repo] [mine]"
metadata:
  author: jamessawle
  version: "1.0"
---

# List PRs

List open PRs with enriched state: CI status, review decisions, conflict detection, and age.

## Arguments

- `$0` (optional) — GitHub repository in `owner/repo` format, or `mine`.
- `$1` (optional) — Pass `mine` to filter to only PRs authored by the authenticated user. Only meaningful when `$0` is a repo.

**Modes:**

| Arguments | Behaviour |
|-----------|-----------|
| _(none)_ | All open PRs in the current repo |
| `owner/repo` | All open PRs in that repo |
| `mine` | Your open PRs across all repos |
| `owner/repo mine` | Your open PRs in that repo |

## Workflow

### Step 1: Gather PR data

#### Cross-repo mode (`$0` is `mine`)

Query PRs authored by the authenticated user:

```bash
gh search prs --state open --author @me --json repository,number,title,author,createdAt,updatedAt --limit 100
```

Then for each unique PR, fetch full details to get fields not available from search (reviewDecision, mergeable, statusCheckRollup, isDraft):

```bash
gh pr view <number> --repo <repository> --json number,url,reviewDecision,mergeable,statusCheckRollup,isDraft,additions,deletions,changedFiles,baseRefName,headRefName
```

```bash
gh api graphql -f query='query { repository(owner:"<owner>", name:"<repo>") { pullRequest(number:<number>) { reviewThreads(first:100) { nodes { isResolved } } } } }'
```

Batch these calls in parallel (up to 10 concurrent) to keep it fast. For each PR, run both the `gh pr view` and the GraphQL query concurrently.

#### Single repo mode (`$0` is a repo or omitted)

If `$0` is omitted, the repo is the current working directory — omit the `--repo` flag and let `gh` infer it.

Query open PRs and repo info in parallel:

```bash
gh pr list [--repo $0] --state open --json number,url,title,author,baseRefName,headRefName,reviewDecision,createdAt,updatedAt,additions,deletions,changedFiles,isDraft,labels,mergeable,statusCheckRollup --limit 100
```

```bash
gh repo view [--repo $0] --json defaultBranchRef --jq '.defaultBranchRef.name'
```

If `$1` is `mine`, filter the results to only PRs where the author login matches the authenticated user. Determine the authenticated user via:

```bash
gh api user --jq '.login'
```

Run this in parallel with the other queries.

Then fetch unresolved review thread counts for each PR via GraphQL. This can be batched into a single query per repo:

```bash
gh api graphql -f query='query { repository(owner:"<owner>", name:"<repo>") { <alias_1>: pullRequest(number:<n1>) { reviewThreads(first:100) { nodes { isResolved } } } <alias_2>: pullRequest(number:<n2>) { reviewThreads(first:100) { nodes { isResolved } } } } }'
```

Use aliases like `pr_1`, `pr_2`, etc. to batch multiple PRs per repo into one query. Run one query per unique repo in parallel.

If no open PRs are found (after filtering), report that and stop.

### Step 2: Classify each PR

For each PR, derive the following fields from the raw data:

#### CI Status

Derive from `statusCheckRollup`:

- **passing** — all checks have conclusion `SUCCESS`, `NEUTRAL`, or `SKIPPED`
- **failing** — at least one check has conclusion `FAILURE`, `CANCELLED`, `TIMED_OUT`, `ACTION_REQUIRED`, or `STARTUP_FAILURE`
- **pending** — at least one check has state `PENDING`, `QUEUED`, `IN_PROGRESS`, or `WAITING` and none are failing
- **none** — no checks configured (`statusCheckRollup` is empty or null)

#### Review Status

Derive from `reviewDecision`:

- **approved** — `APPROVED`
- **changes requested** — `CHANGES_REQUESTED`
- **review required** — `REVIEW_REQUIRED`
- **none** — empty or null (no required reviewers)

#### Conflict Status

Derive from `mergeable`:

- **clean** — `MERGEABLE`
- **conflicts** — `CONFLICTING`
- **unknown** — `UNKNOWN` or null

#### Unresolved Threads

Count from the GraphQL `reviewThreads` response — count nodes where `isResolved` is `false`:

- **N unresolved** — show the count (e.g. `3 unresolved`)
- **-** — no review threads exist

#### Staleness

Calculate from `updatedAt` relative to now:

- **active** — updated within the last 7 days
- **stale** — updated 7–30 days ago
- **abandoned** — not updated in over 30 days

#### Readiness

A composite assessment:

- **ready** — approved + CI passing + no conflicts + not draft
- **blocked** — has conflicts or CI failing
- **waiting** — CI pending or review required, but no blockers
- **draft** — PR is in draft state

### Step 3: Output

Present the results as a markdown table sorted by readiness (ready first, then waiting, blocked, draft), then by PR number ascending within each group.

#### Single repo mode

```markdown
## Open PRs for <owner/repo>

N open PRs: X ready, Y waiting, Z blocked, W draft

| PR | Title | Author | Status | CI | Reviews | Threads | Conflicts | Age |
|----|-------|--------|--------|----|---------|---------|-----------|-----|
| #12 | Add metrics | @user | ready | passing | approved | - | clean | 2d |
| #15 | Update deps | @user | waiting | pending | approved | 2 unresolved | clean | 1d |
| #8 | Refactor auth | @user | blocked | failing | approved | - | conflicts | 14d |
| #20 | WIP: new feature | @user | draft | none | none | - | clean | 3d |
```

#### Cross-repo mode

Group by repository, then use the same table format within each group:

```markdown
## Your open PRs

N open PRs across M repos: X ready, Y waiting, Z blocked, W draft

### owner/repo-a

| PR | Title | Status | CI | Reviews | Threads | Conflicts | Age |
|----|-------|--------|----|---------|---------|-----------|-----|
| #12 | Add metrics | ready | passing | approved | - | clean | 2d |

### owner/repo-b

| PR | Title | Status | CI | Reviews | Threads | Conflicts | Age |
|----|-------|--------|----|---------|---------|-----------|-----|
| #5 | Fix login | waiting | pending | review required | 1 unresolved | clean | 4d |
```

The Author column is omitted in cross-repo mode since all PRs are yours.

#### Age display

Show as a human-readable relative time:

- Under 24 hours: `<1d`
- 1–30 days: `Nd`
- 31–365 days: `Nw`
- Over 365 days: `Ny`

### Step 4: Actionable summary

After the table, provide a brief summary of anything that needs attention:

```markdown
### Needs attention

- **Conflicts**: #8 (owner/repo) — has merge conflicts with main — https://github.com/owner/repo/pull/8
- **Failing CI**: #8 (owner/repo) — 2 checks failing — https://github.com/owner/repo/pull/8
- **Unresolved threads**: #15 (owner/repo) — 3 unresolved review threads — https://github.com/owner/repo/pull/15
- **Stale**: #31 (owner/repo) — no updates in 23 days — https://github.com/owner/repo/pull/31
```

Include the full PR URL at the end of each item so the user can click through directly from the terminal. Only include this section if there are items needing attention. Skip it if all PRs are ready or in draft.

In single repo mode, omit the `(owner/repo)` qualifier.

## Important guidelines

- **Read-only** — this skill never modifies anything. It only queries and reports.
- **Structured output** — always use the table format above so other skills and workflows can rely on a consistent shape.
- **Fresh data** — always query live. Never cache or reuse data from a previous run.
- **Graceful on missing data** — if a field is null or unavailable, show `-` rather than erroring.
