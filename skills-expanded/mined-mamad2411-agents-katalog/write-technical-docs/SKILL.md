---
name: write-technical-docs
description: Use when generating or refreshing technical reference documentation with code-verified content and link integrity checks.
---

# Technical Documentation Skill

## Specialization

This skill is specialized for the workflow described in this file and should remain narrowly bounded to that responsibility.

It should not absorb adjacent planning, execution, or review responsibilities that belong to other assets.

## Role

Use this skill to generate and maintain rich, developer-trustworthy documentation that mirrors the repository structure and stays aligned with real code behavior.

This skill is documentation-first and evidence-first:

- Document what is verifiably true from source code and existing repository artifacts.
- Flag unknowns explicitly instead of guessing.
- Keep links valid and navigable.
- Prefer incremental updates over full rewrites when documents already exist.
- Use descriptive filenames for catalogs and indexes; reserve `README.md` for true folder entry-point guides.

## Mandatory Inputs

- Documentation scope (default: entire workspace).
- Documentation root output path (default: `/.docs/components/<domain>/`).
- Preferred audience (default: developers and maintainers).
- Language/ecosystem hints when available (for API idioms and examples).

If required input is missing, ask focused questions before writing.

## Parallelization Policy

When scope is workspace-wide, split by top-level directory and run discovery in parallel where safe:

1. Build canonical file inventory.
2. Partition inventory by top-level folder and by artifact type (code, config, scripts, docs).
3. Analyze partitions in parallel via `Explore` or equivalent read-only workflows.
4. Merge findings into one documentation graph.
5. Run one final consistency and link audit pass.

## Output Contract

Produce a technical reference documentation set under the selected root (default `/.docs/components/<domain>/`) with this baseline:

- `index.md` - repository documentation home page.
- `code-structure.md` - source tree mirror and navigation map.
- `coverage-report.md` - documented vs undocumented file matrix.
- One documentation page for each significant source file, type, or module.
- Directory-level landing pages that mirror the code hierarchy.

Folder granularity rules:

- Use at least three levels for generated docs when scope is non-trivial: `<domain>/<subdomain>/<artifact-type>/`.
- Keep folder names lowercase and one word per level.
- Avoid flat dumps of many files into a single folder.
- Do not place module documentation files directly in `.docs/components/` unless the user explicitly requests a flat structure.

When creating landing pages:

- Use `README.md` only if the page explains the folder's purpose, usage, and local conventions.
- Use a descriptive filename such as `*-catalog.md` or `*-index.md` when the page is primarily navigational or tabular.

Use the provided templates:

- [technical-api-page-template.md](./references/technical-api-page-template.md)
- [documentation-index-template.md](./references/documentation-index-template.md)
- [coverage-report-template.md](./references/coverage-report-template.md)

## Technical Reference Page Requirements

Each generated reference page should include applicable sections:

1. Summary
2. Package/Namespace/Module
3. Syntax or Signature
4. Parameters
5. Return Value
6. Exceptions and Error Conditions
7. Remarks
8. Thread Safety and Concurrency Notes
9. Security Considerations
10. Performance Notes
11. Examples (basic and advanced where feasible)
12. See Also

Use "Not observed in code" when data is unavailable.

## Reliability and Trust Gates

Before finalizing documentation, enforce all gates:

- Evidence Gate: Every technical claim maps to actual code or existing docs.
- History Gate: When describing change history, superseded behavior, or prior state, use git history (`git log`, `git show`, `git diff`) as source of truth.
- Drift Gate: Remove or correct stale statements contradicted by code.
- Coverage Gate: Attempt to document every file in scope; explicitly justify exclusions. Run [Get-DocumentationMetrics.ps1](./Get-DocumentationMetrics.ps1) to measure XML doc coverage and README coverage objectively.
- Link Gate: Validate that every internal link target exists.
- Consistency Gate: Terminology is aligned with code symbols and established naming.

### Documentation Metrics Script

[Get-DocumentationMetrics.ps1](./Get-DocumentationMetrics.ps1) measures documentation quality across the solution:

- **XML documentation coverage**: percentage of public C# declarations with `///` XML doc comments.
- **README coverage**: percentage of `src/` projects with a [README.md](./../../../README.md).
- **Composite score**: weighted result from both metrics.

Usage:

```powershell
# Check current coverage (default minimum: 80)
./.github/skills/write-technical-docs/Get-DocumentationMetrics.ps1

# Enforce a minimum score and export metrics as JSON
./.github/skills/write-technical-docs/Get-DocumentationMetrics.ps1 -MinimumScore 85 -EnforceMinimum -OutputJsonPath ./.docs/reports/doc-metrics.json
```

The CI/CD pipeline runs this script with `-EnforceMinimum` on every push and pull request. Documentation work is blocked from merging if the composite score falls below the configured threshold.

## Workspace Coverage Rules

Default behavior is full-workspace attempt:

- Include source files, scripts, configuration, and infrastructure artifacts.
- Exclude generated folders only with explicit rationale (for example, build outputs).
- For binary or opaque artifacts, create short descriptor entries rather than fabricating internals.

Maintain a documented exclusion list in `coverage-report.md`.

## Link Integrity Requirements

- Use relative links.
- Ensure every linked document exists at generation time.
- Avoid dead references to planned-but-missing files.
- Re-run link validation after any rename or move.

If links cannot be validated automatically, run a deterministic manual check from the generated index and record unresolved items.

## Review and Update Mode

When invoked in review mode:

1. Inventory current documentation.
2. Identify missing docs and stale docs.
3. Update existing files in place where possible.
4. Create missing pages needed to satisfy coverage.
5. Regenerate index and coverage report.
6. Validate links and record final status.

## Writing Standards

- Markdown only, clear heading hierarchy, flat lists for scanability.
- Keep style concise but technically complete.
- Brevity is an explicit requirement: remove duplication and narrative padding while preserving evidence and developer trust.
- Prefer exact symbol names and file-backed references.
- Never invent behavior, defaults, ranges, or guarantees.
- Use consistent requirement identifiers when writing specification-like sections.
- Never create root-level folders in any workspace.
- Never create top-level reference folders; keep references under owning asset paths.

## Core Documentation Types

This skill addresses three core documentation patterns:

- **README blueprint** - folder entry-point guidance explaining purpose, usage, and local conventions.
- **OO Component docs** - C4 architecture diagrams plus mermaid visualizations with detailed member/interface documentation.
- **Specification / PRD merged documents** - unified documents combining goals, personas, requirements, and acceptance criteria using explicit IDs (REQ-, SEC-, CON-, AC-).

## Completion Checklist

Documentation work is complete only when:

- `index.md`, `code-structure.md`, and `coverage-report.md` are present.
- Documentation tree reflects repository structure.
- Coverage report explains included and excluded files.
- Internal links resolve to existing docs.
- No unresolved evidence gaps remain without explicit note.
- [Get-DocumentationMetrics.ps1](./Get-DocumentationMetrics.ps1) passes at the configured minimum score (default: 80; CI enforces 85).

## Trigger Conditions

Invoke this skill when any of the following is true:

- Technical reference documentation must be created or refreshed.
- Documentation needs code-verified, evidence-backed content.
- Link integrity and developer-trustworthy docs are required before publication.

## Inputs

- User request context and target scope for this skill invocation.

## Required Outputs

- A concrete, workspace-applicable result aligned with this skill purpose.

## Workflow

1. Gather required context and constraints from the workspace and user request.
2. Execute the skill-specific steps and produce the required artifacts or decisions.
3. Validate outputs for completeness and consistency with active workspace instructions.


