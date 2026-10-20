---
name: customer-folder-manager
description: Use when the user wants a lightweight CRM on their local machine — manage customer records in Excel and one folder per customer for attached files (contracts, invoices, documents, etc.). Discovers structure via a setup wizard, then offers add/update/archive customer, attach/index files, and natural-language queries. Trigger phrases include "manage customers", "set up CRM", "track customer files", "thêm khách hàng", "lưu hợp đồng cho khách", "lấy hợp đồng của khách".
---

# Customer Folder Manager

CRM-style local data management. Customer rows live in an Excel workbook (`customers.xlsx`); each customer also has a filesystem folder for attached files organized by category (contracts, invoices, documents, etc.). All file metadata is indexed in the workbook for fast queries.

## When to use

- The user wants a personal/small-business CRM stored locally.
- The user mentions adding customer information, attaching files (contracts, invoices) to customers, or asking "get me the contract of customer X".
- The user wants a setup wizard to start fresh.

## When NOT to use

- The user already has data in Postgres/MySQL — use a SQL skill.
- The user wants a generic Excel data manager (no per-customer folders) — use `excel-data-manager`.
- The user needs multi-user concurrent editing — this skill is single-writer.

## Workflow

1. **First time:** Read `SETUP.md`. Run the setup wizard (`scripts/wizard.py greenfield`) using a JSON spec built from the user's answers.
2. **Routine ops:** Read `WORKFLOW.md`. Use `crud.py`, `file_manager.py`, and `query.py` based on user requests.
3. **Schema change:** Run `scripts/wizard.py update --op <op>`.

## Files

- `SETUP.md` — first-time setup
- `WORKFLOW.md` — daily operations
- `QUICKSTART.md` — cheat sheet of common commands
- `MANUAL-QA.md` — checklist for human verification
- `prompts/` — per-flow prompts the agent uses to chat with the user
- `scripts/` — Python implementations (call via Bash)
- `references/` — config format and default field template
