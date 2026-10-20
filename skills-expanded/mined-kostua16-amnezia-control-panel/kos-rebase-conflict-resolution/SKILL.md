---
name: kos-rebase-conflict-resolution
description: Resolve rebase conflicts for a PR (preserve PR intent + base behavior, address unresolved review feedback touched by conflicts), continue the rebase, and return the prompt's JSON — the agent does NOT push (the workflow force-pushes with-lease).
user-invocable: true
when_to_use: "When the rebase-pr workflow resumes a stopped rebase and run-zai is invoked on conflict, or when diagnosing a rebase-pr run."
category: utilities
argument-hint: "[pr-number]"
keywords: [rebase, conflict, merge-conflict, review-feedback, json, no-push, force-with-lease]
related: [kos-zai-agent-runtime-contract, kos-gh-automation-tooling, kos-zai-run-failure-prevention]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from rebase-pr.yml prompt + docs/workflow-e2e-scenarios.md §6e
  license: repo
  version: "1.1"
---

# Idea

`rebase-pr` rewrites the SAME PR branch onto its base. Clean rebases validate + push **with no AI**; `run-zai` is invoked **only when Git enters a conflict state**, with review feedback pre-fetched so the agent can preserve/address findings touched by conflicts. The agent **resolves conflicts and returns JSON — it does NOT push** (the workflow `validate-pr-gate` gates, then force-pushes `--force-with-lease` to the same branch). A prior "Post ancestry failure" (`upsert-rebase-comment`) is a workflow step, not the agent's job.

## When to invoke this skill directly
- You are the run-zai agent invoked on a rebase conflict for a PR.
- Diagnosing a rebase-pr run.

## References
- `rebase-pr.yml` prompt (continue rebase stopped on conflicts; read trusted conflict context FIRST, then pre-fetched feedback).
- `docs/workflow-e2e-scenarios.md` §6e (branch-refresh tool; clean rebases need no AI; run-zai only on conflict; workflow force-with-lease; gate).
- `analyze-rebase-ancestry.cjs`, `auto-resolve-trivial-rebase-conflicts.cjs`, `evaluate-rebase-eligibility.cjs`, `upsert-rebase-comment.cjs` (workflow steps).
- [[kos-zai-agent-runtime-contract]].

## Communication Style
Conflict count → resolution approach per file → CONTINUED|ABORTED + the JSON. No push.

## Core Principles
YAGNI / KISS / DRY. Preserve PR intent + base behavior; prefer PR changes, reconcile where they diverge. Address unresolved review feedback touched by conflicts. Never force-push (the workflow does). Never weaken tests or drop PR intent to end a conflict.

## Your job (enforce)
1. Read the trusted conflict context file FIRST (workflow-generated status, conflicted paths, rebase metadata).
2. Read the pre-fetched review feedback file SECOND (unresolved threads, review submissions, diff).
3. Enumerate conflicted files (`git diff --name-only --diff-filter=U`) only if the context is insufficient or stale.
4. Resolve each conflict preserving PR intent AND base behavior; if a conflict touches unresolved review feedback, address it as part of the resolution.
5. Continue via `git -c core.editor=true rebase --continue` (no editor); iterate `npx tsc --noEmit` for fast feedback.
6. Stay inside the rebase workflow Bash allowlist: use `Read`, `rtk read`, `rtk grep "<pattern>" <path>`, relative commands like `node`, `npm`, `npx`, `rtk`, and the explicit `git -c core.editor=true rebase --continue` form. Do not use absolute binaries (`/usr/bin/node`), `cat`, `echo`, command substitution, semicolons, pipes, shell control operators, or shell wrappers for validation.
7. Do not inspect `.git/rebase-*` directly; use the trusted conflict context file for rebase metadata.
8. Do not use Grep as a file reader; use Read for files or `rtk grep "<pattern>" <path>` for searches.
9. Leave the tree with **no rebase in progress and no unstaged conflict markers**. If a conflict cannot be resolved, stop and report — do not force a bad merge.

## Hard rules (the prompt)
- **Do NOT push. Do NOT `git commit` or create standalone commits outside the rebase. Do NOT merge/approve/close PRs or post comments.**
- Do NOT weaken or delete tests to make conflicts disappear.
- Do NOT drop source PR intent to make conflicts disappear.

## Output contract (enforce)
Return **JSON only:** `summary`, `conflicts_resolved[] {file,resolution}`, `review_findings_preserved[]`, `review_findings_addressed[]`, `validation {typecheck,tests,lint,format,build}`.

## Failure modes to avoid
- **Agent pushing** — forbidden; the workflow gates + force-pushes.
- **Ignoring review feedback** — conflicts touching unresolved threads must address them.
- **Leaving a half-done rebase** — either complete (clean tree) or report unresolvable.
- **Misattributing the post-ancestry step** — `upsert-rebase-comment` is a workflow step; leave a clean tree so it has data.

## Process Flow (Authoritative)
1. Read trusted conflict context.
2. Read pre-fetched feedback file.
3. Enumerate conflicts; resolve preserving intent+base+review-feedback.
4. `git -c core.editor=true rebase --continue`; iterate `npx tsc --noEmit`; use `rtk node --test ...` for targeted workflow tests when needed.
5. Ensure clean tree (no rebase in progress, no markers) — or report unresolvable.
6. Return the JSON; do not push.

## Output Format
```json
{"summary":"…","conflicts_resolved":[{"file":"…","resolution":"…"}],"review_findings_preserved":[],"review_findings_addressed":[],"validation":{"typecheck":"pass|fail","tests":"…","lint":"…","format":"…","build":"…"}}
```

## Critical Constraints
- Never push / commit-outside-rebase / merge / approve / close / comment.
- Never weaken tests or drop PR intent to end a conflict.
- Resolve conflicts preserving both PR intent and base behavior; address review feedback touched by them.
