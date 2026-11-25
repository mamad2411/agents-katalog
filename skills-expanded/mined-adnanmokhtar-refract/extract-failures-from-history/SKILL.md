---
name: extract-failures-from-history
description: "Round-two: recurring failure themes from git log (revert, hotfix, incident, rollback), written as `### ` entries in ai/failures/_index.md — never per-theme files."
kind: skill
pack: learning
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: extract-failures-from-history

## Purpose

A failure that happened once is a story. A failure family that happened 4 times across 18 months is an architectural lesson. Round-two reads the project's actual history and finds the lessons.

The output drives the theme entries Phase 4.7-DEEP appends to `ai/failures/_index.md` — the ONE append-only don't-retry catalog, which architectural agents must inject in pre-flight (per Hard Rule). **Never a per-theme file**: `ai/failures/<theme>.md` is forbidden by `/learn-from-task` step 6, `knowledge-curator` § 4b and [`learning-sink.md`](../../../../snippets/learning-sink.md); a second file is a catalog no consumer reads. Each theme is one `### <YYYY-MM-DD> — <theme>` entry in the index, in the shape its `## Format per entry` declares. Without this step, agents propose ideas that already failed in this codebase.

## Premise

- Real source is the truth. Read every candidate commit's subject + body + diff before classifying it into a theme — keyword matches alone are not classifications.
- Every recorded theme cites the SHAs of its representative commits + the top affected files; every prevention-checklist bullet maps to evidence visible in those commits.
- Customer names, dollar amounts, and individual-engineer blame are sanitized (per the privacy rule) — institutional learning, not blame.
- Empty extraction is honest — `## No recurring failure themes` is a valid output for a young codebase or a clean main branch.
- Fabrication — promoting one revert to a "recurring theme", inventing a `cache-invalidation` lesson when no commit mentions caching, naming individual engineers — corrupts every architectural agent's pre-flight injection.

## Mechanical halt

- Hand-wave in failure output — `etc.`, `...`, `several commits`, `appears to be a pattern`, `the team often`, a theme without ≥`min_theme_occurrences` SHA citations, a `root_cause_family` not grounded in a diff you read — REFUSE to write the row.
- Re-read the diffs and regenerate the theme, OR relegate the finding to `one_off_failures`.
- If git is inaccessible OR commit count is below 30 OR no theme reaches `min_theme_occurrences`, write `<NOT-DETECTED: failures: <reason — git unavailable | <N> commits below 30 | no themes ≥ <min>>>` per the WEAK gate.
- Never invent themes from training-data familiarity with the listed taxonomy — only what the actual git history shows counts.

## When to use

- `/setup-project --refine` Phase 2.12 — once per project.
- Manually when a developer says "we keep hitting <X> bug" and wants the failure recorded as a permanent lesson.

## Inputs

- `lookback` (default: 24 months OR all-time if repo is younger).
- `min_theme_occurrences` (default: 2 — a theme must have ≥ 2 instances to count as recurring).
- `extra_doc_paths` (optional) — explicit user-opted paths like `docs/postmortems/`, `docs/incidents/`, `INCIDENTS.md`. Skipped unless user passes `--include-incidents=<path>` to setup-project.
- `output_section` — section path (default: `## Failure history`).

## Procedure

### Step 1 — Establish git accessibility

Run `git log --oneline -1`. If git not accessible (no `.git/`, shallow clone, permission error), abort with `[REFINE-WEAK: failures — git not accessible]`.

Run `git log --pretty=format:'%h %s' --since='<lookback> ago' | wc -l`. Need ≥ 30 commits to do useful theme grouping. If less, flag `[REFINE-WEAK: failures — too few commits]`.

### Step 2 — Sweep commit messages for failure-marker keywords

Search the git log for case-insensitive matches:

