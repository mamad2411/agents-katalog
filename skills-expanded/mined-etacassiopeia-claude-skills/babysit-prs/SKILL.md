---
name: babysit-prs
description: Watch one or more open PRs' CI to green and merge them, self-correcting on failure — diagnose, fix, push, re-watch until merged. Squash-merges single-commit PRs; preserves history with a crafted merge commit for multi-commit feature/epic/milestone branches. When you are a ruleset bypass actor (repo admin), admin-overrides a required-review-only block by default — even when other collaborators exist; --admin-merge is a legacy no-op. Usage: /babysit-prs [<pr-number>...] [--all] [--admin-merge]
user_invocable: true
argument-hint: "[<pr-number>...] | --all [--admin-merge]"
allowed-tools:
  - Bash(gh pr view:*)
  - Bash(gh pr list:*)
  - Bash(gh pr checks:*)
  - Bash(gh run view:*)
  - Bash(gh api:*)
  - Bash(git remote get-url:*)
  - Bash(git branch:*)
  - Bash(git status:*)
  - Bash(git log:*)
  - Bash(git worktree list:*)
---

## Live Context (loaded at invocation)

- **Requested PRs (args)**: `$ARGUMENTS` (empty → default to the current-branch PR)
- **Repo remote**: !`git remote get-url origin 2>/dev/null`
- **Current branch**: !`git branch --show-current 2>/dev/null`
- **My login**: !`gh api user --jq .login 2>/dev/null`
- **Open PRs (mine)**: !`gh pr list --author @me --state open --json number,title,headRefName,baseRefName 2>/dev/null`

(The skill body fetches per-PR state, repo permissions, and branch protection itself — keep
the Live Context free of shell expansions and jq templates, which the permission checker
rejects at preload.)

---

# Babysit PRs — Watch-Fix-Merge Loop

**Goal:** drive each requested PR from "open" to "merged", unattended. Watch CI; when it's green,
merge; when it's red, diagnose the failure, fix it on the PR's branch, push, and re-watch — until
every PR is merged or a hard stop is hit. Invoking this skill **is** authorization to merge the
named PR(s) once their gate is green (same standing as invoking a push/PR skill).

**Guiding principle:** *green CI is necessary, not sufficient.* Before merging, confirm the PR is
actually mergeable (not BEHIND/CONFLICTING, no unmet required check), and pick the merge method
that matches the branch's shape. Never force-push, never touch a branch that isn't the PR's own
head, never merge a PR whose failure you couldn't explain.

**Hard cap: 3 fix cycles per PR.** If a PR still fails after 3 fix→push→watch rounds, stop
babysitting *that* PR, report why, and move on to the others. Never merge a PR whose gate is red.

---

## Phase 0 — Resolve the PR set

Build the list of PRs to babysit, in the order to process them:

1. **Explicit numbers** (`/babysit-prs 319 320 321`) → babysit exactly those.
2. **`--all`** (or `--mine`) → every open PR authored by me (from Live Context).
3. **No args** → the PR whose head is the current branch (`gh pr view --json number`). If there
   is none, stop and say so.

**Flag — `--admin-merge`:** legacy no-op, kept for back-compat. As of the Phase 3 rule below, a
ruleset **bypass actor** (repo admin) already admin-overrides a review-only block by default,
whether or not other collaborators exist — so this flag changes nothing for a bypass actor. It only
still matters if you are *not* a bypass actor (in which case you cannot merge regardless). CI must
still be green and the PR MERGEABLE; the override only ever skips the review gate, never a red check.

For each PR, load once: `gh pr view <n> --json number,title,state,mergeable,mergeStateStatus,baseRefName,headRefName,headRefOid,commits,isCrossRepository,url`.

