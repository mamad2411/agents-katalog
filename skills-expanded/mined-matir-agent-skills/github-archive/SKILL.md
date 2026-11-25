---
name: github-archive
description: Investigates GitHub security incidents using tamper-proof GH Archive data via BigQuery. Provides immutable forensic evidence for verifying activity and recovering deleted content.
metadata:
  version: 0.2.0
  category: forensics
---
# Github Archive

## Quick Start
```bash
github-archive download --org google --repo osv-scanner
```

## Workflow
1. Identify target GitHub organization or repository.
2. Fetch archive metadata and download release/source artifacts.
3. Verify integrity and perform analysis.

## Rules & Constraints
- Use authenticated requests to avoid low rate limits.
- Respect repository licenses and terms of service.

## When to Use
- Recovering deleted or modified evidence from GitHub.
- Large-scale source code auditing.

## When NOT to Use
- Real-time repository monitoring (use webhooks instead).
- Interactions that require git history (use git clone instead).

## References
- [Skill Manual](references/github-archive-manual.md)
