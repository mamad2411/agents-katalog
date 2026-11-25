---
name: prune-doc-artifacts
description: Use when auditing .docs planning and execution artifacts to identify stale, superseded, or generated leftovers and produce safe archive or removal candidates.
---

# Prune Doc Artifacts

## Specialization

Find candidate documentation leftovers from completed plans and execution runs without deleting anything automatically.

## Self-Containment Requirement

- REQUIRED: Keep execution self-contained within this skill. Do not delegate execution to sibling skills.
- REQUIRED: Keep execution self-contained within this skill. Do not delegate execution to sibling skills.

## Trigger Conditions

Invoke this skill when any of the following is true:

- Planning or change artifacts need an audit for stale or superseded documents.
- The docs tree may contain safe archive or removal candidates.
- Documentation hygiene must be restored without deleting blindly.

## Inputs

Required:
- Workspace root path.
- Optional focus path (default: `.docs`).

Optional:
- Include legacy review directories based on rename aliases (default: true).
- Include duplicate execution checklists (default: true).

## Safety Rules

- Never delete files in the first pass.
- Always run reference checks before proposing removal.
- Use git history (`git log`, `git show`, `git diff`) as the provenance source for superseded status; do not trust local snapshot mirrors as authoritative history.
- Treat historical ledgers and ADR files as keep-by-default unless explicitly marked superseded.
- Prefer `archive` recommendations before `delete` when confidence is medium.

## Workflow

1. Run `./references/scripts/Find-StaleDocs.ps1 -IncludeRefSnapshots $false` from workspace root.
2. Review output by category, reference count, and confidence.
3. Keep files with active references in live indexes.
4. Verify stale or superseded claims against git history before recommending archive or removal.
5. Mark duplicate checklists as keep-one/archive-rest candidates.
6. Produce a recommendation table: Keep, Archive, Remove candidate.
7. If approved by user, execute a separate change that updates links and removes/archives files.

## Output Contract

Return a grid-first report with:
- Category summary with X of Y candidates.
- Detailed candidate table (`Path`, `Category`, `ReferenceCount`, `Confidence`, `SuggestedAction`, `Reason`).
- Explicit "No action without confirmation" line.

## Done Criteria

This skill run is complete only when:
- Candidate list is produced.
- Every candidate has a reference count.
- Every candidate has a suggested action and confidence.
- No files are deleted during discovery.

## Required Outputs

- A concrete, workspace-applicable result aligned with this skill purpose.


