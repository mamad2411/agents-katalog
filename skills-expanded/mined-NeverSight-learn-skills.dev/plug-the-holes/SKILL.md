---
name: plug-the-holes
description: Disciplined security and ship-blocker audit loop for a vibe-coded or inherited app. Walks the attack surface money-and-identity-first, demonstrates every Hole with a re-runnable exploit test before it counts, fixes, and re-verifies. Use when the user wants to find and close launch-blocking security issues - auth gaps, broken multi-tenant isolation, exposed secrets, unprotected endpoints, missing authorisation, runaway-cost endpoints - or asks "is this safe to ship / launch / put in front of customers". Run after setup-deslop and map-the-surface, before launch-gate. This is the core of the deslop pipeline.
---

# Plug The Holes

Find and close the defects that can hurt someone on launch day, and **only** those. Everything else is noted and deferred. The audit of a generated codebase drowns in theoretical worries; the discipline that saves you is one rule:

> **Demonstrate, don't assert.** A Hole is not real until you have reproduced it with an **exploit test**: a curl, a script, a failing test that makes the bad thing actually happen. No exploit test → **Suspected**, not Confirmed, and it does not block the gate.

This mirrors the feedback-loop discipline in `/diagnose`: the exploit test *is* the skill. Once you have it, the fix and the proof-of-fix are mechanical.

Prerequisites: `STACK.md` (from `/setup-deslop`, which tells you what "endpoint", "internal", and "tenant scope" mean *in this codebase*) and `SURFACE.md` (from `/map-the-surface`). Normally `/deslop` will have produced both before routing here; if you are invoking this skill directly and either is missing, stop and run `/deslop` (or just `/setup-deslop` then `/map-the-surface`) first — auditing without them means guessing the stack and the surface. Read [../deslop/GLOSSARY.md](../deslop/GLOSSARY.md); severity buckets and finding states are used verbatim.

## The order is the method

Audit in this sequence. It's **money-and-identity-first**: the categories that end companies come before the ones that merely embarrass them. Don't reorder for convenience.

1. **Secrets & credentials.** Exposed keys are the cheapest catastrophe to find and the worst to ship.
2. **Authentication.** Can you act as someone you're not?
3. **Tenant isolation.** Can tenant A touch tenant B's data? *The* SaaS Hole.
4. **Authorisation on every entry point.** Is each surface point locked to the right role, at the data layer?
5. **Public vs internal surface.** Is anything sensitive callable that shouldn't be?
6. **Input validation.** Can a malformed payload corrupt data or inject?
7. **Cost & abuse.** Can a stranger run up your bill (especially AI endpoints)?
8. **Data integrity & critical-path races.** Double-charge, double-submit, partial-write.
9. **Backups, env separation, observability.** Can you recover and see failures post-launch?

The exhaustive, stack-agnostic checks for each category live in [references/CHECKLIST.md](./references/CHECKLIST.md). **What each check means in your codebase** is in this project's `STACK.md` - read it first; it names your surface unit, your scoping seam, your secrets convention. (The thinking behind STACK.md, with worked examples for several stacks, is in `setup-deslop/references/MAPPING-PATTERN.md`.)

## The loop

Two passes. First sweep all categories into one Suspected list. Then run the exceptions checkpoint **once** against that list, so the user sees the whole picture and you don't waste exploit-test effort on things that are deliberately compensated. Then work the list finding-by-finding.

### 1. Sweep
Go through every category, in order, and hypothesise the Suspected Holes, driving off `SURFACE.md` and the matching section of `STACK.md`. Don't test anything yet. Each must be **falsifiable**: state the bad outcome concretely. *"`getInvoices` doesn't filter by the tenant key from STACK.md, so a logged-in user from org A can read org B's invoices by guessing IDs"* beats *"authorisation looks weak"*. The product of this pass is the full **Suspected** list.

### 2. Exceptions checkpoint, once, against the whole list
Present the Suspected list to the user as a numbered list and ask, for each: *is there a compensating control or intended design I should know about before I attack it?* (e.g. "that endpoint's unauthed but sits behind edge auth", "cross-tenant reads there are deliberate, it's the support console").

This is **not** an "ignore these" switch. A claimed mitigation is a claim, and claims get tested. Classify each response:

- **Verifiable compensating control** → don't drop the finding; **redirect the exploit test at the control.** "Behind edge auth" → the test becomes *a request without the edge headers must be rejected*. If the control holds, the finding is discharged as **Closed-by-control** *with the test as evidence*. If it doesn't hold, treat it as a normal Suspected Hole and proceed.
- **Intended design with no enforceable control** (e.g. a deliberate cross-tenant support console) → it becomes an **Accepted Exception**: recorded with the owner's justification and name, carried *visibly* to `/launch-gate` for explicit sign-off. It is **not** silently closed.
- **No / unsure** → audit as normal.

Capture every flagged item's control/justification now; `/launch-gate` will require an owner to stand behind each Accepted Exception. Never let a finding leave this checkpoint as "ignored" with nothing recorded.

### 3. Build the exploit test
For each remaining Suspected Hole (and each claimed control from step 2), construct the cheapest re-runnable thing that makes the bad outcome happen, or proves the control holds:
- a curl against a running dev server with a low-privilege token,
- a failing test that calls the entry point as the wrong tenant,
- a script that loops a paid endpoint unauthenticated and counts the calls that succeed,
- (for a control) the same, but asserting the control *blocks* it.

Prefer a test at the seam over manual clicking. Tag any temporary instrumentation `[DESLOP-xxxx]` so cleanup is one grep.

### 4. Run it: Confirm or discharge
- **Red** (bad thing happens) → **Confirmed Hole**. Log it (see [references/FINDING-FORMAT.md](./references/FINDING-FORMAT.md)).
- **Green** (couldn't make it happen / control held) → discharge it. Either it's safe, or your test is too weak; note which. A discharged worry is a *good* outcome: noise removed.

### 5. Fix at the right seam
Close it where it should be closed, not where it's cheapest to patch. The headline case: **scope once, at a seam.** If three entry points each forget to filter by tenant, the fix is the single shared scoping seam named in `STACK.md` that they all route through, not three copy-pasted filters. This is the point where plugging a Hole and de-slopping the architecture are the same edit. Where the right seam doesn't exist yet, that absence is itself a finding to carry into `/improve-codebase-architecture`.

### 6. Re-verify, then Close
Re-run the **exact** exploit test. It must now be green. Only then is the finding **Closed**. A fix you didn't watch turn green is a hope, not a fix.

### 7. Triage the rest
Anything you find that isn't a Hole goes to its bucket and **does not stop the audit**:
- **Hardening** → post-gate list.
- **Improvement** → hand to `/improve-codebase-architecture`.
- **Latent bug / race that isn't a launch-day Hole** → hand to `/diagnose`, parked.

Don't fix Improvements mid-audit. That's how the holes phase expands forever.

## Output

A findings log (format in [references/FINDING-FORMAT.md](./references/FINDING-FORMAT.md)) with every item in a bucket and a state. When every Confirmed Hole is Closed, you're ready for `/launch-gate`. Leave the `[DESLOP-xxxx]` instrumentation grep'd out and any throwaway exploit scripts in a clearly-marked `.deslop/exploits/` dir; they're your regression suite for the next audit, not litter.
