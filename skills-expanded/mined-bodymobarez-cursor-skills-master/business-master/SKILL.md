---
name: business-master
description: >-
  Master hub for B2B business systems & platforms at staff/principal depth. Use to build CRM,
  ERP, double-entry accounting/finance, a complete A→Z accounting system (full menus), affiliate/
  referral programs, white-label/multi-tenant products, Postgres multi-tenant isolation (RLS), and
  VAT/e-invoicing compliance (ZATCA, UAE Peppol, EU ViDA). Bundles 8 specialized skills in
  skills/<name>/GUIDE.md. Use for any business-platform, SaaS back-office, CRM, ERP, accounting,
  billing, tenancy, tax, or white-label task.
---

# Business Systems & Platforms — Master Hub

Build correct, auditable, multi-tenant back-office and platform software: CRM, ERP, accounting,
affiliate programs, white-label products — on a shared foundation of **tenant isolation** and
**tax/e-invoicing compliance**. Money must be double-entry and auditable; tenants must be unreachable
from one another by construction; tax must be compliant where mandated. These are not optional polish.

## How to use this hub

Each bundled skill's full instructions live in `skills/<name>/GUIDE.md`. **Read the relevant GUIDE
before acting**, and combine skills when a task spans areas — most real systems do.

**Two foundational skills almost every task depends on:**
- **`multi-tenant-isolation`** — read it whenever the system serves more than one customer/org.
- **`accounting-finance`** — read it whenever money moves (ERP, affiliate payouts, billing).

## Bundled skills (8)

- **crm-builder** — Contacts/accounts, configurable pipelines & kanban, weighted forecast, typed
  activities, lead scoring, customer 360, dedup/merge, and **SQL-enforced** record permissions.  
  → `skills/crm-builder/GUIDE.md`
- **erp-builder** — Modular monolith on one ledger: master data, perpetual inventory valuation
  (FIFO/AVG/STD), stock-move↔journal atomicity, 3-way match, document state machines, gapless numbering.  
  → `skills/erp-builder/GUIDE.md`
- **accounting-finance** — Double-entry ledger as source of truth: integer-minor-unit money, idempotent
  posting, AR/AP, multi-currency (IAS 21), period close, reversals/credit notes, derived statements.  
  → `skills/accounting-finance/GUIDE.md`
- **accounting-system-complete** — The full A→Z accounting **application**: COA, fiscal periods, GL,
  AR/AP + aging, banking + reconciliation, tax, fixed assets/depreciation, multi-currency, budgeting,
  period/year-end close, and derived statements (TB/P&L/Balance Sheet/Cash Flow) + the full menu/IA.  
  → `skills/accounting-system-complete/GUIDE.md`
- **affiliate-system** — Server-side attribution (click_id + cookie + coupon), idempotent conversions,
  percent/flat/tiered/recurring commissions, pending→approved→paid with clawback, ledgered payouts, fraud defense.  
  → `skills/affiliate-system/GUIDE.md`
- **white-label-platform** — One codebase, N brands: host→tenant resolution, custom domains + automated
  ACME TLS, runtime CSS-variable theming, white-labeled emails/PDFs/auth, feature flags, reseller layer, billing.  
  → `skills/white-label-platform/GUIDE.md`
- **multi-tenant-isolation** *(foundational)* — Postgres RLS (`ENABLE`+`FORCE`, `SET LOCAL` under
  PgBouncer), shared-DB vs schema/DB-per-tenant trade-offs, RBAC→ABAC→ReBAC, sharding, residency, cross-tenant tests.  
  → `skills/multi-tenant-isolation/GUIDE.md`
- **einvoicing-compliance** *(foundational for money)* — One VAT engine + 2026 mandates: KSA ZATCA Phase 2
  (clearance, UBL 2.1, CSID, PIH hash chain, TLV QR), UAE Peppol/PINT AE via ASP, EU ViDA/EN 16931, Arabic/RTL invoices.  
  → `skills/einvoicing-compliance/GUIDE.md`

## Routing

| User wants… | Start with | Usually also read |
|-------------|------------|-------------------|
| Sales pipeline / leads / deals | `crm-builder` | `multi-tenant-isolation` |
| Inventory / orders / procurement / mfg | `erp-builder` | `accounting-finance`, `einvoicing-compliance` |
| Invoices / ledger / payments / statements | `accounting-finance` | `einvoicing-compliance` |
| Full accounting app (modules + menus A→Z) | `accounting-system-complete` | `accounting-finance` |
| VAT / ZATCA / UAE / EU e-invoicing | `einvoicing-compliance` | `accounting-finance` |
| Referral / affiliate / partner payouts | `affiliate-system` | `accounting-finance` |
| Reseller / multi-brand / custom domains | `white-label-platform` | `multi-tenant-isolation` |
| "Keep tenants' data separate" | `multi-tenant-isolation` | — |

## Pairs well with

`backend-api-master` (auth, Stripe, integrations), `payments-master` (gateways/payouts),
`tailwind-master` (`tailwind-design-tokens` for white-label theming, RTL/Arabic), `ui-master`
(`charts-and-dashboards` for reporting), `marketplace-master` (multi-vendor commerce).

## Note

Bundled skills are intentionally `GUIDE.md` (not `SKILL.md`) so only this master appears in the skills
list. Money/tax code: implement to the user's local standard (IFRS/GAAP, local tax law) and recommend a
professional review for regulated/audited books.
