---
name: convert-statement
description: Use when the user attaches a bank statement PDF or asks for CSV/XLSX/QBO/Xero export of a converted statement. Do not use for spending analysis, reconciliation, or benchmark scoring — those have their own skills.
---

# Convert

**Input:** a public HTTPS PDF URL, host-provided PDF attachment, or local file path the host cannot pass directly.
**Output:** the conversion summary, key account details, statement period, balances, transaction count, and optional CSV/XLSX/QBO/Xero download links.

<!-- claude-only:start -->
**Before anything else:** if the Bankstatemently tools are not available in this session, the Bankstatemently connector is not connected. Tell the user that first, and how to connect it: Customize → Connectors → Bankstatemently → Connect, which asks them to sign in to a Bankstatemently account. Then ask whether they want to connect or have you do the task directly. If you do it directly, say that the result was not produced by Bankstatemently.
<!-- claude-only:end -->

Follow this sequence:

1. If the input is a public HTTPS URL or host-provided PDF attachment, call `convert_statement`.
2. If the input is a local file path and the host cannot pass the file directly, call `request_upload`, upload the PDF bytes from the file's absolute path to the returned URL, then call `convert_statement` with the upload id.
3. If conversion is still processing, poll `get_statement` until the statement is ready or the tool returns a terminal summary.
4. Present the tool summary, key account details, statement period, balances, and transaction count. Use the response summary as the source of truth when present.
5. Ask which export the user wants. For CSV, XLSX, QBO, or Xero, call `get_statement` with the requested output format and present the returned link.

**Example prompt:** Convert this bank statement PDF and give me a CSV download: https://bankstatemently.com/benchmark/statements/bsb-004-statement.pdf
