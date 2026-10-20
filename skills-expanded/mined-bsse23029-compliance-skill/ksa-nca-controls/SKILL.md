---
name: ksa-nca-controls
description: Saudi National Cybersecurity Authority controls — ECC-2:2024 Essential Cybersecurity Controls and CCC-2:2024 Cloud Cybersecurity Controls — plus the CST Cloud Computing Regulatory Framework and Saudi data-residency classification. Use for security-control and cloud-hosting questions in a Saudi deployment.
---

# Saudi NCA controls and cloud regulation

Registry: `SA-NCA-ECC`, `SA-NCA-CCC`, `SA-CST-CCRF`.

- **ECC-2:2024** — supersedes ECC-1:2018. 4 domains, 28 subdomains, 108 main controls, 92
  subcontrols. The Saudi security baseline.
- **CCC-2:2024** — modular extension for cloud. Binds **Cloud Service Tenants**, not just providers.
  We are a CST of Azure, so the CST control set applies to us directly.
- **CST CCRF** — cloud regulatory framework from the Communications, Space and Technology
  Commission; data classification levels, with **levels 3–4 carrying in-Kingdom residency
  expectations**. *Version unverified in the registry — confirm before citing a level.*

Both NCA pages refused connection from automated tooling on 2026-08-20; fetch the PDFs manually.

Who is bound is a question of contract and sector as much as law: NCA controls are mandatory for
Saudi government and critical national infrastructure, and they flow down through procurement to
vendors. For a hotel-sector SaaS the practical position is that **Saudi enterprise buyers will ask
for ECC alignment**, and any government or CNI-adjacent tenant will require it. Treat it as a
buyer requirement with regulatory teeth rather than debating direct applicability.

## Control checklist

| ID | Requirement | Surfaces |
|---|---|---|
| NCA-01 | Cybersecurity governance: documented policies, defined ownership, periodic review | organisational |
| NCA-02 | Asset inventory covering systems, data stores and third-party services | backend, cicd |
| NCA-03 | Identity and access management: least privilege, unique identities, privileged access control, MFA on administrative access | backend, cicd |
| NCA-04 | Data classification, and handling rules per class — identity documents and payment data at the top | backend |
| NCA-05 | Cryptography: encryption in transit and at rest, key management and rotation | backend, cicd |
| NCA-06 | Secure configuration and hardening of servers, containers and the web tier | cicd |
| NCA-07 | Vulnerability management: scanning cadence, remediation SLAs by severity, patching | cicd, backend |
| NCA-08 | Penetration testing on a defined cycle and after material change | all |
| NCA-09 | Event logging and continuous monitoring with retention | backend, cicd |
| NCA-10 | Incident response plan, roles, and reporting obligations — including to the NCA where applicable | organisational |
| NCA-11 | Backup, recovery and tested restoration | backend, cicd |
| NCA-12 | Third-party and outsourcing cybersecurity requirements flowed down to vendors | organisational |
| NCA-13 | Secure development lifecycle and change management | cicd |
| NCA-14 | Web application protection for internet-facing services | frontend, backend |
| CCC-01 | Tenant data separation — no cross-tenant access in a shared environment | backend |
| CCC-02 | Data returned in a usable format at end of service, and securely deleted afterwards | backend |
| CCC-03 | Cloud responsibility split documented: what Azure covers vs what we cover | cicd |
| CCC-04 | Cloud data location and classification consistent with CCRF and PDPL transfer rules | cicd |
| CCC-05 | Cloud incident reporting paths, including provider-side incidents | cicd |

## How this pairs with the international standards

ECC maps closely onto `ISO-27002` controls and `SOC2-TSC` CC-series criteria; CCC-2:2024 maps onto
`ISO-27017`/`ISO-27018`. Where a tenant asks for ISO 27001 *and* ECC, build the control set once and
cross-walk — but keep the citations distinct in the grid, because the audit evidence differs.

CCC-01 (tenant separation) and `backend-compliance` B-01 are the same control seen from two sides.
Grade it once in the backend grid, cite both.
