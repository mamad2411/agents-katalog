---
name: msp-maintenance
description: >
  Use this skill for your MSP's proactive, recurring operations: patching and update
  cycles, maintenance windows, backup monitoring and test restores, monitoring and alert
  triage, the on-call rotation, change management for risky changes, documentation currency,
  and vendor or license renewals. Trigger on "patch window", "maintenance window", "did the
  backups run", "test restore", "alert storm", "who is on call", "can we make this change",
  "update the firewall", or any question about the recurring delivery work between tickets.
  msp-helpdesk owns the reactive desk (tickets, priorities, response targets); this skill owns
  the scheduled work that prevents tickets. Apply alongside msp-client-comms (maintenance
  notices), msp-qbr (the scorecard rows this work feeds), msp-metrics (SLA and ticket data),
  msp-legal (the negligence carveout that makes these logs matter), msp-pricing
  (after-hours multipliers for emergency work), and msp-security (the standard this
  work delivers against).
---

# {{COMPANY_NAME}} Proactive Maintenance Operations

> **Defaults you must review.** The specific numbers in this skill are shipped example defaults
> from a working MSP. Review and replace them with your own before anything goes client-facing.

This skill is the source of truth for the recurring work {{COMPANY_NAME}} does when nothing
is broken: patching, backup verification, monitoring, on-call coverage, and controlled change.
This is the substance behind the managed fee. The reactive desk (msp-helpdesk) is what clients
see; this cycle is why they see it rarely.

One liability fact shapes the whole skill, inherited from msp-legal: the MSA's ransomware cost
allocation carries a negligence carveout. {{COMPANY_NAME}}'s protection in a bad scenario is a
dated log showing the routine ran: patches applied, backups verified, alerts handled. Every
section below ends in a record because the record is part of the service.

Write maintenance procedures, change plans, and patch and test-restore steps to
msp-technical-writing in strict mode. Write the logs and notes in flavored mode. Client
maintenance notices belong to msp-client-comms.

---

## Patching (example default)

**Workstations:** automated weekly patch cycle through the RMM. Reboots enforced monthly at
minimum; a machine that has dodged its reboot past the deadline gets scheduled with the user,
not skipped. Third-party application patching rides the same weekly cycle where the RMM covers
the app.

**Servers:** monthly maintenance window, the **third Thursday, 8:00 pm to midnight, {{TIMEZONE}}**.
Sequence per server: snapshot or verified backup point first, then
patches, then reboot, then service verification against a per-server checklist (services up,
backups scheduled, key app responds). Clients with affected services get the planned-maintenance
notice (msp-client-comms template 1) at least 3 business days ahead.

**Out-of-band:** critical or actively-exploited vulnerabilities do not wait for the window.
Test, then deploy as soon as reasonable, any day. If the fix is disruptive, use the emergency
maintenance variant of the notice: one honest sentence on why it cannot wait.

**Exceptions:** a client or app that cannot tolerate a patch gets a documented exception with a
review date, not a quiet skip. A client who refuses patching against recommendation is a Risk
Acceptance Waiver conversation (msp-legal).

**Record:** patch status per endpoint lives in the RMM; the monthly window gets a closing note
(what was patched, what was deferred and why). This feeds the QBR scorecard's Updates row.

---

## Backup Verification (example default)

- **Every business day:** backup job results checked. A failed job is a P2 ticket
  (msp-helpdesk) the same morning, worked until the backup chain is healthy again. Two
  consecutive silent days on any job is treated as a failure even if no alert fired.
- **Every month, per client:** one hands-on test restore (a file set, mailbox item, or VM boot,
  rotated so restore types vary through the quarter), logged with date, what was restored, and
  result. This is what lets {{COMPANY_NAME}} say "we verify your backups monthly" in writing and
  what feeds the QBR scorecard's Backups row honestly.
- A failed test restore is a P1-adjacent event: treat the client as effectively unprotected
  until the chain is fixed and a re-test passes. Do not sit on it until the QBR.

**Record:** the restore log (date, client, scope, result, tech) is the single most important
document in this skill. In a ransomware dispute it is the difference between a defensible
posture and the negligence carveout.

---

## Monitoring and Alert Triage

The rule that keeps a small team sane: **an alert is either actionable or it is tuned out of
existence.** An alert nobody would act on is noise, and noise trains the desk to ignore the one
that matters.

- Alerts that indicate business impact map into the msp-helpdesk priority matrix and become
  tickets (server down or unreachable: P1 path; backup failure: P2; disk trending full: P3 with
  a scheduled fix). Informational alerts do not become tickets; they get tuned.
