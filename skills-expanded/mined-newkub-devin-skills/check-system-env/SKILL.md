---
name: check-system-env
description: Check OS, shell, environment variables, and global root paths
argument-hint: "[scope]"
related:
  - check-code-structure
  - update-devin-global-skills
  - alternative
  - report

---

## Goal

Inspect Windsurf's system environment including OS, shell, environment variables, and global root paths

## Scope

Inspect:
- Operating System (OS)
- Shell type and version
- Important environment variables
- Global root paths (workflows, skills, rules)
- MCP configuration
- CLI programs inventory
- Browser history analysis
- User behavior analysis and development environment → see `references/extended-checks.md` (steps 11-13)

## Execute

### 1. Check Operating System

> Goal: Check Operating System

Check the OS in use:

1. Run `$PSVersionTable.OS` to show the OS version
2. Run `[System.Environment]::OSVersion.VersionString` to show the OS version string

```powershell
# Check OS
$PSVersionTable.OS
[System.Environment]::OSVersion.VersionString
```

### 2. Check Shell Information

> Goal: Check shell type and version

1. Run `$PSVersionTable.PSVersion` to show the PowerShell version
2. Run `$PSVersionTable.PSEdition` to show the shell type

```powershell
# Check PowerShell version
$PSVersionTable.PSVersion

# Check shell type
$PSVersionTable.PSEdition
```

### 3. Check Environment Variables

> Goal: Check important environment variables

1. Run `$env:PATH -split ';'` to show PATH
2. Run `$env:USERPROFILE` to show the user profile path
3. Run `$env:HOME` to show the home path
4. Run `$env:CODEIUM_HOME` to show the Codeium home
5. Run `$env:WINDSURF_HOME` to show the Windsurf home

```powershell
# Check PATH
$env:PATH -split ';'

# Check HOME/USERPROFILE
$env:USERPROFILE
$env:HOME

# Check Windsurf specific
$env:CODEIUM_HOME
$env:WINDSURF_HOME
```

### 4. Check Global Root Paths

> Goal: Check Global Root Paths

Check Windsurf's global root paths:

1. Check `$env:USERPROFILE\.codeium\windsurf\global_workflows`
2. Check `$env:USERPROFILE\.codeium\windsurf\skills`
3. Check `$env:USERPROFILE\.codeium\windsurf\global_rules`
4. Check `$env:USERPROFILE\.codeium\windsurf\mcp_config.json`

```powershell
# Global workflows path
$env:USERPROFILE\.codeium\windsurf\global_workflows

# Global skills path
$env:USERPROFILE\.codeium\windsurf\skills

# Global rules path
$env:USERPROFILE\.codeium\windsurf\global_rules

# MCP config path
$env:USERPROFILE\.codeium\windsurf\mcp_config.json
```

### 5. Check MCP Configuration

> Goal: Check MCP configuration

1. Run `Get-Content $env:USERPROFILE\.codeium\windsurf\mcp_config.json` to show the MCP config

```powershell
# Read MCP config
Get-Content $env:USERPROFILE\.codeium\windsurf\mcp_config.json
```

### 6. Check Global Workflows

> Goal: Check the existing global workflows

1. Run `Get-ChildItem $env:USERPROFILE\.codeium\windsurf\global_workflows -Filter "*.md"` to list the workflows

```powershell
# List global workflows
Get-ChildItem $env:USERPROFILE\.codeium\windsurf\global_workflows -Filter "*.md"
```

### 7. Check Global Skills

> Goal: Check Global Skills

Check the existing global skills:

1. Run `Get-ChildItem $env:USERPROFILE\.codeium\windsurf\skills -Recurse -Filter "*.md"` to list the skills

```powershell
# List global skills
Get-ChildItem $env:USERPROFILE\.codeium\windsurf\skills -Recurse -Filter "*.md"
```

### 8. Check Global Rules

> Goal: Check the existing global rules

1. Run `Get-ChildItem $env:USERPROFILE\.codeium\windsurf\global_rules -Filter "*.md"` to list the rules

```powershell
# List global rules
Get-ChildItem $env:USERPROFILE\.codeium\windsurf\global_rules -Filter "*.md"
```

### 9. Check CLI Programs Inventory

> Goal: Check the CLI programs installed on the machine

1. Run `Get-Command git, npm, bun, pnpm, yarn, docker, node, python, rust, go, cargo -ErrorAction SilentlyContinue` to show the important CLI tools
2. Run `where.exe git npm bun pnpm yarn docker node python 2>$null` to show the CLI tool paths
3. Run `npm list -g --depth=0 2>$null` to show the global npm packages
4. Run `bun pm ls -g 2>$null` to show the global bun packages
5. Run `pip list 2>$null` to show the Python packages

```powershell
# Check CLI tools
Get-Command git, npm, bun, pnpm, yarn, docker, node, python, rust, go, cargo -ErrorAction SilentlyContinue | Select-Object Name, Source

# Check CLI tool paths
where.exe git npm bun pnpm yarn docker node python 2>$null

# Check global npm packages
npm list -g --depth=0 2>$null

# Check global bun packages
bun pm ls -g 2>$null

# Check Python packages
pip list 2>$null
```

### 10. Check Browser History Analysis

> Goal: Check Browser History Analysis

Check browser history paths and their status:

1. Check `$env:LOCALAPPDATA\Google\Chrome\User Data\Default\History` (Chrome)
2. Check `$env:LOCALAPPDATA\BraveSoftware\Brave-Browser\User Data\Default\History` (Brave)
3. Check `$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\History` (Edge)
4. Check `$env:APPDATA\Mozilla\Firefox\Profiles` (Firefox)

```powershell
# Check browser history paths
Write-Output "Chrome: $env:LOCALAPPDATA\Google\Chrome\User Data\Default\History"
Write-Output "Brave: $env:LOCALAPPDATA\BraveSoftware\Brave-Browser\User Data\Default\History"
Write-Output "Edge: $env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\History"
Write-Output "Firefox: $env:APPDATA\Mozilla\Firefox\Profiles"

# Check if history files exist
Test-Path "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\History"
Test-Path "$env:LOCALAPPDATA\BraveSoftware\Brave-Browser\User Data\Default\History"
Test-Path "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\History"
Test-Path "$env:APPDATA\Mozilla\Firefox\Profiles"
```

## Rules

### 1. OS Detection

Detect the OS correctly:
- Windows: use PowerShell commands
- macOS/Linux: use bash commands
- Report the OS version and architecture

### 2. Shell Detection

Detect the shell type:
- PowerShell (Core/Desktop)
- Bash/Zsh (macOS/Linux)
- Shell version and edition

### 3. Path Validation

Verify that the paths exist:
- Global workflows path
- Global skills path
- Global rules path
- MCP config path

### 4. Report Format

Report in table format per `/report`:
- Use a "No." column first, ordered 1, 2, 3, ...
- Use appropriate headers and alignment
- Use symbols (✅, ❌, ⚠️) for status

- Use /check-code-structure, /update-devin-global-skills, /alternative if needed

## Expected Outcome

- Report OS, shell, and environment variables in a table
- Report global root paths in a table
- Report MCP configuration in a table
- Report global workflows/skills/rules in a table
- Report CLI programs inventory in a table
- Report browser history analysis in a table
- Report development environment in a table