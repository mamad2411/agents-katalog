---
name: cloud-well-architected-framework-review
description: >
  Guides running a Well-Architected-style review of an existing cloud
  workload against the standard pillars used across AWS, Azure, and GCP's
  respective frameworks — operational excellence, security, reliability,
  performance efficiency, cost optimization, and (where the provider
  includes it) sustainability — scoring each pillar, identifying
  cross-pillar trade-offs, and producing a prioritized remediation backlog.
  Use when a user asks to "run a Well-Architected review", "do an AWS
  Well-Architected Framework (WAF) assessment", "review this workload
  against Azure Well-Architected / GCP Architecture Framework", "find our
  biggest architectural risks", "why does our cost optimization score keep
  getting deprioritized", or "build a remediation backlog from an
  architecture review". Framed generically since AWS, Azure, and GCP each
  publish their own version of this framework with different tooling and
  pillar names.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: standards-and-compliance-frameworks
  maturity: stable
---

# Cloud Well-Architected Framework Review

## Purpose

Every major cloud provider publishes some form of Well-Architected Framework
— AWS's Well-Architected Framework, Azure's Well-Architected Framework, and
Google Cloud's Architecture Framework — as a structured set of questions and
best practices grouped into pillars, typically: operational excellence,
security, reliability, performance efficiency, cost optimization, and (in
AWS's and Azure's current frameworks) sustainability. The pillars, exact
question wording, and supporting tooling (AWS's Well-Architected Tool,
Azure's Well-Architected Review assessment, Google's Architecture Framework
recommender integrations) differ by provider, but the underlying discipline
is the same: systematically walk a real, existing workload through each
pillar's questions, score the gaps, and turn the findings into a prioritized,
owned remediation backlog instead of a one-time slide deck that nobody
revisits. This skill guides that review process generically, applicable
regardless of which provider's framework or tool is used, and is explicit
that a Well-Architected review is a self-assessment or peer/solutions-
architect-led review — it produces engineering recommendations and risk
prioritization, not a compliance certification, a security audit finding, or
a substitute for the standards-mapping and legal/audit processes covered in
[security-compliance-mapping-soc2-iso-pci-nist](../security-compliance-mapping-soc2-iso-pci-nist/SKILL.md).

## When to use

- A user asks to "run a Well-Architected review" on a specific workload,
  application, or account/subscription/project.
- Preparing for or following up on a cloud provider's own WAF review
  (e.g. an AWS Solutions Architect-led review) and needing to turn the
  output into an actionable, prioritized backlog.
- A workload has grown organically and the team wants a structured
  cross-cutting health check rather than another point security scan.
- Leadership asks "where are our biggest architectural risks" across
  reliability, security, cost, performance, operations, and (if in scope)
  sustainability simultaneously, not just one dimension.
- A team has been reviewed before and cherry-picked easy wins from one or
  two favorite pillars (commonly security or performance) while letting
  cost optimization or sustainability findings go stale.
- Prioritizing remediation work across multiple workloads with limited
  engineering capacity.

## Prerequisites & environment

- A clearly scoped **workload** — a Well-Architected review is done per
  workload (a bounded application or system with a defined owner), not
  per entire cloud account/organization; reviewing "everything" at once
  produces vague, unactionable output.
- Access to the workload's architecture diagram, IaC (Terraform/
  CloudFormation/Bicep/Deployment Manager), monitoring dashboards, cost
  and usage data, and incident history — the review is grounded in real
  operational evidence, not just an architecture diagram in isolation.
