---
name: soc2-trust-criteria
description: SOC 2 Trust Services Criteria and Type II readiness — what the criteria require, which categories to scope, and how a SOC 2 engagement differs from an ISO certification. Use when preparing for enterprise or hotel-group due diligence, or mapping controls to CC-series criteria.
---

# SOC 2

Registry: `SOC2-TSC`. Publisher: AICPA.

**Current criteria: the 2017 Trust Services Criteria with the 2022 revised points of focus.**
There is no 2025 revision. The 2022 update changed *points of focus* only — guidance on applying
the criteria — not the criteria themselves. Areas it touched: availability, confidentiality and
privacy criteria; remote-workforce controls (asset recovery on termination, physical and digital
access restrictions); and change management (segregation of duties, patch management).

## What SOC 2 actually is

An **attestation report** produced by a CPA firm, not a certificate. Two forms:

- **Type I** — controls suitably designed at a point in time. Fast, and of limited value.
- **Type II** — controls operated effectively over a period, typically 3–12 months. **This is what
  hotel groups and enterprise buyers mean when they say "SOC 2".**

The consequence for planning: Type II requires an **observation window with evidence**. You cannot
fix everything the week before. Access reviews, change tickets, vulnerability scan results,
incident records and backup tests must exist as a *history*. Start generating that evidence now,
even if the audit is a year out — that is the single highest-leverage action for this product's
enterprise readiness.

## Category scoping

| Category | Include? |
|---|---|
| **Security** (Common Criteria) | Mandatory — always in scope |
| **Availability** | Yes — a PMS that is down stops a hotel from checking guests in |
| **Confidentiality** | Yes — guest identity documents, commercial rate data |
| **Processing Integrity** | Consider — billing, folio and fiscal invoice correctness is a genuine integrity claim |
| **Privacy** | Optional; often better served by `ISO-27701` + PDPL work than by the SOC 2 privacy category |

Scoping every category by default is a common and expensive mistake. Scope Security + Availability +
Confidentiality unless a buyer asks otherwise.

## Common Criteria, mapped to this system

| CC | Theme | Where it bites here |
|---|---|---|
| CC1 | Control environment | Organisational — policies, roles, background checks |
| CC2 | Communication and information | Documented policies reaching the team |
| CC3 | Risk assessment | Documented, periodic, covering the third-party integrations |
| CC4 | Monitoring activities | Internal review cadence |
| CC5 | Control activities | The controls themselves |
| CC6 | **Logical and physical access** | Auth, RBAC, tenancy isolation, MFA on admin and cloud, secrets, key management, offboarding |
| CC7 | **System operations** | Monitoring, vulnerability management, incident detection and response |
| CC8 | **Change management** | The CI/CD surface — approvals, testing, separation of environments |
| CC9 | Risk mitigation | Vendor management, business continuity, insurance |

CC6, CC7 and CC8 are where engineering evidence lives; the rest is documentation. In the grid, CC8
rows belong to the **CI/CD** surface — this is the clearest reason to keep the three grids separate.

## Relationship to the rest of the stack

CC-criteria map onto `ISO-27002` controls and `SA-NCA-ECC` almost one-for-one. Implement once,
evidence once, cite three ways. Where a Saudi tenant asks for ECC and a European chain asks for
SOC 2, the underlying work is largely the same — the reports differ.

SOC 2 does **not** satisfy PDPL, GDPR or PCI DSS. Buyers sometimes assume it does; it does not, and
saying so plainly is better than letting the assumption ride.
