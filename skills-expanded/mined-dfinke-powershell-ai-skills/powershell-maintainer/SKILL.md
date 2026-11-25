---
name: powershell-maintainer
description: Help write, review, refactor, and maintain PowerShell scripts, functions, and modules with practical PowerShell 7+ and Windows PowerShell 5.1 awareness. Use for idiomatic cmdlet design, advanced functions, pipeline/object output, parameter validation, error handling, paths and encoding, secure credential handling, native command interop, PSScriptAnalyzer/Pester validation, and cross-platform maintainability.
---

# PowerShell Maintainer

Use this skill for general PowerShell coding and maintenance. Prefer the target repository's conventions when they are clear.

## Workflow

1. Orient to the project.
   - Check target PowerShell versions, supported operating systems, CI matrix, module manifest, dependencies, and existing style.
   - Prefer `pwsh` for PowerShell 7+ work; use Windows PowerShell 5.1 only when legacy modules or host constraints require it.
   - Inspect existing functions before introducing new naming, layout, or helper patterns.

2. Write maintainable functions and scripts.
   - Use approved `Verb-Noun` names for public functions.
   - Use `[CmdletBinding()]` for reusable functions and advanced scripts.
   - Add `SupportsShouldProcess` for state-changing operations and honor `$PSCmdlet.ShouldProcess()`.
   - Use parameter validation attributes for important inputs.
   - Emit objects for data; reserve `Write-Host` for user-facing console decoration.
   - Use full cmdlet names in committed code, not aliases.

3. Handle errors deliberately.
   - Use `-ErrorAction Stop` or a scoped `$ErrorActionPreference = 'Stop'` when `try`/`catch` must handle cmdlet failures.
   - Never leave `catch` blocks empty.
   - Capture `$_` early in a `catch` block if the error will be reused.
   - Check `$LASTEXITCODE` after native executables when the exit code matters.

4. Keep code portable unless the task is Windows-only.
   - Use `Join-Path`, `$PSScriptRoot`, and platform checks such as `$IsWindows`, `$IsLinux`, and `$IsMacOS`.
   - Specify encoding when writing files that will be read across platforms; prefer UTF-8 without BOM in PowerShell 7+, and account for Windows PowerShell 5.1's different encoding behavior.
   - Avoid hard-coded drive letters, path separators, and interactive assumptions.
   - Mark Windows-only code clearly instead of pretending it is cross-platform.

5. Protect users and systems.
   - Do not hard-code secrets or write credentials to logs.
   - Prefer `PSCredential`, SecretManagement, managed identity, environment-specific auth, or an existing repo pattern.
   - Avoid `Invoke-Expression` for constructed or untrusted input.
   - Use `-WhatIf`, `-Confirm`, dry-run modes, or explicit guards for destructive operations.

6. Validate before finishing.
   - Run the repository's existing checks first.
   - Use `Invoke-ScriptAnalyzer` when available.
   - Use `Invoke-Pester` for tests that exist or that you add.
   - For changes touching external systems, verify with mocks, dry runs, or a documented manual step.

## Common Checks

Discover the runtime:

```powershell
$PSVersionTable
Get-Module -ListAvailable
```

Find commands and help:

```powershell
Get-Command -Name Get-ChildItem
Get-Help Get-ChildItem -Full
Get-Verb
```

Inspect objects:

```powershell
$result | Get-Member
$result | Select-Object -First 1 *
```

Run validation:

```powershell
Invoke-ScriptAnalyzer -Path ./src -Recurse
Invoke-Pester
```

## Gotchas

- Parenthesize command calls inside logical expressions: `if ((Test-Path $a) -or (Test-Path $b))`.
- Use `ConvertTo-Json -Depth` for nested objects.
- Avoid `Format-*` in the middle of pipelines; format at the display boundary.
- Avoid `+=` in large loops; collect pipeline or `foreach` output directly.
- Treat `Write-Output`, `Write-Verbose`, `Write-Warning`, `Write-Error`, and `Write-Information` as different streams with different purposes.
- Account for Constrained Language Mode or locked-down hosts when the target environment may enforce AppLocker or WDAC.

## Examples

- `examples/advanced-function.ps1`: an advanced function with validation, pipeline input, and `ShouldProcess`.
- `examples/script-skeleton.ps1`: a script layout with help, parameters, strict mode, and error handling.
