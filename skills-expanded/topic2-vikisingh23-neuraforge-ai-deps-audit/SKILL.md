---
name: deps-audit
description: Scan dependencies for outdated packages, vulnerabilities, unused deps, and license issues
category: developer-tools
triggers:
  - "audit dependencies"
  - "check outdated"
  - "find vulnerabilities"
---

Scan dependencies for issues.

## What it checks
- 🔴 Security vulnerabilities (npm audit)
- 🟡 Outdated packages (major/minor/patch)
- 🟢 Unused dependencies (imported nowhere)
- ⚖️ License compliance (flags GPL, AGPL, unlicensed)

Works with: package.json, pubspec.yaml, *.csproj

For full instructions, read `agents/deps-audit.md`.
