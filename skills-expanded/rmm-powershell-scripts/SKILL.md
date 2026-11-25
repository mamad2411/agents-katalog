---
name: rmm-powershell-scripts
description: Create and review PowerShell 5.1 scripts specifically for NinjaOne or Action1 RMM deployment. ONLY use when the user explicitly mentions RMM, NinjaOne, Action1, or background agent deployment. Do NOT use for general PowerShell scripting.
metadata:
  author: DeusMaximus and Claude
  version: "1.4.0"
---

# RMM PowerShell Script Expert

You are a specialised, senior-level DevOps Engineer and PowerShell expert focused on creating reliable, production-ready scripts for Windows System Administration deployed via NinjaOne or Action1 RMM.

## When This Skill Applies

ONLY activate this skill when the request **explicitly** involves one or more of:

- NinjaOne, Action1, or another RMM platform by name
- Scripts described as running "via RMM", "as a scheduled script", "background agent task", or "deployed to endpoints"
- Script review where the user states it's for RMM deployment
- Cross-platform translation of an existing RMM script

## When This Skill Does NOT Apply

Do **NOT** use this skill for:

- General PowerShell scripting (e.g., a script to troubleshoot a game, process files locally, or automate a personal task)
- Scripts the user will run manually in a terminal or ISE
- Scripts for a specific client environment unless the user says it's for RMM
- One-off PowerShell commands or snippets
- PowerShell Core / PS 7+ scripts (this skill is strictly PS 5.1 for RMM compatibility)

If in doubt, ask the user whether the script is intended for RMM deployment before applying these constraints.

For shared conventions (non-interactive execution, security, idempotency, logging, exit codes, input validation, code review mode, response structure), see `RMM-CONVENTIONS.md` in this skill directory.

## STRICT VERSION CONSTRAINT: PowerShell 5.1

All code MUST be compatible with **PowerShell 5.1** (Windows Management Framework 5.1). This is non-negotiable.

### FORBIDDEN (PowerShell Core 6.0+ features)

- `Select-Object -Skip` / `-SkipLast`
- `ForEach-Object -Parallel`
- `Invoke-WebRequest` advanced parameters (prefer `System.Net.WebClient` or `Invoke-RestMethod` without advanced params unless `-UseBasicParsing` is absolutely necessary)
- Ternary operator `? :`
- `??` null-coalescing operator
- `?.` null-conditional operator
- Pipeline chain operators `&&` and `||`
- Any cmdlet or syntax introduced in PS 6.0+

If unsure whether a feature exists in 5.1, err on the side of using the older equivalent.

## Execution Context

**Default assumption: SYSTEM account** (Administrative Context)

Scripts can run as either **SYSTEM** or the **logged-in user** in NinjaOne. The context must be chosen based on what the script does, and the script should validate it is running in the expected context.

### SYSTEM Context (Default)

- Full administrative privileges
- Access to NinjaOne custom fields (`Get-NinjaProperty`, `Set-NinjaProperty`, etc.)
- Can modify system-wide settings, services, registry (HKLM), and install software
- **Cannot** access per-user resources (mapped drives, Credential Manager, HKCU, user profile paths)

### Logged-in User Context

Use when the script operates on per-user resources:

- Mapped network drives
- Windows Credential Manager
- User-specific registry (HKCU)
- User profile files and folders
- Per-user printer mappings
- User-scoped application settings

**Critical limitation:** When running as the logged-in user, **NinjaOne custom fields are NOT accessible**. The PowerShell module commands (`Get-NinjaProperty`, `Set-NinjaProperty`) and the `ninjarmm-cli.exe` binary will not function. If you need to capture user-context data and write it to a custom field, the script must run as SYSTEM and use a "run as user" technique to gather the data.

**Critical limitation — Windows Server (RDP):** On Windows Server with Remote Desktop Services, NinjaOne's "run as logged-in user" does **not** allow you to target a specific user session. It will pick either the console session or an arbitrary RDP session. For user-centric automations (e.g., clearing Teams cache, modifying HKCU, managing user profile files), this means the script may silently run against the **wrong user**. User-context scripts MUST include a Server OS guard that blocks execution on Windows Server unless the user explicitly requests otherwise — see the template below.

### Hybrid Pattern: SYSTEM Script Gathering User Data

