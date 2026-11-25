---
name: deep-review-codebase
description: Principle-based review — think, run once, fan out, report, persist, route fixes (report-only)
argument-hint: "[path-or-target] [--diff]"
related:
  - deep-thinking
  - deep-analyze
  - deep-validate
  - use-subagents
  - report-review
  - deep-review-codebase-then-fix
  - update-devin-project-rules
  - update-astgrep-rules
  - update-review-cli-then-run
  - follow-deep
  - list-workspaces
  - suggest-next-action
  - review-issues
  - review-gaps
---

## Goal

Review any scope across every dimension that applies to it, with maximum coverage and minimum tokens, following six principles — Think → Run once → Fan out → Report → Persist → Route. Report only; fixes go through `/deep-review-codebase-then-fix`

## Scope

Use when a review of a scope (path, workspace, diff, whole repo, issue, plan) is needed — the single canonical reviewer; every `improve`/`optimize`/`review` caller dispatches here, and `/follow-deep` routes a task here whenever it needs a deep review pass

- dimensions are not a fixed catalog — they come from the review CLI/linter output and from `/deep-thinking` per scope (never a blind sweep)
- domain knowledge the old catalogs held is delegated: mechanical checks live in the review CLI + ast-grep `rules/`, agent guidance lives in `.devin/rules/`, conventions in `follow-*`/`review-devin-global-harness`
- one dimension only, without the full scan pipeline → `/review-issues` (provably wrong behavior) or `/review-gaps` (promised but not delivered); `/review` runs both plus the inconsistency pass
- report only, no code changes — to fix findings → `/deep-review-codebase-then-fix` per domain

## Execute

Every run follows the six principles in order.

### 1. Think

> Goal: decide which dimensions apply to this scope — never blind-sweep

1. Run `/deep-thinking` on the scope — what kind of artifact is this (CLI, web, API, docs, skills), which risks exist, which dimensions can yield findings; if the scope's shape is unclear, take structure/dependency evidence from `/deep-analyze` first
2. Pick the mode: `[path-or-target]` limits scope; `--diff` reviews only files changed per `git diff` (one full scan per day/release, diff otherwise)
3. Set a hard budget: workspaces (enumerate a monorepo with `/list-workspaces`) ≤ 10 per run, subagent dispatches ≤ 30 — over budget → top-priority only, record `skipped (budget)` with reasons in the ledger
4. Create the progress ledger `reports/.deep-review-codebase-<time>.ledger.json` — `{dispatched: {dimension: {workspace, status}}, startedAt}`; update on every dispatch; it makes coverage verifiable and the run resumable

### 2. Run once

> Goal: one deterministic full scan, sliced — never rerun the CLI per dimension

1. Manual pre-pass first (`git status`, spot-read changed files, check report freshness); CLI/analyzer issues → record in `update-review-cli-then-run/references/known-issues.md` before continuing
2. Prepare the analyzer: `tools/review-codebase` (or `/update-review-cli-then-run` to create it; the Rust `linter` CLI is a drop-in alternative); if neither is available, use whatever deterministic scan the project has (`run-check`, linters) and say so in the report
3. Run ONE full scan → `reports/review-report.json`; store score/grade/domain breakdown/baseline delta
4. Validate the output schema before dispatch (keys, severity, evidence, `fixSkill` present per finding; `falsePositiveRate`/`analyzerErrors` sane) — broken output goes to `/update-review-cli-then-run`, not around it
5. Use `/use-scripts` to slice the JSON into `reports/.deep-review-codebase-<time>/findings-<dimension>.json` — one dimension per file, deterministic, no parsing in the parent context

### 3. Fan out

> Goal: one reviewer per dimension, max coverage, disjoint slices

