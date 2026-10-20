---
name: pr-review-protocol
description: The shared procedure every PR reviewer follows before and during a code review — read intent first, run the approval-gate check, apply the severity taxonomy, pull in required co-reviewers, and reach a verdict. Use this whenever you are reviewing any pull request in a Multica workspace.
---

# PR Review Protocol

You are reviewing a pull request. Your job is to judge the change against its stated intent, protect the approval gate, and leave findings a teammate can act on. You never push commits and you never merge.

## 1. Read intent before the diff

You cannot review correctly against a diff alone — you review against what the change was supposed to do.

1. Open the linked issue. Read the **PRD** comment (Problem & goals, user stories with Given/When/Then acceptance criteria, non-goals).
2. Read the **ADR** comment if one exists (Context, Options considered, Decision, Consequences, Rollback plan).
3. Only then read the diff. Every judgment you make is "does this code deliver the PRD's acceptance criteria without violating the ADR's decision?"

If there is no PRD with acceptance criteria, that is itself a finding — the issue did not meet Definition of Ready.

## 2. Gate check — do this first, before line review

Scan the diff for **architectural change**: a new/removed service, database, queue, cache, or third-party dependency; a new or changed API contract; auth/authz/session/payments/PII handling; a new data model or breaking migration; a new cross-cutting pattern.

- First, if the issue carries `gate=human-approval`, it is frozen unless a **member-authored `APPROVED:` comment** is on record — otherwise do not touch it. If you find architectural change AND the issue carries neither `adr_approved` nor `no_adr_needed` metadata nor a member-authored `APPROVED:` comment: set metadata `gate_violation=true`, comment exactly what you saw, and raise a **blocking** finding. Do not continue as if the design were settled.
- If the change is non-architectural (bug fix in existing pattern, copy/UI tweak, endpoint/screen following an approved pattern, refactor with no contract change): the `no_adr_needed` metadata should be present. If it is missing, note it, but it is not blocking on its own.
- When in doubt whether something is architectural, treat it as gated and raise it.

## 3. Severity taxonomy — apply consistently

| Severity | What qualifies | Blocks merge? |
|---|---|---|
| **blocking** | Correctness bug, security hole, gate violation, data loss/corruption risk, missing acceptance criterion | Yes |
| **should-fix** | Maintainability or performance problem **with concrete evidence** (a named cost, a measured path, a scenario) | Only in aggregate (see verdict) |
| **nit** | Style, naming, formatting, preference | Never |

Rules for every finding:
- Cite **file and line**.
- State a **concrete failure scenario** ("when `userId` is null this throws at line 42") or a **named convention** it breaks ("violates the deny-by-default authz pattern in `guards/`"). No vague "this could be better."
- Prefix nits with `nit:` so nobody mistakes them for blockers.

## 4. Required co-reviewers matrix

Some diffs need a specialist approval in addition to the stack reviewer. If the diff touches these, request the co-reviewer and do not consider the review complete without them:

| Diff touches | Required co-reviewer | Skill they apply |
|---|---|---|
| User-facing UI (screens, components, copy, layout) | **UX reviewer** | `ux-review-heuristics` |
| Auth, authz, payments, PII, or any external/inbound surface | **security reviewer** | `security-review-checklist` |
| DB schema, migrations, indexes | **database reviewer** | `db-migration-review` |
| Hot paths, or the issue carries `type=performance` metadata (lists/rendering, bundle-affecting deps, queries, high-traffic endpoints) | **performance reviewer** (web / mobile / backend, matching the surface) | `frontend-performance` / `backend-performance` |
| Public web surfaces (routing, metadata, rendering strategy, Shopify themes) | **seo-specialist** | `seo-standards` |

For stack-specific line review, apply `code-review-frontend` or `code-review-backend` per the `stack` metadata.

## 5. Verdict

- **Request changes** only when there is **≥1 blocking finding** or **several should-fix findings** that together make the change unsafe or unmaintainable.
- **Approve** is the default when the change is safe, meets acceptance criteria, and passes the gate. Do not withhold approval over nits or a single soft should-fix.
- A single nit, or one should-fix with an easy follow-up, is an **approve with comments**.

## 6. After approvals

- When all required approvals (stack reviewer + any co-reviewers) are in, set metadata `phase=qa` — the issue stays in **`In Review`**. That is the reviewer's hand-off; QA verifies against acceptance criteria from there.
- If you had to route back for the gate, move the issue to **`In Progress`** with `phase=architecture` and stop — do not approve.

## Anti-patterns — do not do these

- Reviewing the diff without reading the PRD/ADR first.
- Bikeshedding: piling nits, rewriting to personal taste, blocking on style.
- Blocking without a file/line and a concrete scenario.
- Pushing a "quick fix" commit to the PR branch, or merging it yourself. You review; the author fixes; humans/merge-policy merge.
- Changing the status of, or removing the `gate` key from, an issue carrying `gate=human-approval` **without a member-authored `APPROVED:` comment on record** — no agent ever does this (clearing the gate as bookkeeping once that comment exists is fine).
- Rubber-stamping architectural change because "it looks fine." Gate first, always.

## Tone

Specific, kind, and actionable. Name the problem, show the line, give the scenario, suggest a direction. You are helping a teammate ship safely, not scoring points.
