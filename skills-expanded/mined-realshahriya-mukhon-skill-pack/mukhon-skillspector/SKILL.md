---
name: mukhon-skillspector
description: |
  Security scanner for AI agent skills and Model Context Protocol (MCP) servers.
  Detects vulnerabilities, prompt injections, malicious code patterns, data exfiltration,
  and supply-chain threats before installing or executing agent skills. Supports static
  analysis and semantic LLM verification using Anthropic (Claude), OpenAI, or local engines.
license: MIT
metadata:
  version: v2.12.0
  publisher: nvidia
---

# SkillSpector: AI Agent Skill Security Scanner

SkillSpector is a comprehensive security analysis engine designed to evaluate AI agent skills (used by Claude Code, Codex, Antigravity, and MCP tools) before they are installed or run. It detects 71+ vulnerability patterns across 17 categories including prompt injection, data exfiltration, privilege escalation, and tool misuse.

## Quick Start CLI Commands

### 1. Static Scan (Fast, Zero API Calls)
Scan any skill directory, Git repository, or archive without invoking an LLM:
```bash
skillspector scan ./path/to/skill/ --no-llm
```

Scan a remote GitHub skill repository:
```bash
skillspector scan https://github.com/user/target-skill --no-llm
```

### 2. Semantic Scan with Anthropic (Claude)
Use Anthropic's Claude to analyze contextual intent, disambiguate false positives, and verify descriptions against behavior:
```bash
export SKILLSPECTOR_PROVIDER=anthropic
export ANTHROPIC_API_KEY="your-anthropic-key"
# Optional model override:
# export SKILLSPECTOR_MODEL="claude-3-5-sonnet-20241022"

skillspector scan ./path/to/skill/
```

Alternatively, if authenticated via the Claude CLI on the local machine:
```bash
export SKILLSPECTOR_PROVIDER=claude_cli
skillspector scan ./path/to/skill/
```

### 3. Report Formats & Output
Save report as Markdown, JSON, or SARIF for CI/CD:
```bash
# Markdown report
skillspector scan ./my-skill/ --format markdown --output scan-report.md

# JSON report for automated pipelines
skillspector scan ./my-skill/ --format json --output scan-report.json

# Fail CI/CD gate on findings
skillspector scan ./my-skill/ --fail-on-findings
```

### 4. Recursive Scans
Scan an entire directory of multiple skills:
```bash
skillspector scan ./all-skills/ --recursive
```

### 5. Run as MCP Server
SkillSpector can also run as an MCP server to allow real-time skill scanning inside agent sessions:
```bash
skillspector mcp
```
