---
name: follow-create-powershell-module
description: Create PowerShell modules/scripts to standard with manifest, functions, and Pester tests
argument-hint: "[module-name]"
related:
  - use-pwsh-shell
  - devin-scripts-toolkit
  - deep-review-codebase
  - follow-best-practice
  - run-test
  - run-check
  - report
---

## Goal

Create a PowerShell module or script project that follows best practices: module manifest (`.psd1`), script module (`.psm1`), public/private functions, comment-based help, and Pester tests

## Scope

- For creating PowerShell modules, script collections, or automation tooling on Windows (with cross-platform pwsh support)
- Covers module layout, naming (Verb-Noun), parameter validation, pipeline support, and error handling
- Does not cover publishing to PSGallery beyond the basic checklist

- Target `pwsh` 7.x (PowerShell Core, cross-platform — not Windows PowerShell 5.1) — always confirm the latest LTS/preview versions via `/deep-research` + `/follow-best-practice` (not pinned in this file — per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: Prepare context before creating

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to look at tooling
2. Run `/deep-review-codebase` if the module involves project dependencies
3. Check the PowerShell version with `$PSVersionTable.PSVersion` — target `pwsh` 7.6+ (LTS) by default

### 2. Gather Requirements

> Goal: Know what the module must do

1. Take `module-name` and purpose from the argument or ask the user
2. Identify the main functions to export (use approved verbs: `Get-`, `Set-`, `New-`, `Remove-`, `Test-`, `Invoke-`)
3. Determine the output type: objects for pipeline or formatted text
4. Determine the platform: Windows-only or cross-platform

### 3. Create Module Layout

> Goal: Standard PowerShell structure

1. Create the structure:
   - `<ModuleName>/<ModuleName>.psd1` — manifest from `New-ModuleManifest`
   - `<ModuleName>/<ModuleName>.psm1` — root module that dot-sources functions
   - `<ModuleName>/Public/*.ps1` — exported functions
   - `<ModuleName>/Private/*.ps1` — internal helpers
   - `<ModuleName>/Tests/*.Tests.ps1` — Pester tests
2. In the `.psm1`, dot-source `Public/*.ps1` then `Export-ModuleMember -Function` for public functions only
3. In the `.psd1`, specify `RootModule`, `ModuleVersion`, `GUID`, `Author`, `FunctionsToExport`

### 4. Write Functions

> Goal: Functions following PowerShell idioms

1. Every function uses `[CmdletBinding()]` and a `param()` block
2. Use parameter validation: `[Parameter(Mandatory)]`, `[ValidateSet]`, `[ValidateNotNullOrEmpty]`
3. Support the pipeline with `[Parameter(ValueFromPipeline)]` where appropriate
4. Use `Write-Verbose`, `Write-Warning`, `Write-Error` — not `Write-Host` — for diagnostics
5. Add comment-based help: `.SYNOPSIS`, `.DESCRIPTION`, `.PARAMETER`, `.EXAMPLE`
6. Return objects (`[PSCustomObject]`), not formatted strings

### 5. Add Tests

> Goal: Test coverage with Pester

1. Install Pester if missing: `Install-Module Pester -Scope CurrentUser -Force`
2. Create `Tests/<Function>.Tests.ps1` with `Describe`, `Context`, `It`
3. Test the happy path, parameter validation, and error cases
4. Run `/run-test` with `Invoke-Pester ./Tests`

### 6. Verify And Report

> Goal: The module imports and actually works

1. Run `Import-Module ./<ModuleName> -Force` then `Get-Command -Module <ModuleName>`
2. Run `Invoke-ScriptAnalyzer -Path ./<ModuleName> -Recurse` and fix findings
3. Run `/run-check` if the project has a lint pipeline
4. Report via `/report`: functions, coverage, analyzer results

## Rules

- Function names must be `Verb-Noun` using approved verbs (`Get-Verb`)
- Every public function must have comment-based help and a Pester test
- Do not use `Write-Host` for output that downstream consumers need
- Do not hardcode paths, credentials, or machine-specific values
- Support `-WhatIf` and `-Confirm` (`SupportsShouldProcess`) for state-changing functions
- Pass `PSScriptAnalyzer` before shipping

- Use /use-pwsh-shell when needed
- Use /devin-scripts-toolkit when needed
- Use /follow-best-practice when needed

## Expected Outcome

- The module imports and `Get-Command` lists the exported functions
- Functions follow `Verb-Noun` with parameter validation and comment-based help
- Pester tests pass and `Invoke-ScriptAnalyzer` has no significant findings
- Ready to use or extend without restructuring
