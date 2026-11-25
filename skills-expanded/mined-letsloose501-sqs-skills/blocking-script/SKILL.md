---
name: blocking-script
description: Imports a CSV export into the ledger. Use when a bank export lands in the downloads folder, or when the user asks to import transactions.
---

# Blocking script

1. Run the importer over the export.
2. Stop when the ledger balance matches the export total.

## When to open which reference

[scripts/import.py](scripts/import.py) is the importer; nothing else reads the CSV.
