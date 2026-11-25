---
name: aigov-matter-workspace
version: 1.0.0
description: Set up and organize a governance/legal matter workspace for a single AI system review — a structured, defensible record that ties intake, triage, AIA, vendor terms, gap analysis, decisions, and sign-offs into one auditable container.
author: matrixx0070
tags: [ai-governance, matter-management, audit-trail, recordkeeping, compliance, sign-off]
capabilities: []
---

## When to use

Use this when an AI system, feature, or vendor tool enters governance review and you need one organized, versioned place to hold everything that review produces. This is the container the other aigov- skills fill: it collects their outputs, tracks status, and preserves the decision trail so the organization can later show *what it knew, when, and who approved it*.

**Not for:** building the inventory of systems (use aigov-ai-inventory), classifying a use case's risk (use aigov-use-case-triage), writing the impact assessment (use aigov-aia-generation), reviewing a vendor's AI terms (use aigov-vendor-ai-review), mapping controls to regulations (use aigov-reg-gap-analysis), watching for legal changes (use aigov-policy-monitor), drafting policy (use aigov-policy-starter), the first-time discovery interview (use aigov-cold-start-interview), or tailoring artifacts to your org (use aigov-customize).

This skill provides organizational and decision-support scaffolding, not legal advice. Before anything with legal stakes is relied on, filed, or represented to a regulator, a qualified attorney must review the matter and its conclusions.

## Method

1. Open the matter: assign a stable matter ID, the AI system name, owner, sponsor, and a one-line purpose. Set status to `INTAKE`.
2. Lay out the canonical folder/record structure (see Output format) with a fixed slot for each aigov- artifact, so a missing artifact is visible as an empty slot rather than silently absent.
3. Link, don't copy: each slot points to the source artifact with its version/hash and date. **Decision:** if an artifact is still draft, mark the slot `PENDING` and block downstream sign-off until it resolves.
4. Start the decision log immediately — every material call (risk tier, proceed/hold, mitigations required) gets a dated entry with rationale and the person accountable.
5. Define the sign-off roster by role (system owner, legal, privacy/DPO, security, business sponsor) and the gate each must clear before go-live. **Decision:** high-risk classification triggers mandatory legal + privacy sign-off, not optional review.
6. Set retention and traceability: record the review period, evidence links, and how long the matter must be retained after the system is retired.
7. Advance status through the lifecycle (`INTAKE → IN-REVIEW → APPROVED/CONDITIONAL/BLOCKED → MONITORING → RETIRED`) and schedule the re-review date.

## Example

Matter `AIG-2026-014`, "Resume-screening assistant (vendor X)". Triage returned high-risk (employment decision). The workspace shows AIA `PENDING`, vendor-terms slot filled (v2, indemnity flag open), gap-analysis linked. Decision log: `2026-07-11 — classified high-risk, legal + DPO sign-off mandatory, go-live BLOCKED until AIA complete`. Roster: owner ✓, security ✓, legal ✗, DPO ✗. Status `IN-REVIEW`, re-review 6 months. The empty AIA slot makes the blocker obvious at a glance.

## Pitfalls

- **Copying artifacts instead of linking versions.** Snapshots drift; a record that cites "the AIA" without a version/date can't prove what was actually approved.
- **Decision log written after the fact.** Reconstructed rationale is weak evidence. Log each call the day it's made, with the accountable name.
- **Sign-off as a checkbox.** A name without a role, a gate, and a date is not defensible accountability — capture all four.
- **No retention or re-review clock.** Records deleted too early destroy your liability defense; systems never re-reviewed drift out of compliance silently.

## Output format

```
# AI Governance Matter — <matter-id>
System: <name>   Owner: <>   Sponsor: <>   Purpose: <one line>
Status: INTAKE|IN-REVIEW|APPROVED|CONDITIONAL|BLOCKED|MONITORING|RETIRED
Risk tier: <from aigov-use-case-triage>   Opened: <date>   Re-review: <date>

## Artifacts (link + version + date; PENDING if missing)
[ ] Intake facts            -> <link> v<> <date>
[ ] Inventory entry         -> <link> v<> <date>
[ ] Use-case triage         -> <link> v<> <date>
[ ] AIA / impact assessment -> <link> v<> <date>
[ ] Vendor AI terms review   -> <link> v<> <date>
[ ] Reg gap analysis        -> <link> v<> <date>

## Decision log (append-only)
<date> — <decision> — rationale: <...> — accountable: <name/role>

## Sign-off roster
<role> — <name> — gate: <> — status: pending/approved — <date>

## Retention & traceability
Review period: <>   Evidence links: <>   Retain until: <retired + N yrs>

Decision-support only. Qualified attorney must review before legal reliance or filing.
```

## Reference

### What a defensible AI-governance record needs

A record is "defensible" when a regulator, auditor, or court can reconstruct the decision without trusting anyone's memory. Five load-bearing elements:

| Element | What it proves | Failure if absent |
|---------|----------------|-------------------|
| **Versioning** | Which exact artifact was approved | Can't show what was actually relied on |
| **Decision log** | What was decided, when, why, by whom | Rationale looks reconstructed / post-hoc |
| **Sign-off roster** | Accountability by role, with gates | No provable ownership of the call |
| **Evidence links** | Claims backed by source artifacts | Assertions unsupported |
| **Retention** | Record survives as long as liability does | Evidence gone when a claim arrives |

### Mapping to NIST AI RMF (GOVERN and MANAGE)

The AI Risk Management Framework organizes work into four functions: **GOVERN, MAP, MEASURE, MANAGE**. The matter workspace is primarily a GOVERN and MANAGE instrument.

| RMF function | What the workspace supplies |
|--------------|------------------------------|
| **GOVERN** | Accountability structures (sign-off roster, named owners), documentation and record-keeping, policies applied to this system, roles and escalation |
| **MAP** | Context and intake facts, use-case triage, inventory linkage (populated by sibling skills) |
| **MEASURE** | Links to AIA metrics, testing/eval evidence, identified risks |
| **MANAGE** | Ongoing-monitoring artifacts, re-review cadence, decision log of risk-treatment calls, status lifecycle |

GOVERN's emphasis on accountability and documentation maps directly to the decision log + roster; MANAGE's ongoing-monitoring expectation maps to the status lifecycle and the re-review clock. Treat the workspace as where GOVERN's paper trail and MANAGE's monitoring artifacts actually live for one system.

### EU AI Act technical documentation & record-keeping (high-risk)

For high-risk systems, the EU AI Act expects providers/deployers to maintain **technical documentation** and **record-keeping** demonstrating conformity — kept current and available to authorities. Relevant expectations the workspace should be able to satisfy:

- **Technical documentation** describing the system, its purpose, design, and risk-management steps (the AIA and gap-analysis slots feed this).
- **Automatic logging / traceability** over the system's lifecycle, so events and decisions can be reconstructed.
- **Record retention** for a defined period after the system is placed on the market or put into service.
- **Post-market monitoring** — documented ongoing observation of the deployed system (the MONITORING status and re-review cadence).

Why retention and traceability matter for **liability**: if the system causes harm, the organization's defense is its documented, contemporaneous diligence. A traceable, retained, version-controlled matter record is the difference between "we assessed and mitigated this on <date>, approved by <roles>" and an unprovable claim. Treat all specific obligations, thresholds, and dates as **to-verify with counsel** — the Act's applicability and requirements are phased and detailed, and this skill organizes evidence rather than interpreting the law.
