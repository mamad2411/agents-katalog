---
name: check-shell-profile
description: Check shell profile ($PROFILE), PATH, aliases, and env for broken or slow config
argument-hint: "[shell]"
related:
  - check-system-env
  - resolve-errors
  - report

---

## Goal

Inspect shell startup profiles and environment config for errors, duplicate PATH entries, broken aliases, missing tools, and startup slowdowns

## Scope

- Covers PowerShell (`$PROFILE` for every host), NuShell (`env.nu`, `config.nu`), CMD (`AutoRun`), Git Bash, and any WSL shells found on the machine
- Checks PATH duplicates/dead entries, module imports that fail, aliases pointing at nonexistent targets, and startup time
- Read-only: inspect and report only — never edit a profile without an explicit instruction

## Execute

### 1. Detect Shells And Profiles

> Goal: know which shells the machine uses and where the profiles live

1. Run `/check-system-env` to see the installed shells
2. PowerShell: read `$PROFILE` in every scope (`AllUsersAllHosts`, `CurrentUserAllHosts`, `CurrentUserCurrentHost`)
3. NuShell: `$nu.env-path` and `$nu.config-path`
4. CMD: registry `HKCU\Software\Microsoft\Command Processor\AutoRun`
5. Record the profile files that actually exist

### 2. Validate Profile Syntax

> Goal: the profile parses with no error at startup

1. PowerShell: run `pwsh -NoProfile -Command "[System.Management.Automation.PSParser]::Tokenize((Get-Content $PROFILE -Raw), [ref]`$null)"` or `Test-Path` + an isolated dot-source
2. NuShell: run `nu --check-config` or `nu -c "source $nu.env-path"` in a subprocess
3. Record syntax errors with line numbers

### 3. Check PATH Health

> Goal: a clean PATH with no duplicates or dead entries

1. Split PATH into entries and `Test-Path` each one
2. Flag: `dead` (directory missing), `duplicate` (repeated), `empty`
3. Compare Machine PATH vs User PATH to find shadowed entries
4. Verify that tools the profile imports actually exist (`Get-Command <name>`)

### 4. Check Aliases And Functions

> Goal: aliases point at targets that exist

1. `Get-Alias` and `Get-Command -CommandType Function` from the profile
2. Check that each target command exists — flag `broken` if it doesn't
3. Look for aliases that shadow important commands

### 5. Measure Startup Time

> Goal: know whether the profile makes the shell slow

1. Run `Measure-Command { pwsh -NoLogo -Command exit }` and compare against `pwsh -NoProfile`
2. Flag `slow` if startup with the profile takes >2 seconds
3. Pinpoint the slow profile sections (module imports, network calls, prompt init)

### 6. Report

> Goal: summarize findings with fix suggestions

1. Build a `/report` with columns: `No.`, `Area`, `Finding`, `Severity`, `Location`, `Suggestion`
2. Severity: `error`, `warning`, `info`
3. Hand off to `/resolve-errors` if there are errors

## Rules

### 1. Read-Only

- Never edit profiles, PATH, or the registry without an explicit instruction
- Every suggestion must have evidence (file:line or command output)

### 2. Isolated Execution

- Inspect profiles in a separate subprocess — never dot-source into the current session
- Do not run profile code with side effects against the system

### 3. Coverage

- Check every shell found, not just PowerShell
- Include `mise` activation and tool shims in the PATH check

- Use /check-system-env if needed
- Use /resolve-errors if needed

## Fix

> Follow `deep-review-codebase/SKILL.md` when the user confirms fixing the findings

1. Prioritize findings by severity — canonical steps in `deep-review-codebase/SKILL.md`
2. Fix per finding — profile profiling, plugin audit, lazy loading for slow startup (shell profile)
3. Preserve behavior + verify + report — canonical in `deep-review-codebase/SKILL.md`

## Expected Outcome

- Know which profile has errors, which PATH entry is dead, which alias is broken
- Know startup time and what causes the slowdown
- Prioritized report with a fix suggestion per finding
