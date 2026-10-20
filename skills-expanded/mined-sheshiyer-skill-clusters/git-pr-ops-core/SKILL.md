---
name: git-pr-ops-core
description: "Shared reference for the git-pr-ops cluster: the gated review→prepare→merge pipeline, the `.local/` artifact handoff (review.json findings), head-SHA pinning, the push/merge safety rules (force-with-lease, no auto-merge, never push main), and the finding-severity contract. USE WHEN preparing or merging a GitHub PR, resolving review findings, or wiring the issue→PR flow — the interlocking rules every spoke shares."
cluster: git-pr-ops
version: 1.0.0
---

# git-pr-ops Core

Shared model for the `git-pr-ops` cluster. The review, prepare, and merge spokes all depend on these
interlocking conventions — keep them consistent here so no spoke contradicts another.

## 1. The pipeline (this cluster's defining feature)

Work moves through **three gated stages**, each producing an artifact the next stage consumes. The
stages are ordered and **not optional**: a later stage refuses to run without the prior artifact.

```
review-pr ──review.json──> prepare-pr ──prep.env──> merge-pr ──> MERGED
 (read-only)               (resolve + push)         (squash + pin)
```

- **`review-pr`** is **read-only**: it analyzes the diff against the merge-base and emits both a human
  report (`.local/review.md`, sections A–J) and machine-readable findings (`.local/review.json`). It
  never pushes, merges, or keeps code changes. → `review-pr`
- **`prepare-pr`** consumes `review.json`, resolves every required finding (see §3), runs the gates,
  and pushes the fixes to the **PR head** with `--force-with-lease`. It emits `.local/prep.env`
  (carrying `PREP_HEAD_SHA`) and ends by printing `PR is ready for /merge-pr`. → `prepare-pr`
- **`merge-pr`** consumes `prep.env`, verifies required checks, and performs a deterministic squash
  merge **pinned to `PREP_HEAD_SHA`** (`--match-head-commit`), with co-author trailers and post-merge
  verification. It ends in `MERGED`. → `merge-pr`

**Rule:** never skip a stage or hand-edit past the artifact gate. The artifacts in `.local/` are the
contract between stages — they live in the PR worktree (`.worktrees/pr-<PR>`) and must exist and be
valid before the next stage runs.

## 2. The `.local/` artifact set

| Artifact | Produced by | Consumed by | Purpose |
|---|---|---|---|
| `review.md` | `review-pr` | human | readable review, sections A–J |
| `review.json` | `review-pr` | `prepare-pr` | structured findings + recommendation |
| `prep.md` | `prepare-pr` | human | resolved-findings + gate summary |
| `prep.env` | `prepare-pr` | `merge-pr` | `PREP_HEAD_SHA` + merge context |
| `pr-meta.env` / `*-context.env` | wrapper scripts | the stages | PR metadata, merge-base, mode |

The wrapper scripts (`scripts/pr-review`, `scripts/pr-prepare`, `scripts/pr-merge`, `scripts/pr`) are
**cwd-agnostic** — run them from the repo root or inside the PR worktree.

## 3. Finding-severity contract

`review.json` carries findings with a `severity`. The prepare stage's obligation is severity-driven:

- **BLOCKER** — must be resolved before prepare can push. Hard gate.
- **IMPORTANT** — must be resolved before prepare can push. Hard gate.
- **NIT / MINOR** — optional; resolve if cheap, otherwise note and move on.

Minimum `review.json` shape: a `recommendation` (e.g. `READY FOR /prepare-pr`), a `findings[]` array
(`id`, `severity`, `title`, `area`, `fix`), a `tests` object (`ran`, `gaps`, `result`), a `docs`
status, and `changelog` (changelog is **mandatory** in this workflow). Keep prepare's scope tight —
resolve the findings, update the changelog/docs, nothing gratuitous.

## 4. Push & merge safety (default-deny)

The base branch is sacred; the PR head is the only writable target, and only carefully:

- **Never** `git push` directly, and **never** push to `main`/the base branch.
- Prepare pushes **only** to the PR head, **only** with `--force-with-lease` against the known head SHA
  (idempotent if local prep HEAD already equals the remote PR head; one automatic rebase + gate-rerun
  + lease-retry is allowed).
- Merge is **head-SHA pinned** (`--match-head-commit`) so a race can't merge unreviewed commits.
- **Never** `gh pr merge --auto` in this flow.
- Merge ends in **`MERGED`**, never `CLOSED`; cleanup (worktree/branch) happens **only after** a
  confirmed merge. Do not delete the worktree mid-pipeline.

## 5. The other two lanes

Two spokes feed or report on the pipeline rather than walking it:

- **`gh-issues`** — autonomous issue→PR engine. Fetches issues via the GitHub REST API (curl + a
  repo-scoped `GH_TOKEN`), spawns parallel sub-agents that each branch `fix/issue-<N>`, implement a
  minimal fix, test, open a PR, and (in a later phase) address review comments. Supports fork mode,
  `--watch`, and `--cron`. Each sub-agent uses a **confidence gate** (skip if < 7/10) and never
  force-pushes or touches the base branch. → `gh-issues`
- **`github-next-wave-orchestrator`** — read-only repo scan → a **Status Report** (repo pulse, issue
  landscape, PR/CI health, Green/Yellow/Red readiness) + a ranked **Next Wave** plan. Executes only on
  explicit approval; never fabricates state, never closes issues or merges PRs unprompted. → `github-next-wave-orchestrator`

Both ultimately feed the review→prepare→merge pipeline once a PR exists.

## 6. The `gh` CLI vs the REST API

- **`gh` CLI** (`github` spoke) is the default for interactive/ad-hoc work — issues, PRs, CI runs,
  `gh api` for anything the subcommands don't cover. Always pass `--repo owner/repo` when outside a
  git dir, or use URLs directly. → `github`
- **curl + REST** is used by `gh-issues` precisely because it runs in environments where `gh` may be
  absent; it carries `GH_TOKEN` as a Bearer token. The pipeline wrappers (`review/prepare/merge`) use
  `gh` under the hood for metadata and diffs.

## 7. Shared guardrails

- **The pipeline is gated, not optional**: `review-pr` → `prepare-pr` → `merge-pr`, each blocked on the
  prior `.local/` artifact.
- Review is **read-only**; resolve all BLOCKER + IMPORTANT findings before pushing.
- Push **only** to the PR head, **only** with `--force-with-lease`; never push the base branch.
- Merge is **head-SHA pinned**, required-check gated, squash, and ends in `MERGED`. No `--auto`.
- Changelog is mandatory; state every required finding resolved and every gate result.
- Cleanup only **after** a confirmed merge; never delete a worktree mid-pipeline.
- Autonomous lanes (`gh-issues`, next-wave) never close issues, merge PRs, or fabricate state without
  explicit approval; sub-agents stop below their confidence threshold rather than guess.
