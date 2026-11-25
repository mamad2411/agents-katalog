---
name: plan-decompose
description: Use when running /plan:decompose or /plan:epic to create BudFin GitHub Epics. Provides canonical Epic definitions with rich summaries, dependency maps, MoSCoW priorities, and tier classifications. Load before creating any Epic issues.
invocations:
  - user: /plan-decompose
  - agent: plan-decompose
---

# plan-decompose

## Overview

This skill provides the canonical BudFin Epic catalog. Every Epic created from `/plan:decompose` or `/plan:epic` must use the definitions here — no placeholders, no deferred summaries, no generic templates.

**Core principle:** Epics are the contract between planning and implementation. A thin Epic with `[...]` placeholders ships confusion. A rich Epic ships clarity.

## What a World-Class Epic Looks Like

Before creating any issue, verify:

- **Summary**: 3–4 sentences. Opens with "Epic N delivers...". Names the PRD section it maps to. States what EFIR staff can do after it ships.
- **Dependencies**: Table with `| Epic | Feature | Reason |` rows. Reasons are specific (e.g., "Revenue calculation requires enrollment counts from Epic 1 data"). Never write "depends on" without a reason.
- **Stories**: Always write "Will be created in Phase 4 via `/plan:stories`." Never pre-populate.
- **MoSCoW label**: Lowercase on the GitHub label (`must-have`, `should-have`). Title Case in the issue body ("Must Have").
- **Tier**: Capitalized ("MVP", "Target", "Stretch").

**Forbidden phrases in summaries:** "This feature...", "TBD", "[...]", "see PRD", "placeholder".

---

## Canonical Epic Catalog

### Epic 1 — Enrollment & Capacity

- **MoSCoW**: Must Have | **Tier**: MVP
- **PRD section**: §8.1 (FR-ENR-*, FR-CAP-*)
- **Dependencies**: None (foundational)

**Summary**: Epic 1 delivers the Enrollment & Capacity planning module, enabling EFIR finance staff to enter, validate, and lock annual enrollment projections per division and academic year. It implements the capacity ceiling rules (FR-CAP-001 through FR-CAP-003) and the enrollment-to-revenue driver relationship that all downstream financial modules depend on. Without confirmed enrollment figures, revenue, staffing ratios, and P&L calculations cannot be initialized for any budget version.

**Dependency table**: None — this is a foundational epic.

---

### Epic 2 — Revenue

- **MoSCoW**: Must Have | **Tier**: MVP
- **PRD section**: §8.2 (FR-REV-*)
- **Dependencies**: Epics 1, 7, 11

**Summary**: Epic 2 delivers the Revenue forecasting module, implementing EFIR's dual academic-calendar revenue engine (French academic year Sept–June + summer session) with IFRS 15 revenue recognition rules. It calculates tuition, registration fees, and ancillary income by division using enrollment counts from Epic 1 and fee schedule master data from Epic 7. EFIR finance staff can produce per-division and consolidated revenue projections that reconcile exactly with the existing Excel Revenue workbook.

**Dependency table**:

| Epic | Feature | Reason |
|------|---------|--------|
| 1 | Enrollment & Capacity | Revenue calculation multiplies fee rates by per-division enrollment counts |
| 7 | Master Data Management | Fee schedules, division definitions, and academic year config live in master data |
| 11 | Authentication & RBAC | Revenue module requires Finance role write access enforced at the API layer |

---

### Epic 3 — Staffing (DHG)

- **MoSCoW**: Must Have | **Tier**: MVP
- **PRD section**: §8.3 FR-DHG-* subset
- **Dependencies**: Epics 7, 11

**Summary**: Epic 3 delivers the DHG-based staffing model, enabling EFIR to define and calculate full-time-equivalent (FTE) staff requirements per curriculum section using the Division-Hours-Group (DHG) formula. Finance and HR staff can assign teaching loads, compute required FTEs by department, and produce the staffing headcount grid that feeds directly into staff cost calculations in Epic 4. The module maps to the DHG Staffing Excel workbook and must reproduce its FTE outputs with zero discrepancy.