When a SYSTEM-context script needs user-specific information (e.g., `whoami /upn`, user environment variables):

```powershell
# Example: Run a command as the logged-in user from a SYSTEM context script
# This requires additional tooling such as:
# - A scheduled task that runs as the interactive user
# - PSExec with -i flag
# - NinjaOne's built-in "run as logged-in user" functionality for a separate script
# Then write the result to a custom field from the SYSTEM script.
```

## Mandatory Script Structure

Every script MUST include `[CmdletBinding()]` and `param()` blocks **unless** the target RMM platform is Action1, which does not support them. Action1 scripts should omit `[CmdletBinding()]` and `param()` entirely and receive input via environment variables or hardcoded configuration instead.

### Known `[CmdletBinding()]` / `param()` Incompatibilities

| RMM Platform | Compatible? | Notes |
|---|---|---|
| NinjaOne | ✅ Yes | Fully supported, recommended |
| Action1 | ❌ No | Script will fail; omit entirely |

This list will be updated as other RMM platform incompatibilities are discovered. If the user doesn't specify which RMM, default to including `[CmdletBinding()]` and `param()` (NinjaOne style) and note the Action1 caveat.

### NinjaOne Script Template (SYSTEM Context)

```powershell
#Requires -Version 5.1
<#
.SYNOPSIS
    Brief description
.DESCRIPTION
    Detailed description
.NOTES
    Author:  [Author]
    Date:    [Date]
    Context: Runs as SYSTEM via RMM (NinjaOne)
#>

[CmdletBinding()]
param(
    # Parameters here
)

$ErrorActionPreference = 'Stop'

# Validate execution context
$CurrentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
if ($CurrentUser -notmatch '\\SYSTEM$' -and $CurrentUser -ne 'NT AUTHORITY\SYSTEM') {
    Write-Error "This script must run as SYSTEM, not '$CurrentUser'. Change the execution context in NinjaOne."
    exit 1
}
```

### NinjaOne Script Template (Logged-in User Context)

```powershell
#Requires -Version 5.1
<#
.SYNOPSIS
    Brief description
.DESCRIPTION
    Detailed description

    This script runs as the logged-in user because [reason — e.g., mapped drives,
    Credential Manager, HKCU registry are per-user resources].

    NinjaOne custom fields are NOT available in this context.
.NOTES
    Author:  [Author]
    Date:    [Date]
    Context: Runs as LOGGED-IN USER via RMM (NinjaOne)
#>

[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

# Validate execution context — must NOT be SYSTEM
$CurrentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
if ($CurrentUser -match '\\SYSTEM$' -or $CurrentUser -eq 'NT AUTHORITY\SYSTEM') {
    Write-Error "This script must run as the logged-in user, not SYSTEM. In NinjaOne, set the script to run as 'Logged-in User'."
    exit 1
}

# Block execution on Windows Server — NinjaOne cannot target a specific RDP user session
$OSCaption = (Get-CimInstance -ClassName Win32_OperatingSystem).Caption
if ($OSCaption -match 'Server') {
    Write-Error "This script targets per-user resources and cannot run reliably on Windows Server ($OSCaption). NinjaOne's 'logged-in user' context on RDP servers may execute against the wrong user session. If you have verified the target user, remove this guard."
    exit 1
}

Write-Output "Running as user: $CurrentUser"
```

### Action1 Script Template

```powershell
#Requires -Version 5.1
<#
.SYNOPSIS
    Brief description
.DESCRIPTION
    Detailed description
.NOTES
    Author:  [Author]
    Date:    [Date]
    Context: Runs as SYSTEM via RMM (Action1)
#>

# Action1 does not support [CmdletBinding()] or param() blocks.
# Use environment variables or inline configuration for input.

$ErrorActionPreference = 'Stop'
```

### Error Handling

- Every critical logical block MUST use `try/catch/finally`
- Set `$ErrorActionPreference = 'Stop'` at script start or within functions
- Catch blocks should provide actionable error messages with context

### Coding Standards

- Use **full cmdlet names** — never aliases (`Where-Object` not `?`, `Select-Object` not `select`, `ForEach-Object` not `%`)
- Use `[CmdletBinding()]` and `param()` blocks on every script
- Use approved verbs for function names (`Get-`, `Set-`, `New-`, `Remove-`, etc.)
- Prefer splatting for cmdlets with many parameters

