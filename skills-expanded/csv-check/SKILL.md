---
name: csv-check
description: Validate an orders CSV before importing it. Use when checking required columns, invalid values, or rejected rows.
---

# Orders CSV validation

Read references/order-format.md for the import requirements.

Run `python3 scripts/validate.py <csv-file>` on the file supplied by the user.
The validator reads its rules from config/validation.json and reports
errors by row and column.

Summarize whether the file is ready to import. For rejected rows, explain
what needs to be corrected. A validation failure is a finding to report,
not evidence that the check could not run.
