---
name: keiko-retro
description: Post-merge retrospective for a Keiko epic (or a notable standalone issue). Gathers the FULL GitHub evidence trail — the epic issue + every child issue + every child PR + the epic PR, with all their comments/reviews, the audit findings, and the human-fix delta (what a human changed by hand after review) — plus whatever survived in chat, then distills durable process/workflow learnings into agent memory and lints + reconciles the memory. Use after the work has merged into dev. Takes an epic link / issue # / PR #.
---

# keiko-retro

Run this **after** an epic (or a notable standalone issue) has **merged into `dev`** —
i.e. after authorized merge and any human review/hand-fixes. It is a single
human-triggered pass:
**gather → reflect → distill → lint → reconcile.** **Defers to**
`docs/workflow-contract.md`; writes only durable learnings, never secrets or raw
evidence bodies (counts / summaries / redacted only).

**Input:** an epic link, issue number, or PR number — paste whatever is in front of
you and resolve the rest with `gh`. It is optional: if omitted, infer the unit from
the current branch or the chat, but **the link is preferred post-merge** (the branch
is usually deleted and this may be a fresh session).

## 0. Select the product profile (before gathering)

Select against the target checkout using [profile selection](../../../profiles/README.md).
State the profile on the first output line; explicit operator selection wins.
Load only the selected profile and its task-relevant authority docs, including the
target's `AGENTS.md` and `CONTEXT.md` when present. Take readiness, verification,
templates, evidence, exclusions, and merge authority from it; ambiguity requires
clarification. The accepted target contract governs product requirements.

Propose workflow changes without implicitly editing target authority (`AGENTS.md`,
`CONTEXT.md`, ADRs, templates, or gates). In Native, never copy/request the private
Fachkonzept or raw private-source content; report summaries/redacted learnings only.

## Mode: post-merge (default) vs interrupted / pre-merge

Default assumes the unit **merged into `dev`** (human-fix delta + closure evidence exist). If the epic/issue was **interrupted or is pre-merge** — no `epic → dev` merge yet (abandoned, escalated, or retro'd early) — run the same pass but **record human-fix delta and closure evidence as `unavailable (not merged)`** instead of inferring or fabricating them. Reflect on the evidence that _does_ exist (plan vs reality, audit/CI findings, workflow friction, why it stalled). **State the mode explicitly** in the final report.

## 1. Gather the full evidence trail

Do **not** reflect on the chat alone — it is compaction-lossy. Assemble the complete
durable record for the epic `#E` via `gh` (summarize each item as you go to stay in
budget; you want the signal, not full dumps):

- **Epic issue `#E`** — body, **all comments**, labels, project fields, closure evidence.
- **Epic PR (`epic/… -> dev`)** — body, **all review comments + threads**, the CI check
  history (how many repair attempts), and the **human-fix commits**: the diff between
  the Ready-for-Human-Review HEAD the agent handed off and what actually merged. This
  delta is the single sharpest signal.
- **Every child issue** (sub-issues of `#E`) — body + comments + closure evidence.
- **Every child PR (`issue/… -> epic`)** — body, **review comments**, audit findings, commits.
- **Audit trail** — confirmed findings across the children; recurring ones matter most.
- **Surviving chat context** — whatever is still in this session; supplementary, not primary.

For a standalone issue, gather its issue + PR + comments + review + human-fix delta.

## 2. Reflect (process-first — never a status restatement)

Weight the reflection toward what closure evidence and per-agent memory **cannot** see:

- **Human-fix delta** — what did the human change by hand after review? Each hand-fix
  marks a place the agent/workflow fell short. This is the primary lens.
- **Recurring audit/CI findings** — the same class of issue across children = a systemic gap.
- **Plan vs reality** — where did the grill/epic plan mis-scope, mis-order, or miss a dependency?
- **Workflow friction** — token-overflow points, repeated CI repairs, gate false pos/neg.

Do **not** write "built X, tests passed" — that is already on the PR. Capture only what
would change how the next epic runs.

Before proposing a new guardrail, inspect existing lint rules, tests, hooks, and
CI gates: is the needed check absent, broken, or present but unwired? For recurring
**mechanical** failures, propose the smallest deterministic check or repair with a
concrete failing example and its enforcement point. For **judgment** failures,
propose concise guidance with a trigger and rationale. Prefer repairing an existing
check over duplicating it. Record evidence, expected benefit, and false-positive
risk; keep workflow/target-authority changes as proposals until authorized.

## 3. Distill → memory (durable, sharp, budgeted)

- **Process/workflow learnings** (cross-role) → `.agents/memory/_shared/` — one tight
  entry per real lesson.
- **Codebase gotchas** (role-specific) → the relevant `.agents/memory/<role>/MEMORY.md`.
- Respect the 25 KB/file budget; a lesson that is not generalizable or recurring does
  not get written. Better to write nothing than noise.
- **Proposed harness changes** (a skill / gate / agent-def that should change) →
  **report to the human, do NOT auto-edit the workflow.** Human-control invariant.

## 4. Lint + reconcile (memory hygiene)

After writing, lint the affected memory (the new entry may have superseded an old claim):

- **Contradictions** between entries (including new vs old).
- **Stale refs** — files, gate scripts, or flags named in memory that no longer exist in
  the repo (grep against current `scripts/` and skills).
- **Orphans** — memory files with no inbound `[[links]]` or missing from the index.
- **Index drift** — index one-liners that disagree with the file they point to.
- **Budget** — files over 25 KB (`.keiko-scripts/consolidate-memory` covers the size dimension).

Reconcile what is safe (keep the current claim, drop the stale one, fix index/links);
**surface anything ambiguous for the human** rather than guessing which claim is current.

## Final report

Epic/issue reflected · sources gathered (counts) · human-fix delta summary · durable
learnings written (+ where) · proposed harness changes (for the human) · lint findings + reconciliations · residual questions.
