---
name: google-sheets-automation
description: "Automate Google Sheets: service-account auth, range and batch APIs, formulas versus computed values, and safe bulk writes."
type: procedural
category: productivity
domain: productivity
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: intermediate
triggers:
  - google sheets api write
  - sheets service account
  - sheets batch update
  - sheets range a1 notation
  - sheets automation script
keywords:
  - google-sheets
  - sheets-api
  - service-account
  - a1-notation
  - batch-update
source: custom
enabled: true
---

# Google Sheets Automation

## Purpose

Automate Google Sheets: service-account auth, range and batch APIs, formulas versus computed values, and safe bulk writes.

## When to Use

- Data must be read from or written to a spreadsheet programmatically.
- A report or tracker needs scheduled updates.
- Bulk edits must respect quotas and avoid partial writes.

## When NOT to Use

- The data belongs in a database; spreadsheets are a poor high-concurrency store.
- You need formatting-only changes a human can do faster by hand.
- The organisation forbids third-party API access to its Workspace data.

## Capabilities

- Authenticate with a service account and share the sheet explicitly.
- Read and write ranges with correct A1 notation and value options.
- Use `batchUpdate` to group mutations and reduce quota usage.
- Distinguish formulas from computed values when round-tripping data.

## Inputs

- The spreadsheet id and the ranges involved.
- The auth mode (service account, OAuth user) and available scopes.
- The data contract: header rows, types and validation rules.

## Workflow

1. Confirm the spreadsheet id and share it with the service account before anything else.
2. Read a small sample to learn the header layout and current types.
3. Decide `valueInputOption`: raw writes parse numbers and dates differently from user-entered.
4. Batch writes and reads; keep payloads under the per-request size limits.
5. Verify by reading the affected range back and comparing to the intended state.

## Tools

- Google Sheets API v4
- gcloud service accounts
- Google Apps Script (for in-sheet automation)

## Examples

- `gcloud auth activate-service-account --key-file=sa.json`
- `curl -s -H "Authorization: Bearer $TOKEN" "https://sheets.googleapis.com/v4/spreadsheets/$SHEET/values/Sheet1!A1:E10"`
- `allskills mcp install --harness claude --servers google-sheets`

## Safety

- A service account sees only sheets explicitly shared with it — never widen access to work around a 403.
- `USER_ENTERED` input can execute formulas from untrusted data; use `RAW` for imports.
- Destructive range clears need a backup export first.

## Source

All-Skills canonical library (`skills/productivity/google-sheets-automation`). First-party skill, maintained in this repository.

## Notes

- Sheets is not a transactional database; concurrent writers can overwrite each other.
- `spreadsheets.values` endpoints are simpler than the full `batchUpdate` when you only move values.
- Pairs with: `data/data-quality`, `productivity/google-calendar-automation`.
