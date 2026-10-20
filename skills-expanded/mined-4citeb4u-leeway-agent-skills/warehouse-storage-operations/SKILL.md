---
name: warehouse-storage-operations
description: Governs receiving, inspection, put-away, location control, inventory counting, picking, packing, shipping, returns, damage handling, and storage safety. Use for warehouse, stockroom, storage-facility, inventory-control, or fulfillment work.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  source: Original LeeWay work-domain skill requested during D/E capability reconciliation
---

# Warehouse and Storage Operations

Define facility zones, item identifiers, units, lot/serial/expiry rules, custody, equipment qualifications, hazard classes, temperature/security needs, and system of record.

Run every movement as a traceable transaction: expected item and quantity; physical observation; discrepancy/damage quarantine; accepted quantity; origin and destination locations; responsible operator; timestamp; and system confirmation. Require scan or dual verification where consequence warrants it.

Separate `EXPECTED`, `PHYSICALLY_OBSERVED`, `SYSTEM_RECORDED`, `MOVED`, and `RECONCILED`. Inventory software output does not prove physical presence. Escalate safety, hazardous-material, damaged-goods, access, capacity, and custody exceptions to the authorized human.
