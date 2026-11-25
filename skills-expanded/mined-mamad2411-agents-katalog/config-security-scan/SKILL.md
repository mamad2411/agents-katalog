---
name: config-security-scan
description: Scan .claude/ directory for security misconfigurations, exposed secrets, unsafe permissions
allowed-tools: [Bash, Read, Grep, Glob]
keywords: [security, config, scan, audit, claude, settings, mcp, hooks, agents, secrets, permissions]
---

# Config Security Scan

Scan your `.claude/` directory and related configuration files for security issues. Inspired by AgentShield pattern - checks CLAUDE.md, settings.json, MCP configs, hooks, and agent definitions for misconfigurations, exposed secrets, and unsafe permissions.

## Usage

```
/config-security-scan [path]
```

Default path: `.claude/` in current project.

## What It Checks

### 1. Secrets Detection (CRITICAL)
```
- API keys, tokens, passwords in CLAUDE.md
- Hardcoded credentials in hook scripts
- Secrets in MCP server configs
- Bearer tokens in agent definitions
- .env files committed to git
```

### 2. Permission Escalation (HIGH)
```
- dangerouslySkipPermissions in settings.json
- Overly broad tool permissions (all tools for simple agents)
- MCP servers with filesystem write access
- Hooks with shell execution and no validation
- Agents with Bash tool that don't need it
```

### 3. MCP Server Security (HIGH)
```
- Unknown/untrusted MCP servers
- MCP servers with network access + filesystem access
- Missing authentication on MCP endpoints
- MCP servers running as root/admin
- Unverified npm packages in MCP configs
```

### 4. Hook Security (MEDIUM)
```
- Hooks that execute user input
- Hooks without error handling
- Hooks that modify git config
- Hooks that access external networks
- Hooks with hardcoded paths
```

### 5. Agent Definition Security (MEDIUM)
```
- Agents with unnecessary tools
- Agents with system-level Bash access
- Agent descriptions that could enable prompt injection
- Agents without clear scope boundaries
```

### 6. Configuration Hygiene (LOW)
```
- Unused MCP server configs
- Deprecated settings
- Conflicting rules
- Missing recommended security settings
```

## Scan Procedure

```bash
# Step 1: Find all config files
find .claude/ -type f \( -name "*.json" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.js" -o -name "*.mjs" -o -name "*.ts" \)

# Step 2: Secret patterns
grep -rn "api[_-]?key\|password\|secret\|token\|bearer\|sk-\|pk_\|ghp_\|gho_\|xoxb-\|xoxp-" .claude/

# Step 3: Permission checks
grep -rn "dangerouslySkipPermissions\|allowedTools.*Bash\|shell_exec\|eval(" .claude/

# Step 4: MCP config review
cat .mcp.json 2>/dev/null | jq '.mcpServers | keys'

# Step 5: Hook review
ls .claude/hooks/ 2>/dev/null
```

## Output Format

```markdown
# Config Security Scan Report
Scanned: [path]
Date: [timestamp]

## Summary
- CRITICAL: X issues
- HIGH: Y issues
- MEDIUM: Z issues
- LOW: W issues

## CRITICAL Issues

### [Issue Title]
**File:** [path]
**Line:** [number]
**Issue:** [description]
**Fix:** [remediation]

## Recommendations
1. [Action item]
```

## Hard Exclusion List (Skip These)

These are NOT security issues in the .claude/ context:
- Environment variable references (not actual values)
- Test/example credentials clearly marked as such
- Public API keys meant to be public
- SHA hashes used as identifiers
- Base64-encoded non-secret data
- localhost/127.0.0.1 URLs

## Integration

- **security-reviewer**: Calls this skill during security audits
- **verifier**: Includes config scan in pre-commit checks
- **shipper**: Runs before deployments
