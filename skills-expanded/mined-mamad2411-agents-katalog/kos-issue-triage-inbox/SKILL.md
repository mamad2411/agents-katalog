---
name: kos-issue-triage-inbox
description: Triage and catch-up issues per the prompts — triage (classify, exactly-one priority label, dedup, triaged label, summary) and issue-catch-up (6-phase act-on-categorized-issues with DRY-RUN/RATE-LIMITED modes).
user-invocable: true
when_to_use: "When the triage workflow handles a new issue, or the issue-catch-up workflow runs its 6-phase sweep on categorized orphaned/stale issues."
category: utilities
argument-hint: "[issue-number or 'orphans']"
keywords: [triage, inbox, issue-catch-up, phases, dry-run, rate-limited, priority-label, triaged]
related: [kos-zai-agent-runtime-contract, kos-gh-automation-tooling, kos-zai-run-failure-prevention, kos-claude-turn-budget]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from triage.yml (/gsd:inbox) + issue-catch-up.yml (6-phase) prompts
  license: repo
  version: "1.1"
---

# Idea

Two workflows share issue-handling with **different** contracts:
- **triage** (`/gsd:inbox`) — TRIAGE-ONLY on one new issue: classify, set **exactly one** priority label, dedup, add `triaged`, post the summary. Do NOT fix/read source/suggest code/create PRs.
- **issue-catch-up** — act on **categorized** orphaned/stale issues across **6 phases**, honoring **DRY-RUN** and **RATE-LIMITED** modes, with exact `gh` commands per phase.

Both execute `gh issue …` mutations (these workflows permit it). Neither fixes code.

## When to invoke this skill directly
- triage: a new issue needs classifying + labeling.
- issue-catch-up: the scheduled sweep runs on categorized issues.

## References
- `triage.yml` prompt (exactly-one priority label; serious → `high`; dep-vuln `fixAvailable:false` → also `backlog`; `triaged` via `edit-issue-labels.sh`; read-only via `gh.sh`; duplicate → comment + `duplicate` + close; exact summary format).
- `issue-catch-up.yml` prompt (6 phases; DRY-RUN; RATE-LIMITED → only Phase 1 + 3).
- `./.github/workflows/scripts/edit-issue-labels.sh`, `./.github/workflows/scripts/gh.sh`.
- [[kos-zai-agent-runtime-contract]].

## Communication Style
triage: one action + the labels you applied. catch-up: per-phase actions + sweep totals.

## triage contract (enforce)
1. Classify bug/feature/question; assess priority critical/high/medium/low.
2. Apply **EXACTLY ONE** priority label (serious/high-severity, e.g. CVSS High → `high`). For a dep-vulnerability with advisory `fixAvailable:false`, **also** add `backlog`.
3. Check duplicates via `gh.sh search issues`.
4. Add `triaged` via `./.github/workflows/scripts/edit-issue-labels.sh --add-label "triaged"`. Apply other labels via `edit-issue-labels.sh`.
5. If duplicate: comment "Duplicate of #N. Closing." → add `duplicate` → `gh issue close … --reason "not planned"`.
6. Post summary comment in the prompt's exact format (only list labels YOU added).
- **Do NOT** fix, read source, suggest code changes, or create PRs. STOP after labels + summary.

## issue-catch-up contract (enforce)
Modes: **DRY-RUN** (`true` → prefix every action "DRY RUN:", do NOT execute `gh issue close/create/edit/comment` — write what would happen); **RATE-LIMITED** (`true` → only Phase 1 + Phase 3; skip others).
- **Phase 1 — Close Stale** (`should_close_dupe` with `duplicate_of` → comment+`duplicate`+close; else `should_close_canceled` → close).
- **Phase 2 — Re-trigger Triage & Dead Letters** (`triage_dead_letter` → `needs-review` + comment; `needs_retriage` → `/triage` + re-triage comment).
- **Phase 3 — Priority Escalation** (`priority_escalation` → attention comment).
- **Phase 4 — Orphaned Fixed Reminders** (`orphaned_fixed` → close-or-remove-label reminder).
- **Phase 5 — Smart Grouping** (only if `groupable_candidates` ≥3: group by classification/priority/root-cause/symptoms; create canonical `[GROUPED]` issue; label originals `duplicate` + close).
- **Phase 6 — Route Manual Fix Triage & Dead Letters** (`fix_dead_letter` → `needs-review`; `triaged_no_fix`, max 5 → guard then `needs-review` + manual-fix comment).

## Failure modes to avoid
- **triage fixing/reading code** — forbidden; triage-only.
- **Multiple priority labels** — exactly one (plus `backlog` only for fixAvailable:false dep-vulns).
- **catch-up ignoring modes** — DRY-RUN must not execute `gh`; RATE-LIMITED must skip to Phase 1+3.
- **Acting on fresh issues in catch-up** — act only on the categorized set provided.

## Process Flow (Authoritative)
- triage: classify → one priority label (+`backlog` if fixAvailable:false) → dedup → `triaged` → (duplicate? close) → summary. Stop.
- catch-up: read modes → execute the applicable phases with exact `gh` commands → sweep totals.

## Output Format
- triage: `ISSUE #<n>: <classification> priority=<label> triaged; duplicates=<none|#n>; summary posted`.
- catch-up: `SWEEP (dry-run=<bool> rate-limited=<bool>): phase-by-phase actions + totals`.

## Critical Constraints
- triage: exactly one priority label; never fix/read source/create PRs.
- catch-up: honor DRY-RUN (no `gh` exec) and RATE-LIMITED (Phase 1+3 only) modes; act only on categorized issues.
- Use `edit-issue-labels.sh` / `gh.sh` as the prompt specifies.
