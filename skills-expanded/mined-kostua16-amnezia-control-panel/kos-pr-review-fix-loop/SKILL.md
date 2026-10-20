---
name: kos-pr-review-fix-loop
description: The PR review/fix discipline for code-review (review-only, return JSON verdict) and fix-review (fix actionable findings, no push, return JSON) — two distinct contracts that share review-evidence handling.
user-invocable: true
when_to_use: "When running code-review (combined AI review of a PR) or fix-review (fix actionable review findings), or when such a run failed at the gate / wake-orchestrator step."
category: utilities
argument-hint: "[pr-number]"
keywords: [code-review, fix-review, review, findings, verdict, passed, concerns, json, no-push, gate]
related: [kos-zai-agent-runtime-contract, kos-claude-turn-budget, kos-zai-run-failure-prevention, kos-gh-automation-tooling, kos-commit-and-push-branch]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from code-review.yml + fix-review.yml prompts + gate/wake-orchestrator failures
  license: repo
  version: "1.1"
---

# Idea

Two PR-focused workflows share review-evidence handling but have **different jobs and output contracts**:
- **code-review** (`/gsd:code-review`) — **review only**. Produce a combined general + STRIDE/OWASP security review; return JSON verdict; **do not fix, do not approve/request-changes/edit labels** (the workflow applies `ai-review-*`/`security-review-*` labels).
- **fix-review** (`/gsd:debug`) — **fix only actionable findings**; iterate `tsc`; run the prompt's gate (`npm run format` then `npm run test && npm run build`); **do not push** (the workflow `commit-and-push` step pushes, gated by `validate-pr-gate`); return JSON.

Both read pre-fetched review feedback. Neither pushes. Observed failures: code-review at the `wake-orchestrator` step (often a tolerated non-zero exit); fix-review at the workflow's commit-and-push/gate step.

## When to invoke this skill directly
- Running a combined PR review (code-review) or fixing review findings (fix-review).
- A run failed at wake-orchestrator / commit-and-push / validate-pr-gate.

## References
- `code-review.yml`, `fix-review.yml` prompts.
- `collect-review-feedback.cjs` / `collect-stale-pr-feedback.cjs` — pre-fetched feedback file.
- `evaluate-fix-review-eligibility.cjs`; `validate-pr-gate` (the gate); `commit-and-push` step (see [[kos-commit-and-push-branch]]).
- `docs/workflow-e2e-scenarios.md` §3 (AI-review label contract), §6d (fix-review `detect-noop` + gate, no push on noop/gate-fail).
- [[kos-zai-agent-runtime-contract]].

## Communication Style
code-review: verdict + cited findings. fix-review: actionable set + per-fix change + gate result. No push in either.

## Core Principles
YAGNI / KISS / DRY. code-review reviews; fix-review fixes actionable only. Neither pushes. Each emits its own JSON.

## code-review contract (enforce)
- One shared pass: PR metadata + changed files + diff (expand to HEAD reads if needed).
- General review + **STRIDE + OWASP** security review.
- Diff hygiene: only flag `+` lines (removed `-` lines are not current); `git show HEAD:<path>` if uncertain.
- Cross-module accuracy + threat-model awareness (don't flag non-security crypto / env overrides / `process.exit` without an exploit path).
- Post actionable findings as inline comments; rate security severity none/low/medium/high/critical.
- **Return JSON only:**
  - `code_review.{verdict: "passed"|"concerns", summary, blocking_findings_count}`
  - `security_review.{verdict: "passed"|"concerns", summary, highest_severity: none|low|medium|high|critical}`
  - `reviewed_files[]` (changed-file manifest considered)
- **Do NOT approve/request changes/edit labels** — the workflow maps verdict → `ai-review-passed/concerns` + `security-review-passed/concerns` labels.

## fix-review contract (enforce)
- Read the pre-fetched feedback file FIRST.
- Fix ONLY actionable findings; ignore nitpicks; one root cause per finding.
- Iterate `npx tsc --noEmit`; before finishing run `npm run format`, then `npm run test && npm run build`; never `$queryRawUnsafe` (use Prisma `$queryRaw` tagged template).
- Stop once the gate is green; if you can't get green, **revert** so the tree is clean (the workflow won't push failing code).
- >8 files need changes → fix highest-severity, report the rest skipped.
- **Do NOT commit/push/resolve threads/post comments** — the workflow gates (`validate-pr-gate`), pushes (`commit-and-push`), and posts the sticky summary. Empty diff → workflow `detect-noop` posts `renderNoChanges`.
- **Return JSON only:** `summary, changed_files[], findings_addressed[{file,change}], findings_skipped[{file,reason}], validation{tsc,lint,tests,format,build}` (each "pass"/"fail"/"skipped").

## Failure modes to avoid
- **code-review approving/editing labels** — forbidden; only return the JSON verdict.
- **fix-review pushing** — forbidden; the workflow pushes after the gate.
- **Wrong verify** — fix-review must run the full gate (`npm run format` + `npm run test && npm run build`), not just `tsc` or `test-only`.
- **wake-orchestrator misread** — its non-zero exit is often tolerated/pre-auth; confirm it's a real error before declaring failure.

## Your Approach
1. Identify which contract (review vs fix).
2. Gather evidence (pre-fetched feedback / PR diff).
3. code-review: review + JSON verdict. fix-review: fix actionable + gate + JSON.
4. Do not push in either.

## Process Flow (Authoritative)
1. Read the prompt → pick contract.
2. (fix-review) read feedback file; (code-review) gather PR metadata + diff.
3. Execute (review / fix) within turn budget.
4. Verify (code-review: none beyond review; fix-review: the full gate).
5. Emit the contract's exact JSON; do not push.

## Output Format
- code-review: the JSON above.
- fix-review: the JSON above.

## Critical Constraints
- code-review never approves/edits labels; it returns the verdict JSON.
- fix-review never pushes; it runs the full gate and returns JSON; empty diff is a clean no-op.
- Neither resolves threads or posts the sticky summary.
