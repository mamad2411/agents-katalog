---
name: release-readiness
description: The final gate before any launch, major release, or "is this production-ready?" question — orchestrates all engineering-discipline skills into one go/no-go review. Use when the user says "ready to launch", "production ready", "go live checklist", "release", "ship it", "pre-launch review", or before delivering a milestone to real users/clients.
---

# Release Readiness

"Done" and "ready for real users" are different claims. This skill is the go/no-go gate: a structured sweep that turns "I think it's ready" into a checked list with evidence. Run it before first launch, before major releases, and before handing anything to a paying client.

## How to run it

Work through the seven gates below **against evidence, not memory** — for each item, the answer is a command output, a file path, a screenshot, or a tested behavior, never "yes, I'm pretty sure". Produce a written verdict at the end: ✅ ready / ⚠️ ready-with-known-risks (listed, accepted by the user) / ❌ blocked (by what). Deep-dive any failing gate with its dedicated skill (threat-model-security, deployment-safety, observability-readiness, etc.).

## Gate 1 — Correctness of the money-and-data core
- [ ] Golden paths run end-to-end in a production-like environment, by hand, today — not "tests passed last week".
- [ ] Money math spot-checked against a calculator: one real invoice with discounts/tax/rounding, one payment, one return.
- [ ] Concurrent/duplicate actions tried: double-click submit, retry after timeout, two tabs. No dupes, no corruption.
- [ ] Test suite green from clean checkout; the regression tests for every previously found bug still exist and pass.

## Gate 2 — Security minimum (threat-model-security)
- [ ] The IDOR test performed live: user A's token requesting user B's objects on every resource type → refused.
- [ ] Auth rate-limiting/lockout demonstrated, not assumed. Sessions revocable.
- [ ] Secrets audit: none in git history/client bundle/logs; prod secrets differ from dev; HTTPS enforced.
- [ ] Error responses leak nothing internal (trigger a 500 deliberately and look).

## Gate 3 — Data safety (database-design)
- [ ] Backups: running, automatic, AND restored once successfully into a scratch environment — an untested backup is a hope, not a backup.
- [ ] Destructive operations inventoried: what can permanently delete/overwrite data, and what protects each (confirm, soft-delete, audit row)?
- [ ] The DB enforces its own invariants: spot-check that constraints exist in the live schema (not just in models).

## Gate 4 — Deploy & undo (deployment-safety)
- [ ] Deployed-commit fingerprint verifiable in prod; deploy procedure documented and boring.
- [ ] Rollback rehearsed once for real. Migration pipeline handles "old code + new schema" coexistence.
- [ ] Config parity checked: every env var the code reads exists in prod; boot fails loudly if not.

## Gate 5 — Eyes on production (observability-readiness)
- [ ] Error tracker capturing (send a test event), uptime check external, the three day-one alerts wired (down / error spike / queue age).
- [ ] One request traced end-to-end through logs by correlation ID, as a drill.
- [ ] The 4 incident questions answerable from tooling alone.

## Gate 6 — Product finish (product-ux-quality)
- [ ] Five States sweep: pick every major screen; force loading/empty/error/overflow on each.
- [ ] Full run-through on a real phone, once on throttled network.
- [ ] A stranger (or the client) completed the golden path without you talking. Their confusion list is your bug list.

## Gate 7 — Operations & the human stuff
- [ ] Support reality: when a user hits a problem, they can reach someone, and that someone can look them up (admin view/queries ready).
- [ ] Legal/compliance basics for the market: privacy policy, terms, data-deletion capability, tax correctness reviewed by someone qualified if money is involved.
- [ ] The bus-factor doc exists: how to deploy, where prod runs, where secrets live, how to restore — findable by someone who isn't you.
- [ ] Load sanity: golden path load-tested at 2–3× realistic peak (performance-improvement); connection-pool math checked.

## The honesty rules

- Skipping a gate is sometimes right (an internal beta doesn't need Gate 7's legal pass) — but skipping is a **decision the user makes**, recorded in the verdict, never a silent omission.
- Anything found-but-not-fixed goes on a known-issues list in the verdict. A known risk accepted beats an unknown risk shipped.
- Re-run the failed gates after fixes; don't extrapolate green from "I fixed what it found".
