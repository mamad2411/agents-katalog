---
name: aspice-requirements
description: Reconstruct one or multiple automotive customer requirement documents from a file or directory, build a global requirement brief, extract a CRS working set, and derive ASPICE-oriented SRS, SWRS, open issues, and CRS-to-SRS-to-SWRS traceability without losing document-level context.
---

# ASPICE Requirements

Use this skill to analyze automotive customer requirement documents and derive structured requirements for ECU software, vehicle control software, diagnostics, communication, safety-related software, cybersecurity-related software, platform software, or application software.

Unless otherwise requested, write CRS Working Set, SRS, SWRS, traceability matrices, and open issues in English. Explanations to the user may be provided in Chinese if the conversation is in Chinese.

## Primary User-Facing Outputs

1. System Requirements Specification, SRS
2. Software Requirements Specification, SWRS
3. CRS-to-SRS-to-SWRS Traceability Matrix
4. Open Issues List

The CRS Working Set is normally an intermediate AI-readable artifact. A formal CRS document may be generated only when explicitly requested.

## PDF and Office Processing Skill Reuse

Before using built-in scripts or implementing custom PDF/Office extraction logic, the agent shall first check whether a dedicated document-processing or PDF-processing skill is already installed or available in the current environment.

If a suitable installed skill exists, prefer using that skill to extract or reconstruct PDF, Word, table, image/OCR, page reference, and layout information. Do not duplicate PDF parsing functionality inside this skill when a specialized skill can provide better extraction quality.

Recommended priority:

1. Use an installed PDF/document-processing skill if available.
2. If no suitable skill is available, use external tools such as Docling, marker, GROBID, or equivalent tools.
3. If neither installed skills nor external tools are available, use the lightweight reconstruction script in `scripts/reconstruct_document.py` on already extracted Markdown or text.

## Core Workflow

Do not directly generate software requirements from raw PDF, raw Word, or unstructured full-document text.

Always follow this workflow:

1. Document Reconstruction
2. Source Document Registry and Combined Document Analysis Model creation
3. Global Requirement Brief creation
4. CRS Working Set extraction by domain or section group
5. SRS derivation from CRS Working Set
6. SWRS derivation from reviewed SRS
7. Traceability and Open Issues generation

Use section-aware chunks internally when needed, but do not expose low-level chunks as default outputs. Preserve a global document view before extracting or deriving requirements.

## Multi-Document and Module-Based Inputs

Customer requirements may arrive as multiple files or module-specific documents under a directory.

When a directory or document set is provided:

1. Reconstruct all relevant source documents.
2. Create a Source Document Registry.
3. Create a Combined Document Analysis Model.
4. Build one Global Requirement Brief for the full document set.
5. Extract CRS Working Set items by domain across documents.
6. Consolidate duplicates and flag conflicts.
7. Preserve document IDs in all CRS source references.
8. Prefer one coherent SRS and one coherent SWRS unless the user explicitly requests module-specific outputs.

## When to Load References

- Use `references/workflow.md` for the overall process.
- Use `references/document-reconstruction-guide.md` for PDF/Word/text reconstruction and directory processing.
- Use `references/global-requirement-brief.md` before extraction or derivation.
- Use `references/requirement-extraction-guide.md` for CRS Working Set extraction.
- Use `references/derivation-rules.md` for CRS-to-SRS and SRS-to-SWRS derivation.
- Use `references/requirement-quality-rules.md` for Automotive SPICE-style quality checks.
- Use `references/traceability-guide.md` for traceability and coverage.
- Use `references/output-templates.md` when formatting outputs.
- Use `references/file-naming-convention.md` when naming generated files and exported artifacts.

## CRS Working Set

Each CRS Working Set item shall include:

- CRS ID
- Customer Requirement
- Domain
- Source Reference
- Status
- Issue

CRS items shall represent customer intent only. Do not add system behavior, software behavior, implementation details, numeric thresholds, safety assumptions, security assumptions, or interface details unless supported by source content or confirmed by the user.

## SRS

Each SRS item shall include:

- SRS ID
- System Requirement
- Domain
- Parent CRS ID
- Derived
- Rationale
- Verification Method
- Status
- Issue

Every SRS item shall trace to at least one CRS item.

## SWRS

Each SWRS item shall include:

- SWRS ID
- Software Requirement
- Domain
- Parent SRS ID
- Software Boundary
- Derived
- Rationale
- Verification Method
- Status
- Issue

Every SWRS item shall trace to at least one SRS item.

## SRS-to-SWRS Transformation Principle

When deriving SWRS items from SRS items, do not directly copy or mechanically reword the SRS text.

SWRS shall be written from a software development perspective and shall describe externally observable software behavior at the software boundary. Use ISO/IEC/IEEE 29148-inspired requirement writing principles: clear stakeholder/software intent, atomicity, feasibility, verifiability, traceability, and explicit rationale for derived requirements.

For each SRS-to-SWRS transformation, consider:

- What software behavior is needed to satisfy the system requirement?
- What are the relevant software inputs, outputs, states, modes, interfaces, data, diagnostics, timing, configuration, calibration, safety, or security aspects?
- What behavior is externally observable and testable?
- What remains system-level, hardware-level, or design-level and should not be forced into SWRS?
- What information is missing and should become an open issue instead of being invented?

The SWRS shall not be a copy of the SRS. It shall refine, allocate, or decompose the SRS into software-relevant requirements while preserving parent traceability.

## Requirement Quality Rules

Each requirement shall:

1. Be traceable to a higher-level requirement or source item.
2. Use clear mandatory language, preferably `shall`.
3. Describe one single need only.
4. Be feasible and verifiable.
5. Avoid ambiguous words such as `fast`, `suitable`, `appropriate`, `user-friendly`, `robust`, `optimized`, and `as needed`.
6. Be classified by domain or requirement type.
7. Distinguish functional, performance, interface, diagnostic, safety, security, configuration, calibration, resource, and timing concerns.
8. Keep software requirements focused on externally observable software behavior.
9. Mark and justify derived requirements.
10. Report missing, unclear, conflicting, or unverifiable information as open issues.

## Traceability Matrix

The main traceability matrix shall include:

- Trace ID
- CRS ID
- SRS ID
- SWRS ID
- Trace Status
- Notes

Allowed trace status values: Complete, Missing SRS, Missing SWRS, System-only, Needs Clarification.

## Output File Naming

When generating files, use the filename rules in `references/file-naming-convention.md`.

## Anti-Hallucination Rules

1. Do not invent requirements.
2. Do not invent source references.
3. Do not derive SRS or SWRS directly from raw source documents without a CRS Working Set.
4. Do not process only local chunks without first building a global document overview.
5. Do not rewrite uncertainty as confirmed facts.
6. Do not merge unrelated requirements.
7. Do not split requirements without preserving traceability.
8. Do not add implementation details unless explicitly supported.
9. Do not derive numeric thresholds, timing values, safety assumptions, security assumptions, diagnostic behavior, or interface details without source support or user confirmation.
10. If information is missing, create an open issue.