```bash
git log --pretty=format:'%h%x00%s%x00%b%x00%cd%x00%an' --since='<lookback> ago' \
  | grep -iE '\b(revert|hotfix|incident|regression|rollback|outage|fix.{0,30}critical|fix.{0,30}prod|emergency|p0|p1|sev1|postmortem|fire|broke|broken|outage|panic|crash|leak|exploit|vulnerability)\b'
```

For each match, extract:
- SHA (`%h`).
- Subject (`%s`) — first line.
- Body (`%b`) — full description (often empty; sometimes contains the cause).
- Date (`%cd`).
- Author (`%an`) — for grouping context, NOT for blame.

### Step 3 — Read the diffs

For each candidate commit, run `git show --stat <sha>` to get the affected files. For commits with non-trivial diffs (< 200 LOC changed), run `git show <sha>` and skim the actual change.

Note:
- Affected files (top 3 by lines changed).
- Affected functions (if extractable from hunk headers).
- Type of change: revert? add validation? add null-check? add transaction? add idempotency? change query plan? add index? cache-related? auth-related?

### Step 4 — Group commits by theme

Define candidate themes:

| Theme | Markers |
|---|---|
| `auth-bypass` | auth, permission, role, token, jwt, session |
| `n-plus-1-perf` | N+1, slow query, timeout, prefetch, eager-load, query optimization |
| `migration-drift` | migration, schema, rename, drop column, foreign key |
| `payment-double-charge` | payment, charge, refund, idempotency, duplicate |
| `tenant-leak` | tenant, multi-tenant, cross-tenant, scope |
| `cache-invalidation` | cache, stale, TTL, invalidat |
| `concurrency-bug` | race, concurrent, deadlock, lock, transaction-isolation |
| `null-handling` | null, NoneType, undefined, NPE |
| `rate-limit-storm` | rate-limit, throttle, retry-storm, thundering-herd |
| `data-loss` | data-loss, accidentally deleted, bug deletes |
| `email-blast` | email, notification, accidentally sent |
| `secret-leak` | secret, credential, key leaked, token exposed |
| `external-api-flake` | webhook, vendor, retry, idempotency-key, third-party |

Group each commit into the theme with the strongest marker match. If multiple match, pick by the commit body's specifics, then by file path (e.g. `app/auth/*` → `auth-bypass`). If none match, group as `other` (don't lose them).

### Step 5 — Cross-reference with existing `ai/failures/_index.md`

If round-one wrote any failures (e.g. via `business-auditor` running before REFINE), read them. For each existing failure:

- Check if the new extraction surfaces it (avoid double-counting).
- Check if the existing failure has a `status:` field (`active`, `validated_failure`, `superseded_by_<adr>`). Append-only — never modify existing.

### Step 6 — Filter to recurring themes

Apply `min_theme_occurrences` (default 2). A theme with 1 instance is a story; ≥ 2 is a recurring lesson. Single-occurrence findings go into `## one-off failures` (not promoted to a theme entry in `ai/failures/_index.md`).

### Step 7 — Read postmortem docs (opt-in only)

If `extra_doc_paths` was provided AND those paths exist:

- Read every `.md` in those paths.
- Look for headings like `## Cause`, `## Resolution`, `## Prevention`, `## Lessons`.
- Map each to a theme.
- Cross-reference with the git-extracted commits (often the postmortem mentions the SHA).

This step requires explicit opt-in via `--include-incidents=<path>` because postmortem docs are sensitive — they may contain customer references, internal financial impact, blameful language.

### Step 8 — Output

Write to `.claude/_refine-extract.md` under `## Failure history`:

