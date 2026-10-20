---
name: github-issue-waves
description: >
  Resolve a batch of GitHub issues in parallel "waves" — each wave is a set of issues
  whose changes don't merge-conflict with each other, executed concurrently by
  worktree-isolated sub-agents that each open their own PR. Waves run sequentially:
  one wave's PRs must be merged before the next wave plans. Progress and lessons are
  persisted under `.claude/notes/` so the campaign can be paused and resumed across
  sessions. Trigger when the user asks to "work through these issues in parallel",
  "run waves of issues", "batch-resolve GitHub issues", "knock out all the bug-hunt
  issues", "process these labels in waves", or any phrasing that pairs a GitHub issue
  filter with parallel execution. Pass label arguments to start a new campaign; pass
  no arguments to resume the active one.
---

# GitHub Issue Waves

## Purpose

Resolve many GitHub issues efficiently while keeping PRs small and reviewable.
The skill plans **waves** (sets of mutually conflict-free issues), executes each
wave's issues in parallel via worktree-isolated sub-agents, and stops after
opening PRs so the human can review and merge at their own pace before the next
wave plans.

This skill orchestrates. It does not implement the issues itself — each issue is
delegated to its own sub-agent. The skill's job is selection, conflict detection,
wave planning, dispatch, sanity-checking, and persistent notes.

---

## Step 0 — Detect mode

The skill runs in two modes. Pick one based on the invocation:

- **New campaign mode** — args are non-empty. Args are GitHub label names (one or
  more). Begin a fresh campaign with those labels.
- **Resume mode** — args are empty. Find the active campaign and continue.

### Resuming

1. List campaign folders under `.claude/notes/` that contain `state.yaml`.
2. For each, read `state.yaml`'s `status` field. Filter to `status: in_progress`.
3. If exactly one in-progress campaign → resume it.
4. If multiple → list them with their labels and most recent wave, ask the user which.
5. If none → tell the user there's no active campaign and ask for labels to start one.

User can also pass `campaign:<slug>` as the only arg to force a specific campaign.

---

## Step 1 — Select issues

```bash
# AND-combine labels via repeated --label flags
gh issue list --state open \
  --label "<label-1>" --label "<label-2>" \
  --json number,title,body,labels,url \
  --limit 100
```