1. Use `/use-subagents` — spawn one domain-review subagent per dimension that has findings; inputs: `dimension`, `workspace-path`, slice file; output contract: findings table (No., Finding, Severity, Evidence, Action, Owner Skill) + dimension summary
2. Subagents read only their slice + files named in evidence — never rerun the CLI, never sweep the codebase
3. A dimension with ≤ 2 findings → the parent analyzes it itself; independent dimensions → parallel batches ≤ 10 (`/follow-parallel`)
4. A dimension the scan doesn't cover but `Think` judged relevant → analyze it manually and mark it `review-failed`/`covered-manually` in the ledger — never silently drop a dimension
5. On timeout/crash/parse error → mark `failed` in the ledger and carry the error into the report; merge results and dedup by `file + rule + dimension` (keep highest severity, combined evidence)
6. Any metric the analyzer misses → hand off to `/update-review-cli-then-run` as an analyzer gap

### 4. Report

> Goal: one table per dimension + a verifiable coverage matrix

1. Run `/report-review` — summary first (score/grade, findings by severity and dimension, mode + scope, must-fix-before-production), then one findings table PER dimension: `No.`, `Action`, `Evidence` (file:line — mandatory), `Severity`, `Risk`, `Priority` (+ status new/existing/fixed/regressed), `Owner skill` (the report's `fixSkill` — never remap yourself), `in update-review-cli-then-run` (Y/N)
2. Include `Coverage` built from the ledger: rows = workspace, columns = dimension, cell = done/skipped(reason)/failed — coverage is proven, not claimed
3. Interrupted midway → report the partial coverage matrix immediately; a partial report beats no report
4. Only on explicit user request → `/create-report-in-dot-devin` with title `deep-review-codebase`
5. Verify before finishing with `/deep-validate`: every row has real evidence, every ledger dimension appears

### 5. Persist

> Goal: findings become durable — the same finding must not survive the next run

1. Findings that are natural-language conventions/agent guidance → `/update-devin-project-rules` (author `.devin/rules/*.md` for the workspace type)
2. Findings that are mechanically enforceable (imports, patterns, API misuse, naming) → `/update-astgrep-rules` (AST rules + `sgconfig.yml`)
3. Findings the analyzer can't see → `/update-review-cli-then-run` adds the check; analyzer bugs → `update-review-cli-then-run/references/known-issues.md`
4. After persisting, re-scan the same scope to confirm the finding now fails loudly or is gone — a rule that doesn't fire on the original violation is not durable

### 6. Route

> Goal: fixes leave this skill — the report-only contract is kept

1. Every fix goes to `/deep-review-codebase-then-fix` per domain — this skill never edits code, business logic, or config
2. Order the suggested fix sequence Foundation → Dependencies → High impact → Critical path → High risk with rough effort (not a flat TODO)
3. Close with `/suggest-next-action`; residual notes list accepted false positives, `review-failed`/`skipped` dimensions, and how to resume

## Rules

- Report only — no code changes, no fix shortcuts; `deep-review-codebase-then-fix` is the only fixer
- Evidence first — every finding cites `file:line` or report evidence; spot-check ≥ 1 item per dimension against real files; no severity from intuition
- One scan per run — subagents share slices; re-review after fixes uses `--diff`, never a full rescan
- Budget and ledger are hard contracts — over budget marks `skipped (budget)`; a dropped dimension in the ledger is a reporting bug
- Never judge a dimension absent because "there probably isn't a problem" — skip only for clearly N/A conditions, with the reason in the ledger
- Loop limit — ≤ 3 rounds of CLI repair via `/update-review-cli-then-run`; per-dimension subagents retry once; `score < 70` after 3 rounds → stop and report
- Write ledger/slice files only under `reports/`

## Expected Outcome

- One full scan sliced per applicable dimension, reviewed at max coverage under budget — proven by the `## Coverage` matrix from the ledger
- Chat report via `/report-review`: per-dimension tables + summary + prioritized fix sequence, no files unless asked
- Findings persisted as `.devin/rules/*.md` + ast-grep rules + analyzer gaps, so they cannot silently recur
- All fixes routed to `/deep-review-codebase-then-fix` per domain — this skill changed no code
- Interrupted runs resume from the ledger without rerunning completed work
