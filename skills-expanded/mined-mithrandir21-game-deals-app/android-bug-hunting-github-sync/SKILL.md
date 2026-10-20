---
name: android-bug-hunting-github-sync
description: >
  Reconciles a fresh Android bug-hunt report against existing GitHub issues AND against the
  merge-target branch's actual code, then files only the genuinely new, still-real findings.
  Auto-skips findings that clearly match an open issue, findings whose cited code is already
  fixed on the merge target (typical when the bug hunt ran on a wave/feature branch that
  lags behind `dev`/`main`), surfaces ambiguous matches for human judgment, and flags
  findings that match a closed issue as potential regressions (without auto-reopening). Use
  this skill after running the android-bug-hunting-dispatcher (or any skill that produced an
  `android-bug-hunt-report.md`) whenever the user asks to "file these as issues", "create
  GitHub issues from the report", "sync bug hunt to GitHub", "open issues for these
  findings", "dedupe and file", or any phrasing that asks to turn a bug-hunt report into
  GitHub issues. Trigger on casual phrasings like "open tickets for these", "push these
  into GitHub", "log these as issues but don't dupe what's already there", "file the ones
  that aren't already fixed". This is the entry point for the file-issues phase — do not
  invoke `gh issue create` directly outside this skill once a bug-hunt report exists.
---

# Android Bug Hunt — GitHub Sync

## Purpose

The dispatcher produces `android-bug-hunt-report.md`. Without this skill, turning that report
into GitHub issues is a manual one-off — and re-running the dispatcher next month would
re-file every finding as a duplicate.

This skill closes the loop. It:

1. Parses the bug-hunt report into structured findings.
2. Pulls the current open + closed `bug-hunt`-labeled issues via `gh`.
3. **Verifies each finding against the merge-target branch's HEAD** — if the cited code is
   already fixed on `dev`/`main`, the finding is dropped before any matching is done. This
   matters because bug hunts often run on a wave/feature branch that's behind the merge
   target; without this step, the skill would file duplicates of bugs already fixed
   upstream (this exact failure mode dropped 4 false positives on 2026-05-02).
4. Scores each surviving finding against existing issues to classify as **auto-skip**,
   **ambiguous**, **regression candidate**, or **new**.
5. Writes a triage plan, waits for the user to approve (and optionally re-classify),
   then files only the approved items via `gh issue create`.

It is intentionally **standalone** — invoked after the user has reviewed the bug-hunt
report, not chained automatically off the dispatcher. The user wants a beat between phases.

---

## Step 0 — Preconditions

Bail fast if any of these fail. **Write nothing** until all preconditions pass.

```bash
# gh present and authed
gh auth status

# Latest report present
test -f .claude/bug-hunt-workspace/android-bug-hunt-report.md
```

Then verify the label scheme. If any of the labels below is missing, create it with the
matching color before proceeding (so issues land with consistent labelling):

| Label                | Color    | Description                                  |
|----------------------|----------|----------------------------------------------|
| `bug-hunt`           | `B60205` | Surfaced by the android-bug-hunt skill audit |
| `severity:high`      | `B60205` | Bug hunt severity: High                      |
| `severity:medium`    | `FBCA04` | Bug hunt severity: Medium                    |
| `severity:low`       | `FEF2C0` | Bug hunt severity: Low                       |
| `effort:trivial`     | `C2E0C6` | <30m, single-file change                     |
| `effort:small`       | `BFD4F2` | <4h, light testing                           |
| `area:*`             | `5319E7` | One per module/concern (compose, coroutines, …) |

```bash
# Snapshot existing labels; create only what is missing.
gh label list --limit 200
```

For an `area:*` label not yet present (a new module surfaced this run), create it with
color `5319E7` and a one-line description. Never rename existing labels.

Then determine and fetch the **merge target** — the branch that PRs from this hunt's
fixes will eventually land on. Step 2.5 reads code from this branch's HEAD to decide
whether each finding is still real:

