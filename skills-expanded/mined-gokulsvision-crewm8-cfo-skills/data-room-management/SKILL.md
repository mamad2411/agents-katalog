---
name: data-room-management
description: Build and maintain the investor data room — organize financials, metrics, legal docs, contracts, and customer references for fundraising due diligence. Use when the user asks about setting up a data room, organizing documents for due diligence, or preparing for an investor audit.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, fundraising, data-room, due-diligence]
related_skills:
  - fundraising-financials
  - fundraising-process-management
  - cap-table-management
  - financial-statement-generation
  - board-reporting
  - monthly-close-process
inputs_required:
  - existing-document-inventory-financials-legal-metrics-contracts
  - fundraise-stage-pre-seed-seed-series-A-B
  - data-room-platform-google-drive-dropbox-docsend-notion
deliverables:
  - data-room-structure-audit-with-status-per-folder
  - prioritized-gap-fill-plan-with-owners-and-deadlines
  - access-log-and-investor-readiness-checklist
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Data Room Management

Build and maintain a comprehensive investor data room. Structure the folder hierarchy, collect and organize all documents, track what's missing, maintain version control, and prepare for due diligence. Goal: when an investor asks for something, the answer is "it's already in the data room."

## Purpose

Speed wins in fundraising. A well-organized data room that answers diligence questions before they're asked can compress a 3-month process into 6 weeks. This skill ensures every document an investor might want is already organized, current, and accessible — so the team spends time on the pitch, not hunting for files.

## When to Use

- "Set up / organize our investor data room"
- "What's missing from our data room?"
- "Organize these documents for due diligence"
- "Create a data room checklist"
- "Update the data room for our next fundraise"

## Inputs Required

1. **Existing document inventory** — whatever financials, legal docs, metrics, and contracts already exist.
2. **Fundraise stage** — pre-seed, seed, Series A, Series B (determines the depth needed).
3. **Data room platform** — Google Drive, Dropbox, Docsend, Notion, dedicated VDR (FirmRoom, Intralinks).

## Quick Reference

| Tier | Access Level | Contents |
|---|---|---|
| Tier 1 (Public preview) | Anyone with link | Pitch deck, one-pager |
| Tier 2 (Signed NDA) | Tracked views | Financials, customer list, cap table |
| Tier 3 (Term sheet received) | Full access | Legal diligence, contracts, employment agreements |
| **Priority order** | **1. Financials** | **2. Customers** → **3. Legal** → **4. Everything else** |

## Procedure

### 1. Audit Current State

For each folder below, mark status:
- ✅ Complete & current
- ⚠️ Exists but stale (> 3 months old)
- ❌ Missing

### 2. Fill Gaps

Prioritize: Financials (03) > Customers (06) > Legal (07) > Everything else.

Hand off to the respective skills:
- Historical financials & forecast → `financial-statement-generation`, `revenue-forecasting`
- Unit economics → `unit-economics-analysis`
- Cap table → `cap-table-management`

### 3. Version Control & Redaction

- **Naming convention**: `[Document] — [Date] v[X] — [Status].pdf`
- **Redact PII**: customer names in public documents if customers haven't consented.
- **Audit trail**: who uploaded what and when.

### 4. Access Control

- **Tier 1 (public preview)**: pitch deck, one-pager. Anyone with the link.
- **Tier 2 (signed NDA)**: financials, customer list, cap table. Track who views.
- **Tier 3 (term sheet received)**: full legal diligence, material contracts, employment agreements.

### 5. Maintain

- Update financials after every monthly close (`monthly-close-process`).
- Refresh team page after every hire/departure.
- Quarterly full audit of the data room.

### Standard Folder Hierarchy

