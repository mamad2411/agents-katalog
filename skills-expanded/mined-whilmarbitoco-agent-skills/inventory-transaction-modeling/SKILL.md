# Inventory Transaction Modeling

## Skill Metadata
```yaml
name: inventory-transaction-modeling
domain: pos-domain
language: java
version: "1.0.0"
description: >
  Design StockMovement entities, transaction ledgers, double-entry bookkeeping,
  and immutable financial records for POS inventory systems.
topics:
  - double-entry bookkeeping
  - immutable domain records
  - transaction ledger design
  - StockMovement entity modeling
  - BigDecimal money handling
constraints:
  - Use Java 21 records for value objects
  - All monetary values use BigDecimal with PHP currency precision
  - Constructor injection for all services
  - All records/immutable — no setters
```

## Purpose

Model inventory transactions as immutable, append-only ledger entries with
double-entry bookkeeping semantics. Every stock change produces balanced
debit+credit pairs that can be audited and reconciled.

## Core Concepts

### StockMovement Entity
- Record-style entity with UUID, sku, quantity delta, movement type, timestamp
- Every movement is immutable after creation
- References a transaction group (journal entry) for double-entry pairing

### Transaction Ledger
- Append-only journal of `JournalEntry` records
- Each entry has a debit side and a credit side
- Journal entries balance to zero (debits == credits)

### Double-Entry Principle
- Every inventory increase (debit inventory account, credit offset account)
- Every inventory decrease (debit offset account, credit inventory account)
- Trial balance must always sum to zero

### Immutable Records
- Java 21 records for all value objects (`Money`, `Quantity`, `LedgerId`, etc.)
- `StockMovement` is an immutable record with a compact constructor for validation
- No mutation methods — new state = new record instance

### Money Handling
- `Money` record: `BigDecimal amount` + `Currency currency`
- Use `java.math.MathContext` for precision control
- PHP currency support via `Currency` enum or attribute

## When to Use This Skill
- Modeling stock-in, stock-out, adjustments in a POS backend
- Implementing a journal entry system for financial reconciliation
- Designing an append-only event store for inventory changes
- Auditing and trial balance computation

## Related Skills
- `stock-movement-architecture` — movement type taxonomy and approval flows
- `audit-trail-patterns` — immutable logging that pairs with ledger entries
- `cash-session-management` — session-scoped transactions that feed the ledger