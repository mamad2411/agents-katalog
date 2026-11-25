---
name: backup-recovery
description: Covers designing ransomware-resilient backups, including the 3-2-1-1-0 rule, immutable and air-gapped copies, protecting the backup system itself, restore-test discipline, and recovery prioritization. Use when the user asks how to design or assess a backup strategy, survive ransomware, make backups immutable, or test and sequence restores.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Backup & recovery

This is the control that saves you in ransomware. Modern attackers hunt and
delete/encrypt backups _first_: backup infrastructure is targeted in the large majority
of ransomware cases, so the design goal is that the attacker
cannot reach, alter, or delete the copy we restore from; having backups is not enough. Backups feed the RTO/RPO from
`load_skill business-continuity`; recovery sequencing feeds `load_skill disaster-recovery`.

## The 3-2-1-1-0 rule

Evolution of 3-2-1, built for ransomware:

- **3** copies of the data (1 production + 2 backups).
- **2** different media/storage types (don't lose all copies to one failure mode).
- **1** copy off-site (geographic separation; survives site loss).
- **1** copy **offline, air-gapped, _or_ immutable**: the ransomware-proof copy.
- **0** errors; every backup verified recoverable (automated integrity check + restore test).

verify: https://opti9tech.com/blog/the-3-2-1-1-0-backup-strategy-explained/

The whole rule fails on the last two: a replicated, online, mutable backup is just a second
target. The "1" offline/immutable + the "0" verified are what make it a control.

## Protect the backups themselves (the part that matters)

- **Immutable / WORM**: object-lock / retention-lock so data cannot be modified or deleted
  for a set period, _including by an admin_ (governance vs compliance lock: compliance lock
  resists even root/vendor). Set retention ≥ your detection-to-recovery window (attackers
  dwell weeks before detonating: short retention = poisoned-only copies).
- **Air-gapped / offline**: physical (tape, rotated offline) or logical isolation; the gap is
  only bridged on a controlled schedule. Nothing always-online is truly air-gapped.
- **Isolate the backup control plane**: separate accounts/credentials/MFA/network from prod
  and from the production directory (AD). If domain-admin compromise reaches the backup
  console, you have no backups. No shared SSO/domain trust into the vault.
- **Encrypt + protect keys** separately, so stolen backups aren't a second breach and key
  loss doesn't brick recovery.
- **Alert on backup tampering**: mass deletes, retention changes, job disablement; these are
  ransomware pre-cursors, not ops noise.

## Restore-test discipline

- A backup you have never restored is a _hypothesis_, not a control. Test restores on a
  cadence (criticality-driven: critical systems quarterly+, others ≥ annually).
- **Measure achieved RTO/RPO** against target each test; restore is usually far slower than
  backup; un-tested RTOs are fiction. Test full system / bare-metal rebuild, not just file-level.
- Restore to an **isolated clean-room** network; never restore a potentially-infected image
  straight onto production. Scan/verify integrity before reconnecting.
- Keep enough **retention/versioning** to roll back _before_ the intrusion (weeks to months);
  pick a clean recovery point, since recent backups may already be encrypted/poisoned.
- Automate verification (the "0"): checksums, test-boot, app-level validation; not just
  "job succeeded".

## Recovery prioritization (sequencing the restore)

Driven by the BIA, not by what's easiest to restore:

1. **Identity & core dependencies first**: domain controllers / IdP, DNS, then the data
   they gate. Restore from clean (not reinfected) copies; rebuild AD carefully (forest
   recovery, reset krbtgt twice) to avoid restoring the attacker's persistence.
2. **Tier-0 / critical activities** by RTO order; bring up minimum-viable (MBCO) first,
   full capacity after.
3. **Don't reconnect until clean**: eradicate first (`load_skill incident-response-leadership`),
   or you re-encrypt a fresh restore. Stage the recovery network behind the clean line.

## Ransomware reality

- Assume prod + all _online_ backups are simultaneously hit; your survival is the
  offline/immutable copy and your tested ability to restore from it within MTPD.
- Backups are an availability control, not a confidentiality one; they don't stop
  double-extortion (data already exfiltrated/leaked). That's a crisis-comms + regulatory
  problem: `load_skill crisis-management`.
- Log a missed restore RTO or unprotected backup path as a finding: `report_finding` →
  `render_report`, and push the SPOF into `load_skill risk-assessment`.
