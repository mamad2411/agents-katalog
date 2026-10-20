---
name: powershell-style-guide
description: >-
  PowerShell coding style guide for automation scripts and modules. Enforces
  naming conventions, commenting standards, error handling, logging, idempotency
  patterns, output standards, and security rules.
when-to-use: >-
  Invoke when writing or reviewing PowerShell scripts (.ps1), modules (.psm1),
  or functions. Also invoke when establishing PowerShell standards for a team or
  onboarding engineers to a PowerShell codebase.
categories:
  - powershell
  - automation
  - code-style
---

# PowerShell Style Guide

Write for the reader, not the writer. The reader might be a junior admin at 2am, another AI agent, or you in 6 months. Plain English names. No cleverness over clarity. Idempotency is non-negotiable.

## Naming Conventions

| Element | Convention | Example |
|---|---|---|
| **Functions** | Verb-Noun (approved verbs from `Get-Verb`) | `Get-StaleServicePrincipal` |
| **Parameters** | PascalCase | `$UserPrincipalName`, `$ResourceGroupName` |
| **Local variables** | camelCase | `$retryCount`, `$userMailboxes` |
| **Boolean params** | Standard names | `$Force`, `$WhatIf`, `$Confirm` (not `$DoIt`) |
| **Script files** | Verb-Noun.ps1 | `Get-StaleServicePrincipal.ps1` |
| **Module folders** | PascalCase | `StaleServicePrincipal/` |

**Rule**: `$userMailboxes` not `$mbxs`. `Get-StaleServicePrincipal` not `Get-StaleSP`.

---

## Code Structure Requirements

- [ ] `[CmdletBinding()]` on every function — no exceptions
- [ ] `SupportsShouldProcess` on every function that changes state
- [ ] `[OutputType()]` on every function
- [ ] Splatting mandatory for any command with 3+ parameters
- [ ] One function per file in modules (Public/Private separation)
- [ ] Parameter sets over boolean flags for mutually exclusive options

### Splatting Example

```powershell
# GOOD — readable, maintainable
$mailboxParams = @{
    Identity        = $UserPrincipalName
    Type            = 'Regular'
    RetentionPolicy = 'Default MRM Policy'
    ErrorAction     = 'Stop'
}
Set-Mailbox @mailboxParams

# BAD — 200-character one-liner
Set-Mailbox -Identity $UserPrincipalName -Type Regular -RetentionPolicy 'Default MRM Policy' -ErrorAction Stop
```

---

## Commenting Standards

```powershell
# GOOD: Explains WHY
# Retry because Graph API returns 429 during tenant-wide operations
Invoke-MgGraphRequest @params

# BAD: Restates the code
# Invoke the Graph request
Invoke-MgGraphRequest @params
```

- [ ] Every function gets comment-based help (`.SYNOPSIS`, `.PARAMETER`, `.EXAMPLE`)
- [ ] Every `catch` block explains what we're catching and why
- [ ] Every `$using:` in `-Parallel` explained if non-obvious
- [ ] Don't comment obvious PowerShell — `# Loop through users` above `foreach` is noise

---

## Error Handling Rules

- [ ] Every `try` has a `catch` with a typed exception where possible
- [ ] Never use bare `catch { }` — always log, re-throw, or handle meaningfully
- [ ] `-ErrorAction Stop` inside `try` blocks (catches non-terminating errors)
- [ ] `$PSCmdlet.ThrowTerminatingError()` with constructed `ErrorRecord` for function errors
- [ ] `-ErrorVariable` when you want to continue but track failures
- [ ] Include original exception in re-thrown errors (`$_.Exception`)

### Decision Tree

```
Error in a try block?
├─ Typed catch available → catch [SpecificException] { handle }
├─ Need to continue processing → -ErrorVariable +errors
├─ Function-level error → $PSCmdlet.ThrowTerminatingError()
└─ Must re-throw → throw (preserves stack trace in PS 7)
```

---

## Logging Standards