```
📁 01 — Company Overview
  ├── Company one-pager / pitch deck
  ├── Mission, vision, values
  ├── Founding story / origin
  └── Press mentions, awards, recognition

📁 02 — Team
  ├── Org chart
  ├── Founder bios & LinkedIn links
  ├── Key hire bios
  └── Advisor list with bios

📁 03 — Financials
  ├── Historical P&L (monthly, last 2-3 years)
  ├── Historical balance sheet (quarterly at minimum)
  ├── Historical cash flow statements
  ├── Annual budget & forecast (3-year projection)
  ├── Unit economics model (CAC, LTV, payback by segment)
  ├── Revenue by customer / cohort analysis
  ├── Burn multiple and efficiency metrics
  └── Cap table (fully diluted, including SAFEs/notes)

📁 04 — Product & Technology
  ├── Product overview / screenshots / demo video link
  ├── Product roadmap (current + next 12-18 months)
  ├── Architecture overview
  ├── IP / patents / trademarks
  └── Security certifications (SOC 2, ISO 27001, etc.)

📁 05 — Market & Competition
  ├── TAM / SAM / SOM analysis
  ├── Competitive landscape / battle cards
  ├── Market trends & analyst reports
  └── Customer segments and personas

📁 06 — Go-To-Market & Customers
  ├── Customer list (anonymized or named, with ARR)
  ├── Top 10 customer case studies / references
  ├── NPS scores / CSAT data
  ├── Sales playbook / GTM strategy doc
  └── Channel / partner strategy

📁 07 — Legal & Compliance
  ├── Certificate of incorporation
  ├── Bylaws / operating agreement
  ├── All financing docs (SAFEs, notes, stock purchase agreements)
  ├── Material contracts (top customers, top vendors)
  ├── Employment / IP assignment agreements
  ├── Privacy policy, terms of service
  ├── Compliance certifications (GDPR, CCPA)
  └── Any litigation / disputes (current or threatened)

📁 08 — Fundraise-Specific
  ├── Use of funds
  ├── Target raise amount & structure rationale
  ├── Current cap table (detailed)
  ├── Pro forma cap table post-raise
  └── Comparable exits / valuation comps
```

## Output Format

- Data room structure audit (what's in each folder, what's current, what's missing)
- Prioritized gap-fill plan with responsible owners and deadlines
- Access log (who's viewed what, for tiered data rooms)
- Checklist: is the data room "investor-ready"?

## Done Criteria

The skill is complete when:
1. Every folder in the standard hierarchy is audited (complete, stale, or missing)
2. A prioritized gap-fill plan is produced with owners and deadlines
3. Documents follow the naming convention and PII is redacted
4. Access controls are set up per tier
5. The data room is assessed as "investor-ready" or a remediation plan is provided

## Pitfalls

- **Over-preparing for the wrong stage**: building a Series B-level data room at seed wastes time. Match depth to the fundraise stage.
- **Hiding problems**: regulatory investigations, co-founder disputes, and lawsuits will be found. Prepare a concise, factual document rather than hoping they're missed.
- **Missing IP assignments**: every founder and employee must have signed IP assignment. This is the #1 diligence kill-switch.
- **Including full customer names without consent**: redact or use "Enterprise SaaS Company ($500k ARR)" format.
- **Letting the data room go stale**: financials from 6 months ago signal disorganization. Refresh after every monthly close.

## Verification

Can an investor find the last 12 months of financials, the cap table, and the customer list within 5 minutes of accessing the data room? Are all documents current (within 90 days)? Are stale or missing items tracked in a remediation plan? If not, the data room is not investor-ready.

## Example

**User prompt**: "Set up / organize our investor data room."
**What should happen**: Audit the current state of all 8 folders in the standard hierarchy, mark each as complete/stale/missing, produce a prioritized gap-fill plan with owners and deadlines, set up access controls per tier, and provide a checklist confirming the data room is investor-ready or detailing what's needed.

**User prompt**: "What's missing from our data room?"
**What should happen**: Compare the current data room contents against the standard hierarchy, flag every folder that is incomplete or stale, rank gaps by priority (financials first, then customers, then legal), and produce a remediation plan with estimated effort to fill each gap.

## Linked Skills

- Build fundraising financial model → `fundraising-financials`
- Plan fundraise timeline & strategy → `fundraising-process-management`
- Cap table → `cap-table-management`
- Generate financial statements → `financial-statement-generation`
- Board & investor materials → `board-reporting`
- Keep financials current → `monthly-close-process`