- Duplicate and flapping alerts are deduplicated at the monitoring tool, not in someone's inbox.
- **After hours, only P1-class alerts page the on-call phone.** Everything else waits for the
  next business morning, consistent with the after-hours rules in msp-helpdesk.
- New client environments get a tuning pass at onboarding (msp-onboarding) and a second pass at
  the 30-day review; steady-state environments get re-tuned whenever a week produces alerts
  nobody acted on.

---

## On-Call (example default)

- **Weekly alternating rotation** between on-call staff. The {{PHONE}} forward points at the
  current primary; if the primary does not respond within 15 minutes, it rolls to the
  secondary.
- Handoff is deliberate: a two-minute check-in at rotation change covering open P1/P2 items,
  fragile clients, and anything mid-change.
- Vacations, sick days, and conflicts get swapped in advance on the shared calendar. The
  rotation is boring on purpose; surprise coverage gaps are how the P1 promise breaks.
- After-hours work billed to clients follows the multipliers in msp-pricing (1.5x after-hours,
  2x holiday), per the client's Order.

---

## Change Management

For risky changes (firewall and network changes, DNS, server configuration, tenant-wide
settings, anything that can take a client offline):

1. **Write the change down first:** what, why, when, blast radius, and the rollback step. Two
   sentences is fine; zero sentences is not.
2. **Second set of eyes** from the owner or a designated senior tech for anything that touches
   a whole site or tenant.
3. **Client notice** through msp-client-comms when users could notice the change; the planned
   or emergency maintenance template as fits.
4. **Rollback ready before starting**, including config export or snapshot where the platform
   allows.
5. **Log the change** in the client's documentation in the same sitting.

A change that skipped these steps and went fine is still a process failure; the one that goes
wrong without them is an outage plus a liability problem.

---

## Documentation Currency

The rule from the documentation-system school, adopted: **update the doc in the same session as
the change.** Passwords rotated, configs changed, hardware swapped, vendor contacts updated: the
client's documentation reflects it before the ticket or change closes. Stale documentation
surfaces at the worst moments (an incident, an offboarding handoff) and both of those moments are
already covered by promises this suite makes (msp-helpdesk, msp-offboarding).

---

## Vendor and License Touchpoints

- License counts get trued against reality during the monthly count reconciliation the Service
  Order defines; pass-through licensing follows msp-pricing.
- Vendor contract renewals, warranty expirations, and OS end-of-life dates feed the QBR horizon
  list (msp-qbr); this skill's job is making sure they are recorded when first seen, not
  reconstructed at QBR prep.
- {{COMPANY_NAME}} is the client's vendor liaison per the service catalog; vendor tickets follow
  the msp-helpdesk vendor category so time is captured.
- Domain renewal dates for Website Care and managed clients are recorded when first seen, and
  confirmed set to auto-renew in the client's registrar account.

## Website Care (recurring work the Care Order promises)

For clients with a Website Hosting and Care Service Order (msp-pricing, msp-legal):
- Keep the site and its hosting platform configuration monitored; certificate, DNS, or deploy
  failures go to msp-helpdesk as tickets.
- The site's repo on your git hosting provider is the source backup; confirm the production
  branch matches what is live so the site can be restored from it.
- Log every content edit as ticket time against the 30-minute monthly allowance; time past it
  bills at the managed rate.
- Watch usage against the hosting platform's included limits. A site heading for a higher tier
  gets a client notice at least 30 days ahead (msp-client-comms), with options to stay in the
  lower tier where feasible.

---

## Setup Decisions

The values below shipped as example defaults from a working MSP, and the items after them are
still genuinely open questions upstream. Settle all of it for your own shop before this skill
goes client-facing:

- Patching: shipped default is workstations weekly automated with monthly enforced reboots;
  servers in a monthly window, third Thursday 8:00 pm to midnight {{TIMEZONE}},
  snapshot first; critical vulnerabilities out-of-band.
- Backups: shipped default is job checks every business day (failures are P2 the same morning);
  one logged test restore per client per month.
- On-call: shipped default is a weekly alternating rotation between on-call staff, with a
  15-minute response roll-over to the secondary, swaps planned in advance.
- The per-server verification checklist contents (the standing proposal above is the minimum
  set; decide your own).
- Which restore types rotate through the monthly test (proposal above: file set, mailbox item,
  VM boot across a quarter).
- Whether change notices go to all clients on shared infrastructure or only directly affected
  ones (proposal above: directly affected only).
