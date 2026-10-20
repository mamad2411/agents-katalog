---
name: productivity-platform-ops
description: "Use when operating productivity platforms and document/work-management APIs from Hermes: Airtable, Linear, Notion, PowerPoint, PDF editing, Teams meeting pipelines, maps/location, or email/document workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Productivity Platform Operations

Class-level guide for platform/API-backed productivity work. Prefer official CLIs/APIs, verify side effects, and keep credentials scoped.

## Work databases and task systems
- Airtable: REST API via curl for bases, tables, records, filters, upserts. Requires `AIRTABLE_API_KEY`.
- Linear: GraphQL API/curl or helper script for issues, projects, teams. Requires `LINEAR_API_KEY`.
- Notion: API or `ntn` CLI for pages, databases, blocks, markdown conversion. Requires `NOTION_API_KEY`.

## Documents and presentations
- PowerPoint: create/read/edit `.pptx`; use deck-specific scripts and references for pptxgenjs or OOXML work.
- nano-pdf: natural-language PDF text/title/typo edits via `nano-pdf` CLI.
- Teams meeting pipeline: Hermes CLI operations for meeting summaries, replay, status, and Microsoft Graph subscriptions.

## Location and maps
- Maps: geocoding, POIs, routes, timezones via OpenStreetMap/Nominatim/Overpass/OSRM. Verify live API responses and cite assumptions.

## Email
- Himalaya: IMAP/SMTP CLI email workflows. Use for terminal-first mailbox search, read, draft, and send when configured.

## Verification checklist
- For create/update/delete operations: capture returned record/page/issue/file ID or path.
- For generated files: stat/read back the output.
- For sends/subscriptions: report the command result and any remote ID/status.
- For API failures: include the HTTP status or CLI error; do not fabricate remote state.

## Common pitfalls
- Check required env vars before API calls.
- Avoid dumping secrets into prompts or logs.
- Use platform-native IDs in follow-up work rather than display names when ambiguity matters.
