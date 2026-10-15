---
name: captainbi-sales
description: "Sales, orders, returns, refunds and FBM shipping commands for CaptainBI CLI. WHEN use for: order lists, refunds, returns, FBM shipping status, and sales-volume analysis. WHEN NOT: do not use for profit/P&L questions, advertising reports, FBA inventory, Amazon SP-API-only tasks, or Feishu-only records."
---

# CaptainBI Sales

Read `captainbi-shared` first.
For task recipes, read `references/workflows.md`.

## WHEN

Use for order lists, refunds, returns, FBM shipping status, and sales-volume analysis.

## WHEN NOT

Do not use for profit/P&L questions unless order-level sales records are explicitly needed; use `captainbi-finance` first for finance reports.

## Command Choice

- Recent orders: `cbi +orders --channel <alias> --start <ts> --end <ts> --summary`.
- Full order pull: `cbi sales orders --channel <alias> --start-modified-time <ts> --end-modified-time <ts> --page-all --output-file orders.json`.
- Returns: `cbi sales returns --channel <alias> --page 1 --rows 100`.
- Refunds: `cbi sales refunds --channel <alias> --page 1 --rows 100`.
- FBM shipping upload is asynchronous and dangerous; follow `references/workflows.md`, require an exact approved request hash, then poll the returned feed ID.

## Examples

```bash
cbi --channel main +orders --start 1781424057 --end 1781510457 --summary --machine
cbi --channel main sales orders --start-modified-time 1781424057 --end-modified-time 1781510457 --page-all --max-records 100 --machine
```

## Notes

- `start_modified_time` and `end_modified_time` use second-level Unix timestamps.
- Empty data is not necessarily an error; check `ok`, `rows`, and `api_code`.
