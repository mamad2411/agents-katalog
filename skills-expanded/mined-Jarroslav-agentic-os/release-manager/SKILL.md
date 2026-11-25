---
name: release-manager
description: >-
  Audit a software release by cross-referencing git commits in a release range
  against tickets carrying the release's fix version, then emit a gap-analysis
  report in Markdown tables. Invoke when the user says "validate the release",
  "release audit", "check what shipped in <version>", "cross-reference commits
  and tickets", "did every ticket get committed", "pre-release check", or asks
  which fix-version tickets have no matching commits (and vice versa).
  Read-only (R0) — reports mismatches, never mutates tags, tickets, or fix
  versions.
  Not for: creating releases, tags, or tickets, fixing the gaps it finds, or watching an open MR (mr-watch).
version: 0.1.0
license: Apache-2.0
allowed-tools:
  - Bash
---

# release-manager

Cross-reference the commits that landed in a release range against the tickets
tagged with that release's fix version, then print a bidirectional gap report.
The audit surfaces the two failure modes teams miss before a cut: tickets in the
fix version with no commit behind them, and commits that shipped without a ticket
(or against a ticket the fix version excludes).

> Blast radius **R0**. This skill only reads — git history, remote tags, and the
> ticket tracker via its adapter. It creates no tags, no tickets, no releases,
> and never edits a fix version. It recommends changes in the report and stops.

Adapter-driven: no ticket backend is hardcoded. The tracker is resolved from
`.agentic/guides/project.md` and `${CLAUDE_PLUGIN_ROOT}/references/work-item-adapters.md`.
Anything beyond Jira / GitHub Issues / GitLab Issues requires a custom adapter
declaration.

## Stored variables

| Variable            | Meaning                                                                |
|---------------------|------------------------------------------------------------------------|
| `repos`             | Repos to scan (paths or `owner/repo` slugs)                            |
| `fix_version_label` | Full release label **verbatim** — used for fix-version queries         |
| `release_version`   | Bare semver extracted from the label — used for tag lookup/comparison  |
| `ticket_provider`   | `jira` \| `github` \| `gitlab` \| `none`                               |
| `project_key`       | Tracker project key (e.g. a Jira project prefix)                       |
| `vcs_tool`          | Per-repo CLI: `gh` \| `glab` \| `git-only`                             |
| `prev_tag`          | Lower bound of the commit range                                       |
| `current_tag`       | Upper bound of the commit range                                       |
| `tickets`           | Fetched ticket records                                                |
| `commits`           | Collected commit records                                             |

> Keep `fix_version_label` and `release_version` **distinct**. Jira fix versions
> are often labelled `Release 3.4.0` or `Prod 3.4.0`; tag comparison needs the
> bare `3.4.0`. Derive `release_version` from the first `\d+\.\d+\.\d+` match
> after stripping non-numeric prefixes off the label.

---

## Phase 1 — Gather inputs

Auto-detect first, ask second. Silently read `.agentic/guides/project.md`
(search cwd and each parent up to the repo root). Parse:

- Sections: `## Work Item Adapter`, `## Work Item Tracker`
- Fields: `adapter_status` (`configured` / `not configured`), `adapter_name`,
  `adapter_lookup`, `ticket_provider`, `project_key`

Ask the user **only** for values you could not auto-detect. Four questions are
possible:

1. **Repo list** — paths or `owner/repo` slugs; the keyword `current` means cwd.
2. **Release version label** — the full label, verbatim.
3. **Ticket system** — Jira / GitHub Issues / GitLab Issues / none.
4. **Project key**.

Skip questions 3 and 4 when `project.md` supplied them. Auto-detected values are
mentioned only inline in the results, never surfaced as a preamble question.

Repo-token disambiguation:

> A token containing `/` or `.` is taken as a path or slug as written. A bare
> token with **no `/` and no `.`** is tried first as a subdirectory of cwd; if
> that directory does not exist, treat it as an `owner/repo` slug.

