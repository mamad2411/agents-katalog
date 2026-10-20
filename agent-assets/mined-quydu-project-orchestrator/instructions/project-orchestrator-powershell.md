---
applyTo: "**/*.ps1,**/*.psm1,**/*.psd1"
description: PowerShell authoring standards.
---

# PowerShell Instructions

- Target PowerShell 7 or later. Do not rely on Windows PowerShell 5.1 behavior.
- Begin every script with `Set-StrictMode -Version Latest` and `$ErrorActionPreference = 'Stop'`.
- Use approved verbs and `PascalCase-Noun` function names. Verify with `Get-Verb`.
- Use full cmdlet names and named parameters. No aliases (`ls`, `%`, `?`, `cat`) in committed code.
- Prefer `Get-ChildItem`, `Where-Object`, and `Select-Object` over external executables.
- Declare `[CmdletBinding()]` and use `[Parameter(Mandatory)]` rather than prompting inline.
- Support `-WhatIf` and `-Confirm` via `SupportsShouldProcess` for any destructive operation.
- Quote paths and use `Join-Path` instead of string concatenation.
- Accept credentials only as `[pscredential]` or `[securestring]`. Never accept or emit plaintext credentials.
- Emit objects, not formatted text. Leave formatting to the caller.
- Wrap external command calls and check `$LASTEXITCODE` explicitly.
- Never use `Invoke-Expression`.
- Avoid commands that trigger an interactive elevation prompt inside automation.