- Provider-specific framework reference and, if available, its tooling:
  - AWS: AWS Well-Architected Framework (six pillars: Operational
    Excellence, Security, Reliability, Performance Efficiency, Cost
    Optimization, Sustainability) and the AWS Well-Architected Tool for
    running a structured workload review with milestones.
  - Azure: Microsoft Azure Well-Architected Framework (five pillars:
    Reliability, Security, Cost Optimization, Operational Excellence,
    Performance Efficiency — sustainability is addressed as a
    cross-cutting consideration rather than its own numbered pillar in
    the current framework) with the Azure Well-Architected Review
    assessment.
  - GCP: Google Cloud Architecture Framework (categories: Operational
    Excellence, Security/Privacy/Compliance, Reliability, Cost
    Optimization, Performance Optimization, and a dedicated Sustainability
    pillar) with Active Assist / recommender-based tooling.
  - Confirm which version of the provider's framework and which pillar
    set applies before scoring — pillar names and counts do shift between
    framework revisions.
- Stakeholders who can speak to each pillar: an application owner
  (operational excellence), a security engineer, an SRE/on-call lead
  (reliability), a performance/capacity owner, and someone who owns the
  cost/FinOps relationship for the workload — a review run by one person
  guessing at every pillar produces weaker findings than one with the
  right people in the room.
- Relevant supporting skills already in place or referenced during review:
  IAM hardening, cost/FinOps practices, and disaster recovery strategy, so
  the review can cite specific gaps rather than restating generic pillar
  questions.

## Step-by-step guidance

1. **Scope the workload.** Name it, define its boundary (which
   services/accounts/subscriptions it includes), identify the business
   owner, and state its criticality tier — a customer-facing payments
   workload and an internal reporting tool warrant different depth.
2. **Select the framework version and confirm the pillar list** for the
   provider in scope (or note if the workload is multi-cloud and needs a
   review pass per provider, since the pillar sets and tooling differ).
3. **Gather evidence per pillar before scoring**, not opinions in a
   vacuum:
   - *Operational excellence*: runbooks, deployment process, change
     failure rate, monitoring/alerting coverage, incident postmortems.
   - *Security*: IAM least-privilege posture, encryption at rest/in
     transit, network segmentation, secrets handling, patch/vulnerability
     management — this pillar overlaps directly with
     [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md),
     [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md),
     and [cis-benchmarks-hardening](../cis-benchmarks-hardening/SKILL.md).
   - *Reliability*: RTO/RPO targets and whether they're actually met,
     multi-AZ/region design, backup testing — cross-reference
     [disaster-recovery-and-backup-strategy](../../../cloud/skills/disaster-recovery-and-backup-strategy/SKILL.md).
   - *Performance efficiency*: right-sizing, caching strategy, load
     testing history, latency SLOs vs actuals.
   - *Cost optimization*: tagging coverage, idle/oversized resource
     count, commitment coverage — cross-reference
     [cloud-cost-finops-optimization](../../../cloud/skills/cloud-cost-finops-optimization/SKILL.md).
   - *Sustainability* (where the provider's framework includes it as a
     pillar): region selection for carbon intensity, resource
     utilization efficiency, managed-service vs. self-hosted trade-offs
     that affect idle capacity.
4. **Score each pillar** using a consistent scale (see Worked example) and
   record the specific evidence behind each score, not just a number —
   "3/5, no evidence" is not defensible six months later.
5. **Identify cross-pillar trade-offs explicitly.** Well-Architected
   reviews frequently surface tensions — e.g. a reliability improvement
   (multi-region active-active) that directly increases cost, or a cost
   optimization (aggressive autoscaling to zero) that increases latency
   variance. Document the trade-off and who decided how to resolve it
   rather than optimizing one pillar in isolation.
6. **Convert every finding into a backlog item** with: pillar, finding,
   risk if unaddressed, estimated effort, and a priority. Do not leave
   findings as prose in a report that nobody re-reads.
7. **Prioritize the backlog** using both risk and effort — a common,
   defensible approach is high-risk/low-effort items first ("quick wins"),
   then high-risk/high-effort items scheduled explicitly, with low-risk
   items tracked but not blocking.
8. **Assign an owner and a re-review date per pillar**, especially for
   pillars that are easy to deprioritize (cost optimization and
   sustainability are the most commonly neglected in practice) — a review
   with no re-check date is a review that will not be revisited.
