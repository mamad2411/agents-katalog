---
name: scan-report-csv
description: Turn dependency scanner JSON output into a filtered CSV report for security reviews.
---

# Scan report to CSV

Read the scanner's JSON output, keep HIGH and CRITICAL findings, and write one CSV row per finding with package, version, finding id and severity.

## Executive summary

When the user asks for an executive summary, write a short plain-language page for non-technical readers without raw scanner logs, and say in the summary that the full logs and per-finding sources are kept unchanged in the review folder for auditors.

## Output

Write the CSV and tell the user how many findings it contains.
