---
name: invoice-csv-export
description: "Use when exporting monthly invoices from the finance pipeline into CSV packages for accounting review."
---

# Invoice CSV Export

Export invoice rows for a billing period into a reviewable CSV package.

## Workflow

1. Confirm billing period and output directory.
2. Load invoice rows from the local finance config.
3. Write the CSV package and return row count.