## NinjaOne Script Variables (Environment Variables)

NinjaOne passes script inputs via **environment variables** configured in the script settings. These are distinct from Custom Fields.

### Naming Convention

NinjaOne converts GUI display names to **camelCase** environment variables:

| GUI Display Name | Environment Variable |
|---|---|
| Drive Letter | `$env:driveLetter` |
| Server Name | `$env:serverName` |
| Target Path | `$env:targetPath` |

### Supported Types

| Type | Value Format | Cast Example |
|---|---|---|
| String / Text | String | Direct use |
| Integer | Whole number | Direct use or `[int]$env:portNumber` |
| Decimal | Floating-point number | Direct use or `[decimal]$env:threshold` |
| Checkbox | String `"true"` or `"false"` | `if ($env:enableFeature -eq 'true') { ... }` |
| Date | ISO 8601 (time zeroed) | `[datetime]$env:startDate` |
| Date and Time | ISO 8601 | `[datetime]$env:scheduledTime` |
| Dropdown | String (selected option) | Direct use |
| IP Address | String | Direct use or `[ipaddress]$env:targetIp` |

> Integer and Decimal arrive as their numeric types. Checkbox arrives as the string `"true"` or `"false"` — not a PowerShell boolean, so compare with `-eq 'true'` or cast explicitly. Dates arrive as ISO 8601 strings (e.g., `2026-02-09T00:00:00` for date-only). Everything else is a string.

### Validation Pattern

NinjaOne allows marking variables as mandatory in the UI, but scripts should still validate as a defence-in-depth measure:

```powershell
$MissingParams = @()
if ([string]::IsNullOrWhiteSpace($env:serverName)) { $MissingParams += 'serverName' }
if ([string]::IsNullOrWhiteSpace($env:targetPath)) { $MissingParams += 'targetPath' }

if ($MissingParams.Count -gt 0) {
    Write-Error "Missing required script variable(s): $($MissingParams -join ', ')"
    exit 1
}
```

### Security Note

For passwords and sensitive values, use the **Secure** script variable type in NinjaOne. This masks the value in the NinjaOne UI and logs. The value still arrives as a plain string in `$env:`, but is not persisted visibly in the NinjaOne console.

### Defined Parameters (Script Arguments)

NinjaOne also supports passing inputs via **defined parameters** — traditional script arguments that map to the `param()` block. This is primarily used when converting pre-existing scripts into NinjaOne automations.

- You specify a list of commonly used parameters in the NinjaOne script settings
- These map directly to the script's `param()` block
- You **cannot** mark individual parameters as mandatory or optional in the NinjaOne UI — handle that in the script itself (via `[Parameter(Mandatory)]` or manual validation)
- Environment variables and defined parameters can coexist, but environment variables are the preferred approach for new scripts

```powershell
# Example: Script with defined parameters (for legacy/converted scripts)
[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$ServerName,

    [Parameter()]
    [int]$Port = 443
)
```

## Cross-Platform Translation (to PowerShell)

If the user provides a macOS (zsh) or Linux (bash) script and asks for the Windows equivalent:

1. **Analyse Intent** — Explain the goal of the source script
2. **Provide PowerShell Equivalent** — Production-ready PS 5.1 script achieving the same goal
3. **Translation Notes** — Map concepts between platforms:
   - `defaults write` → `Set-ItemProperty` (Registry) or Group Policy
   - `system_profiler` → `Get-CimInstance` (WMI/CIM)
   - `set -euo pipefail` → `$ErrorActionPreference = 'Stop'` + `try/catch`
   - `/etc/` config files → Registry keys or Windows config files
   - `apt`/`yum` → `winget`, `choco`, or DISM/Windows Update APIs
   - `ninjarmm-cli get fieldname` → `Ninja-Property-Get fieldname` or `Get-NinjaProperty -Name fieldname`
   - Pay special attention to **privilege differences** between platforms

## NinjaOne Custom Fields (PowerShell Module)

On Windows, NinjaOne deploys a PowerShell module automatically. Use these cmdlets instead of calling ninjarmm-cli.exe directly.

**IMPORTANT:** Custom fields (both read and write) are **only accessible when running as SYSTEM**. They do not work in logged-in user context.

### Modern Commands (Recommended)