| Cmdlet | Purpose | When to Use |
|---|---|---|
| `Write-Verbose` | Operational step tracking | What the script is doing |
| `Write-Information` | Structured output | Data calling scripts can capture |
| `Write-Warning` | Non-fatal issues | User should know but script continues |
| `Write-Error` | Recoverable failures | Never for terminating conditions |
| `Write-Host` | **NEVER in functions/modules** | Bypasses pipeline, can't be captured |

- Timestamps in verbose: `Write-Verbose "[$((Get-Date).ToString('HH:mm:ss'))] Processing $item"`
- Structured logging for automation (JSON/CSV with Timestamp, Level, Message, Script, Line)

---

## Idempotency Pattern

Every script must be safe to run twice. Check state before changing state.

```powershell
# GOOD: Idempotent
$existingGroup = Get-AzResourceGroup -Name $ResourceGroupName -ErrorAction SilentlyContinue
if ($existingGroup) {
    Write-Verbose "Resource group '$ResourceGroupName' already exists — skipping"
} else {
    Write-Verbose "Creating resource group '$ResourceGroupName'"
    New-AzResourceGroup -Name $ResourceGroupName -Location $Location
}

# BAD: Crashes on second run
New-AzResourceGroup -Name $ResourceGroupName -Location $Location
```

**Rules**:
- Report what you did, skipped, and failed — every time
- Return consistent output objects regardless of action taken
- Use `-WhatIf` to let users preview changes

---

## Output Standards

- [ ] Functions return `[PSCustomObject]` with meaningful properties, not strings
- [ ] Include `Status` property: `Created`, `AlreadyExists`, `Updated`, `Failed`, `Skipped`
- [ ] Never mix `Write-Output` with `Write-Host`
- [ ] Suppress unwanted output with `[void]` or `$null =`
- [ ] Pipeline-friendly: one object per item, not a summary at the end

---

## Security Rules (Non-Negotiable)

| Rule | Enforcement |
|---|---|
| No embedded credentials | Use `SecretManagement`, managed identity, workload identity |
| No `ConvertTo-SecureString -AsPlainText` with hardcoded strings | Use Key Vault or `SecretManagement` |
| No `Invoke-Expression` | If you think you need it, redesign |
| Validate all user input | `[ValidatePattern()]`, `[ValidateSet()]`, `[ValidateScript()]` |
| Use `-Credential` parameter | Never prompt for passwords inline |

---

## What NOT to Do

| Anti-Pattern | Use Instead |
|---|---|
| Aliases in scripts (`gci`, `%`, `?`) | Full cmdlet names (`Get-ChildItem`, `ForEach-Object`) |
| `Write-Host` in reusable code | `Write-Verbose`, `Write-Information` |
| `$ErrorActionPreference = 'SilentlyContinue'` at script scope | Scoped `-ErrorAction` per command |
| Positional parameters in scripts | Named parameters always |
| `+=` on arrays in loops | `[System.Collections.Generic.List[object]]` |
| `Select-Object *` in production | Explicit property selection |
| `Format-*` in data-returning functions | Formatting destroys objects |

---

## Function Template

```powershell
function Verb-Noun {
    <#
    .SYNOPSIS
        Brief description of what the function does.
    .DESCRIPTION
        Detailed description.
    .PARAMETER Name
        Description of the parameter.
    .EXAMPLE
        Verb-Noun -Name 'value'
        Description of what this example does.
    #>
    [CmdletBinding(SupportsShouldProcess)]
    [OutputType([PSCustomObject])]
    param(
        [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
        [ValidateNotNullOrEmpty()]
        [string]$Name
    )

    process {
        if ($PSCmdlet.ShouldProcess($Name, 'Action description')) {
            try {
                # Implementation
                [PSCustomObject]@{
                    Name   = $Name
                    Status = 'Created'
                }
            }
            catch [System.SpecificException] {
                # Handle specific error
                Write-Error "Failed to process '$Name': $_"
            }
        }
    }
}
```

## Related Skills

- `error-handling-patterns` — Cross-language retry, circuit breaker, and compensation patterns
- `naming-conventions` — Cross-language Azure resource and code naming standards
