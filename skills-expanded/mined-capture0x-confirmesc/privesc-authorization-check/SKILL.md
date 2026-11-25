---
name: privesc-authorization-check
description: Confirm you are authorized before running any privilege-escalation check or exploitation step. Load this first, before confirmesc-triage or any technique skill.
---

# Authorization check

Privilege-escalation testing against a system you do not own or have no written
permission to assess can be illegal. Run this gate before anything else.

## Checklist

Before scanning or exploiting, confirm all of the following:

1. **Scope.** The target host (and its IP / hostname) is explicitly in scope.
2. **Permission.** One of: it is your own system, it is a CTF or lab you are
   meant to solve, or you have signed written authorization for an engagement.
3. **Limits.** You know what is allowed: passive scan only, active probes, or
   full exploitation. `--poc` and any technique skill are exploitation.
4. **Impact.** Kernel PoCs can crash the host; some techniques write to disk.
   Confirm a maintenance window or sandbox where that matters.

## If any item is unknown

Stop. Do not scan, do not run `--poc`, and do not apply a technique skill. Ask
for clarification of scope and permission first.

## Passing the gate

Only when all four items are satisfied, proceed to `confirmesc-triage` and the
matching technique skills. Keep actions reversible and clean up afterwards (see
`post-exploitation-notes`).