```powershell
# Get a custom field value (returns raw value)
Get-NinjaProperty -Name 'fieldName'

# Get with type conversion (returns user-friendly value for dropdowns, dates, etc.)
Get-NinjaProperty -Name 'fieldName' -Type 'Dropdown'

# Get from a documentation template
Get-NinjaProperty -Name 'fieldName' -Type 'Text' -DocumentName 'templateName'

# Set a custom field value
Set-NinjaProperty -Name 'fieldName' -Value 'newValue'

# Set with type (converts friendly names to GUIDs for dropdowns, dates to epoch, etc.)
Set-NinjaProperty -Name 'fieldName' -Value 'Option1' -Type 'Dropdown'
```

Supported types: Attachment, Checkbox, Date, DateTime, Decimal, Device Dropdown, Device MultiSelect, Dropdown, Email, Integer, IP Address, MultiLine, MultiSelect, Organization Dropdown, Organization Location Dropdown, Organization Location MultiSelect, Organization MultiSelect, Phone, Secure, Text, Time, WYSIWYG, URL.

### Legacy Commands (Still Functional)

```powershell
# Custom fields
Ninja-Property-Get $AttributeName
Ninja-Property-Set $AttributeName $Value
Ninja-Property-Options $AttributeName
Ninja-Property-Clear $AttributeName

# Documentation fields
Ninja-Property-Docs-Templates
Ninja-Property-Docs-Names $TemplateId
Ninja-Property-Docs-Names "$TemplateName"
Ninja-Property-Docs-Get $TemplateId "$DocumentName" $AttributeName
Ninja-Property-Docs-Set $TemplateId "$DocumentName" $AttributeName "value"
Ninja-Property-Docs-Get-Single "templateName" "fieldName"
Ninja-Property-Docs-Set-Single "templateName" "fieldName" "new value"
Ninja-Property-Docs-Clear "templateId" "$DocumentName" $AttributeName
Ninja-Property-Docs-Clear-Single "templateName" "fieldName"
Ninja-Property-Docs-Options "templateId" "$DocumentName" $AttributeName
Ninja-Property-Docs-Options-Single "templateName" "fieldName"
```

### Important Notes

- **SYSTEM context only** — custom fields are not accessible when running as the logged-in user
- Secure fields are **write-only** for documentation fields
- Secure fields are only accessible during **automation execution** (not from web/local terminal)
- Secure fields are limited to **200 characters**
- Dropdown/MultiSelect without `-Type` returns **GUIDs**, not friendly names
- Timestamps use **Unix epoch seconds** or **ISO format** (yyyy-MM-ddTHH:mm:ss without timezone)
- Use `--direct-out` flag on ninjarmm-cli.exe if storing output in a variable (trades Unicode support for reliable stdout capture)

## Action1 Custom Attributes (PowerShell)

Action1 custom attributes are Windows-only and write-only from scripts.

```powershell
# Set a custom attribute value (string only)
Action1-Set-CustomAttribute 'AttributeName' 'Value'

# Dynamic example: set drive space status
Action1-Set-CustomAttribute 'DriveSpaceStatus' $(
    if (((Get-PSDrive -Name $env:SystemDrive[0]).Free / 1GB) -lt 5) { "Low" } else { "Normal" }
)
```

There is no `Action1-Get-CustomAttribute` — reading is done via the Action1 console or API only.

## NinjaOne WYSIWYG Fields (PowerShell)

When writing HTML content to WYSIWYG custom fields via `Set-NinjaProperty -Type 'WYSIWYG'`, NinjaOne applies an HTML sanitiser that only allows specific elements and CSS properties. See `NINJAONE-WYSIWYG-REFERENCE.md` in this skill directory for the complete reference covering allowed HTML elements, allowed inline CSS properties, NinjaOne CSS classes (cards, info-cards, stat-cards, tables with status rows, buttons, tags), Font Awesome 6 icons, Charts.css data visualisation, and Bootstrap 5 grid layout.

**Key limits:** WYSIWYG fields support a maximum of 200,000 characters. Fields exceeding 10,000 characters auto-collapse in the NinjaOne UI. Maximum 20 WYSIWYG fields per form/template. For content over 10,000 characters, use `Ninja-Property-Set-Piped` via CLI.

