---
name: git-pr-ops-orchestrator
description: "Route a GitHub PR/issue task to the right skill among the git-pr-ops specialists — read-only review, finding-resolution + safe push, deterministic squash merge, raw gh CLI queries, autonomous issue-to-PR fixing, and repo status / next-wave planning. USE WHEN a user is reviewing, preparing, merging, or shipping work through GitHub PRs and issues but hasn't named the specific step."
cluster: git-pr-ops
version: 1.0.0
---

# git-pr-ops Orchestrator

The single entry skill for GitHub pull-request and issue operations. It locates the task on the
**review → prepare → merge** delivery pipeline (plus the issue-driven and reporting lanes that feed
it) and delegates to one of its specialist spokes. The cross-cutting model every spoke shares — the
`.local/` artifact handoff, head-SHA pinning, the push/merge safety rules, and the finding-severity
contract — lives in `git-pr-ops-core`; read it before preparing or merging a PR.

## Cluster map (spoke → role)

- **`review-pr`** — read-only PR analysis. Produces `.local/review.md` (human) + `.local/review.json` (structured findings) and hands off to `prepare-pr`. Never pushes or merges.
- **`prepare-pr`** — resolves the BLOCKER/IMPORTANT findings from `review.json`, runs gates, and pushes to the PR head with `--force-with-lease`. Ends with "PR is ready for /merge-pr".
- **`merge-pr`** — deterministic squash merge, head-SHA pinned, required-check gated, with co-author trailers and post-merge verification. Ends in `MERGED`, never `CLOSED`.
- **`github`** — raw `gh` CLI reference (`gh issue`, `gh pr`, `gh run`, `gh api`) for ad-hoc queries, CI-run inspection, and JSON/jq filtering.
- **`gh-issues`** — autonomous issue→PR pipeline: fetch issues, spawn parallel sub-agents to fix them and open PRs, then watch and address review comments. Curl + REST API; supports fork mode, watch, and cron.
- **`github-next-wave-orchestrator`** — repo reality scan → Status Report + a prioritized, parallel-where-possible "next wave" of work. Read-only unless the user approves execution.

## Routing rules (intent → spoke)

**Move one PR through the pipeline (the core flow)**
- "Review this PR" / "is this PR safe to merge?" → `review-pr`
- "Fix the review findings and push" / "get this PR ready" → `prepare-pr` *(requires `review.json`)*
- "Merge it" / "squash and merge" → `merge-pr` *(requires `prep.env`)*

**Inspect / query GitHub directly**
- CI run failed, list runs, view logs, one-off `gh api` / `gh pr` / `gh issue` calls → `github`

**Drive issues autonomously**
- "Work through the open issues" / "auto-fix bugs and open PRs" / "watch for new issues" → `gh-issues`
- "Address the review comments on the open PRs" → `gh-issues --reviews-only`

**Plan / report**
- "Where is this repo right now?" / "summarize issues" / "run the next wave" → `github-next-wave-orchestrator`

Multi-step asks fan out in pipeline order. "Review and merge this PR" → `review-pr` → `prepare-pr` →
`merge-pr`, with the `.local/` artifacts carried forward between each (see `git-pr-ops-core`).

## Standard Operating Flow

1. Locate the task on the lane: is it **one PR** (review → prepare → merge), an **issue batch** (`gh-issues`), a **direct query** (`github`), or a **status/plan** (`github-next-wave-orchestrator`)?
2. If it touches **preparing or merging**, pull the model from `git-pr-ops-core` first — the artifact handoff, head-SHA pin, and push/merge safety rules are interlocking, not independent.
3. Delegate to the spoke(s). The pipeline lane is strictly ordered and gated by artifacts; do not skip `review-pr` before `prepare-pr`, or `prepare-pr` before `merge-pr`.
4. Return: chosen spoke(s), the artifact(s) produced or consumed (`review.json` / `prep.env`), the PR's gate/check status, and the next action.

## Guardrails

See `git-pr-ops-core`. In short: the pipeline is **gated, not optional** — `review-pr` is read-only;
`prepare-pr` pushes only to the PR head with `--force-with-lease` against a known SHA and never to
`main`; `merge-pr` pins the head SHA, honors required checks, and ends in `MERGED`. Never use
`gh pr merge --auto`, never `git push` to a base branch, never delete a worktree mid-pipeline, and
never resolve a PR without its `.local` artifacts. State every required finding you resolve and every
gate result before merging.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills —
only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load
it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
