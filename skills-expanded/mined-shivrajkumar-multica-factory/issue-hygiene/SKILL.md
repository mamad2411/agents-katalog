---
name: issue-hygiene
description: The discipline of keeping issues legible — every status change gets a reasoned comment and the right metadata, blocks state what is needed and from whom, metadata keys are correct, and the comment trail tells the full story. Attach to every agent; apply on every issue interaction.
---

# Issue Hygiene

Attached to every agent. The board is the shared memory of the whole team — humans and agents both read it to know what happened and why. An issue whose history you cannot reconstruct from its comments is a failure of hygiene, regardless of whether the code was good.

## Every status change gets a comment saying why

Never move an issue between statuses silently. Each transition gets a comment that says what you did and why the issue is now where it is. A reader scanning the timeline should understand the journey without opening the PR or asking you.

- Moving to `In Review` (set `phase=code-review`): "Implemented on branch `feat/referral-email`, PR #124 opened. Moving to In Review."
- Handing off to QA (stays in `In Review`, set `phase=qa`): "pr-reviewer-backend and security-reviewer approved (#124). Moving to QA."
- Routing to architecture (gate check on a plausibly architectural change → `In Progress`, `phase=architecture`): use the exact gate-check text from the `human-approval-gate` skill. Routine changes are self-triaged (`no_adr_needed`), not routed.

## Phase-boundary discipline (metadata moves with the status)

Multica has only seven statuses, so the precise pipeline stage lives in the **`phase`** metadata key (`product-definition` / `architecture` / `development` / `code-review` / `qa`). When you change status across a pipeline boundary, **set the `phase` key in the same action** and say why in the comment. A status without the matching `phase` leaves the board ambiguous — several stages share a status (`In Progress` covers product-definition, architecture, and development; `In Review` covers code-review and qa).

## `Blocked` always states what is needed and from whom

An ordinary block (not the human-approval gate) carries metadata **`blocked_reason="<what/who>"`** — this is what distinguishes it from a gate block, which carries the `gate` key instead. `Blocked` without a `blocked_reason` is useless. Every ordinary move to `Blocked` names:

1. **What** is needed (the specific decision, artifact, access, or fix).
2. **From whom** (a named human, team, or upstream issue).
3. Ideally, what unblocks it — the condition under which it can move again.

Example: set `blocked_reason="sandbox creds from platform team before checkout QA"` and comment "Blocked: need the payment provider's sandbox credentials from the platform team (@…) before checkout QA can run. Unblocks when creds are in the shared vault." A `Blocked` issue carrying `gate=human-approval` is a different thing entirely — it is the frozen human-approval gate; leave it alone unless a member-authored `APPROVED:` comment is on record (see the `human-approval-gate` skill).

## Link everything

An issue should connect to its context. Link:

- The **PR(s)** implementing it (and PRs link back to the issue).
- The **ADR** comment or approval that gated it.
- **Related / parent / child** issues, and any **bug** issues filed against it.
- External artifacts the work depends on.

Broken or missing links force the next reader to re-discover context you already had.

## Correct metadata

Multica has no labels — routing, reporting, and audits run off **metadata keys**. Keep them accurate:

- **Stack routing** (`stack` key, drives assignment): `frontend-react`, `frontend-nextjs`, `mobile-react-native`, `shopify`, `backend-nestjs`, `backend-express`, `database-mongodb`, `database-postgres`, `devops`.
- **Work type** (`type` key): `feature`, `bug`, `tech-debt`, `spike`, `hotfix`, `performance`, `incident`, `docs`, `audit-finding`.
- **Gate & process**: `needs_adr=true`, `adr_approved=<name>` (set by an agent as bookkeeping from a member-authored `APPROVED:` comment — never self-approve), `no_adr_needed="<justification>"`, `gate=human-approval`, `gate_violation=true`, `promote_to_skill=true`, `phase=<stage>`, `blocked_reason="<what/who>"`.
- **Priority** (bugs & findings, replaces severity): `urgent`, `high`, `low` (`medium` is the default for ordinary planned work).

Clear metadata that no longer applies. Never set `adr_approved` from your own judgment — only record it from a member-authored `APPROVED:` comment (see the `human-approval-gate` skill).

## The comment trail must tell the full story

By the time an issue reaches `Done`, its comments should read as a coherent narrative:

> **PRD** (`phase=product-definition`) → **ADR + human approval** (or `no_adr_needed`) → **PR(s)** with review outcomes → **QA evidence** against each acceptance criterion → moved to Done.

This ordering is also the Definition of Done. If a stage happened but left no trace, add the trace before advancing.

## Write for the next cold start

Multica never carries session memory between separate pickups of an issue (only a same-trigger crash-retry resumes; a new mention/assignment always starts blank). Before ending a turn mid-investigation, write what you found — root cause location, files touched, decisions made, what's left — as a comment or metadata, not just "in progress." The next dispatch should read your note and skip straight past re-deriving it, not re-explore from zero.

## Never claim a limitation you haven't tested

If you're about to write "unavailable," "not configured," "no access," "not possible in this environment," or anything similar as the reason you skipped a real check (running a test suite, hitting a local server, calling a tool, reaching a credential) — stop. That is a factual claim, and reporting an untested assumption as fact is a fabrication, not an efficient shortcut: it reads as "I did less work" disguised as "the work couldn't be done." Actually attempt the thing first and capture the real error. If it genuinely fails, quote the exact error in your comment and say what you need to unblock it — that's a legitimate `Blocked`. If you never tried, you don't get to claim it doesn't work. This applies whether the fallback you took instead (a lint pass instead of running the app, a guess instead of a lookup) looks reasonable on its own — the problem isn't the fallback, it's reporting it as forced rather than chosen.

## Standing rules

- **Never work an issue assigned to someone else.** If you believe you should own it, comment and let a human reassign — don't just take it.
- **Keep titles descriptive.** "Fix bug" tells no one anything; "Checkout crashes when discount code is empty" does. Rename vague titles when you touch the issue.
- **Do the gate check first.** Before any work, confirm the issue is not frozen (`gate=human-approval`) and carries `adr_approved` or `no_adr_needed` per the `human-approval-gate` skill.
- **One issue, one concern.** If an issue has quietly grown a second unrelated problem, split it and link them.
- **Mention the specific agent, not the squad, when you already know who should own the work.** Mentioning a squad instead of a named agent enqueues the squad leader purely to read the request and re-delegate to the same agent you could have named — a real extra task, cost, and latency for zero decision actually made. Mention the squad only when you genuinely don't know who should pick it up.
