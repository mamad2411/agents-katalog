---
name: launch-gate
description: Define and enforce the explicit, written "safe to ship" line for an app, then make the ship / no-ship call. Verifies every Confirmed Hole is Closed, confirms launch-readiness essentials (backups, rollback, error tracking), and deliberately refuses to let hardening or polish block the launch. Use at the end of the plug-the-holes phase, when the user asks "are we ready to launch / is it safe to ship / what's left before go-live", or whenever a security/deslop pass needs a clear go/no-go decision. Consumes FINDINGS.md and SURFACE.md.
---

# Launch Gate

Draw the line, then hold it. The gate exists to answer one question honestly: *is this safe to put in front of customers?* It stops two opposite failure modes: shipping with a Hole open, and never shipping because there's always one more thing to polish.

> **The gate is a line, not a wish.** It is written down, per app, before the final check. Everything above it must be true to ship. Nothing below it may move it.

Read [../deslop/GLOSSARY.md](../deslop/GLOSSARY.md). Consumes `FINDINGS.md` (from `/plug-the-holes`) and `SURFACE.md` (from `/map-the-surface`).

## Process

### 1. Write the gate, *before* the final check
Create `GATE.md` for the app. The criteria are deliberately a closed list. If it's not on here, it does not block launch. Default criteria:

```markdown
# GATE - <app name>   ·   target launch: <date>

## Must be TRUE to ship (the line)
- [ ] Every Confirmed Hole in FINDINGS.md is Closed or Closed-by-control (re-verified green). Count: __ / __
- [ ] Every Accepted Exception is signed off below (owner + justification). Unsigned exception = NO-SHIP.
- [ ] SURFACE.md "Unknowns" section is empty (nothing unaudited).
- [ ] Secrets: nothing exposed in repo/history/bundle; anything ever exposed is rotated.
- [ ] Tenant isolation proven on every tenant-data path (not assumed).
- [ ] Paid/AI endpoints are authed AND rate-limited/capped.
- [ ] Database backups exist and a restore has been tested once.
- [ ] A bad deploy can be rolled back.
- [ ] Error tracking is live; money/identity paths have structured logs.

## Accepted exceptions (carried risk, eyes open)
<one line per Accepted Exception: finding ID · what it is · why it's accepted · compensating control if any · OWNER who signed off>
<empty is the healthy default; every line here is a risk you are choosing to ship with>

## Explicitly NOT blocking (parked, fix after launch)
- Hardening list (HD-*): <count>
- Improvement list (IM-*): <count> → /improve-codebase-architecture
- Parked bugs/races: <count> → /diagnose
```

Tune the list per app, but tune it *now*, deliberately, not item-by-item under pressure later. Adding a criterion mid-launch "just to be safe" is gold-plating wearing a hard hat.

### 2. Verify by re-running, not re-reading
For each "must be true" item, **confirm by running, not by trusting the log.** For Holes: re-run the exploit tests in `.deslop/exploits/` and watch them go green, including the *control* tests behind any Closed-by-control finding. A findings log that *says* Closed is evidence. A green exploit test is proof. They can disagree (a later edit reopened something); trust the test.

**Accepted Exceptions are not a quiet bypass.** Each one needs a named owner and a written justification in the gate doc. An exception with no owner, or one you (the auditor) would not put your own name to, is treated as an open Hole: NO-SHIP. The point of the bucket is to make carried risk *visible and owned*, never to make it disappear.

If anything is red or unknown, the gate is **NO-SHIP**. Name the exact failing item. Don't soften it.

### 3. Make the call
- **All true → SHIP.** Say so plainly. Parked Hardening/Improvement work does not reduce confidence in the ship decision; that's the whole point of the buckets. Hand the parked lists to Phase 2.
- **Any false → NO-SHIP.** State the single blocking line (or the few). Route each back: open Hole → `/plug-the-holes`; missing backup/rollback/tracking → it's a launch task, not a deferral. Give the shortest path to green, not a lecture.

### 4. Resist the drift
Two pressures will try to move the line, both wrong:
- *"While we're here, let's also fix…"* No. That's Phase 2. Log it, ship, come back.
- *"It's basically fine, we'll sort the auth thing after launch."* No. An open Hole is the one thing the line will not bend for. "After launch" for a tenant-isolation Hole means "after the breach".

The gate's authority comes from being boring and fixed.

## After the gate
Shipping on an ugly-but-safe app is success. Phase 2 (`/improve-codebase-architecture`, `/diagnose`, `/tdd`) now runs *incrementally, in production, without a gate*, because none of it can hurt a customer on day one.
