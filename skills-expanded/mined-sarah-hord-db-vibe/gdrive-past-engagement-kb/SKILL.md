---
name: gdrive-past-engagement-kb
description: Search Google Drive for past RSA/PS engagement documents including SOWs, scope estimates, project plans, and deliverables to inform new scope estimates
---

# Google Drive Past Engagement Knowledgebase

Search a Google Drive folder for relevant prior RSA/PS work — SOWs, scope estimates, project plans, status reports, and deliverables — that can inform new professional services scope estimates.

## Prerequisites

1. Use the `/google-auth` skill to authenticate before any Drive operations.
2. You must have access to the PS shared Google Drive. If you cannot access the folder below, contact your PS team lead for access.

## Past Engagements Folder

Check `~/.claude/fe-rsaagent.local.md` for a custom `past_engagements_folder_id`. If the file exists and defines one, use that folder ID. Otherwise, use the default below.

**Default folder:**

- **Folder ID:** `1TPxwUUdPzSnQRhquL7r7VnibVuxeQm_l`
- **URL:** https://drive.google.com/drive/folders/1TPxwUUdPzSnQRhquL7r7VnibVuxeQm_l

All searches MUST be scoped to the resolved folder only. Do NOT search outside this folder or its subfolders.

<!-- This folder is on a shared drive; use includeItemsFromAllDrives=true and supportsAllDrives=true with corpora=drive and driveId=0ANe2PXW3rONQUk9PVA -->

## How to Search

### Step 1: List and search files in the folder

Use the `/google-docs` skill for all Drive operations, always scoped to folder ID `1TPxwUUdPzSnQRhquL7r7VnibVuxeQm_l`:

- **List files** in the folder
- **Search by keyword** within the folder using terms like:
  - Workload type: `migration`, `ETL`, `lakehouse`, `ML`, `governance`, `Unity Catalog`, `DBR upgrade`
  - Industry: `financial services`, `healthcare`, `retail`, `manufacturing`
  - Engagement type: `SOW`, `scope`, `estimate`, `project plan`
- **Search subfolders** recursively within this folder

### Step 2: Read document content

Use the `/google-docs` skill to read the most relevant documents (2-3 max).

## What to Extract from Past Engagements

When reviewing past engagement documents, extract:

1. **Scope patterns** — What workloads were included? How were phases structured?
2. **Effort estimates** — Hours/weeks per workload type, team size, roles involved
3. **Deliverables** — What artifacts were produced?
4. **Assumptions & constraints** — Common prerequisites and dependencies
5. **Risks** — Recurring risk patterns and mitigations
6. **Pricing structure** — How were engagements priced (T&M, fixed, blended)?

## Do NOT

- Modify or delete any files in the past engagements folder
- Share document contents outside of the current scope estimate context
- Assume past engagement terms apply to new customers without review
