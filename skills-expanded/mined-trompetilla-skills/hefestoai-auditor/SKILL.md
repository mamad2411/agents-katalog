---
name: hefestoai-auditor
description: "AI-powered code analysis with HefestoAI. Run security audits, detect code smells, analyze complexity, and get ML-enhanced suggestions across 17 languages. Use when a user asks to analyze code, run a security audit, check code quality, or find vulnerabilities."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔨",
        "requires": { "bins": ["hefesto"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "hefesto-ai",
              "bins": ["hefesto"],
              "label": "Install HefestoAI (pip)"
            }
          ]
      }
  }
---

# HefestoAI Auditor Skill

AI-powered code quality guardian. Analyzes code for security vulnerabilities, complexity issues, code smells, and best practice violations across 17 languages.

## Quick Start

### Run a full audit

```bash
source ~/.hefesto_env 2>/dev/null
hefesto analyze <path> --severity HIGH
```

### Run audit on specific severity

```bash
hefesto analyze <path> --severity CRITICAL
hefesto analyze <path> --severity MEDIUM
```

### Check HefestoAI status

```bash
hefesto status
```

## Supported Languages (17)

**Code:** Python, TypeScript, JavaScript, Java, Go, Rust, C#
**DevOps/Config:** Dockerfile, Jenkins/Groovy, JSON, Makefile, PowerShell, Shell, SQL, Terraform, TOML, YAML

## What It Detects

### Security Issues
- SQL injection vulnerabilities
- Hardcoded secrets and API keys
- Command injection risks
- Insecure configurations
- Missing authentication checks

### Code Quality
- Cyclomatic complexity (functions too complex)
- Deep nesting (>4 levels)
- Long functions (>50 lines)
- Duplicate code patterns
- Anti-patterns per language

### DevOps Issues
- Dockerfile: missing USER, no HEALTHCHECK, running as root
- Shell: missing `set -euo pipefail`, unquoted variables
- Terraform: missing tags, hardcoded values
- YAML/JSON: schema violations

## Interpreting Results

HefestoAI outputs results in this format:

```
📄 <file>:<line>:<col>
├─ Issue: <description>
├─ Function: <name>
├─ Type: <issue_type>
├─ Severity: CRITICAL | HIGH | MEDIUM | LOW
└─ Suggestion: <fix recommendation>
```

### Severity Guide
- **CRITICAL**: Security vulnerabilities, complexity >20. Fix immediately.
- **HIGH**: Code smells, complexity 10-20. Fix in current sprint.
- **MEDIUM**: Style issues, minor improvements. Fix when convenient.
- **LOW**: Informational, best practice suggestions.

### Summary Section

```
📊 Summary:
   Files analyzed: <count>
   Issues found: <total>
   Critical: <count>
   High: <count>
   Medium: <count>
   Low: <count>
```

## Pro Tips

### Exclude virtual environments
Always exclude venv/node_modules to avoid false positives from dependencies:
```bash
hefesto analyze <path> --severity HIGH --exclude venv,node_modules,.git
```

### Install pre-push hook
Automatically audit before pushing to remote:
```bash
hefesto install-hook
```

### Run REST API server
Serve analysis via HTTP API (8 endpoints):
```bash
hefesto serve --port 8000
```

## Licensing Tiers

| Tier | Price | Key Features |
|------|-------|-------------|
| **FREE** | $0/mo | Static analysis, 17 languages, pre-push hooks |
| **PRO** | $8/mo (launch) | ML semantic analysis, REST API, BigQuery, deep security |
| **OMEGA** | $19/mo (launch) | IRIS monitoring, auto-correlation, real-time alerts |

All paid tiers include a **14-day free trial**.

### Upgrade Links
- **PRO**: https://buy.stripe.com/4gM00i6jE6gV3zE4HseAg0b
- **OMEGA**: https://buy.stripe.com/14A9AS23o20Fgmqb5QeAg0c

### Activate License
```bash
export HEFESTO_LICENSE_KEY=<your-key>
hefesto status  # verify tier
```

## About

Created by **Narapa LLC** (Miami, FL) — Arturo Velasquez (@artvepa)
GitHub: https://github.com/artvepa80/Agents-Hefesto
Support: support@narapallc.com

> "El código limpio es código seguro" 🛡️
