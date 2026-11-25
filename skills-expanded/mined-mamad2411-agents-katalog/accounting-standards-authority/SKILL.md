---
name: accounting-standards-authority
description: Enforces the @afenda/accounting-standards boundary: versioned IFRS/MFRS/SFRS authority metadata, standards-to-process routing, posting validation contracts, and evidence snapshots — never journal posting, ledger mutation, or Kernel IFRS logic.
paths:
  - packages/accounting-standards/**
  - docs/PAS/ACCOUNTING-STANDARDS/**
---

# @afenda/accounting-standards — Authority Skill (PAS-003)

## PAS rollout status (mirror header — sync on slice close)

| Field | Value |
| --- | --- |
| **Runtime status** | B0–B20 delivered — 31 tests · ERP consumer at `/modules/accounting/standards-readiness` |
| **Remaining slices** | — |
| **Consumer proof** | **Delivered** — `apps/erp/src/lib/accounting-standards` (B20) |

> Canonical: [`docs/PAS/ACCOUNTING-STANDARDS/PAS-003-ACCOUNTING-STANDARDS-AUTHORITY-STANDARD.md`](../../../docs/PAS/ACCOUNTING-STANDARDS/PAS-003-ACCOUNTING-STANDARDS-AUTHORITY-STANDARD.md) · Slices: [`ACCOUNTING-STANDARDS/SLICE/`](../../../docs/PAS/ACCOUNTING-STANDARDS/SLICE/README.md) · Closure: [`pas-status-index.md`](../../../docs/PAS/pas-status-index.md)

---

## Boundary (one sentence)

`@afenda/accounting-standards` **owns versioned accounting-standard authority metadata, standard-to-process routing, validation contracts, rule identifiers, explanation metadata, and evidence snapshots; it never owns journal posting execution, ledger persistence, consolidation calculation, tax filing, transfer-pricing rate policy, UI rendering, or AI-only accounting judgment.**

---

## When to use this skill

Apply this skill when touching:

- `packages/accounting-standards/**`
- any `@afenda/accounting-standards` import
- IFRS/MFRS/SFRS standard version registries or rule IDs
- posting validation input/rule/result contracts
- standard-to-process routing from Kernel relationship context
- standards-backed warning/block/evidence snapshot questions

**Kernel boundary:** Branded IDs and `LegalEntityContext` / relationship vocabulary live in `@afenda/kernel` ([PAS-001](../../../docs/PAS/KERNEL/PAS-001-KERNEL-VOCABULARY-AUTHORITY-STANDARD.md)). Do not add IFRS treatment logic to Kernel.

---

## Decision matrix

> Can this belong in accounting-standards?

| Question | If yes → | In this package? |
| --- | --- | --- |
| Does this define versioned IFRS/MFRS/SFRS/GAAP authority metadata? | Add standard/version registry record. | **Yes** |
| Does this map a process to a potentially relevant standard? | Add process-routing entry. | **Yes** |
| Does this return pass/info/warning/block for a posting draft? | Add validation rule/result contract. | **Yes** |
| Does this explain why a posting may conflict with a standard? | Add explanation registry entry. | **Yes** |
| Does this store cited evidence version for audit? | Add evidence snapshot contract. | **Yes** |
| Does this post the actual journal entry? | Belongs to Accounting. | **No** |
| Does this mutate ledger balances? | Belongs to Accounting. | **No** |
| Does this calculate consolidation entries? | Belongs to Consolidation. | **No** |
| Does this calculate tax payable or filing values? | Belongs to Tax. | **No** |
| Does this set transfer-pricing markup rates? | Belongs to Intercompany/Finance policy. | **No** |
| Does this render UI drawers or forms? | Belongs to apps/erp surfaces (consumer — B20). | **No** |
| Does this generate AI accounting advice without registry evidence? | Prohibited. | **No** |
| Does this define Kernel tenant/company identity? | Belongs to Kernel. | **No** |
| Does this encode IFRS/MFRS treatment logic inside Kernel? | Belongs here or Accounting runtime. | **No** (Kernel) |

---

## Hard stops

### Prohibited imports — never add these to accounting-standards

```
apps/erp
@afenda/accounting  @afenda/consolidation  @afenda/intercompany  @afenda/tax
@afenda/database  @afenda/ui  @afenda/metadata-ui  @afenda/appshell
Auth/session packages  Database clients  React  Next.js  External ERP/accounting SDKs
```

### Accounting Standards must never own

```
General ledger posting execution  Journal entry persistence  Ledger mutation
Chart of accounts ownership  Financial statement generation  Consolidation computation
Ownership/control/NCI/goodwill calculation  Transfer-pricing rates  Tax computation/filing
ERP UI behavior  AI free-form accounting judgment  Unversioned standard references
Long copied IFRS standard text  Kernel identity/relationship vocabulary
```

### Documentation-only slices

When the task is **explicitly documentation or skill maintenance only**, add:

```
Do not modify packages/accounting-standards/src/** (except tombstone/skill paths)
Do not change package exports
Do not mark registry surfaces complete before slice delivery
```

For implementation slices, the Phase 0 contract governs scope — not this list.

---

## Phase 0 — accounting-standards change contract

Before editing any accounting-standards file, state these six lines:

```
1. Objective       — the exact change, in one sentence
2. Allowed layer   — packages/accounting-standards only (or docs/skill for governance slices)
3. Files to change — explicit list
4. Prohibited      — Kernel IFRS logic, accounting posting, database, UI, consumer packages
5. Authority       — Financial Reporting Standards Authority (PAS-003)
6. Gates           — pnpm --filter @afenda/accounting-standards typecheck
                     pnpm --filter @afenda/accounting-standards test:run
                     pnpm quality:architecture
                     pnpm architecture:cycles
                     pnpm architecture:drift
                     pnpm quality:boundaries
```

If a slice handoff exists, paste the 9-field block from `docs/PAS/ACCOUNTING-STANDARDS/SLICE/<file>.md` into Phase 0 first.

---

## Required read order

1. This file (SKILL.md) — boundary, hard stops, Phase 0
2. [reference/authority-surfaces.md](reference/authority-surfaces.md) — contract shapes (Status: Target until slice delivers)
3. [reference/package-structure.md](reference/package-structure.md) — current vs target tree
4. [docs/PAS/ACCOUNTING-STANDARDS/PAS-003-ACCOUNTING-STANDARDS-AUTHORITY-STANDARD.md](../../../docs/PAS/ACCOUNTING-STANDARDS/PAS-003-ACCOUNTING-STANDARDS-AUTHORITY-STANDARD.md) — §0 Agent Quick Path
5. Next slice: [docs/PAS/ACCOUNTING-STANDARDS/SLICE/](../../../docs/PAS/ACCOUNTING-STANDARDS/SLICE/README.md) — paste 9-field handoff into Phase 0
6. [PAS-003 Appendix A](../../../docs/PAS/ACCOUNTING-STANDARDS/PAS-003-ACCOUNTING-STANDARDS-AUTHORITY-STANDARD.md#appendix-a--borrow-reference-inventory-temporary) — **temporary** borrow inventory (implementation hints only; not canonical authority)

**Maturity:** Enterprise Accepted — B20 ERP consumer workflow proof delivered (PAS-003 §11.6 · ADR-0027).

**Slice gate:** B0–B20 delivered (2026-06-30).

---

## Authority surface summary

| Surface | Owns | Does not own |
| --- | --- | --- |
| Standard family registry | IFRS/MFRS/SFRS/GAAP families | Journal accounts |
| Standard/version registry | Cited edition, effective dates, source URLs | Live ledger balances |
| Process routing | Kernel event → standard keys | Final consolidation entries |
| Posting validation | pass/info/warning/blocked + evidence | Journal persistence |
| Explanation registry | User/AI-safe cited summaries | UI rendering |
| Evidence snapshot | Immutable validation audit payload | Database writes |

Full TypeScript shapes: [reference/authority-surfaces.md](reference/authority-surfaces.md).

---

## Required gates

```bash
pnpm --filter @afenda/accounting-standards typecheck
pnpm --filter @afenda/accounting-standards test:run
pnpm quality:architecture
pnpm architecture:cycles
pnpm architecture:drift
pnpm quality:boundaries
```

Recommended when registries exist:

```bash
pnpm check:accounting-standard-version-registry
pnpm check:accounting-standard-rule-evidence
```

`check:accounting-standards-metadata-consumer-proof` — PASS against `apps/erp` (B20).

---

## Doctrine

Accounting Standards turns cited standard versions into deterministic validation metadata. **Consumers** decide whether warnings block workflow and **Accounting** owns posting.

Kernel owns **identity and relationship vocabulary**.  
Accounting Standards owns **versioned standards truth and validation rules**.  
Accounting owns **journals and ledgers**.

When in doubt: if it mutates the ledger or lives in Kernel ID vocabulary, it does **not** belong here.