Derive both version variables now: store the label as `fix_version_label`, and
set `release_version` to the `\d+\.\d+\.\d+` match after stripping non-numeric
prefixes.

## Phase 2 — Detect the VCS CLI per repo

For each repo, map the remote hostname to a CLI, verify it with `--version`, and
fall back to plain `git log` if the CLI is missing or unauthenticated.

| Remote hostname | `vcs_tool`  |
|-----------------|-------------|
| `github.com`    | `gh`        |
| any gitlab host | `glab`      |
| anything else   | `git-only`  |

## Phase 3 — Find current and previous tags

Fetch tags from **all** remotes — a clone may track a fork plus the canonical
upstream — then sort:

```
git tag --sort=-version:refname
```

**Current tag** — match `release_version` in this order: exact semver →
`v`-prefixed → substring match.

**Previous tag** — do not guess.

> Never take the next descending tag blindly. That picks up a hotfix or patch cut
> sitting just below the release; teams almost always want the minor-to-minor
> diff.

Algorithm:

1. Filter to clean semver tags below the release — exclude suffixes such as
   `-SNAPSHOT`, `-RC`, `-hotfix`.
2. Compute the **base candidate** `MAJOR.(MINOR-1).0` and the **latest-patch
   candidate** in that minor series.
3. If both exist and differ, offer both; **base minor `.0` is the default**.
4. A single candidate is confirm-or-override.
5. **User confirmation of `prev_tag` blocks progression to Phase 4.**

No tags at all → the range starts at the root commit:

```
git rev-list --max-parents=0 HEAD
```

Emit one status line per repo (output contract):

```
[repo] current_tag=<tag>  prev_tag=<prev_tag>
```

## Phase 4 — Collect commits

The range is bounded on **both** ends: `prev_tag..current_tag` — not `..HEAD`.
Only if `current_tag` is missing, fall back to `prev_tag..HEAD` and emit a
warning. Exclude merge commits.

Local git log:

```
git log <range> --no-merges --pretty=format:"%H|%s|%ae|%ad" --date=short
```

Parse each line as `hash|subject|author_email|date`.

Slug-only repos resolved through `gh` (no local checkout): pull commits from the
GitHub API with pagination, exclude merges by the `Merge` subject prefix, and
fall back to date-based filtering when the tag SHA is unavailable:

```
gh api repos/<slug>/commits --paginate -q '.[] | [.sha, .commit.message, .commit.author.email, .commit.author.date] | @csv'
```

Extract ticket IDs from each **subject** with the regex `[A-Z][A-Z0-9_]+-\d+`.

Commit record shape:

```
{ repo, short_hash (first 8 chars), hash, subject, author_email, date, ticket_ids }
```

## Phase 5 — Fetch tickets via the adapter

Resolve the adapter by priority:

1. **Configured** (`adapter_status: configured`) → run the `adapter_name` /
   `adapter_lookup` commands **verbatim**.
2. **Not configured** → infer from the first repo's `vcs_tool`: `gh` → GitHub
   Issues, `glab` → GitLab Issues, `git-only` → none. Record an explicit
   assumption note.
3. **Provider `none` / no inference possible** → skip the ticket phase, leave
   `tickets` empty, and note it in the report header.

Consult `${CLAUDE_PLUGIN_ROOT}/references/work-item-adapters.md` for the
**Resolution Order** and the **Known Adapters** table. The operation id resolved
there is `list-by-fix-version`. Substitute these placeholders into the adapter
command before running it:

`{{FIX_VERSION}}` · `{{PROJECT_KEY}}` · `{{RELEASE_VERSION}}` · `{{SLUG}}`

Fix-version query fallback fires **only on zero results**, trying in order until
one returns rows:

1. bare semver (`release_version`)
2. `v`-prefixed
3. `Prod `-prefixed
4. `Release `-prefixed
5. adapter-specific substring match (e.g. JQL `~`, `glab ... --search`)

> Zero tickets is a result, not an error — but prompt the user to double-check
> the label spelling, since a typo in the fix version reads identically to "no
> tickets."

