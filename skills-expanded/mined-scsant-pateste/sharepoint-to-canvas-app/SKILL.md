---
name: sharepoint-to-canvas-app
description: Converts SharePoint list requirements into a Canvas App plan with screens, forms, filters, approvals, history, and data-source verification.
allowed-tools: Bash, Read, AskUserQuestion
---

# SharePoint to Canvas App

Use this when the user has SharePoint lists and wants a Canvas App experience on
top of them.

## Workflow

1. Confirm the Canvas Authoring MCP session is connected through
   `configure-canvas-mcp`.
2. Ask the user to add the SharePoint data source in Power Apps Studio if it is
   not already present.
3. Use the Canvas Authoring MCP data-source tools, when available, to list data
   sources and inspect schema. If tools are unavailable, ask for a pasted schema
   or a sanitized list of columns.
4. Map each list to an app role:
   - primary transaction list
   - lookup/reference list
   - audit/history list
   - configuration list
5. Produce a Canvas App brief for `canvas-app` with:
   - browse/search/filter screen
   - detail screen
   - new/edit form
   - approval or review screen when status transitions exist
   - administration screen only when the user requests role-managed setup
   - history/comments surface when auditability is required
6. Prefer Power Fx formulas that make SharePoint delegation limits explicit.
   Warn when a requested filter, search, or sort pattern is likely nondelegable.
7. Require visible post-save receipts bound to the SharePoint item id or a stable
   business key.

## Defaults

- Treat SharePoint `Title` as a technical default unless the user says it is the
  business title.
- Do not hardcode user emails or tenant-specific URLs.
- Keep choice values from the source schema exactly as supplied.