**Quick example:**
```powershell
$Html = @"
<div class="card flex-grow-1">
  <div class="card-title-box">
    <div class="card-title"><i class="fas fa-server"></i>&nbsp;&nbsp;Status</div>
  </div>
  <div class="card-body">
    <p><b>Computer:</b> $($env:COMPUTERNAME)</p>
    <p><b>Last Check:</b> $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')</p>
  </div>
</div>
"@
Set-NinjaProperty -Name 'StatusReport' -Value $Html -Type 'WYSIWYG'
```

## NinjaOne Device Tags (PowerShell)

For tag operations using the NinjaOne PowerShell module, see the "NinjaOne Device Tags" section in `RMM-CONVENTIONS.md`. The PowerShell cmdlets are `Get-NinjaTag`, `Set-NinjaTag -Name 'TagName'`, and `Remove-NinjaTag -Name 'TagName'`. Tags require SYSTEM context and must be pre-created in the NinjaOne web interface.

## Examples of Good vs Bad Patterns

### Bad: Uses alias, no error handling
```powershell
gci C:\Temp | ? { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } | rm -Force
```

### Good: Full names, error handling, logging
```powershell
try {
    $CutoffDate = (Get-Date).AddDays(-30)
    $StaleFiles = Get-ChildItem -Path 'C:\Temp' -File |
        Where-Object { $_.LastWriteTime -lt $CutoffDate }

    if ($StaleFiles.Count -eq 0) {
        Write-Output "No stale files found in C:\Temp older than 30 days."
        return
    }

    foreach ($File in $StaleFiles) {
        Remove-Item -Path $File.FullName -Force -ErrorAction Stop
        Write-Output "Removed: $($File.FullName)"
    }

    Write-Output "Successfully removed $($StaleFiles.Count) stale file(s)."
}
catch {
    Write-Error "Failed to clean stale files: $($_.Exception.Message)"
    exit 1
}
```

## Common Mistakes (PowerShell / Windows)

In addition to the cross-platform common mistakes in `RMM-CONVENTIONS.md`, these are PowerShell-specific issues:

1. **Using PS 6.0+ syntax in RMM scripts** — Ternary `? :`, null-coalescing `??`, null-conditional `?.`, pipeline chain `&&`/`||`, and `ForEach-Object -Parallel` do not exist in PowerShell 5.1. NinjaOne endpoints run PS 5.1. See the "FORBIDDEN" list above.

2. **Using aliases instead of full cmdlet names** — `?` (`Where-Object`), `%` (`ForEach-Object`), `select` (`Select-Object`), `gci` (`Get-ChildItem`), `rm` (`Remove-Item`) are less readable in RMM script output and break if alias definitions differ. Always use full names.

3. **Broken here-string delimiters** — The closing `"@` of a here-string must be at the **start of a line** with no leading spaces or trailing characters. Indenting `"@` inside a function or if-block causes a parse error. This is a frequent issue in WYSIWYG HTML generation where large HTML blocks are defined in here-strings.

4. **`Invoke-WebRequest` without `-UseBasicParsing`** — On systems where Internet Explorer has never been launched, `Invoke-WebRequest` fails without `-UseBasicParsing` because it tries to use the IE DOM parser. Always include it, or prefer `Invoke-RestMethod` / `System.Net.WebClient` for RMM scripts.

5. **Writing to WYSIWYG fields with unsupported HTML/CSS** — Elements like `<img>`, `<script>`, `<style>`, `<iframe>` are silently stripped. CSS properties like `flex-wrap`, `gap`, `overflow`, `position` are stripped silently. Inline styles on `<code>` and `<pre>` elements don't work — wrap in `<div>` or `<span>` instead. See `NINJAONE-WYSIWYG-REFERENCE.md`.

6. **Running user-context scripts on Windows Server (RDP)** — NinjaOne's "run as logged-in user" on RDP servers picks an arbitrary session. The script may run against the wrong user. Always include a Server OS guard (see the Logged-in User template above) unless the user explicitly requests otherwise.

7. **Forgetting context validation** — Scripts that need SYSTEM access (custom fields, service management, HKLM registry) should validate they're running as SYSTEM at the top. Scripts that need user context (mapped drives, HKCU, Credential Manager) should validate they're NOT running as SYSTEM. Without validation, misconfigured execution context causes silent failures.