Filter out issues that already have a PR linked from this campaign (check
`state.yaml`'s `issues[].pr` field for re-queries on subsequent waves).

If the result is empty: campaign is complete. Run **Step 8 (Wrap up)** instead
of continuing.

---

## Step 2 — Detect conflicts

Build a conflict graph over the candidate issues. Two issues are
**conflicting** if any of these hold:

1. **Hot file overlap** — both touch a file from the hot-file list (below).
2. **File-set overlap** — both planner agents (Step 2c) report the same file.
3. **Logical dependency** — one issue's body contains `Blocked by #N`,
   `Depends on #N`, or `Requires #N` referring to the other (or a chain ending
   at an unmerged sibling).

Two issues are **parallel-safe** only if none of the above hold.

### 2a. Hot-file list

These files are touched by many issues and conflict trivially. Any pair that
both touch one of these is **never** parallel:

- `gradle/libs.versions.toml`
- `settings.gradle.kts` / `settings.gradle`
- The root `build.gradle.kts` / `build.gradle`
- Any `AndroidManifest.xml` at the root (app module)
- `gradle/wrapper/gradle-wrapper.properties`

Edit this list when the project's hot files change.

### 2b. `area:*` label pre-filter

Two issues with **fully disjoint `area:*` label sets** are *candidates* for
parallel — proceed to 2c. Two issues sharing any `area:*` label are *suspect* —
also proceed to 2c, but expect the planner agents to confirm a conflict. Do not
rely on `area:*` alone; it's a hint, not a verdict.

### 2c. Planner sub-agents

For each candidate issue, spawn a lightweight planner agent (no worktree, no
edits) to report which files it would touch. Spawn all planners **in a single
message** so they run in parallel.

**Planner prompt template:**

```
You are planning the implementation of GitHub issue #{NUM} in this repo. DO NOT
edit any files. Read the issue, read enough of the codebase to understand the
fix, and report back ONLY:

1. A list of files you would modify (absolute paths from repo root).
2. A list of files you would create.
3. A one-line summary of the fix approach.
4. Any logical dependency on other issues (look for "Blocked by #N",
   "Depends on #N", "Requires #N" in the issue body — and quote the line).

Issue title: {TITLE}
Issue body:
---
{BODY}
---

Output exactly this YAML (no prose before or after):

```yaml
issue: {NUM}
modifies:
  - path/to/File.kt
creates: []
approach: "One-line summary."
depends_on: []  # list of issue numbers this is blocked by
```
```

Aggregate planner outputs into the conflict graph.

---

## Step 3 — Propose a wave

From the conflict graph, find a maximal independent set respecting:

- **Wave cap:** 4 issues max per wave (configurable; raise only with reason).
- **Dependency rule:** an issue with `depends_on: [N]` cannot be in any wave
  while `N` is open or unmerged.
- **Hot-file & file-set rule:** no two issues in the same wave conflict.

Show the proposal to the user before executing:

```
Wave {N} proposal ({K} issues):
  • #47  Coil ImageLoader uses Dispatchers.Default → Dispatchers.IO
        files: data/.../CoilModule.kt
  • #48  fullscreenSemiTransparentBackground recomposes
        files: ui/.../Modifiers.kt
  • #45  *DelayAtLeast Flow operators use System.currentTimeMillis
        files: common/.../DelayAtLeast.kt

Deferred to later waves (conflicts noted):
  • #44  SideEffect mutates Activity window state — conflicts with #48 (shares ui/.../Theme.kt)
  • #46  StoreViewModel .catch swallows Paging errors — depends on #45

Proceed with this wave? (yes / adjust / abort)
```

Allow the user to drop, add, or swap issues. Re-validate the conflict graph
after any change. Only proceed once the user confirms.

---

## Step 4 — Execute the wave

Spawn one Agent per issue **in a single message** with `isolation: "worktree"`.
All agents in a wave run concurrently.

**Per-issue sub-agent prompt template:**

```
You are resolving GitHub issue #{NUM} end-to-end in an isolated worktree.

## Issue
Title: {TITLE}
URL: {URL}
Body:
---
{BODY}
---

## Your job
1. Implement the fix. Make commits with clear messages on a new branch named:
   `wave/{CAMPAIGN_SLUG}/issue-{NUM}-{TITLE_SLUG}`
   The branch must be created off `dev`.
2. Run the project's tests/lint where relevant. If tests are broken by your
   change, fix them.
3. Push the branch to `origin`.
4. Open a PR with:
   - Base: `dev`
   - Title: `{TYPE}(#{NUM}): {short title}` where TYPE is `fix` for
     bug/bug-hunt issues, `refactor` for refactor issues, `feat` for new
     features. Match recent commit style in `git log --oneline -20`.
   - Body: starts with `Closes #{NUM}.`, then a brief summary of the change,
     then the standard Claude Code attribution line at the end.
5. Return a short report containing exactly:
   - Branch name
   - PR number and URL
   - Files changed (list)
   - Any tests added/modified
   - Any surprises, blockers, or things the reviewer should know

## Constraints
- Do NOT touch files outside what the fix requires. The orchestrator pre-cleared
  your file set against other parallel issues; touching unexpected files risks
  conflict with sibling agents.
- Do NOT merge the PR. Stop after opening it.
- If you cannot complete the issue (test failures you can't fix, ambiguity in
  the issue, missing context), open NO PR. Return a failure report explaining
  what blocked you.

## Files you said you would touch (from planning step)
{PLANNER_FILE_LIST}
```

---

## Step 5 — Sanity-check each result

For every sub-agent that returned, verify before trusting its self-report:

```bash
# Branch exists on origin
gh api "repos/:owner/:repo/branches/{BRANCH}" >/dev/null 2>&1

# Has commits ahead of dev
git fetch origin {BRANCH} dev
git rev-list --count origin/dev..origin/{BRANCH}  # must be ≥ 1

# PR exists, is open, targets dev
gh pr view {PR_NUMBER} --json state,baseRefName,headRefName
```

Mark the issue as:

- `done` — all checks pass, PR is open against `dev`.
- `failed` — any check fails, OR the agent self-reported failure. Record the
  reason in `state.yaml` and `wave-{N}.md`. Do not retry automatically — the
  user can re-run the issue in a future invocation.

A wave continues even if some issues fail. Other successful PRs are still
opened and counted.

---

## Step 6 — Write notes

The campaign folder is `.claude/notes/{YYYY-MM-DD}-{label-slug}/`. The label
slug is the labels joined with `-` (e.g., `bug-hunt-severity-low`).

### `state.yaml` — machine-readable source of truth

```yaml
campaign_slug: "2026-05-01-bug-hunt-severity-low"
labels: ["bug-hunt", "severity:low"]
created: "2026-05-01"
status: "in_progress"  # in_progress | complete
current_wave: 1
issues:
  - number: 47
    title: "Coil ImageLoader uses Dispatchers.Default instead of Dispatchers.IO"
    wave: 1
    branch: "wave/2026-05-01-bug-hunt-severity-low/issue-47-coil-dispatcher"
    pr: 54
    pr_url: "https://github.com/.../pull/54"
    status: "open"  # open | merged | closed | failed
    files: ["data/.../CoilModule.kt"]
  - number: 48
    title: "..."
    wave: 1
    status: "failed"
    failure_reason: "Sub-agent could not reproduce the recomposition; issue body lacks repro steps."
```

### `wave-{N}.md` — human-readable log

One file per wave, written at the end of the wave. Include:

- Wave summary: K issues attempted, J succeeded, F failed
- Per-issue: status, PR link (if any), one-line fix summary, surprises
- Conflicts that deferred issues out of this wave (with reasons)
- Notes from sanity-check failures, if any

### `lessons.md` — running

Append after each wave. Two sections:

```markdown
## Campaign lessons

- (wave 1) Issue #47 — Coil ImageLoader: project uses Hilt-provided ImageLoader
  in `data/CoilModule.kt`, not the default one. Pattern: any IO-dispatcher fix
  in this repo should check Hilt modules first.

## Promotion candidates (project-wide)

- [ ] Flow operators that use wall-clock time (`System.currentTimeMillis`,
  `Instant.now()`) break tests using virtual time. Default to injectable Clock
  or `TimeSource`. — drafted from issue #45
```

---

## Step 7 — Promote lessons to project-wide

Before exiting (or before planning the next wave), show the
**Promotion candidates** section to the user. For each candidate:

```
Promote to project-wide `.claude/lessons.md`?
  [y] yes — append now
  [n] no  — leave as campaign-only
  [e] edit — let me rewrite it before promotion
  [s] skip all remaining
```

For each `y` or `e`: append the (possibly-edited) lesson to the repo-level
`.claude/lessons.md` and check the box in the campaign's `lessons.md`. Use the
existing format of `.claude/lessons.md` if there is one — read it before writing
to match the convention.

This is a confirm-gate, not silent auto-promotion. Lessons file is too important
to write to without a sanity check.

---

## Step 8 — Exit, or wrap up

### After a successful wave

1. Update `state.yaml`: bump `current_wave`, set issue statuses, set
   `status: in_progress`.
2. Write `wave-{N}.md`.
3. Update `lessons.md` and run Step 7 promotion.
4. Print a summary to the user:

```
Wave {N} complete.
  PRs opened: #54 (#47), #55 (#48), #56 (#45)
  Failed: 0

Next steps:
  1. Review and merge the PRs at your pace.
  2. Re-run this skill (no args) to plan wave {N+1} once PRs are merged.

State saved to: .claude/notes/{campaign-slug}/
```

5. **Stop.** Do not poll, do not auto-plan the next wave. The user merges PRs
   and re-invokes when ready.

### When campaign is complete (Step 1 returned zero)

1. Set `state.yaml` `status: complete`.
2. Write a final `summary.md` in the campaign folder: total waves, total
   issues, success rate, links to all PRs, any unresolved failures.
3. Run Step 7 promotion one last time on any remaining candidates.
4. Tell the user the campaign is done.

---

## Re-entry edge cases

- **Prior-wave PRs still open at re-entry.** Don't auto-plan the next wave.
  Show the user the open PRs and recommend waiting. If the user says "proceed
  anyway", the planner must treat files in those open PRs as occupied — defer
  any candidate wave-N+1 issue that touches them.
- **An issue from a previous wave was closed without a PR merge** (user closed
  manually, or PR was rejected). Mark the issue's status accordingly in
  `state.yaml`. It will not re-appear since `gh issue list --state open` won't
  return it.
- **A previously-failed issue.** The next campaign re-query will pick it up
  again if still open and matching labels — fresh attempt.
- **New issues appearing under the same labels mid-campaign.** Each wave
  re-queries `gh issue list`, so new issues join the candidate pool naturally.

---

## Configuration knobs

Edit these in this SKILL.md when the project's needs change:

- **Hot-file list** (Step 2a) — add files that frequently appear in many issues.
- **Wave cap** (Step 3) — default 4. Raise if reviewer bandwidth is high.
- **Type inference** (Step 4 sub-agent prompt) — add mappings if new label
  → commit-type conventions emerge.
- **Base branch** — currently `dev` per project convention. Update if
  the project's main branch changes.

---

## What this skill does NOT do

- Does not merge PRs. Human review is required.
- Does not implement issue logic itself — every implementation is delegated to
  a sub-agent. The skill is an orchestrator.
- Does not poll for PR merge. Re-invocation is the polling mechanism.
- Does not retry failed sub-agents. Failures are logged; user decides.
- Does not auto-promote lessons to `.claude/lessons.md`. Promotion is gated
  on user confirmation.