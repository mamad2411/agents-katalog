---
name: cmd-safety-check
description: Classify terminal commands by impact and require safeguards before risky execution.
category: security
aliases:
- command
- safety
- terminal
- security
- risk
- execute
triggers:
- Is this command safe
- Check this command
- Should I run this
- Command safety
- Risk assessment
keywords:
- command
- terminal
- safety
- risk
- execute
- shell
- bash
dependencies: []
risk: medium
version: 1.0.0
source: custom
enabled: true
capabilities:
- cmd-safety-check
- security
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- check
- cmd
- command
- risk
- safety
- security
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Cmd Safety Check

## Purpose
Classify terminal commands by their potential impact and risk level, requiring
appropriate safeguards before execution. The skill prevents accidental destructive
actions and ensures users understand the consequences of risky commands.

## When to Use
- Before running unfamiliar or complex commands
- When executing potentially destructive operations
- For commands involving system changes or deletions
- Before running commands with sudo/elevated privileges

## When NOT to Use
- For simple, well-understood commands (echo, ls, cd)
- When speed is critical for trivial operations
- For read-only diagnostic commands

## Capabilities
- Command parsing and analysis
- Risk classification (safe, caution, dangerous, critical)
- Impact prediction (what will be affected)
- Safeguard recommendations
- Rollback strategy suggestions
- Dry-run support where available

## Inputs
Natural-language request, execution context, and configuration parameters.

## Workflow
1. **Parse** — Analyze command syntax and arguments
2. **Classify** — Assign risk level based on command and context
3. **Explain** — Describe what the command will do
4. **Recommend** — Suggest safeguards or safer alternatives
5. **Confirm** — Require explicit approval for dangerous+ commands
6. **Execute** — Run only after confirmation

## Tools
None required (pure logic).

## Examples
**User:** "Is it safe to run: rm -rf node_modules/"
**Response:**
```
âš ï¸ Risk Level: DANGEROUS

Analysis:
- Command: rm -rf node_modules/
- Impact: Permanently deletes node_modules folder
- Scope: All nested files and folders
- Reversibility: Cannot be undone

Safeguards recommended:
â–¡ Verify you're in the correct directory first
â–¡ Use --dry-run flag if available
â–¡ Consider: rm -i node_modules/ for interactive mode

Say "confirm" to proceed, or I'll suggest a safer alternative.
```

## Safety
- ALWAYS explain risk before any destructive command
- Require explicit confirmation for dangerous+ operations
- Suggest safer alternatives when available
- Never auto-execute risky commands
- Provide rollback strategies where possible

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical security category.
