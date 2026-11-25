---
name: disaster-recovery
description: Guides picking a DR strategy tier against RTO/RPO and cost, designing cloud failover and failback, and running the right DR test type (NIST 800-34). Use when the user asks to design or choose a disaster recovery strategy, hot/warm/cold or pilot-light setups, multi-region failover, or how to test a DR plan.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Disaster recovery

DR is _how_ you hit the RTO/RPO that continuity (`load_skill business-continuity`)
set. Don't choose a tier by appetite for shininess; choose the cheapest tier that
meets the activity's RTO/RPO, per the BIA. Frame on **NIST SP 800-34 Rev. 1**
(contingency planning) and the **AWS DR** strategy ladder.
verify: https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-34r1.pdf
verify: https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html

## Strategy tiers (cost ↑ as RTO/RPO ↓)

| Tier                           | How it works                                                                 | RTO           | RPO            | Standby cost              |
| ------------------------------ | ---------------------------------------------------------------------------- | ------------- | -------------- | ------------------------- |
| Backup & restore               | Back up; provision + restore on disaster. Nothing running at DR site.        | hours to days | hours          | ~storage only (cheapest)  |
| Pilot light                    | Core (DB replicated, AMIs/IaC ready) always on; app tier "dark" til failover | 10s of min    | seconds to min | low (data + minimal core) |
| Warm standby                   | Scaled-down _full_ stack always running; scale up on failover                | minutes       | seconds        | ~50 to 70% of prod        |
| Hot / multi-site active-active | Full prod in 2+ sites serving live; DNS/LB shifts traffic                    | near-zero     | near-zero      | ~2× prod (most expensive) |

The decision is economic: pick where the cost of an outage crosses the cost of
standby. Don't buy active-active for a Tier-3 app, and don't run a Tier-0 revenue
system on nightly backups. Tier per-activity, not one tier for the whole estate.

## Cloud DR patterns

- **Replication** sets RPO: async (cross-region, seconds to minutes lag, cheap) vs
  synchronous (zero data loss, latency-bound, costly). Match to the RPO, not vanity.
- **IaC + immutable images** make pilot-light/backup-restore credible: recovery is
  `terraform apply` against a pre-staged region, not hand-clicking under pressure.
- **Multi-region ≠ multi-AZ.** AZ redundancy survives a datacenter; region DR survives
  a regional outage or account/control-plane compromise. Pick by the threat in the BIA.
- **Beware shared blast radius**: same cloud account, same IAM, same backup vault as
  prod ⇒ a ransomware/account compromise takes DR with it. Isolate the DR copy
  (separate account/tenant, immutable vault: `load_skill backup-recovery`).
- **DR-region data residency (APAC pitfall)**: the DR region must satisfy the _same_
  data-sovereignty law as prod. A EU/US team that fails over to the nearest/cheapest region
  can breach localization rules (China PIPL, India DPDPA, Indonesia, Vietnam); pick the DR
  site by residency law, not just latency and cost.

## Failover & failback

- **Failover**: promote DR to primary (stop replication, promote DB, repoint DNS/LB,
  validate health, _then_ admit traffic). Have a tested runbook; declare with named
  authority (`load_skill crisis-management`), don't drift into it.
- **Failback**: the harder, skipped half. Returning to primary must re-sync data
  accumulated at DR _without loss_ and be scheduled (often a maintenance window). Plan
  it before the disaster; many teams fail over fine and then can't get home cleanly.
- **DNS/TTL**: low TTLs on failover records or cutover is gated by stale caches.

## DR test types (escalating rigor: NIST 800-34 TT&E)

| Type                   | What it proves                                                | Disruptive? |
| ---------------------- | ------------------------------------------------------------- | ----------- |
| Tabletop / walkthrough | People know roles, runbook, decisions (see crisis-management) | no          |
| Parallel / simulation  | DR stood up & validated _alongside_ live prod; no cutover     | no          |
| Full interruption      | Real failover: prod off, run on DR, then failback             | yes (risk)  |

- Test ≥ annually, more for high-impact systems. A backup/DR you haven't _restored_ is
  a hypothesis, not a control; measure achieved RTO/RPO against target each test.
- Escalate ladder over time; don't jump to full-interruption on an untested plan.
- Capture gaps as findings: `report_finding` each missed RTO so it lands in `render_report`.

## Ransomware lens

- DR ≠ ransomware recovery if your DR replicates corruption. Async replication faithfully
  copies encrypted/poisoned data to the DR site; replication is **not** a backup. You
  need point-in-time, immutable restore (`load_skill backup-recovery`) to roll _back_,
  not just fail _over_.
- Add a "recover to clean point" scenario to the test programme, not only "site loss".