Ticket record shape:

```
{ key, summary/title, type, status, assignee }
```

**Pagination of ticket results must complete before matching begins.**

## Phase 6 — Match both directions

Matching rule: a commit belongs to a ticket **iff the ticket key appears in the
commit subject, case-insensitive**. Build both lookup maps: `ticket_to_commits`
and `commit_to_tickets`.

Sort every record into four buckets:

| Bucket                  | Definition                                                                    |
|-------------------------|-------------------------------------------------------------------------------|
| Tickets with no commits | Fix-version ticket, no matching commit anywhere in the range                  |
| Commits with no ticket  | Commit subject carries no `[A-Z][A-Z0-9_]+-\d+` pattern                        |
| Matched tickets         | Ticket ↔ commit(s) matched                                                    |
| Orphan-ticket commits   | Commit references a real ticket whose fix version **excludes** this release   |

> Orphan-ticket commits are the most common audit gap: the code shipped but the
> ticket's fix version was never updated. Flag them for a fix-version correction.

## Phase 7 — Print the report

Report title: `Release <release_version> — Validation Report`

Header stats:

- Repositories scanned
- Commit count (merges excluded)
- Ticket count in fix version

Sections — the headings are an output contract; reproduce them exactly:

### Tickets Without Commits

| Ticket | Summary | Type | Status | Assignee |
|--------|---------|------|--------|----------|

### Commits Without Tickets

| Repo | Commit | Date | Author | Message |
|------|--------|------|--------|---------|

### Commits Referencing Tickets NOT in Fix Version

| Repo | Commit | Date | Ticket | Message |
|------|--------|------|--------|---------|

### Matched — Tickets With Commits

| Ticket | Summary | Status | Commits |
|--------|---------|--------|---------|

### Summary and Action Items

Every gap table gets a checkmark empty-state sentence when it has no rows (e.g.
"✓ Every fix-version ticket has at least one commit."). The summary must also
flag:

- Unmatched tickets that may be CVE / security work living in a repo you did not
  scan — offer a rescan.
- Open / non-Closed tickets in the fix version.
- Commit references to tickets absent from the tracker — label these
  **"unknown ticket reference"**.

---

## Decision rules

| Condition                             | Action                                                       |
|---------------------------------------|--------------------------------------------------------------|
| `project.md` found + fields present   | Skip questions 3–4, use silently                             |
| `adapter_status: configured`          | Run adapter commands verbatim                                |
| Unknown adapter                       | Ask the user, or continue with empty tickets after a warning |
| prev-tag base vs latest-patch conflict| User chooses; default = base minor `.0`                      |
| `current_tag` missing                 | Warn, fall back to `prev_tag..HEAD`                          |

## Error handling

| Situation                   | Response                                                             |
|-----------------------------|---------------------------------------------------------------------|
| Missing repo path           | Skip, warn, continue                                                |
| No tags in a repo           | Base the range at the root commit, note it                          |
| Adapter unauthenticated     | Warn; accept a manual ticket list, or produce a commits-only report |
| CLI missing                 | Drop to `git-only`, note it                                         |
| Zero commits / zero tickets | Note it, never halt (zero tickets → prompt a label-spelling check)  |

## References

- `${CLAUDE_PLUGIN_ROOT}/references/work-item-adapters.md` — the adapter
  **Resolution Order** and the **Known Adapters** command table; defines the
  `list-by-fix-version` operation and the placeholder contract
  (`{{FIX_VERSION}}`, `{{PROJECT_KEY}}`, `{{RELEASE_VERSION}}`, `{{SLUG}}`).
- `.agentic/guides/project.md` — the ticket adapter and work-item tracker
  declarations (`## Work Item Adapter`, `## Work Item Tracker`), produced and
  maintained elsewhere in the plugin suite.

## Non-goals

- No tag, ticket, or release creation — read-only audit.
- No fix-version edits — recommend only.
- No CI/CD gating, changelog generation, or deployment steps.
- No hardcoded ticket backend.
