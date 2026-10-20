---
name: solidworks-pdm
description: SolidWorks PDM Pro vault workflows — search, browse, variable search, checkout/checkin via native solidworks_pdm_* tools. Use for vault metadata and controlled file operations with user approval.
---

# SolidWorks PDM

## Purpose

Operate a connected SolidWorks PDM Pro vault through native `solidworks_pdm_*` tools (native platform MCP at clock-in). Search files, browse folders, run variable queries, and perform checkout/checkin only with explicit user approval.

## When to Use

- User needs to find parts, drawings, or documents in the vault.
- Exploring folder structure or variable-based searches.
- Controlled checkout/checkin when the user confirms file ids.

## When NOT to Use

- Teamcenter PLM item/BOM work → **teamcenter-plm**.
- CAD mass properties, STEP export, or COM automation → `solidworks_submit_job` only when customer bridge is deployed (otherwise report NOT_CONFIGURED).
- Unapproved writes — always confirm file lists before checkout/checkin.

## Expected Outcome

- Search hits with file/folder ids for follow-up.
- Browse results with folder hierarchy context.
- Checkout/checkin results only after approval.
- Clear blockers when vault URL, vault name, or credentials are missing.

## Workflow

1. When credentials may be wrong, call `solidworks_verify_connection`.
2. **Search then browse**: `solidworks_pdm_search` for names/part numbers; `solidworks_pdm_browse_folder` with `folderId` (1 = root).
3. **Advanced search**: `solidworks_pdm_search_variables` for multi-field vault queries.
4. **Writes need approval**: `solidworks_pdm_checkout` and `solidworks_pdm_checkin` require explicit user approval — confirm file list before executing.
5. **CAD jobs**: `solidworks_submit_job` / `solidworks_get_job_status` need customer CAD bridge deployment; prefer PDM tools for vault metadata until available.

## Main tools

| Tool | Use |
|------|-----|
| `solidworks_verify_connection` | Confirm vault access |
| `solidworks_pdm_search` | Name/part number query |
| `solidworks_pdm_search_variables` | Structured search body |
| `solidworks_pdm_browse_folder` | folderId |
| `solidworks_pdm_checkout` / `solidworks_pdm_checkin` | files[] — approval required |

## Examples

**User:** "Find drawing DWG-442 in the vault."

Call `solidworks_pdm_search` with query `DWG-442`. Return file/folder hits with ids.

**User:** "Check out these two files for edit."

Confirm FileId/FolderId pairs with the user, then call `solidworks_pdm_checkout` after approval.