```bash
# Default: GitHub's default branch (usually `dev` or `main`).
MERGE_TARGET=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)

# If the user has named a different target ("merge into staging", "PR base is release"),
# use that instead. Confirm in the plan summary.

git fetch --quiet origin "$MERGE_TARGET"
```

If `git fetch` fails (offline, no `origin`), warn the user and **skip Step 2.5** — fall
through to Step 3 with a `## Merge-target verification skipped` note in the plan so the
user knows findings weren't filtered against upstream code.

Last: warn the user if the working tree is dirty in a way that could distort path matching
(`git status --porcelain` returns non-empty in directories named in the report). Don't
abort — just surface it.

---

## Step 1 — Parse the report

Extract every `BUG-NNN` block from `android-bug-hunt-report.md`. The dispatcher emits each
finding in this canonical form:

```markdown
### BUG-001: <Short title>

| Field | Value |
|---|---|
| **Severity** | Critical / High / Medium / Low |
| **Category** | "Memory leak", "Race condition", "Lifecycle violation", … |
| **Location** | `path/to/File.kt:LINE` |
| **Effort** | Trivial / Small / Medium / Large |
| **Confidence** | High / Medium / Low |

**Description.** …
**Impact.** …
**Evidence.** …
**Recommended fix.** …
**Confidence rationale.** …
```

For each finding, build a record:

```jsonc
{
  "id": "BUG-001",
  "title": "WebView never destroyed",
  "severity": "High",            // → severity:high
  "category": "Resource leak",
  "effort": "Trivial",           // → effort:trivial
  "confidence": "High",
  "locations": ["feature/webview/.../WebView.kt:81-108", ...],
  "areaLabel": "area:webview",   // see mapping below
  "severityLabel": "severity:high",
  "effortLabel": "effort:trivial",
  "body": "<full markdown of the finding, verbatim>"
}
```

**Parsing tolerance.** The dispatcher format may evolve. If the parser can't find one of
the fields above, fall back to `null` rather than aborting — but log which findings were
partially parsed so the user can fix the report.

**Effort mapping.** `Medium` and `Large` from the report do **not** have matching
`effort:*` labels yet. If a finding lands there, omit the `effort:*` label entirely and
note it in the triage plan ("no effort label — `Medium` not in scheme").

**Severity mapping.** `Critical` is treated as `severity:high` (the scheme has no
`severity:critical`). Note the downgrade in the plan.

### Area-label inference

Use the path tokens first; fall back to category text. Keep this table inside the SKILL.md
so it's edited exactly the same way the rest of the skill is.

| Path / category contains              | `area:*` label       |
|---------------------------------------|----------------------|
| `feature/webview`, "WebView"          | `area:webview`       |
| `@Composable`, `feature/*/ui/`, "Compose", "recomposition" | `area:compose` |
| `Flow`, `StateFlow`, `MutableStateFlow`, `viewModelScope`, "coroutine" | `area:coroutines` |
| `Activity`, `Fragment`, `lifecycle`, "leak"                | `area:lifecycle` |
| `Pager`, `PagingSource`, `RemoteMediator`                  | `area:paging`    |
| `common/ui/theme`, "Theme"                                 | `area:theme`     |
| `Storage`, `SharedPreferences`, `DataStore`                | `area:storage`   |

If multiple match, prefer the most specific (`area:webview` over `area:compose` for a
WebView composable). If none match, omit the `area:*` label and surface this in the plan
("no area label inferred — consider creating a new `area:*` label").

---

## Step 2 — Fetch existing issues

```bash
gh issue list \
  --label bug-hunt \
  --state all \
  --limit 200 \
  --json number,title,state,stateReason,labels,body,url
```

Cache to memory. Split into:
- `open` — `state == "OPEN"`
- `closed` — `state == "CLOSED"`, with `stateReason` retained (`completed`, `not_planned`,
  `reopened`, …)

If `--limit 200` is hit, raise it and re-fetch. The matcher needs the full set.

---

## Step 2.5 — Verify each finding against the merge target

