---
name: excel-data-manager
description: Use when the user wants to manage tabular data (customers, transactions, contracts, expenses, or any custom domain) stored in Excel files. The skill discovers structure via a setup wizard, then offers CRUD, queries, and PDF reports — without imposing any specific schema. Trigger phrases include "manage customers in Excel", "track transactions", "set up a database in spreadsheets", "thêm khách hàng", "ghi giao dịch", "báo cáo tháng".
---

# Excel Data Manager

Schema-driven Excel data management. The user keeps their data in Excel files (any structure they like). The skill learns the structure via a one-time setup wizard, persists it as `schema.json`, and from then on can add/query/report on the data on demand.

## When to use

- User mentions managing data stored in Excel files.
- User asks about CRUD on customers/transactions/contracts/expenses or similar domain.
- User asks for a periodic report (monthly/weekly/daily summary).

## When NOT to use

- Data is in a real database (Postgres, MySQL) — use a SQL skill instead.
- Data is in Google Sheets cloud-only — this skill works on local .xlsx files.
- User wants concurrent multi-user editing — this skill is single-writer.

## Workflow

1. **First time**: Read `SETUP.md`. Run the setup wizard (`scripts/wizard.py`) to discover structure.
2. **Routine ops**: Read `WORKFLOW.md`. Use CRUD, query, and report scripts based on user requests.
3. **Schema change**: Re-run wizard with `--mode update`.

## Files

- `SETUP.md` — first-time setup
- `WORKFLOW.md` — daily operations
- `QUICKSTART.md` — cheat sheet
- `prompts/` — per-flow prompts the agent uses to chat with the user
- `scripts/` — Python implementations (call via Bash)
- `references/` — schema format reference and example schemas
