---
name: superforge
description: >
  Use when starting a substantial product or feature phase, choosing the next
  specialist across strategy, design, engineering, verification, security, or
  release. Skip bounded follow-up edits.
license: MIT
metadata:
  author: Takao Umehara
  version: "5.1"
compatibility: Standalone. Uses installed superforge-* skills when available.
---

# Superforge — Thin Phase Router

Choose the smallest safe route. Load details only when their condition is true; the router is not a work phase.

## 1. Continue before restarting

If the request is a bounded follow-up to work already underway, **continue the active phase**.
Preserve its constraints and do not repeat intake, routing,
settings, or artifacts. Restart only when the goal changes, a new specialty is
needed, or the user enters a verification or release gate.

| Entry | Use for | Action |
|---|---|---|
| `/superforge quick` | Bounded correction | Handle inline under the active constraints |
| `/superforge build` | New feature or meaningful change | Size, route, implement, verify |
| `/superforge ship` | Public release or paid launch | Run verify, then ship |
| `/superforge` | No mode supplied | Infer the smallest matching entry |

## 2. Size the work

| Size | Observable scope | Default |
|---|---|---|
| **Small** | One issue, normally 1–3 files, no architecture/release decision | Inline: **no specialist, no intake, no new docs, and no run log** |
| **Medium** | One domain, several related files, one clear outcome | Use exactly one primary specialist |
| **Large** | New product/feature, cross-domain change, migration, or release | Plan phases; use one specialist at a time; verify at the end |

When uncertain, choose the smaller route until evidence requires promotion.

## 3. Pick the primary specialist

| Need | Route |
|---|---|
| Idea is unclear | `superforge-brain` |
| Market, pricing, acquisition, viability | `superforge-biz` |
| Brand, voice, identity, generated media | `superforge-brand` |
| Cinematic scroll or video-scrub world | `superforge-scroll` |
| Interface or product UX | `superforge-ui` |
| Multi-component implementation | `superforge-dev` |
| Test strategy or TDD | `superforge-test` |
| Bug, incident, or root cause | `superforge-debug` |
| Accessibility | `superforge-a11y` |
| Critical critique | `superforge-roast` |
| Functional proof | `superforge-verify` |
| Security review or exposed secret | `superforge-secure` |
| Release readiness, legal/ops checks | `superforge-ship` |
| Hand off to another tool, model, or async agent | `superforge-handoff` |

Treat the desired outcome as sufficient input; do not require a specialist or technology name. Announce the entry, size, and current route in one line, then work. Ask about the route only
when two materially different goals remain plausible.

## 4. Enforce the skill budget

- Use **one primary specialist at a time**. A later verify/ship gate is a new
  phase, not another simultaneous craft skill.
- Treat overlapping UI/design skills as alternatives. `superforge-ui` owns the
  integrated path; add another only when the user explicitly requests it.
- If the selected specialist is unavailable, work inline; do not stop to install it.
- Small work stays inline: **load no specialist file**; dispatch no agent just to change models.
- Before any actual agent dispatch, read `references/model-prompting.md` and
  show the assignment. Otherwise do not load that reference.
- After choosing a primary specialist, read `references/wiring.md` only if a
  deeper installed skill is genuinely required.

## 5. Keep only durable state

If `docs/superforge.md` exists, read its current constraints; if not, a Medium or Large phase first
reads `references/setup.md`. Keep **current state, never chronological history**; archive superseded claims.
Create or update an artifact only for a Large decision, handoff, release, or a
Medium decision that must survive a new session. Read `references/artifacts.md`
only then.

Append `docs/superforge-log.md` only after a **correction, failure, retry, or release**:
the user repeated/reversed an instruction, execution failed/retried, or a release verdict was issued.
An ordinary request to correct the product is not a log trigger. Read `references/run-log.md` only after a trigger.

## 6. Gates and stop conditions

- Before claiming completion, require **fresh verification evidence**. Use
  `superforge-verify` for a Large phase or consequential Medium phase.
- `/superforge ship` always sequences `superforge-verify` → `superforge-ship`.
- Commit and push at each verified checkpoint, per the branch policy; unpushed work is lost when usage runs out.
- Stop for irreversible loss, spending money, missing credentials, a security
  or privacy boundary, or a choice that changes the goal. Otherwise choose a
  defensible default, record it only if durable, and continue.
- For a new or ambiguous Large phase, read `references/intake.md`. For help,
  read `references/help.md`. For version-dependent claims, check `SOURCES.md`
  before relying on them.