```yaml
extraction_date: <YYYY-MM-DD>
git_lookback: <duration>
total_commits_scanned: <N>
candidate_failure_commits: <N>
strong_signals: ["recurring-themes", "diff-analyzed", "postmortems-read"]   # subset present

recurring_themes:
  - theme: <e.g. auth-bypass>
    occurrences: <N>
    status: active  # default; user can change to validated_failure / superseded_by_ADR-NNNN later
    affected_files:
      - <file/path/sample.py>     # top 3 by frequency across the N commits
    commits:
      - { sha: <hash>, subject: <subject>, date: <YYYY-MM-DD> }
      # ≤ 5 representative commits; the full list goes in the theme's entry in ai/failures/_index.md if STRONG
    root_cause_family: |
      <2-3 sentence narrative — what kind of mistake recurs.
       e.g. "Permissions checked at controller layer but bypassed when service layer
       was called from a background job that didn't propagate the user context."
       Cite the most representative commit's diff inline.>
    prevention_checklist:
      - <bullet — concrete check a future agent can run in pre-flight>
      - <bullet>
    cited_postmortem: <docs/postmortems/2025-04-15-cross-tenant-data.md>   # if extra_doc_paths set

one_off_failures:
  - { theme: <name>, sha: <hash>, subject: <subject>, date: <YYYY-MM-DD> }
  # short list — recorded for completeness, not promoted to a theme entry
```

## Quality gate

- **STRONG**: ≥ 2 recurring themes (each with ≥ 2 occurrences) extracted, ≥ 1 with prevention-checklist of ≥ 3 bullets.
- **MEDIUM**: 1 recurring theme found. Consumed, not discarded: Phase 4.7-DEEP appends the one theme entry to `ai/failures/_index.md`, and `compute-anchor-density § Step 4` counts `failure-theme` for a block that cites it (STRONG **or** MEDIUM counts; only WEAK is excluded). One theme with diffs read and SHAs cited is real signal — the tier exists to say "thin, not absent", which is a different fact from both neighbours.
- **WEAK**: 0 recurring themes (codebase too young, history too clean, or the team lands all hotfixes outside main). Output `## No recurring failure themes` finding. Phase 4.7-DEEP appends no theme entry in this case.

## Privacy / safety

- **Never extract failure-history content from any source the user hasn't opted into.** The skill stays inside the repo + local git log; no external bug-tracker calls; no Sentry / Datadog API calls; no Slack scraping.
- **Postmortem docs are opt-in** via `--include-incidents=<path>`. Default: skip.
- **Customer names / specific dollar amounts / individual employee blame** must NOT appear in the output. If the extraction encounters them in commit messages or postmortem bodies, sanitize:
  - Replace customer names with `<customer>`.
  - Replace dollar amounts with `<significant-amount>`.
  - Strip individual names from blame contexts (group context — "the team / engineer who ..." — is fine).
- **Public repo check**: if the project's git remote is a public host (github.com/<user>/<repo> with public visibility), warn the user before appending theme entries to `ai/failures/_index.md`, since the file is committed and visible. The user can choose to gitignore `ai/failures/` or proceed.

## Anti-patterns

- **Treating every revert as an incident** — many reverts are benign (deps update broke build, revert, fix forward in 10 minutes). Read the diff before classifying.
- **Calling a single-occurrence bug a recurring failure** — the threshold is the protection. A one-off is a story; a pattern is a lesson.
- **Inventing a theme not represented in commits** — if `cache-invalidation` doesn't appear in any commit, it's not a finding.
- **Naming individual engineers** — failure catalog is institutional learning, not blame. Strip names.
- **Extracting from a fork's `main` while ignoring `develop`** — many shops do hotfixes on `main` and feature work on `develop`. Walk both.
- **Skipping commit bodies** — the subject is often terse ("fix bug"); the body has the details. Always read both.

## Verify (postconditions)

Contract: [`templates/snippets/postcondition-check.md`](../../../../snippets/postcondition-check.md). **Preconditions are not verification** — this skill guards its entry and must also check its exit. Every entry under `## Failure modes` that this skill's own write could cause becomes a check here, observed rather than assumed, reported when it passes as well as when it fails, and `NOT RUN` with a reason where no signal is available. A failure mode the skill documented and never checked is a risk it accepted on the caller's behalf without saying so.
