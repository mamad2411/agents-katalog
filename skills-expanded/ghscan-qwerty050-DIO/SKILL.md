---
name: inventory-recurring
description: Track inventory items and restock intervals.
user-invocable: true
---

# Inventory

## Rules
- Items with `interval_days` automatically get restock reminders via the recurrence engine.
- Use `record_action=true` on updates to mark a restock.
- Check overdue items with `overdue_only=true`.
