# Stock Movement Architecture

## Skill Metadata
```yaml
name: stock-movement-architecture
domain: pos-domain
language: java
version: "1.0.0"
description: >
  Model the 5 stock movement types (Purchase, Sale, Adjustment, Return, Loss)
  with approval workflows and configurable thresholds.
topics:
  - stock movement type taxonomy
  - approval workflows for stock adjustments
  - threshold-based triggers
  - purchase vs sale vs adjustment vs return vs loss
constraints:
  - Use Java 21 sealed interfaces for movement type hierarchy
  - Constructor injection for all services
  - All movement amounts use BigDecimal with PHP currency
  - Approval rules configurable per movement type and threshold
```

## Purpose

Define a type-safe, extensible taxonomy of stock movement types with built-in
approval workflows. Movements above configurable thresholds require manager
approval before being committed to the ledger.

## Core Concepts

### 5 Movement Types (Sealed Interface)
- **`Purchase`** — stock received from supplier (increases inventory)
- **`Sale`** — stock sold to customer (decreases inventory)
- **`Adjustment`** — manual correction: `INCREASE` or `DECREASE` sub-types
- **`Return`** — stock returned to supplier (decreases inventory)
- **`Loss`** — stock lost/damaged/expired (decreases inventory)

### Approval Workflow
- Configured via `ApprovalRule(MovementType type, Money threshold)`
- Movements exceeding threshold → `PENDING_APPROVAL` status
- Manager provides `Approval` (approver ID, timestamp, reason) → `APPROVED`
- Approved movements proceed to ledger posting
- Rejected movements are archived with rejection reason

### Threshold Configuration
- Per-movement-type threshold (e.g., adjustments > ₱5,000 need approval)
- Zero threshold = no approval needed for that type
- Configurable at runtime via admin interface

### Type-Safe Design
- Java 21 `sealed interface MovementType` restricts the hierarchy
- `switch` expressions with exhaustive pattern matching
- Each type implements `affectsStock()` (increase/decrease) and `requiresApproval(Money amount)`

## When to Use This Skill
- Inventory management module in POS backend
- Stock adjustment approval workflows
- Loss/expiry reporting
- Purchase receiving and return processing

## Related Skills
- `inventory-transaction-modeling` — movements feed the double-entry ledger
- `audit-trail-patterns` — approval actions are audit-logged
