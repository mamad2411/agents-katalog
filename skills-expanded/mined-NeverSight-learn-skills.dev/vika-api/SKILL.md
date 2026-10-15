---
name: vika-api
description: |
  Use Vika.cn REST API via curl to manage online spreadsheet data. ALWAYS use this skill when users mention Vika, vika.cn, 维格表, 维格云 or any of these patterns:
  - IDs starting with "dst" (datasheet/数据表), "spc" (space/空间站), "fld" (field/字段), "rec" (record/记录), "viw" (view/视图)
  - Online collaborative tables/spreadsheets with API operations
  - Batch import/export data to online tables
  - Read/create/update/delete records via API
  - Upload attachments to datasheets
  - Search datasheets or spaces, list workspaces
  - Member fields, team management in online tables
---

# Vika.cn API Skill

Interact with Vika.cn via **curl** commands. No scripts needed - just direct API calls.

## Setup

Before making API calls, ensure environment variables are set:

```bash
# Set default host if not already set
[ -z "$VIKA_HOST" ] && export VIKA_HOST="https://vika.cn"

# API token is required (get from User Center > Developer Token)
# export VIKA_TOKEN="uskXXXXXXXXXXXXX"
```

Run the first line before any curl commands to ensure `VIKA_HOST` has the default value.

## Quick Reference

| Operation | Endpoint | Method |
|-----------|----------|--------|
| Get records | `/fusion/v1/datasheets/{dstId}/records` | GET |
| Create records | `/fusion/v1/datasheets/{dstId}/records` | POST |
| Update records | `/fusion/v1/datasheets/{dstId}/records` | PATCH |
| Delete records | `/fusion/v1/datasheets/{dstId}/records?recordIds=` | DELETE |
| Get fields | `/fusion/v1/datasheets/{dstId}/fields` | GET |
| Create field | `/fusion/v1/spaces/{spcId}/datasheets/{dstId}/fields` | POST |
| Delete field | `/fusion/v1/spaces/{spcId}/datasheets/{dstId}/fields/{fldId}` | DELETE |
| Get views | `/fusion/v1/datasheets/{dstId}/views` | GET |
| Create datasheet | `/fusion/v1/spaces/{spcId}/datasheets` | POST |
| Upload attachment | `/fusion/v1/datasheets/{dstId}/attachments` | POST |
| Get spaces | `/fusion/v1/spaces` | GET |
| Get nodes | `/fusion/v1/spaces/{spcId}/nodes` | GET |
| Search nodes | `/fusion/v2/spaces/{spcId}/nodes?type=` | GET |
| Get node detail | `/fusion/v1/spaces/{spcId}/nodes/{nodeId}` | GET |

## Basic Examples

```bash
# Get all records
curl -X GET "$VIKA_HOST/fusion/v1/datasheets/dstXXX/records" \
  -H "Authorization: Bearer $VIKA_TOKEN"

# Create records
curl -X POST "$VIKA_HOST/fusion/v1/datasheets/dstXXX/records" \
  -H "Authorization: Bearer $VIKA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"records":[{"fields":{"Title":"New Task","Status":"Todo"}}]}'

# Update records
curl -X PATCH "$VIKA_HOST/fusion/v1/datasheets/dstXXX/records" \
  -H "Authorization: Bearer $VIKA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"records":[{"recordId":"recXXX","fields":{"Status":"Done"}}]}'

# Delete records
curl -X DELETE "$VIKA_HOST/fusion/v1/datasheets/dstXXX/records?recordIds=recXXX&recordIds=recYYY" \
  -H "Authorization: Bearer $VIKA_TOKEN"

# Upload attachment
curl -X POST "$VIKA_HOST/fusion/v1/datasheets/dstXXX/attachments" \
  -H "Authorization: Bearer $VIKA_TOKEN" \
  -F "file=@/path/to/image.png"

# Get spaces list
curl -X GET "$VIKA_HOST/fusion/v1/spaces" \
  -H "Authorization: Bearer $VIKA_TOKEN"

# Search datasheets by name
curl -X GET "$VIKA_HOST/fusion/v2/spaces/spcXXX/nodes?type=Datasheet&query=keyword" \
  -H "Authorization: Bearer $VIKA_TOKEN"
```

## Response Format

All responses:
```json
{"success": true, "code": 200, "message": "SUCCESS", "data": {...}}
```

## Important: cellFormat Parameter for Reading Records

When user wants to **read/query records** and does NOT specify `cellFormat` in their request, ASK them to choose:

> "Which cell format do you prefer for the response?
> - `string` - Human-friendly format, all values converted to strings, dates formatted. Best for viewing data or exporting to CSV.
> - `json` - Structured format (default), preserves original types. Best for script processing or multi-step automation.
>
> Use `string` for simple data viewing; use `json` for programmatic processing."

**Usage:**
```bash
# Human-readable format (string)
curl -X GET "$VIKA_HOST/fusion/v1/datasheets/dstXXX/records?cellFormat=string" \
  -H "Authorization: Bearer $VIKA_TOKEN"

# Structured format for scripts (json, default)
curl -X GET "$VIKA_HOST/fusion/v1/datasheets/dstXXX/records?cellFormat=json" \
  -H "Authorization: Bearer $VIKA_TOKEN"
```

**When to skip asking:**
- User mentions "human readable", "export CSV", "view data", "display" → use `string`
- User mentions "script", "automation", "pipeline", "multi-step", "parse" → use `json`
- Complex multi-step operations or chained commands → use `json`

## Detailed Documentation

For complete parameter details and examples, read the reference files:

| Reference | When to read |
|-----------|--------------|
| `references/records.md` | Record CRUD with filtering, sorting, pagination |
| `references/fields.md` | Field types, create/delete fields |
| `references/views.md` | Get view list |
| `references/datasheets.md` | Create new datasheets |
| `references/attachments.md` | Upload files and use in records |
| `references/spaces-nodes.md` | Workspaces, folders, search |
| `references/members-teams.md` | User and team management |
| `references/field-types.md` | All field value formats |

## Tips

1. Use `fieldKey=id` for stability (field IDs don't change when renamed)
2. Max 10 records per create/update request
3. URL-encode `filterByFormula` values
4. Upload attachment first, then use its `token` in record fields