9. **Report the full pillar scorecard**, not just the pillars with good
   scores — a review that only surfaces the pillars where the team already
   looks good is not a Well-Architected review, it is a highlight reel.

## Best practices

- Score every pillar every time, even ones the requesting team would
  rather not discuss — a review that consistently omits cost optimization
  or sustainability findings has stopped being a Well-Architected review.
- Ground every score in a specific piece of evidence (a dashboard metric,
  an IaC snippet, an incident ticket) — "we feel good about reliability"
  is not a score.
- Make trade-offs explicit and attribute the decision to a named owner —
  Well-Architected pillars actively conflict (cost vs. reliability,
  performance vs. cost, security vs. operational velocity); the value of
  the review is surfacing and deciding the trade-off, not pretending all
  six pillars can be maximized simultaneously with the same budget.
- Re-review on a cadence (e.g. every 6–12 months or after a major
  architecture change), and track score deltas over time — a single
  point-in-time review value decays as the workload evolves.
- Treat the provider's own review tooling (AWS Well-Architected Tool
  milestones, Azure Well-Architected Review assessment, GCP Active
  Assist recommendations) as data sources to fold into evidence
  gathering, not as a replacement for talking to the people who actually
  operate the workload.
- Distinguish "not applicable to this workload" (documented, with reason)
  from "not addressed yet" (an actual backlog item) — collapsing the two
  hides real risk.
- When reviewing a multi-cloud workload, run a pass per provider using
  that provider's own pillar names/tooling rather than forcing one
  provider's framework onto another provider's services.

## Common pitfalls

- **Symptom:** The review report only covers security and performance in
  depth, with cost optimization and sustainability reduced to a single
  bullet each ("looks fine").
  **Fix:** Require evidence-backed scoring for every pillar in scope
  before the review is considered complete; if a pillar genuinely has no
  data, that itself is a finding ("no cost visibility for this workload")
  rather than an implicit pass.
- **Symptom:** A high-risk reliability finding (e.g. single-AZ database
  with no tested failover) sits in the backlog for a year because it was
  filed as "medium priority" with no owner or date.
  **Fix:** Every backlog item needs an owner and either a target date or
  an explicit, approved risk-acceptance with an expiry/review date —
  unowned findings are how Well-Architected reviews become shelfware.
- **Symptom:** Reliability is "improved" by moving to multi-region
  active-active without updating the cost forecast, and the resulting bill
  increase becomes its own escalation a quarter later.
  **Fix:** Score and discuss cross-pillar trade-offs during the review
  itself — a reliability recommendation that materially changes cost
  should carry an explicit cost-optimization counter-entry and a
  documented decision, not surface as a surprise later.
