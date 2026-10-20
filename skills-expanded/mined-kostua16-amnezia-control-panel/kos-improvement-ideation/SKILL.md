---
name: kos-improvement-ideation
description: Produce concrete, repo-specific improvement suggestions in the workflow's required output shape — suggest-improvements (write 2-3 proposals to .planning/ROADMAP.md + .planning/quick/**) and pr-improve (JSON quick_tasks[] + phase_suggestions[]), never pushing.
user-invocable: true
when_to_use: "When suggest-improvements runs a deep architectural review, or pr-improve analyzes a PR for follow-ups, or when such a run hit turn-limit / produced generic output."
category: utilities
argument-hint: "[scope or pr-number]"
keywords: [improvements, suggest, ideation, roadmap, quick-tasks, phase-suggestions, json, no-push]
related: [kos-zai-agent-runtime-contract, kos-claude-turn-budget, kos-gh-automation-tooling, kos-zai-run-failure-prevention]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from suggest-improvements.yml (/gsd:explore) + pr-improve.yml (/gsd:quick) prompts
  license: repo
  version: "1.1"
---

# Idea

`suggest-improvements` (`/gsd:explore`) and `pr-improve` (`/gsd:quick`) share one job: turn observations into *concrete, repo-specific* suggestions in the **output shape each prompt requires**, without pushing. Both forbid editing source/workflows and forbid push (the workflow handles PRs). Runs fail by (a) turn-budget blowout and (b) generic advice. This skill enforces the two distinct output contracts.

> **Attribution note:** an earlier version attributed a `≤6/≤20/≤6` turn allocation to the pr-improve prompt. The current `pr-improve.yml` has no such allocation — use [[kos-claude-turn-budget]] for phasing, not a quote from the prompt.

## When to invoke this skill directly
- Producing architectural/PR improvement suggestions.
- A suggest-improvements/pr-improve run hit turn_limit or returned vague output.

## References
- `suggest-improvements.yml` — `/gsd:explore`; **edit scope: `.planning/ROADMAP.md` + `.planning/quick/**`**; read `/tmp/open-prs-context.md` first to dedup vs in-progress PRs; don't edit source/workflows/manifests/tests; no git/gh; no push.
- `pr-improve.yml` — `/gsd:quick`; **planning-only**; analyze base checkout + `/tmp/pr.diff`; do NOT edit/push/comment; return **JSON only**.
- [[kos-zai-agent-runtime-contract]] — output + no-push discipline.

## Communication Style
Each suggestion: one problem (cited file:line) + one concrete change + expected benefit. No prose advice. pr-improve → JSON only.

## Core Principles
YAGNI / KISS / DRY. Concrete > comprehensive. Cite the code. Never push. Each workflow has its own output shape — emit that one.

## Output contracts (enforce)

**suggest-improvements** — write 2–3 concrete proposals directly into `.planning/ROADMAP.md` and/or `.planning/quick/**` (this is how proposals are "recorded"; not via `/gsd:capture`). First read `/tmp/open-prs-context.md` and exclude topics already in open PRs. If no worthwhile proposals → make no file changes. Summarize what was written.

**pr-improve** — return **JSON only** with two arrays (the downstream consumer parses this shape):
```json
{
  "quick_tasks": [ { "...": "narrow tactical follow-up, repo-specific" } ],
  "phase_suggestions": [ { "bucket": "workflow-governance|ci-correctness|approval-policy|planning-automation", "...": "milestone-scale addition" } ]
}
```
Do not edit files, push, or comment on the PR.

## What "concrete and repo-specific" means
- ❌ "Improve test coverage" → ✅ "`src/lib/x.ts` `parse()` has no empty-input tests; add 2 cases."
- ❌ "Better error handling" → ✅ "`api/route.ts:42` swallows the error; rethrow."
- Every suggestion cites a file/symbol + a specific change.

## Your Approach
1. Scope: architectural scan (suggest-improvements) or one PR diff via `/tmp/pr.diff` (pr-improve).
2. (suggest-improvements only) dedup vs `/tmp/open-prs-context.md`.
3. Keep 2–3 highest-value, code-cited observations.
4. Emit the workflow's output contract (write to `.planning/…` / JSON).
5. Never push, never edit source.

## Failure modes to avoid
- **Turn blowout** → over-scanning; cap investigation, deliver 2–3.
- **Generic output** → no file/symbol = useless; reject your own suggestion.
- **Wrong mechanism** → suggest-improvements writes to `.planning/ROADMAP.md`+`quick/**` (not `/gsd:capture`); pr-improve emits JSON (not prose) and never edits.
- **Pushing/editing** → both forbid it.

## Process Flow (Authoritative)
1. Investigate (budget-capped) → candidate observations.
2. (suggest-improvements) dedup vs open PRs.
3. Filter to 2–3 concrete, cited ones.
4. Emit the workflow's exact output (`.planning/…` writes / JSON).
5. Do not push.

## Output Format
- suggest-improvements: `PROPOSALS WRITTEN: <files> — <file:line> problem => change (benefit)`.
- pr-improve: the JSON above.

## Critical Constraints
- Never ship a suggestion without a file/symbol citation.
- suggest-improvements: edit only `.planning/ROADMAP.md` + `.planning/quick/**`; dedup vs `/tmp/open-prs-context.md`.
- pr-improve: JSON only, never edit/push/comment.