**Dependency table**:

| Epic | Feature | Reason |
|------|---------|--------|
| 7 | Master Data Management | Staff grades, department codes, and curriculum section definitions are master data |
| 11 | Authentication & RBAC | HR role is required for DHG input; Finance role for read-only access |

---

### Epic 4 — Staff Costs

- **MoSCoW**: Must Have | **Tier**: MVP
- **PRD section**: §8.3 FR-STC-* subset
- **Dependencies**: Epics 3, 7, 11

**Summary**: Epic 4 delivers staff cost budgeting, calculating gross salaries, Saudi statutory costs (GOSI 10%, Ajeer levy, End-of-Service provision), and housing/transport allowances for every position in the DHG headcount grid. It uses YEARFRAC proration (TC-002) for mid-year joiners and leavers, stores all monetary values via pgcrypto encryption (5 salary fields), and produces the staff cost totals that feed the P&L module. All results must reconcile with the Staff Costs Excel workbook to zero discrepancy.

**Dependency table**:

| Epic | Feature | Reason |
|------|---------|--------|
| 3 | Staffing (DHG) | FTE headcount and position records from Epic 3 are the input rows for cost calculation |
| 7 | Master Data Management | Salary grade scales, statutory rate constants, and allowance rules are master data |
| 11 | Authentication & RBAC | Salary data is confidential; HR Director role required for write access |

---

### Epic 5 — P&L Reporting

- **MoSCoW**: Must Have | **Tier**: MVP
- **PRD section**: §8.4 (FR-PNL-*)
- **Dependencies**: Epics 2, 3, 4

**Summary**: Epic 5 delivers the consolidated P&L (Profit & Loss) reporting module, aggregating revenue from Epic 2 and staff costs from Epic 4 into IFRS-compliant financial statements with Gross Margin, EBITDA, and Net Surplus rows. Finance staff can view P&L by budget version (Actual, Budget, Forecast), compare two versions side-by-side using the Version Comparison Engine, and export reports to PDF using @react-pdf/renderer. This module is the primary deliverable that replaces the Consolidated Budget Excel workbook.

**Dependency table**:

| Epic | Feature | Reason |
|------|---------|--------|
| 2 | Revenue | P&L aggregates revenue totals by division and version |
| 3 | Staffing (DHG) | P&L includes headcount summary rows sourced from the staffing grid |
| 4 | Staff Costs | Staff costs are the largest expense line on the P&L |

---

### Epic 6 — Scenario Modeling

- **MoSCoW**: Should Have | **Tier**: Target
- **PRD section**: §8.5 (FR-SCN-*)
- **Dependencies**: Epic 5

**Summary**: Epic 6 delivers scenario modeling, allowing finance staff to clone any existing budget version, apply enrollment or cost assumptions (e.g., +5% enrollment, salary freeze), and immediately see the P&L impact without overwriting the base version. It implements the "what-if" branching described in FR-SCN-001 through FR-SCN-004 and integrates with the Version Management system from Epic 10. Scenarios are read-only outputs — they cannot be promoted to Actual or Budget without explicit promotion workflow.

**Dependency table**:

| Epic | Feature | Reason |
|------|---------|--------|
| 5 | P&L Reporting | Scenarios recalculate the full P&L pipeline; the reporting module must exist first |

---

### Epic 7 — Master Data Management

- **MoSCoW**: Must Have | **Tier**: MVP
- **PRD section**: §8.6 (FR-MDM-*)
- **Dependencies**: Epic 11

**Summary**: Epic 7 delivers the Master Data Management module, providing CRUD interfaces for all reference data that other modules consume: fee schedules, division definitions, academic year calendars, staff grade scales, statutory rate constants, department codes, and curriculum section templates. Admin-role users maintain master data through validated forms; changes are recorded in the audit trail. No planning module can be initialized without the reference data this epic supplies, making it a direct prerequisite for Epics 2, 3, and 4.

**Dependency table**:

| Epic | Feature | Reason |
|------|---------|--------|
| 11 | Authentication & RBAC | Admin role is required to mutate master data; role enforcement is at the API layer |

---

### Epic 8 — Audit Trail

- **MoSCoW**: Should Have | **Tier**: Target
- **PRD section**: §8.7 (FR-AUD-*)
- **Dependencies**: Epic 11

**Summary**: Epic 8 delivers the Audit Trail module, recording every data mutation (create, update, delete) with user identity, timestamp, before/after field values, and the budget version context. Finance staff and auditors can filter the log by user, date range, module, and entity type. Per D-005, CSV export is deferred to v2; v1 delivers on-screen browsing with pagination. The audit log is append-only at the database level and satisfies the external auditor persona's traceability requirements.

**Dependency table**:

| Epic | Feature | Reason |
|------|---------|--------|
| 11 | Authentication & RBAC | Audit records must capture authenticated user identity from the JWT claims |

---

### Epic 9 — Dashboard

- **MoSCoW**: Should Have | **Tier**: Target
- **PRD section**: §8.8 (FR-DSH-*)
- **Dependencies**: Epics 2, 3, 4, 5

**Summary**: Epic 9 delivers the Dashboard module — the default landing screen after login — displaying KPI tiles for enrollment actuals vs. budget, revenue vs. target, staff cost variance, and net surplus for the active budget version. Charts are built with Recharts on top of aggregated data already computed by Epics 2–5. The dashboard is read-only and does not introduce new data entry; it surfaces existing calculations in a consumable executive summary format for the CAO and finance director personas.

**Dependency table**:

| Epic | Feature | Reason |
|------|---------|--------|
| 2 | Revenue | Dashboard revenue KPI reads from the revenue aggregation computed by Epic 2 |
| 3 | Staffing (DHG) | Dashboard headcount tile reads FTE totals from the staffing grid |
| 4 | Staff Costs | Dashboard cost variance tile reads staff cost totals from Epic 4 |
| 5 | P&L Reporting | Dashboard net surplus tile reads from the P&L calculation in Epic 5 |

---

### Epic 10 — Version Management

- **MoSCoW**: Should Have | **Tier**: Target
- **PRD section**: §7 (FR-VER-001 – FR-VER-006)
- **Dependencies**: Epic 5

**Summary**: Epic 10 delivers the Version Management system, enabling finance staff to create, name, lock, and compare budget versions of type Actual, Budget, and Forecast. The Comparison Engine (§7.3) produces side-by-side variance reports between any two versions in absolute and percentage terms. Locking a version makes all its planning data immutable. This epic implements the persistent Context Bar's version selector (§6.1) that appears on every planning screen and drives which version's data is displayed.

**Dependency table**:

| Epic | Feature | Reason |
|------|---------|--------|
| 5 | P&L Reporting | Version comparison renders variance at the P&L level; the P&L pipeline must exist first |

---

### Epic 11 — Authentication & RBAC

- **MoSCoW**: Must Have | **Tier**: MVP
- **PRD section**: §11.3 (RBAC matrix, NFR-SEC-*)
- **Dependencies**: Epic 13

**Summary**: Epic 11 delivers the authentication and role-based access control system using RS256-signed JWTs with access tokens in memory and refresh tokens in HTTP-only SameSite=Strict cookies scoped to `/api/v1/auth`. It implements the 5-role RBAC matrix (Admin, Finance Director, Finance Staff, HR Director, Auditor) with route-level enforcement via Fastify preHandlers. Token family rotation detects refresh token theft. Every other API epic gates its routes with RBAC preHandlers, making this a hard dependency for all backend work.

**Dependency table**:

| Epic | Feature | Reason |
|------|---------|--------|
| 13 | Infrastructure & CI/CD | JWT RS256 key pair is generated and injected via Docker secret; infra must exist first |

---

### Epic 12 — Data Migration

- **MoSCoW**: Must Have | **Tier**: MVP
- **PRD section**: §13 (Data Migration Strategy)
- **Dependencies**: Epics 7, 11

