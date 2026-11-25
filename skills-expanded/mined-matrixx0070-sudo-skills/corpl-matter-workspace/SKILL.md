---
name: corpl-matter-workspace
version: 1.0.0
description: Set up an organized workspace for a corporate/M&A matter — folder structure, document index, key-dates register, and the contacts and privilege markers.
author: matrixx0070
tags: [corporate-legal, matter, workspace, organization, index, privilege]
capabilities: []
---

## When to use

Use this right after intake to stand up the working home for a matter: a consistent folder structure, a master document index, a key-dates and parties register, and the privilege/confidentiality markers. A well-organized workspace is what makes every downstream corpl- workflow fast and traceable.

**Not for:** gathering the facts (use corpl-cold-start-interview first); the substantive legal work itself; deciding privilege status of a specific document — apply the labeling convention and flag genuine questions to counsel. This skill organizes; it makes no legal determinations. It also does not execute filesystem changes — it defines and records the structure.

## Method

1. **Name and key the matter.** Matter name, client, matter ID/number, responsible attorney, and matter type.
2. **Lay out the folder structure** by workstream — corporate/org docs, diligence (by category), transaction documents, correspondence, board/governance, closing, and post-closing.
3. **Build the master document index.** Each document: name, category, version/date, source, and privilege marker. This index is the single source of truth for what exists and where.
4. **Create the key-dates register.** Signing, closing, drop-dead, filing deadlines, covenant dates — with owners.
5. **Record the parties and contacts** — client-side, counterparty, other advisors — and their roles.
6. **Set privilege and confidentiality defaults.** *Decision point:* mark attorney work product and privileged communications ("Privileged & Confidential — Attorney Work Product") and restrict distribution; flag ambiguous items to counsel rather than guessing.
7. **Confirm the structure** with the responsible attorney and point the other workflows at it.

## Example

Matter "Project Harbor" (client: Acme, ID 2026-041, resp. attorney: Lee, type: stock acquisition). Folders: 01-corporate, 02-diligence (by category), 03-transaction-docs, 04-correspondence, 05-governance, 06-closing, 07-post-closing. Index seeded with 41 diligence documents from the data room, each tagged and versioned. Key dates: signing 6/30, target close 7/15. Parties: buyer/seller/advisors registered. Diligence memos marked privileged.

## Pitfalls

- **Ad hoc folders per person.** Inconsistent structure defeats the point; use one convention.
- **An index that drifts.** If documents are added without indexing, the index becomes a liability.
- **No version control.** Working off a superseded document silently corrupts every deliverable built on it.
- **Loose privilege handling.** Mislabeling or over-sharing work product can waive privilege.

## Output format

```
MATTER WORKSPACE — <matter name> (ID <n>)
Client / responsible attorney / matter type:
Folder structure:
  01-corporate | 02-diligence(<categories>) | 03-transaction-docs | 04-correspondence | 05-governance | 06-closing | 07-post-closing
Master document index:
  | Doc | Category | Version/date | Source | Privilege marker |
Key-dates register: <event — date — owner>
Parties & contacts: <name — role — side>
Privilege/confidentiality defaults:
Confirmed by attorney: <name>
```

## Reference

A matter workspace pairs a consistent folder taxonomy (organized by workstream) with a master document index that carries version, source, and privilege marker on every item. The key-dates register and parties list keep deadlines and contacts in one place. Privilege labeling ("Privileged & Confidential — Attorney Work Product") and distribution limits are applied by default; genuine privilege questions go to counsel. This workspace is the shared substrate the other corpl- skills read from and write to.