The bug hunt may have run on a feature/wave branch that is behind the merge target. A
finding that's real on the wave branch may already be fixed on `origin/$MERGE_TARGET`.
Filing it would create a duplicate of work already done.

For each parsed finding, decide whether the cited antipattern still exists on the merge
target. Three outcomes:

- **Still-broken** — the cited code (or close enough) is present on `origin/$MERGE_TARGET`.
  The finding survives to Step 3.
- **Already-fixed-on-merge-target** — the cited code is gone or has been refactored.
  The finding is dropped (with the user's veto in Step 4).
- **File-missing-on-merge-target** — the file no longer exists at the cited path.
  Could be a rename/move; surface as ambiguous and let the user decide.

### How to verify

For each finding's primary `Location` path (strip `:LINE`):

```bash
# Fetch the file from the merge target without checking it out.
git show "origin/$MERGE_TARGET:<path>" 2>/dev/null
```

If `git show` exits non-zero, the file is missing → **File-missing-on-merge-target**.

Otherwise, derive a **signature** from the finding's `Evidence` block:

- Take the first 1–3 distinctive non-empty, non-comment, non-fence lines from the
  Evidence code block (skip `// …`, `# …`, lines that are only braces/parens).
- Each signature line must be ≥ 12 characters and not a literal language keyword
  (`else`, `return`, `}`, `)`). If a line is too short or too generic, take the
  next one.
- Two signatures are usually plenty; three for noisy patterns.

A finding is **Still-broken** iff at least one signature line appears (substring match,
whitespace-collapsed) in the merge-target file. If none match, classify as
**Already-fixed-on-merge-target**.

### When the Evidence block isn't a faithful signature

Some findings cite *absence* of code (e.g. "no `CancellationException` re-throw before
generic catch"). In that case, the signature should be the *enclosing structure* (e.g.
the catch block) and the verifier checks whether the fix has been applied — typically
by searching for a pattern the recommended fix would have introduced (`catch (t:
CancellationException) { throw t }`). If neither the bug pattern nor the fix pattern is
unambiguously present, classify as **ambiguous-needs-review** (treat as still-broken
for Step 3 but call out in the plan's verification notes).

### Multi-location findings

If a finding cites multiple paths, run the verifier per path:

- All paths fixed → **Already-fixed-on-merge-target**.
- Some fixed, some still broken → **Still-broken (partial fix)**, surface which paths
  in the plan so the issue body can be narrowed when filed.
- All paths missing → **File-missing-on-merge-target**.

### Worked example (from 2026-05-02 hunt)

Finding cites `feature/giveaways/.../GiveawaysViewModel.kt:36-66` with Evidence
referencing `flow { emitAll(giveawaysRepository.observeGiveaways()) }` and three
separate `viewModelScope.launch { … }` blocks. Verifier runs:

```bash
git show origin/dev:feature/giveaways/src/main/java/pm/bam/gamedeals/feature/giveaways/ui/GiveawaysViewModel.kt
```

The merge-target file uses a single `parametersFlow.flatMapLatest { … }` chain — none
of the signature lines match. Classified **Already-fixed-on-merge-target**. Without
this step, Step 3 would have scored highly against an existing open issue (or filed a
new duplicate).

### Output of this step

Annotate each finding record with:

```jsonc
{
  …,
  "mergeTargetVerification": {
    "branch": "dev",
    "verdict": "still-broken" | "already-fixed" | "file-missing" | "ambiguous-needs-review",
    "checkedPaths": ["feature/giveaways/.../GiveawaysViewModel.kt"],
    "signatureMatches": [{ "path": "...", "line": "...", "matched": true }],
    "note": "Optional human-readable rationale, surfaced in the plan."
  }
}
```

Findings with verdict `already-fixed` skip Step 3 entirely. Everything else proceeds.

---

## Step 3 — Match findings to existing issues

For each finding, score every candidate existing issue. Run **open** and **closed**
candidates through the same scorer, then branch on state for the outcome.

### Scoring

| Signal                                                                 | Weight             |
|------------------------------------------------------------------------|--------------------|
| Shared `path:` (ignoring `:line`) appears in candidate body            | **+3 per shared path** |
| Category-token overlap in title (see token list below)                 | **+2** (cap once)  |
| Matching `area:*` label                                                | **+1**             |
| Matching `severity:*` label                                            | **+1**             |

**Path matching.** Strip `:LINE` and `:LINE-LINE` suffixes before comparing. A finding at
`Foo.kt:142` matches an issue body referencing `Foo.kt:138`. Exact path-string match only
— do **not** match on basenames alone (`WebView.kt` would collide across modules).

**Category tokens.** Maintain this token list in the SKILL.md. Match case-insensitively
in the candidate's title:

```
WebView · stateIn · WhileSubscribed · MutableStateFlow · asStateFlow · Paging · RemoteMediator ·
recomposition · LaunchedEffect · DisposableEffect · SideEffect · rememberSaveable ·
collectAsState · collectAsStateWithLifecycle · repeatOnLifecycle · flowWithLifecycle ·
SharedPreferences · DataStore · Storage · Theme · Coil · OkHttp · Retrofit · Sandwich ·
viewModelScope · Hilt · Room · DAO · Crashlytics
```

A finding's "category tokens" are derived from its title + `category` field. Score `+2`
if any token from the finding appears in the candidate's title (cap at +2 — don't compound).

### Classification

After scoring, take the highest-scoring candidate (`top`) and the second-highest
(`second`):

- **Strong match**: `top.score >= 5` AND `top.score - second.score >= 2`.
- **Ambiguous**: `top.score >= 3` AND not strong.
- **No match**: `top.score < 3`.

Then branch on candidate state:

| Verdict                       | State   | Outcome                                                        |
|-------------------------------|---------|----------------------------------------------------------------|
| Strong match                  | open    | **Auto-skip** — record `skip:dup-of-#NN`                       |
| Strong match                  | closed  | **Regression candidate** — `regression?:closed-#NN`            |
| Ambiguous                     | open or closed | **Surface for review** — include top 1–3 candidates with scores |
| No match                      | —       | **New** — will be filed                                        |

**Closed-issue weighting.** If a closed candidate has `stateReason: not_planned`, that's a
stronger "we deliberately won't fix this" signal than `completed`. Show the `stateReason`
in the plan; never auto-reopen.

**Module-rename fallback.** If a finding produces zero path-match scores against any
candidate (top score is purely from title/labels), run
`git log --follow --oneline -- <one of the finding's paths>` once and check whether the
file was renamed from a path that *does* appear in any candidate. If so, surface that
candidate at +3 with a `(rename of <old-path>)` note. Do this lazily — only for findings
with zero path matches, not for every finding.

---

## Step 4 — Write the triage plan

Write `.claude/bug-hunt-workspace/github-sync-plan.md`. Overwrite if it exists (the
previous plan is no longer the current state):

```markdown
# GitHub Sync Plan — <YYYY-MM-DD>

Source report: `.claude/bug-hunt-workspace/android-bug-hunt-report.md`
Merge target verified against: `origin/<branch>` at <short-sha> (or "skipped — see warnings")
Existing issues fetched: <N> open, <M> closed (label `bug-hunt`)

## Summary
- Findings: N
- Already fixed on merge target (will be skipped): F
- Auto-skip (open dup): A
- Regression candidates (closed match): R
- Ambiguous (need a call): M
- New (will be filed on approval): K
- File-missing on merge target (need a call): X
- Parse warnings: P
- Label warnings: L

## Already fixed on merge target (will be skipped)
- BUG-NNN — <title>
  - Verified against: `origin/dev:feature/giveaways/.../GiveawaysViewModel.kt`
  - Signature lines from Evidence not found on merge target — appears fixed.
  - **Default if you don't override below: skip silently (no issue filed, no log noise beyond "fixed-on-<branch>")**
  - To file anyway (e.g. you're working on a long-lived branch and want the issue tracked
    independently), move under `## New` below.

## File missing on merge target (need a call)
- BUG-NNN — <title>
  - Cited path `<path>` does not exist on `origin/<branch>`. Possible rename/move.
  - **Default if you don't override below: file new** (with a `> Note: cited file missing on <branch>; verify path` prefix)

## Auto-skipped (open duplicates)
- BUG-001 — WebView never destroyed → #30 (score 7; shared path `feature/webview/.../WebView.kt`, title token `WebView`, area, severity)
- …

## Regression candidates (closed match — confirm before reopen)
- BUG-NNN — <title> → closed #45 (`completed`, score 6)
  - Suggested action: comment on closed #45 with the new evidence, OR file new with body prefix `> Possible regression of #45.`
  - Why surfaced: <signals>
  - **Default if you don't override below: comment-only (no new issue)**

## Ambiguous (need a call)
- BUG-NNN — <title>
  - Candidate 1: #37 (score 4; shared path `…HomeViewModel.kt`)
  - Candidate 2: #38 (score 3; matching title token `stateIn`)
  - **Default if you don't override below: file new**

## New (will be filed on approval)
- BUG-NNN — <title>  ·  severity:X · effort:Y · area:Z
  - <one-line tagline>

## Parse / label warnings
- BUG-NNN parsed without effort label (report said `Medium`, not in scheme)
- BUG-NNN: no `area:*` label inferred — consider creating one
- BUG-NNN: severity downgraded `Critical` → `severity:high`
- (if applicable) Merge-target verification skipped: <reason — `git fetch origin <branch>` failed, no remote, etc.>
  → All findings will proceed to Step 3 unfiltered. Re-run with network access for tighter results.

---

## How to override

Edit this file, then re-invoke the skill (Step 5 reads this file fresh):

- To **skip** an item, move it to a `## User-skipped` section (any heading containing
  "skip" works).
- To **promote** a regression candidate to a new issue, move it under `## New` and
  optionally add `prefix-with-regression-note: yes` on the next line.
- To **reclassify** an ambiguous to skip, move it under `## User-skipped` with a
  one-line reason.
- Any item left in its original section is treated per its default action above.
```

Present the plan path to the user in chat in one short message. **Stop and wait.** Do
not proceed to Step 5 without explicit approval. Phrases that count as approval: "go",
"file them", "ship it", "looks good", "approved". Phrases that don't: "looks ok"
(without an action verb), questions, anything ambiguous — ask back.

---

## Step 5 — Apply the plan

Re-read `.claude/bug-hunt-workspace/github-sync-plan.md` (so user edits stick).

Build the action list:
- Everything under `## New` → file a new issue.
- Everything under `## Regression candidates` left in place → comment on the closed
  issue with the new evidence; do **not** open a new issue (default action).
- Anything moved under `## New` from regression → file a new issue with body prefix:
  `> Possible regression of #NN (closed <stateReason>).`
- Anything under `## File missing on merge target` left in place → file a new issue
  with body prefix: `> Note: cited path was not found on \`origin/<branch>\` at sync
  time; verify/relocate before fixing.`
- Anything under `## Already fixed on merge target` left in place → skip silently
  (record `fixed-on-<branch>` in the log).
- Anything moved under `## New` from `## Already fixed on merge target` → file a new
  issue (the user has explicitly opted in despite the merge-target verifier saying it's
  fixed; respect their judgment).
- Anything under `## User-skipped` (or any heading containing "skip") → skip silently.
- Anything under `## Auto-skipped` → skip silently (already handled in Step 3).

### Filing a new issue

Heredoc the body to a temp file (avoids shell-escaping pitfalls with backticks, `$`,
quotes, code fences):

```bash
BODY_FILE=$(mktemp /tmp/bughunt-body-XXXXXX.md)
cat > "$BODY_FILE" <<'EOF'
<the finding's full markdown body, verbatim from the report>
EOF

gh issue create \
  --title "<title>" \
  --label "bug,bug-hunt,<severityLabel>,<effortLabel>,<areaLabel>" \
  --body-file "$BODY_FILE"

rm -f "$BODY_FILE"
```

If a label is missing for a given finding (e.g. no `effort:*` because `Medium`), drop it
from the comma list — don't substitute. Report it in the warnings.

### Commenting on a closed issue (regression default)

```bash
COMMENT_FILE=$(mktemp /tmp/bughunt-comment-XXXXXX.md)
cat > "$COMMENT_FILE" <<'EOF'
The android-bug-hunting-dispatcher surfaced this issue again on <YYYY-MM-DD>. Possible regression — please review:

<the finding's full markdown body, verbatim>
EOF

gh issue comment <NN> --body-file "$COMMENT_FILE"
rm -f "$COMMENT_FILE"
```

### Crucial: consult `.claude/lessons.md` before recommending refactors

Before filing each issue, scan `.claude/lessons.md` (Active section only) for any lesson
whose Tags overlap with the finding's category or paths. If a lesson contradicts the
finding's "Recommended fix", surface it inline in the issue body under a `> Note:`
blockquote — do not silently file an issue that recommends something the project has
already deliberately rejected.

Worked example from this codebase: `L-2026-04-30-04` says "keep ViewModel functions
Flow-shaped — don't lower to `viewModelScope.launch { try/catch }`". A finding whose
recommended fix proposes that lowering must include a `> Note:` linking back to the
lesson and offering a Flow-shaped alternative.

---

## Step 6 — Sync log

Append to `.claude/bug-hunt-workspace/github-sync-log-<YYYY-MM-DD>.md` (one file per
calendar day; multiple invocations same day append to the same file):

```markdown
# GitHub Sync Log — <YYYY-MM-DD HH:MM>

Source report: `.claude/bug-hunt-workspace/android-bug-hunt-report.md`
Merge target: `origin/dev` @ <short-sha>

- BUG-001 → skipped (dup of #30)
- BUG-002 → skipped (dup of #31)
- BUG-003 → skipped (fixed on `origin/dev` — Evidence signature lines absent from `feature/giveaways/.../GiveawaysViewModel.kt`)
- BUG-005 → skipped (file missing on `origin/dev:<path>`; user accepted default)
- BUG-007 → filed as #50 — https://github.com/owner/repo/issues/50
- BUG-012 → regression candidate; commented on closed #22
- BUG-013 → ambiguous; filed new (#51) per user override
- BUG-019 → user-skipped (`reason: covered by #44 already`)

## Failures (RESUMABLE)
<empty if all succeeded>
```

The log is the **resume point**. If `gh` fails partway through, every successful action
is recorded above the `## Failures` section; subsequent re-invocations of this skill
must read this log first and skip any `BUG-NNN` already marked as `filed` or `skipped`.

### `## Failures (RESUMABLE)` section

If `gh issue create` or `gh issue comment` fails (rate limit, network, malformed body),
write:

```markdown
## Failures (RESUMABLE)
- BUG-007 — `gh issue create` failed: <stderr>
  - Body file preserved: /tmp/bughunt-body-XXXXXX.md
  - Resume: re-invoke this skill; it will pick up here.
```

Then **stop**. Don't continue with the rest of the action list — surface the failure to
the user. The next invocation reads the log, skips BUG-001..BUG-006 (already done),
and retries BUG-007 onward.

---

## Step 7 — Final report to user

One short message. No prose preamble:

```
Filed: K new issues — <urls, one per line>
Skipped: A duplicates of open issues, F already fixed on origin/<branch>
Regression comments: R on closed issues
Failures: F (see log for resume)
Log: .claude/bug-hunt-workspace/github-sync-log-<date>.md
```

---

## Sharp edges

- **Wave-branch lag**: the bug hunt may have run on a feature/wave branch behind the
  merge target. Step 2.5 verifies each finding against `origin/$MERGE_TARGET` HEAD
  before scoring against issues. Without this, four out of seven findings on the
  2026-05-02 hunt would have been filed as duplicates of bugs already fixed on `dev`.
- **Signature-line false negatives**: Step 2.5's verifier substring-matches Evidence
  code lines into the merge-target file. If the fix introduced a token-identical line
  (e.g. signature line is `viewModelScope.launch {` and the fix kept that line but
  added structure around it), the verifier will say "still broken". Pick distinctive
  signature lines, and treat verifier verdicts as advisory — the user's plan-edit veto
  in Step 4 is the source of truth.
- **Findings citing absent code**: some findings describe missing patterns rather than
  present antipatterns ("no `CancellationException` re-throw"). The verifier checks
  for the *fix pattern* in those cases. If neither bug nor fix pattern matches
  unambiguously, classify as `ambiguous-needs-review` and surface in the plan.
- **Line drift**: a finding at `Foo.kt:142` matches an existing issue's `Foo.kt:138`.
  Path matching strips `:line` suffixes — see Step 3.
- **Consolidation/split**: if one finding overlaps two open issues with similar scores,
  it is *ambiguous* by definition. Surface both candidates; do not pick.
- **Title drift**: never match purely on title. Step 3's classifier requires
  `top.score >= 3` to be ambiguous and `>= 5` to be strong; either way at least one
  shared path or a +2 token bump is required (a label-only +2 cannot reach the
  ambiguous threshold).
- **`stateReason` distinction**: closed `not_planned` is a stronger don't-refile signal
  than `completed`. Surface both verbatim; never auto-reopen.
- **Module renames**: handled lazily in Step 3 via `git log --follow` only for findings
  with zero path matches.
- **Vocabulary creep**: the category-token list lives in this SKILL.md (Step 3). When
  the codebase grows new vocabulary, edit the list here.
- **Idempotency across runs**: re-running the skill on the same report after partial
  failure must read the latest `github-sync-log-*.md` first and treat any `BUG-NNN`
  marked `filed` or `skipped` (including `user-skipped`) as already-handled.
- **Local `BUG-NNN` identity**: BUG numbers are per-report, not global. Do not try to
  globalize them across runs — once a finding is filed, the GitHub issue number is the
  global identity.
- **Body verbatim**: the finding's markdown body is filed verbatim. If the dispatcher
  ever drops a section (e.g. omits `Confidence rationale`), file what's there. Don't
  fabricate missing sections.
- **Workspace files**: `.claude/bug-hunt-workspace/github-sync-plan.md` and
  `github-sync-log-*.md` live alongside the dispatcher's output. If the project's
  `.gitignore` doesn't already exclude `*-log-*.md` under that directory, mention it
  to the user once (don't auto-edit `.gitignore`).

---

## Anti-patterns — avoid these

- **Auto-reopening closed issues.** A close is a deliberate signal. Surface, comment,
  but never `gh issue reopen`.
- **Filing without a triage plan.** Step 4's plan is the user's veto point. Even on a
  "smoke test" run that produces zero new issues, write the plan and report it.
- **Matching on basename only.** `WebView.kt` exists in many modules. Always match on
  the full repo-relative path.
- **Re-deriving labels per run.** The label scheme is in Step 0. Don't invent new
  conventions per invocation. New `area:*` labels are fine; new severity tiers or
  effort buckets are not.
- **Hiding parse failures.** If a finding can't be fully parsed, surface it in the
  plan's "Parse warnings" section — don't silently drop it.
- **Skipping the lessons-file consultation.** Step 5 explicitly checks
  `.claude/lessons.md` before filing. Skipping this is how stale recommendations make
  it back into issues we've already rejected (`b41c34d` / `4f20fa5` is the cautionary
  tale).
- **Skipping merge-target verification because "the dispatcher already ran".** The
  dispatcher reads only the working tree (often a wave branch). The merge target's
  HEAD is what the user is trying to land fixes on. Step 2.5 is the only place in
  this pipeline that compares findings against upstream code. A `git fetch` failure
  means proceeding *unfiltered* — call this out in the plan summary so the user can
  re-run with network later rather than discovering 4 duplicate filings the next day.