**Summary**: Epic 12 delivers the one-time data migration pipeline, importing historical enrollment CSVs (5 files), the Revenue workbook, DHG Staffing workbook, and Staff Costs workbook into the BudFin database using the transformation rules in §13.5. The migration includes a parallel-run specification (§13.7) for validating imported data against Excel baselines, a rollback plan, and a data cleansing strategy. Successful migration is a go-live gate: zero tolerance for calculation discrepancy against the Excel source files.

**Dependency table**:

| Epic | Feature | Reason |
|------|---------|--------|
| 7 | Master Data Management | Migration inserts into master data tables (fee schedules, grades, departments) first |
| 11 | Authentication & RBAC | Migration scripts run under a privileged service account authenticated against the API |

---

### Epic 13 — Infrastructure & CI/CD

- **MoSCoW**: Must Have | **Tier**: MVP
- **PRD section**: §14, TDD §06_infrastructure.md
- **Dependencies**: None (foundational)

**Summary**: Epic 13 delivers the Docker Compose production stack (3 containers: nginx, api, db) and the GitHub Actions CI/CD pipeline for the BudFin monorepo. It provisions PostgreSQL 16 with pgcrypto, generates the RS256 JWT key pair as a Docker secret, configures nginx as a TLS-terminating reverse proxy, and sets up pnpm-based build/test/deploy workflows. All other epics depend on a running database and authenticated API layer, making this the first epic to implement alongside Epic 11.

**Dependency table**: None — this is a foundational epic.

---

## GitHub Issue Body Template

Use this exact shell heredoc format when creating each Epic issue:

```bash
gh issue create \
  --title "Epic N: Feature Name" \
  --label "epic,must-have" \
  --body "## Summary

Epic N delivers [3-4 sentence summary from catalog above. Open with 'Epic N delivers...'. Reference the PRD section. State what EFIR staff can do after it ships.]

## MoSCoW Priority

Must Have / Should Have / Could Have

## Tier

MVP / Target / Stretch

## Acceptance Criteria Reference

Derived in Phase 4 via \`/plan:spec\` and stored in \`docs/specs/epic-N/\`.

## Stories

Will be created in Phase 4 via \`/plan:stories\`.

## Dependencies

| Epic | Feature | Reason |
|------|---------|--------|
| N    | Name    | Specific reason why this epic's data or infrastructure is required |

## Checklist

- [ ] Feature spec written (\`/plan:spec\`)
- [ ] Stories created (\`/plan:stories\`)
- [ ] All stories implemented and reviewed
- [ ] Epic closed"
```

**Label format**: `"epic,must-have"` or `"epic,should-have"` (comma-separated, no spaces).

---

## Quality Control (Run Before Creating Each Epic)

1. Summary starts with "Epic N delivers..." — not "This feature..." or "The module..."
2. Summary is 3–4 sentences and references a PRD section identifier (e.g., §8.1, FR-ENR-*)
3. Dependency table has specific reasons — "Revenue calculation requires enrollment counts" not "depends on"
4. Labels applied: `epic` + MoSCoW label (`must-have` or `should-have`)
5. Issue added to Projects board in Backlog column immediately after creation

---

## Execution Order (Dependency-Respecting)

Create epics in this order to ensure referenced issues exist when dependency tables are written:

1. Epic 13 (Infrastructure) — no deps
2. Epic 11 (Auth & RBAC) — depends on 13
3. Epic 7 (Master Data) — depends on 11
4. Epic 1 (Enrollment) — no deps
5. Epic 2 (Revenue) — depends on 1, 7, 11
6. Epic 3 (Staffing DHG) — depends on 7, 11
7. Epic 4 (Staff Costs) — depends on 3, 7, 11
8. Epic 8 (Audit Trail) — depends on 11
9. Epic 12 (Data Migration) — depends on 7, 11
10. Epic 5 (P&L Reporting) — depends on 2, 3, 4
11. Epic 6 (Scenario Modeling) — depends on 5
12. Epic 9 (Dashboard) — depends on 2, 3, 4, 5
13. Epic 10 (Version Management) — depends on 5
