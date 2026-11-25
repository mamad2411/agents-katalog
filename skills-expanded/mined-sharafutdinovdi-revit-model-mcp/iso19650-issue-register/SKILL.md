---
name: iso19650-issue-register
description: Create an Excel issue register with element snapshots for model review against EIR/BEP/ISO 19650, or a реестр замечаний.
---

# ISO 19650 issue register

## Inputs

Use the model open in Revit and the documents the user attaches or names: EIR, OIR/AIR, BEP and applicable ISO 19650 parts.
If no EIR or BEP is supplied, use ISO 19650-2 and the UK National Annex defaults and record that assumption in `project.documents`.
Read the applicable source text before quoting a clause.
If a named document is unavailable, report the gap and mark its checks as not assessed.
ISO defaults are review assumptions, not inferred client requirements.

## Step 1: Extract checkable requirements

Read the documents and list requirements verifiable in the model with their clause numbers, source, quoted text and planned evidence.
Distinguish information management process requirements from facts visible in a Revit model.
Do not claim full ISO 19650 compliance from model data alone.

Consider these families only when supported by the checked documents or explicitly marked defaults:

- File and information container naming. UK National Annex naming fields include project, originator, volume/system, level/location, type, role and number. Check status and revision codes against the applicable source.
- Level and grid naming, shared coordinates, project base point and units.
- Project information parameters and sheet title block fields.
- Classification, such as Uniclass 2015 codes on types when required.
- Level of information need, expressed as required parameters per category.
- Model health: warnings, in-place families, imported CAD, unplaced or unbounded rooms, duplicate marks and unused views.
- View and sheet naming.

## Step 2: Check the model

Start with `revit_document_info` and `revit_list_catalog` to discover localized category and parameter names.
Use paged reads until the relevant population is covered.
Treat non-empty `skipped`, partial responses and truncation as evidence gaps.

| Requirement family | Tools and evidence |
| --- | --- |
| Identity, units, levels and project information | `revit_document_info`, `revit_list_catalog`, `revit_query_elements`, `revit_element_details`. Read project information and parameter values through catalog/query/detail reads where exposed. Mark unavailable metadata as not assessed. |
| Container naming, status, revision and sheets | `revit_document_info`, `revit_list_catalog`, `revit_list_views`, `revit_query_elements`, `revit_element_details`. Inspect model identity, sheet parameters and title block instances. A file name alone does not prove CDE status or revision. |
| Coordinates and project base point | `revit_shared_coordinates`, `revit_links_status`, `revit_compare_link_datums`. Compare measured values with the supplied coordinate requirements. |
| Level and grid naming | `revit_document_info`, `revit_query_elements`, `revit_list_catalog`. Read datum names and compare with the required convention. |
| Classification and required information | `revit_parameter_fill_check`, `revit_aggregate_elements`, `revit_query_elements`, `revit_element_details`. Inspect type parameters as well as instance parameters. |
| Model health | `revit_model_health`, `revit_list_warnings`, `revit_family_audit`, `revit_links_status`. Use `revit_query_elements` and `revit_aggregate_elements` for rooms and duplicate marks. |
| View, sheet and spatial relationships | `revit_list_views`, `revit_list_relations`, `revit_query_elements`, `revit_view_info`. Confirm membership and use before calling a view unused. |

Use `revit_capture_elements` for an evidence preview when needed.
The register tool captures its own images; previews do not need to be saved by the client.
All review tools are reads. Do not call mutation tools during this review.

## Step 3: Write findings

Create one issue per requirement breach.
Quote the requirement and identify its source and clause.
State the measured fact with counts, units and the population checked.
Give a concrete recommendation and the responsible task team or role when known.
Do not invent due dates, owners, requirements or inaccessible evidence.

Cap `element_ids` at 200 per issue.
Choose representative affected elements for the snapshot and state the total affected count in `finding` when the list is a sample.
Use `snapshot: plan` for spatial or plan evidence, `3d` for geometric evidence and `none` for findings without useful model geometry.
The tool captures at most 25 snapshots in severity order, preserving issue order within each severity.
Failed captures and the capture time budget produce warnings without discarding the register.
Element snapshots require local or SSH transport; HTTP does not support them.

| Severity | Rule |
| --- | --- |
| critical | Blocks information exchange or coordination. |
| major | Breaks a contractual requirement. |
| minor | Quality or consistency problem. |
| info | Observation. |

## Step 4: Write the workbook

Call `revit_issue_register` with project metadata, `project.documents` and the findings.
Each document entry contains `title`, `reference` and `revision` when known.
Label the ISO 19650-2 and UK National Annex entries as defaults when used without an EIR/BEP.

Use the user's output path when supplied.
Otherwise choose a new path on the machine running the MCP server according to that machine's OS:
`C:\Users\Public\Documents\<model>_issue_register_<yyyy-mm-dd>.xlsx` on Windows, or `~/Documents/<model>_issue_register_<yyyy-mm-dd>.xlsx` on macOS/Linux.
Use a filesystem-safe model name and a distinct suffix if the file exists.
The tool refuses to overwrite files.
Pass `document` and `process_id` when needed to select the reviewed model.

## Step 5: Report the result

Reply with the workbook path, severity count table and the top five issues by severity.
Include snapshot warnings and checks not assessed.
State which requirements came from supplied documents and which came from ISO defaults.
Never invent requirements absent from the documents.
