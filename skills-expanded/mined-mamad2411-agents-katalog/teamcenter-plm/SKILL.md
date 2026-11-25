---
name: teamcenter-plm
description: Siemens Teamcenter PLM read workflows — search items, open BOMs, list datasets, verify SOA connectivity. Use when tracing parts, revisions, BOM impact, or datasets on released revisions.
---

# Teamcenter PLM

## Purpose

Operate a connected Siemens Teamcenter instance through native `teamcenter_*` tools (native platform MCP at clock-in). Search items, load revisions, open BOM windows, and list datasets without fabricating PLM identifiers.

## When to Use

- User asks to find parts, assemblies, or revisions in Teamcenter.
- BOM impact analysis, where-used, or revision rule questions.
- Listing drawings, specs, or datasets on an ItemRevision.
- Verifying SOA connectivity after Integrations connect or when errors appear.

## When NOT to Use

- SolidWorks PDM vault operations → **solidworks-pdm**.
- Jira/Confluence requirements only → **jira** / **confluence** skills.
- Write/release workflows not exposed by current tools — escalate to a human PLM admin.

## Expected Outcome

- Search results with item ids, names, and revision hints.
- BOM children with revision rule noted (default Latest Working).
- Dataset lists tied to a known ItemRevision uid.
- Clear blockers when base URL, username, or vault password is missing.

## Workflow

1. When connectivity is uncertain, call `teamcenter_verify_connection`.
2. **Search before get**: `teamcenter_search_items` with a concise query; then `teamcenter_get_item` with ids from results.
3. **BOM is read-only**: `teamcenter_get_bom` with parent ItemRevision uid and optional `revisionRule`.
4. **Datasets on revisions**: `teamcenter_list_datasets` with the ItemRevision uid.
5. Never log passwords — credentials come from Integrations (base URL + username + vault password).

## Main tools

| Tool | Use |
|------|-----|
| `teamcenter_verify_connection` | Confirm SOA session |
| `teamcenter_search_items` | Query + limit |
| `teamcenter_get_item` | itemId, optional revisionId |
| `teamcenter_get_bom` | parentUid, optional revisionRule |
| `teamcenter_list_datasets` | parentUid |

## Examples

**User:** "Find part ABC-123 in Teamcenter."

Call `teamcenter_search_items` with query `ABC-123`. Summarize matching item ids, names, and revisions; offer `teamcenter_get_item` for one hit.

**User:** "Show BOM for revision uid xyz."

Call `teamcenter_get_bom` with `parentUid` `xyz`. Present top-level children and note the revision rule used.
