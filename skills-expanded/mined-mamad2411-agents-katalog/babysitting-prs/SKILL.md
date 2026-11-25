---
name: babysitting-prs
description: Runs a single babysitting pass on an open pull request — detects the platform (GitHub, Bitbucket, or Truora's Bitbucket+betico), pulls review and CI state, applies fixes to actionable feedback, resolves threads, and hands the PR to the platform's native ready-gate. Designed to be invoked on a cadence via `/loop`. Use when the user says "babysit my PR", "watch this PR", "loop my PR", "check my PR", or asks to keep a PR moving toward merge without doing the merge directly.
---

# Babysitting PRs

One iteration of a "keep my PR moving" loop. Platform-agnostic at the top; platform commands live in `references/`.

Designed to be driven by `/loop`:

```
/loop 5m /babysitting-prs
```

Each tick does **one full pass**, reports state, and exits. The loop owns cadence — this skill owns correctness.

## Skill Contents

- `SKILL.md` — agnostic playbook (this file)
- `references/github.md` — `gh` command map for GitHub
- `references/bitbucket.md` — `bkt` command map for vanilla Bitbucket Cloud; defers to `bitbucket-receiving-code-review` for full detail
- `references/truora-betico.md` — Truora-specific betico playbook (loaded only when the remote is a Truora Bitbucket repo)
- `scripts/detect-platform.sh` — prints `github`, `bitbucket-truora`, `bitbucket`, or `unknown` based on `git remote get-url origin`

## When NOT to use

- PR is already merged or closed → tell the user to stop the loop.
- No PR exists for the current branch → run `creating-bitbucket-prs` or `branch-pr` first.
- The change is unfinished → finish the work; babysitting is for review/landing, not authoring.

## Loop contract

Every tick MUST:

1. Be **idempotent** — safe to re-run. Never apply the same fix twice, never re-post the same comment, never re-resolve a resolved thread.
2. Be **conservative** on writes — apply fixes only when feedback is clearly actionable and the change is in scope. Push back in a comment when it isn't.
3. **Never merge directly.** The skill's terminal action is posting `bot: ready` (Bitbucket) or enabling native auto-merge (`gh pr merge --auto`). Platform owns the actual merge.
4. **On `bitbucket-truora` only**: never edit the PR title manually — betico owns it. Drive title state via `bot: ready` / `bot: not ready` comments. See `references/truora-betico.md`. On plain GitHub or vanilla Bitbucket, editing titles is fine.
5. End with a **structured report** (see "Report" below) so the loop's next tick — and the user — can see what changed.

If the PR is merged or closed at the start of the tick, skip to "Stop conditions" and report.

## Step 0 — Working-hours guard

This skill is review-facing. Pinging reviewers off-hours is rude and noisy.

Before doing anything, check the local clock:

```bash
HOUR=$(date +%H); DOW=$(date +%u)   # DOW: 1=Mon … 7=Sun
```

If `DOW >= 6` (Sat/Sun) or `HOUR < 9` or `HOUR >= 18`, **exit early** with a one-line report: `"Outside working hours (Mon–Fri 09:00–18:00). Skipping tick."` Do NOT sleep, do NOT post anything. The `/loop` interval owns cadence — the guard just makes off-hours ticks no-ops.

Override only when the user explicitly says "check now" or invokes the skill directly (not via `/loop`).

## Step 1 — Identify PR and detect platform

Resolve the PR for the current branch (or from a URL the user passed in this turn).

```bash
PLATFORM=$(scripts/detect-platform.sh)
BRANCH=$(git branch --show-current)
```

- `PLATFORM=github` → use `references/github.md`.
- `PLATFORM=bitbucket-truora` → use `references/bitbucket.md` AND `references/truora-betico.md`. The Truora repos run betico, which owns the PR title and the merge gate.
- `PLATFORM=bitbucket` → use `references/bitbucket.md` only. No betico — Step 5 stops at "ready, needs manual merge" since vanilla Bitbucket has no native auto-merge equivalent.
- `PLATFORM=unknown` → stop and ask the user which platform; do not guess.

If no PR is open for `$BRANCH`, stop and report "no PR for branch — create one first".

## Step 2 — Pull state

For the resolved PR, fetch in parallel:

- **PR metadata**: title, state (open/merged/closed), base branch, head SHA, draft status.
- **Reviews / approvals**: who approved, who requested changes, who is still pending.
- **CI**: latest run for the head SHA — state and conclusion.
- **Unresolved threads**: every comment thread not yet resolved at the **thread root** (Bitbucket has a stale-resolution gotcha — see `references/bitbucket.md`).
- **Dependencies** (if the PR description has a Dependencies section): merge state of each linked PR.

Cache the head SHA. You will re-read it in Step 5.

## Step 3 — Triage threads

Bucket every unresolved thread into one of:

- **Actionable** — reviewer wants a code change you can make safely in scope.
- **Question** — reviewer asks *why*. Usually means the code needs a comment, not a code change.
- **Disagreement** — reviewer's suggestion conflicts with a prior decision, the spec, or measured behavior.
- **Out of scope** — valid feedback, but belongs in a follow-up issue.
- **Informational** — no response required (e.g., "nice catch", "lgtm").

For each bucket:

| Bucket | Action this tick | Reply tone |
|---|---|---|
| Actionable | Apply the fix → commit (work-unit-commits) → push → reply on thread → resolve via API | **Terse**: one word — `done` or `fixed`. Optionally a single line linking the commit. No paragraphs. |
| Question | Add the missing code comment → push → reply | **Brief**: 1–2 sentences answering the *why*. |
| Disagreement | Reply with evidence (link to docs, decisions, benchmarks). Do NOT resolve. If 3+ back-and-forths, escalate (top-level comment proposing a sync). | **Full**: this is the only bucket that gets the warm comment-writer treatment. |
| Out of scope | Reply acknowledging + link to a follow-up issue. Resolve. | **Brief**: acknowledge + link. |
| Informational | Resolve silently if it's a leaf reply; otherwise leave alone. | n/a |

Resolution gate — **only resolve a thread when both sides agree it's done**:

- Author side: the fix landed in a pushed commit (Actionable / Question), or a follow-up issue exists (Out of scope).
- Reviewer side: the thread root either requested the change (which you just made) or the latest reviewer comment signals acceptance ("thanks", "ok", thumbs-up reaction). If the reviewer's last word was a new question or pushback, do NOT resolve — reply and wait for the next tick.

Always respond on the PR even if the conversation moved to chat or a call — visibility for the next reader.

Use `comment-writer` only for the **Disagreement** bucket. The other buckets are intentionally terser to avoid flooding humans with paragraphs after small fixes.

## Step 4 — CI and merge conflicts

**Merge conflict with the base branch** → STOP the loop. Post `bot: not ready` (Bitbucket) or `gh pr merge --disable-auto` (GitHub) if a ready-gate is already armed, then report `STOP — merge conflict with <base>, resolve manually`. Do not try to resolve conflicts inside the loop.

CI state for the current head SHA:

- **In progress** — note ETA and move on.
- **Failed (caused by this PR)** — fix it as an actionable item this tick. One retry only.
- **Failed (flake — known-flaky test or infra error)** — trigger one re-run via the platform CLI and note it. If it fails again on the next tick with the same flake, treat as broken (next bullet).
- **Failed (broken `main`, dep regression, persistent flake)** → STOP the loop. Post `bot: not ready` if applicable, then report `STOP — CI broken, see <link>`. Never silently retry forever.
- **Passed** — proceed to Step 5.

## Step 5 — Ready-gate

**Dependencies first.** If the PR description has a Dependencies section and any listed PR is unmerged, post `bot: not ready` (Bitbucket) or keep auto-merge disabled (GitHub) and skip the rest of Step 5. Report `waiting on dependencies: <PR list>`. The loop will retry next tick.

Otherwise, before arming the gate, **all** of these must be true:

- Every dependency PR in the description has merged.
- Every actionable / question / out-of-scope thread is resolved via the API (per the Step 3 resolution gate).
- Latest CI run on the **current** head SHA is green.
- No merge conflict with the base branch.
- Re-read the head SHA — if it changed since Step 2, restart from Step 1. A new push invalidates the green CI you just observed.

When all gates pass, in order:

1. **Un-draft** the PR if it is still draft:
   - GitHub: `gh pr ready`.
   - Bitbucket (any flavor): `bkt pr update "$PR_ID" --draft=false`.
2. **Arm the platform gate**:
   - GitHub: `gh pr merge --auto --squash` (or `--merge` / `--rebase` per repo convention).
   - `bitbucket-truora`: post top-level `bot: ready` only if the title doesn't already show ready (see `references/truora-betico.md`).
   - Vanilla `bitbucket`: stop here. No native auto-merge — report `ready — needs manual merge by approver`.

If something later regresses (new comment, CI run turns red, dependency un-merged), undo:

- GitHub: `gh pr merge --disable-auto`.
- `bitbucket-truora`: post `bot: not ready`.
- Vanilla `bitbucket`: nothing to undo (no gate was armed) — just re-draft if appropriate.

This skill never runs `git merge`, `gh pr merge` without `--auto`, `bkt pr merge`, or any other direct merge command.

## Stop conditions

End the loop (tell the user to stop `/loop`) when:

- PR state is `merged` or `closed`.
- **CI is broken** in a way the loop cannot fix this tick (broken `main`, dep regression, repeat flake).
- **Merge conflict** with the base branch.
- Reviewer has requested changes and there are no actionable threads to resolve in this tick — the ball is in the human's court.
- A blocker requires user judgment the skill cannot make safely (escalation to Tech Lead, ambiguous reviewer ask, secret/credential question).

In all cases, the report's `Next:` line MUST start with `STOP — <reason>` so the loop's next tick recognizes it and the user sees a clear stop signal.

## Report

End every tick with this exact shape:

```
PR: <link>
Platform: <github|bitbucket>
Head SHA: <short>
State: <open|merged|closed> | Draft: <yes|no>
CI: <state/conclusion>
Approvals: <n approved, n requested-changes, n pending>
Threads: <n actionable, n question, n disagreement, n oos, n informational>

Actions this tick:
- <bullet per concrete action: commit pushed, thread resolved, bot:ready posted, …>

Next: <one of: "waiting for CI (~Xm)", "waiting for reviewer", "ready — auto-merge enabled", "STOP — <reason>">
```

The `Next:` line is what the loop's next tick reads first to decide whether to keep going.

## Cross-references

- `bitbucket-receiving-code-review` — full Bitbucket command reference; this skill delegates to it for `bkt` specifics.
- `creating-bitbucket-prs`, `branch-pr` — use these to create the PR before starting the babysitting loop.
- `comment-writer` — wording for replies.
- `work-unit-commits` — commit shape when applying fixes.
