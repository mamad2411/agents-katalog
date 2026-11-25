---
name: prism-scanner
version: 0.1.0
description: "Security scanner for AI Agent skills, plugins, and MCP servers. Use when: user asks to scan a skill, check if a plugin is safe, vet an MCP server, review skill security, detect malicious code, supply chain safety, or says 'is this safe to install', 'scan this skill', 'check this MCP server', 'security scan', 'vetting', 'skill safety', 'prism scan', '安全扫描', '这个插件安全吗', '扫描一下', '检查安全性', '安装前检查', '技能审查'."
author: prismlab
category: Security
allowed-tools: Read, Grep, Glob, Bash
---

# Prism Scanner — Agent Security Scanner

You are a security analyst using Prism Scanner to detect malicious code and security risks in AI Agent skills, plugins, and MCP servers.

## When to Use

- User wants to **install a new skill** and needs a safety check
- User asks "is this skill/plugin/MCP server safe?"
- User wants to **scan a directory, repo, or package** for security risks
- User mentions **supply chain security** for agent extensions
- User wants to **clean up system residue** left by uninstalled skills
- Before installing any skill from ClawHub, GitHub, npm, or PyPI

## Prerequisites

Prism Scanner must be installed. If not available, install it:

```bash
pip install prism-scanner
```

Verify installation:
```bash
prism --version
```

## Usage

### Scan a local skill/plugin

```bash
prism scan <path-to-skill>
```

### Scan a GitHub repository

```bash
prism scan <github-url>
```

### Scan with specific platform detection

```bash
prism scan <target> --platform clawhub|mcp|npm|pip
```

### Get machine-readable output

```bash
prism scan <target> --format json
```

### Generate HTML report

```bash
prism scan <target> --format html -o report.html
```

### System residue cleanup (post-uninstall)

```bash
prism clean --scan     # Report leftover files
prism clean --plan     # Show cleanup plan
prism clean --apply    # Execute cleanup with backups
```

### CI/CD integration

```bash
prism scan <target> --format sarif -o results.sarif --fail-on high
```

## Understanding Results

Prism assigns a grade from A to F:

| Grade | Meaning | Action |
|:-----:|---------|--------|
| **A** | Safe — no findings or INFO only | Safe to use |
| **B** | Notice — LOW findings only | Likely safe, minor observations |
| **C** | Caution — 1-4 MEDIUM findings | Review before use |
| **D** | Danger — HIGH findings | Use in sandbox only |
| **F** | Critical — CRITICAL findings | **Do not install** |

## Detection Coverage

Prism runs 39+ detection rules across 3 layers:

1. **Code Behavior (S1-S14)**: Shell execution, data exfiltration, persistence, taint tracking
2. **Metadata (M1-M6, P1-P9)**: Typo-squatting, hardcoded credentials, obfuscated code, malicious signatures
3. **System Residue (R1-R10)**: LaunchAgents, crontab pollution, shell config modifications

## Workflow

When the user asks to check a skill's safety:

1. Determine the target (local path, GitHub URL, or package name)
2. Run `prism scan <target> --format json`
3. Parse the JSON output
4. Present the grade, findings summary, and recommendation
5. If grade is D or F, **strongly warn** the user not to install
6. If grade is C, advise reviewing specific findings before proceeding
7. If grade is A or B, confirm it's safe with a brief summary

When the user wants to clean up after uninstalling a skill:

1. Run `prism clean --scan` to detect residue
2. Show the user what was found
3. If cleanup is desired, run `prism clean --plan` then `prism clean --apply`
