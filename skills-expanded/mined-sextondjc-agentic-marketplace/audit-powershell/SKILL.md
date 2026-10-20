---
name: audit-powershell
description: Use when auditing PowerShell scripts for safety, reliability, and style issues, and when you need actionable correction recommendations.
---

# PowerShell Script Review

## Specialization

Review PowerShell scripts in the workspace, identify correctness and maintainability issues, and provide concrete recommendations for correction.

This skill is review-first. It does not make edits unless explicitly requested.

## Trigger Conditions

Use this skill when one or more are true:

- You need a quality or safety assessment of `.ps1` or `.psm1` files.
- You want recommendations before merging PowerShell automation changes.
- Script behavior is brittle, interactive, or not automation-safe.
- You need a repeatable review report for PowerShell scripts.

Do not use this skill for general C# code review.

## Standards

Apply these workspace standards during review:

- [powershell.instructions.md](./../../instructions/powershell.instructions.md)
- [secure-coding.instructions.md](./../../instructions/secure-coding.instructions.md)
- [governance-lifecycle.instructions.md](./../../instructions/governance-lifecycle.instructions.md)

## Inputs

Required:

- Review scope path (workspace root by default).

Optional:

- Target file(s) or folder(s).
- Severity focus (`Error`, `Warning`, `Information`).
- Report directory (default: `.docs/changes/audit-powershell-reviews`).

## Assets

- Workspace review helper script: `references/scripts/Invoke-PowerShellScriptReview.ps1`

## Exported Artifacts

This skill publishes markdown reports for cross-agent consumption.

- Export format: `Markdown` only
- Default report path: `.docs/changes/audit-powershell-reviews/`
- Default filename: `audit-powershell.md`
- Stable latest filename: `latest-audit-powershell.md` (written by default)

## Invocation Model

Use this as a normal workspace skill through the `powershell-reviewer` agent.

- Primary entry point: `powershell-reviewer` agent performs the review and recommendations.
- The helper script is an internal implementation asset for repeatable report generation.
- Reviews must include IDE diagnostics (`Problems`) plus script analyzer findings.

Do not require users to invoke PowerShell commands directly for standard review requests.

## Workflow

1. Resolve review scope and enumerate `*.ps1` and `*.psm1` files.
2. Run the helper script for baseline findings (PSScriptAnalyzer + heuristic checks).
3. Group findings by severity and rule category.
4. For each finding, provide:
   - what is wrong,
   - why it matters,
   - a concrete correction recommendation.
5. If no findings are present, report that explicitly and call out residual risks (for example, runtime-path coverage not validated).

## Output Contract

Return a concise report with:

- A severity summary table.
- A findings table with columns:
  - `File`
  - `Line`
  - `Severity`
  - `Rule`
  - `Issue`
  - `Recommendation`
- A short "next fixes" list prioritized by highest severity first.
- Persisted markdown report in `.docs/changes/audit-powershell-reviews/` so other agents can ingest it.

## Recommendation Patterns

Use recommendation language that is directly actionable:

- Replace aliases with full cmdlet names.
- Replace `Write-Host` data output with object output or `Write-Verbose` for diagnostics.
- Remove `Read-Host` from automation scripts; use parameters with validation attributes.
- Add `[CmdletBinding(SupportsShouldProcess = $true)]` for mutating operations.
- Replace broad `catch` blocks with explicit error handling and structured error records.
- Remove `Invoke-Expression` and prefer direct command invocation.

## Done Criteria

Review is complete only when:

- All in-scope PowerShell files were scanned.
- Findings are severity-ranked and include concrete corrections.
- Standards references were applied.
- Unverified areas are explicitly listed.

## Required Outputs

- A concrete, workspace-applicable result aligned with this skill purpose.


