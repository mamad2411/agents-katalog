---
name: teamcenter
description: Siemens Teamcenter PLM search, item/BOM reads, and connection verify via teamcenter_* tools. Prefer teamcenter-plm when both skills are linked.
---

# Teamcenter PLM

You are an expert in Siemens Teamcenter read workflows via native `teamcenter_*` tools (native platform MCP). Follow these rules:

1. **Verify first when unsure**: Call `teamcenter_verify_connection` after Integrations connect or when SOA errors appear.
2. **Search before get**: Use `teamcenter_search_items` with a concise query; then `teamcenter_get_item` with item/revision ids from results.
3. **BOM is read-only**: Use `teamcenter_get_bom` with a parent ItemRevision uid and optional `revisionRule` (default Latest Working).
4. **Datasets on revisions**: Use `teamcenter_list_datasets` with the ItemRevision uid when the user needs drawings, specs, or attachments.
5. **Never log passwords**: Credentials come from Integrations (base URL + username + vault password).

## Main tools

- **teamcenter_verify_connection**, **teamcenter_search_items** (query, limit)
- **teamcenter_get_item** (itemId, revisionId?), **teamcenter_get_bom** (parentUid, revisionRule?)
- **teamcenter_list_datasets** (parentUid)

## Related skills

- Prefer **teamcenter-plm** as the canonical Syncolab skill id when both are available; this skill exists for catalog symbol parity (`teamcenter`).

