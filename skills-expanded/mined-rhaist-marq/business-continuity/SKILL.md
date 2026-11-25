---
name: business-continuity
description: Guides running a Business Impact Analysis, deriving RTO/RPO/MTPD, and structuring a business continuity plan aligned to ISO 22301. Use when the user asks to write a BCP, perform a BIA, set recovery objectives, align with ISO 22301, or plan continuity for a cyber outage.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Business continuity

Continuity is a business deliverable, not an IT one. You decide _which activities
must survive, how fast, and how much data they can lose_; then IT/DR
(`load_skill disaster-recovery`) builds to those numbers. Anchor on **ISO 22301:2019**
(BIA is clause 8.2.2); the 2024 Amd 1 adds climate considerations.
verify: https://www.iso.org/standard/75106.html

## Business Impact Analysis (the BIA method)

Work activity-by-activity (a process/service, not a server). For each:

1. **Criticality**: what breaks if it stops? Score impact over _time_ (1h / 24h /
   1wk / 1mo) across axes: revenue, legal/regulatory, safety, contractual SLA,
   reputation. Impact almost always grows non-linearly with outage duration.
2. **MTPD** (Maximum Tolerable Period of Disruption): the outage length after which
   the organisation's viability is irrevocably threatened. This is a _business
   survival_ limit, set by the business, not negotiable down by IT convenience.
3. **Dependencies**: map upstream/downstream (apps, data, people/skills, facilities,
   suppliers, utilities). A process is only as recoverable as its slowest dependency;
   surface single points of failure here. A 1h-RTO app on a 3rd party with a 24h SLA
   is a lie; fix the dependency or relax the RTO.
4. **Minimum resources**: the floor of staff, systems, and data needed to run at a
   degraded-but-acceptable level (the MBCO, Minimum Business Continuity Objective).

Output: a prioritised list of critical activities with their MTPD, dependencies, and
resource floor. Everything downstream derives from this; don't skip to solutions.

## Deriving RTO and RPO

Nested constraint: **RPO ≤ data-loss tolerance** and **RTO < MTPD** (always leave a
buffer; RTO == MTPD has zero margin and will breach).

- **RTO** (Recovery Time Objective): target time to restore the activity. Derive it
  _below_ MTPD with contingency for detection + decision + actual recovery, not just
  the restore step.
- **RPO** (Recovery Point Objective): max acceptable data loss, in time. RPO directly
  sets backup/replication frequency: RPO 4h ⇒ you must capture state ≥ every 4h. RPO
  near-zero ⇒ synchronous replication (expensive; justify it from the BIA).
- Sanity check: every RTO/RPO has a cost. If everything is "Tier 0, RTO 0", the BIA
  wasn't done: force the business to rank, because the budget will.

## BCP structure (what the plan contains)

- **Scope & roles**: activation authority, BC team, deputies (no single points).
- **Per-activity recovery plan**: RTO/RPO, the workaround (manual/degraded mode to
  hit MBCO while systems recover), dependencies, and the restore procedure.
- **Resource & contact directory**: staff, suppliers, sites, alternate-site arrangements.
  Keep an **offline copy**: a continuity plan only readable on the down system is useless.
- **Communications plan**: internal cadence + external/stakeholder messaging (the crisis
  layer: `load_skill crisis-management`).
- **Maintenance**: review on change and at least annually; exercise the plan (DR test
  types in `disaster-recovery`).

## ISO 22301 alignment (PDCA, clauses 4 to 10)

- Cl. 4 context & scope · Cl. 5 leadership + policy · Cl. 6 objectives · Cl. 7 resources/competence.
- **Cl. 8 operation**, the engine: 8.2 BIA + risk assessment, 8.3 strategy selection,
  8.4 procedures (BCP), 8.5 exercise programme.
- **Cl. 9** performance evaluation (metrics, internal audit, management review) · **Cl. 10**
  improvement (corrective action). It's a PDCA management system; certification needs
  evidence of the loop turning, not a binder on a shelf.

## Ransomware lens

- Treat ransomware as a _continuity_ event, not just a security one: assume primary
  systems AND online backups are simultaneously unavailable. Your RTO/RPO must hold when
  recovery starts from clean, offline copies (`load_skill backup-recovery`); re-derive
  RTO including rebuild-from-bare-metal + integrity-verification time, which dwarfs a
  routine restore.
- BIA feeds the risk register: push critical-activity SPOFs into `load_skill risk-assessment`.
