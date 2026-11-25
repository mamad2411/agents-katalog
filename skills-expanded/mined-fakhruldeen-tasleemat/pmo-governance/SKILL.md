---
type: Skill
name: pmo-governance
description: Bilingual PMO artifact scaffolding, deliverable retrieval, and structural data validation using Tasleemat.
---

# PMO Governance Skill

This skill equips agents with standard operating procedures for retrieving deliverables and structurally validating completed data payloads using the Tasleemat library.

## Workflow
1. Identify the required deliverable ID using `tasleemat_list_artifacts` or `tasleemat_get_artifact`.
2. Retrieve the official template and practitioner guide using `tasleemat_get_asset`.
3. Populate the deliverable adhering to Document Control headers and metadata conventions.
4. Validate structured payloads across all 114 PMO deliverables using `tasleemat_validate_data` (strict or draft mode).
5. Note: Structural schema validation confirms field types and constraints only; it does not replace human PMO approval, business viability evaluation, or PMI/DGA certification.