- **Symptom:** The review is treated as a compliance deliverable ("we did
  our Well-Architected review, we're good for audit") and handed to a
  customer or auditor as evidence of security/compliance posture.
  **Fix:** A Well-Architected review is an internal architecture and risk
  health check run by the team (optionally with the cloud provider's
  solutions architects) — it is not a certification and does not
  substitute for a SOC 2/ISO 27001/PCI-DSS audit; route compliance-mapping
  needs to
  [security-compliance-mapping-soc2-iso-pci-nist](../security-compliance-mapping-soc2-iso-pci-nist/SKILL.md)
  and be explicit with stakeholders about the difference.
- **Symptom:** The same workload is reviewed once at launch and never
  again; eighteen months later nobody can say whether the findings were
  ever fixed or whether new risks have appeared.
  **Fix:** Set a re-review cadence and track score deltas per pillar over
  time as part of the backlog, not just a one-time snapshot.

## Worked example

Illustrative Well-Architected review of a mid-tier e-commerce order-processing
workload on AWS (framework used: AWS Well-Architected Framework, 6 pillars).
Scoring scale: 1 (significant gaps) – 5 (best-practice aligned).

| Pillar | Score | Key evidence | Top finding |
|---|---|---|---|
| Operational excellence | 3/5 | Deploys via CI/CD, but no automated rollback; on-call runbook exists but last updated 14 months ago | Runbook stale; no automated rollback on failed deploy |
| Security | 4/5 | IAM roles scoped per-service, secrets in Vault, but one legacy EC2 instance still uses a long-lived static credential | Legacy instance not yet migrated to federated/instance-role auth |
| Reliability | 2/5 | Primary RDS instance is single-AZ; no documented/tested failover; RTO target of 1 hour is unverified | Single-AZ database is a single point of failure against the stated RTO |
| Performance efficiency | 4/5 | Autoscaling configured with headroom, p99 latency within SLO for 11 of 12 months | Minor: cache hit ratio below target during flash-sale traffic spikes |
| Cost optimization | 2/5 | <30% of compute spend covered by Savings Plans/Reserved Instances; several oversized instances flagged idle >30 days | Low commitment coverage and unaddressed idle-resource findings |
| Sustainability | 2/5 | Workload runs in a single region chosen for latency, not evaluated for carbon intensity; several dev/test resources run 24/7 unnecessarily | No non-prod scheduling; region carbon-intensity not evaluated |

Illustrative cross-pillar trade-off note: "Moving the RDS instance to
Multi-AZ (Reliability fix) increases monthly database cost by roughly
95%. Recommendation: proceed given the workload processes customer
payments and the stated 1-hour RTO is currently unmet and unverifiable;
approved by `<WORKLOAD_OWNER_PLACEHOLDER>`."

Illustrative prioritized backlog (excerpt):

| Priority | Pillar | Finding | Effort | Owner | Target |
|---|---|---|---|---|---|
| P0 | Reliability | Single-AZ RDS with unverified failover | Medium | `<DB_TEAM_PLACEHOLDER>` | Next sprint |
| P0 | Cost optimization | Idle resources running >30 days | Low | `<PLATFORM_TEAM_PLACEHOLDER>` | This week |
| P1 | Security | Legacy instance on static credentials | Medium | `<SECURITY_ENG_PLACEHOLDER>` | 2 sprints |
| P1 | Cost optimization | <30% commitment coverage | Medium | `<FINOPS_OWNER_PLACEHOLDER>` | Next quarter |
| P2 | Sustainability | No non-prod off-hours scheduling | Low | `<PLATFORM_TEAM_PLACEHOLDER>` | Next quarter |
| P2 | Operational excellence | Runbook stale, no automated rollback | Low | `<APP_TEAM_PLACEHOLDER>` | Next sprint |

Re-review scheduled for `<REVIEW_DATE_PLACEHOLDER>` (illustrative: 6 months
out), with the same pillar scorecard re-run to track deltas.

## Cross-references

- [cis-benchmarks-hardening](../cis-benchmarks-hardening/SKILL.md) — infrastructure/OS-level hardening evidence that feeds the security pillar.
- [security-compliance-mapping-soc2-iso-pci-nist](../security-compliance-mapping-soc2-iso-pci-nist/SKILL.md) — where to go if the review's security findings need to be mapped to a formal compliance framework for audit purposes.
- [owasp-top-10-secure-coding-standards](../owasp-top-10-secure-coding-standards/SKILL.md) — application-layer security depth beyond what a workload-level security pillar review typically covers.
- [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md) — detailed remediation for security-pillar IAM findings.
- [cloud-cost-finops-optimization](../../../cloud/skills/cloud-cost-finops-optimization/SKILL.md) — detailed remediation for cost-optimization-pillar findings.
- [disaster-recovery-and-backup-strategy](../../../cloud/skills/disaster-recovery-and-backup-strategy/SKILL.md) — detailed remediation for reliability-pillar RTO/RPO findings.
- [aws-landing-zone-setup](../../../cloud/skills/aws-landing-zone-setup/SKILL.md), [azure-landing-zone-setup](../../../cloud/skills/azure-landing-zone-setup/SKILL.md), [gcp-landing-zone-setup](../../../cloud/skills/gcp-landing-zone-setup/SKILL.md) — organization-level guardrails that reduce recurring findings across many workload reviews.