- Drop any PR that is already `MERGED`/`CLOSED` (report it, don't error).
- **Order by dependency:** if PR B's base is PR A's head branch (a stack), A must merge first.
  Otherwise process in ascending PR number. Record the order.

Initialize a durable **babysit-log** at `<scratchpad>/babysit-prs.md` (template at the end) with one
row per PR: number, title, chosen merge method (Phase 1), and status `pending`. Update it at every
state change — it is the loop's spine across context compaction and lets you resume mid-run.

If more than one PR is in play, keep them in the log and work them **in order**; a PR blocked
waiting on CI does not block starting the next one, but do not merge out of dependency order.

---

## Phase 1 — Choose the merge method per PR (decide up front)

Per the repo owner's rule:

- **1 commit** → **squash merge** (`--squash`). The single commit message already stands.
- **≥ 2 commits** → **merge commit** (`--merge`), **preserving the individual commits**, because
  these are the milestone / feature / epic branches whose history matters. Author a real merge
  commit message — do **not** accept GitHub's default `Merge pull request #N from …`:
  - **Title:** the PR title, conventional-commit style (e.g. `feat: …`), suffixed `(#<pr>)`.
  - **Body:** 2–5 lines summarizing what the branch delivers as a whole, then `Closes #<issue>`
    (if the PR closes one) and the milestone/epic if applicable. No Claude attribution in the body
    (the global pre-push hook blocks "Claude"; a `Co-Authored-By` trailer only if explicitly asked).

Reason from the branch, not just the count, when they disagree: a `epic/*` head or a base that is
an epic/integration branch is always a merge-commit even if it currently has one commit; a normal
`fix/*`/`feat/*` branch that accumulated fixup commits is still fine to squash if the owner would
want one clean commit — when unsure, prefer **preserve (merge commit)** for anything on/into an
epic branch and **squash** for a standalone issue PR. Record the decision and the reason in the log.

---

## Phase 2 — Watch CI to a terminal state

For each PR being processed, watch its checks until every one **concludes** (not just until the
happy path appears — a crash or hang must break the wait too).

- Poll `gh pr checks <n>` (exit status is non-zero while pending/failing). A robust watch:
  use a background monitor whose filter emits on **both** success and failure/terminal lines, so
  silence never masks a crashloop. Poll interval ≥ 30s (CI is remote; respect rate limits).
- Treat a check as terminal when its state is `pass`, `fail`, `skipping`, `cancelled`, or
  `timed_out`. `pending`/`queued`/`in_progress` are not terminal — keep waiting.
- When several PRs are in flight, watch them together; act on each as it reaches a terminal state.

**Outcome per PR:**
- All required checks `pass` (skips are fine) → **Phase 3 (pre-merge gate)**.
- Any required check `fail`/`cancelled`/`timed_out` → **Phase 4 (diagnose & fix)**.

Record the terminal check summary in the log.

---

## Phase 3 — Pre-merge gate & merge

Re-fetch `mergeable` + `mergeStateStatus` immediately before merging (CI green ≠ mergeable):

| mergeStateStatus | Meaning | Action |
|---|---|---|
| `CLEAN` | mergeable, all gates met | **merge now** |
| `HAS_HOOKS` | mergeable, passing hooks | merge now |
| `UNSTABLE` | non-required check failing | merge only if the failing check is genuinely non-required; else treat as Phase 4 |
| `BLOCKED` | a required gate unmet | diagnose which (below) |
| `BEHIND` | base moved; strict checks require up-to-date | update branch (below), then back to Phase 2 |
| `DIRTY` | merge conflict with base | resolve conflict on the PR branch (Phase 4-style), push, back to Phase 2 |

**`BLOCKED` triage:** determine *which* gate is unmet — from `reviewDecision` on the PR **plus**
the branch's rules. **Read the rules from both sources**, because a modern repo often has neither
in the legacy API:
- Legacy branch protection: `gh api repos/{owner}/{repo}/branches/{branch}/protection` — this
  **404s ("Branch not protected") when the repo uses a *ruleset* instead**. A 404 here does **not**
  mean "no rules".
- Repository **rulesets** (the common case): `gh api repos/{owner}/{repo}/rules/branches/{branch}`
  lists the active rules; a `pull_request` rule means a review is required. Fetch the ruleset detail
  (`gh api repos/{owner}/{repo}/rulesets/{id}`) for `required_approving_review_count` and, crucially,
  `bypass_actors` — whether your role (e.g. RepositoryRole `5` = Admin) may bypass.

Classify and act:
- **Required review is the sole block** (`reviewDecision == REVIEW_REQUIRED`, no failing required
  check, `mergeable == MERGEABLE`) **and you can bypass it** (you're a repo admin / in the ruleset's
  `bypass_actors`) → admin-override is the intended path: merge with **`--admin`**. This holds
  **whether or not other collaborators exist** — being a `bypass_actors` entry (e.g. RepositoryRole
  Admin, `bypass_mode: always`) *is* the owner's standing authorization to merge their own PRs past
  the review gate. The `--admin-merge` flag is therefore a no-op for a bypass actor (kept only for
  back-compat); the override applies regardless. The review gate still stands for non-bypass
  collaborators — this only lets the bypass actor merge their own green, mergeable PR.
  - If you are **not** a bypass actor → you cannot merge it; report "needs approval" and stop.
- A required **status check** that never ran → find and re-trigger it (or report if you can't).

**`BEHIND` / strict checks:** update the PR branch onto its base
(`gh pr update-branch <n>`), which re-runs CI → return to **Phase 2**. Note in the log that an
update re-armed the pipeline (this can loop; each pass still counts toward nothing — only *fix*
cycles are capped, but guard against an infinite base-moves race by stopping after 3 update rounds
and reporting).

**Merge** with the Phase-1 method:
- Squash: `gh pr merge <n> --squash --delete-branch [--admin]`
- Merge commit: `gh pr merge <n> --merge --delete-branch [--admin] --subject "<title>" --body "<body>"`

After a successful merge:
- Mark the PR `merged` in the log.
- **Clean up:** if the head branch had a local worktree (`git worktree list`), remove it
  (`git worktree remove <path>`); delete the local branch if present. Update `master` locally
  (`git fetch --prune`, fast-forward). If a memory file tracks this PR/worktree, update it.
- If this PR was the base of a stacked PR, that dependent may now be mergeable — process it next.

---

## Phase 4 — Diagnose & fix a red pipeline (per PR, capped at 3 cycles)

1. **Get the real failure**, don't guess: from `gh pr checks <n>` find the failing run, then
   `gh run view <run-id> --log-failed` (or open the specific failed job). Identify the exact
   failing step (compile error, clippy lint, test name, fmt diff, deny advisory, flaky infra).
2. **Work on the PR's own branch.** Check it out — prefer an isolated worktree
   (`git worktree add .claude/worktrees/pr-<n> <headRefName>` after `git fetch origin <headRefName>`),
   falling back to a direct checkout. Never edit files outside what the failure requires.
3. **Reproduce locally**, then **fix minimally** — fix the failure, don't expand scope. Follow the
   project's rules (for Rust: no `unwrap`/`panic`/`todo` on production paths, errors propagate,
   comments only where the *why* is non-obvious).
4. **Verify locally before pushing** — run the project's gate so you don't burn a CI cycle on an
   obvious miss: Rust → `cargo fmt`, `cargo clippy -- -D warnings` (or the repo's exact CI flags,
   e.g. `--workspace --all-targets --all-features`), `cargo test`, `cargo deny check` if a
   `deny.toml` exists. Scala → `sbt compile scalafmtCheckAll test`. Note any check that can only
   run in CI (e.g. Docker-gated integration tests) and say so.
5. **Distinguish a flake from a real failure.** If the failure is infrastructure/flaky (network,
   container pull, transient runner error) and the code is sound, re-run the job
   (`gh run rerun <run-id> --failed`) instead of "fixing" — but say so in the log, and don't
   re-run more than twice before treating it as real.
6. **Commit & push:** conventional-commit message, imperative, explains *why*; **no Claude
   attribution** in the body (global pre-push hook blocks "Claude"). Push to the PR branch.
7. Increment this PR's fix-cycle counter; append a `cycle N` line to the log. Return to **Phase 2**
   (the push re-arms CI).

**If cycle 3 still fails:** stop babysitting this PR. Record the unresolved failure (step, log
excerpt, why it's not a flake) in the log, leave the PR open, and continue with the other PRs.

---

## Phase 5 — Final report

When every requested PR has reached a terminal outcome (merged, or stopped-blocked), report:

```
## Babysit PRs — Summary

| PR | Title | Method | Result | Cycles |
|----|-------|--------|--------|--------|
| #319 | …     | squash | MERGED | 0 |
| #320 | …     | merge  | BLOCKED (needs human review) | 0 |
| #321 | …     | squash | STOPPED after 3 cycles: <failing check> | 3 |

### Merged
- #319 <sha> — worktree/branch cleaned up

### Needs your attention
- #320 — required review, and you are NOT a ruleset bypass actor; can't admin-override. Green & ready.
- #321 — <failure>; log at <scratchpad>/babysit-prs.md

### Next step
<e.g. "All requested PRs merged." or "Approve #320 to let a re-run finish it.">
```

---

## Babysit-Log Template

Write to `<scratchpad>/babysit-prs.md` in Phase 0; update every state change:

```markdown
# Babysit-Log — <repo> — <date>
order: [#319, #320, #321]   (dependency-sorted)

## #319 — <title>
- method: squash (1 commit)  | reason: standalone issue PR
- watch: Build ✓ Lint ✓ Unit(stable/beta) ✓ Redis ✓ Compat ✓
- gate: BLOCKED → required review, bypass actor (admin) → --admin
- result: MERGED <sha>; worktree removed
- cycles: 0/3

## #320 — <title>
- method: merge commit (7 commits) | reason: epic/feature branch, preserve history
- status: watching / fixing (cycle 1) / merged / stopped
- cycles: 0/3
```

---

## Hard Constraints

- **Merge = the requested outcome.** Invoking `/babysit-prs <n>` authorizes merging those PRs when
  green. But still honor the pre-merge gate — never merge a red or non-mergeable PR.
- **`--admin` only** to satisfy a required *review* when you are a ruleset bypass actor (repo admin).
  This applies even when other collaborators exist — bypass-actor status is the standing
  authorization. Never use `--admin` to bypass a failing required status check.
- **Only touch the PR's own head branch.** Never force-push; never rebase someone else's branch
  without cause; never edit files unrelated to the failing check.
- **No Claude attribution** in commit or merge-commit bodies (global pre-push hook).
- **3 fix cycles per PR**, then stop that PR and report — never ship a red gate.
- **Process multiple PRs in dependency order**; a base PR merges before its dependents.
- Keep the babysit-log current so the loop survives compaction and is auditable.
