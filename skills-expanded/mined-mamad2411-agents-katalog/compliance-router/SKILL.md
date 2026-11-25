---
name: compliance-router
description: Entry point for any compliance, privacy, security-standard or regulatory question about this HMS. Decides which jurisdictions and which of the three surfaces (frontend, backend, CI/CD) are in scope, then names the specific skills to load. Use before any audit, gap analysis, grid refresh, or "are we compliant with X" question.
---

# Compliance router

Nothing in this stack applies blanket. This skill decides **what is actually in scope** before any
other compliance skill runs. Applying every framework to every module is the failure mode that
makes compliance work worthless.

## Step 1 — Establish deployment facts

Never assume. Ask, or read from the tenant config, before routing:

1. Where is the **property** (hotel) physically located?
2. Where is the **operating company** incorporated?
3. Where is this instance **hosted** — Azure region, S3 region, DB region?
4. Where does **guest data come to rest** (DB, object storage, backups, logs, analytics)?
5. Which **third parties receive personal data** (payment gateway, SMS/WhatsApp, email, OpenAI/LM Studio, OTA)?
6. Is this a **hosted multi-tenant** deployment, a single-tenant cloud deployment, or a standalone on-prem install?
7. Does the payment flow ever put **cardholder data** in our systems, or is it fully redirect/hosted-field?
8. Do the guests include **EU/EEA residents** or **California residents**?
9. Is any **AI feature** guest-facing or used in a decision about a person?

If an answer is unknown, say so in the output and mark affected grid rows `unknown-scope` —
do not guess a jurisdiction.

## Step 2 — Route jurisdictions

Priority order for this product: **Saudi Arabia → wider MENA → Pakistan → international**.

| Trigger | Load |
|---|---|
| Property or data in Saudi Arabia (default assumption for this product) | `ksa-pdpl`, `ksa-nca-controls`, `ksa-zatca-einvoicing`, `ksa-hospitality-reporting` |
| Property in UAE, Qatar, Bahrain, Oman, Kuwait, Egypt, Jordan | `mena-jurisdictions` (per-country; UAE also splits federal vs DIFC vs ADGM) |
| Property, company or invoicing in Pakistan | `pakistan-compliance` |
| EU/EEA guests, or an EU-facing booking site | `intl-privacy-laws` (GDPR + ePrivacy) |
| California consumers over CCPA thresholds | `intl-privacy-laws` (CCPA/CPRA) |
| US protected health information | `intl-privacy-laws` (HIPAA gate — normally N/A here) |

There is no such thing as "MENA compliance". MENA is a market grouping; each country has its own
regulator. Route per country or say nothing.

## Step 3 — Route the framework layer

Always in scope for this product, regardless of jurisdiction:

- `owasp-appsec` — ASVS 5.0 is the requirement source for both app surfaces
- `iso-27k-family` — 27001/27002 ISMS, 27701 privacy, 27017/27018 cloud
- `soc2-trust-criteria` — what enterprise hotel-group buyers will ask for
- `nist-csf` — risk framing and cross-walks
- `secure-sdlc-supply-chain` — SSDF, SLSA, SBOM, vuln management, pentest
- `management-systems` — ISO 9001 quality, ISO 22301 continuity/DR

Conditionally:

- `pci-dss-scoping` — whenever payments, folios, refunds or card data are in the picture
- `ai-governance` — whenever OpenAI, LM Studio, an AI CI agent or automated decisioning is involved
- `hms-data-lifecycle` — whenever the question touches guest personal data (nearly always)

## Step 4 — Route the surface

**Treat the three surfaces separately. Never merge their findings into one verdict.**

| Surface | Skill | Covers |
|---|---|---|
| Frontend | `frontend-compliance` | `frontend/` — Vite/React SPA, build-baked env, browser storage, consent, headers |
| Backend | `backend-compliance` | `backend/` — Express APIs, DB, auth, tenancy, integrations, retention, logs |
| CI/CD & deployment | `cicd-compliance` | `.github/workflows/`, `backend/.github/workflows/`, Dockerfiles, Azure Container Apps, ACR |

A control can land on one, two or all three surfaces with a different verdict on each. Encryption
in transit may be fine at the edge and absent between the container and the database; those are two
rows, not one.

## Step 5 — Sources

Every factual claim must trace to an entry in `compliance/sources/REGISTRY.yaml`. Load
`compliance-sources` for the citation and freshness rules before asserting any legal requirement.

## Output contract

Produce, in this order:

1. **Scope statement** — the deployment facts used, and which were unknown.
2. **In-scope list** — jurisdictions and frameworks, each with the registry id that makes it apply.
3. **Explicitly out-of-scope list** — with the reason (this is as valuable as the in-scope list; it
   is what stops the next person re-litigating HIPAA).
4. **Skills to load next.**
