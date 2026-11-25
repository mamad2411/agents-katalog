---
name: secrets-gitleaks
description: Hardcoded secret detection and prevention in git repositories and codebases using Gitleaks.
metadata:
  version: 0.2.0
  category: devsecops
---
# Secrets Detection with Gitleaks

## Quick Start
```bash
# Scan current repository for secrets with verbose output
gitleaks detect -v
```

## Workflow
1. **Target Identification**: Identify repositories or directories containing source code, configuration files, or documentation to scan.
2. **Initial Audit**: Run a full repository scan including git history to establish a security baseline.
3. **Local Prevention**: Install Gitleaks as a pre-commit hook on developer workstations to prevent new secrets from being committed.
4. **CI/CD Integration**: Configure automated scans in build pipelines to enforce security gates and track findings.
5. **Remediation**: Rotate exposed credentials immediately and clean up git history using `git filter-repo` if necessary.

## Rules & Constraints
- **RULE-1**: Always use the `--redact` flag in logs and reports to prevent accidental exposure of detected secrets.
- **RULE-2**: Exposed credentials must be rotated immediately, even if they are removed from the codebase.
- **RULE-3**: Do not rely solely on automated scans; review findings for false positives and adjust `.gitleaks.toml` accordingly.

## When to Use
- Scanning repositories for exposed passwords, API keys, and tokens.
- Auditing codebases for compliance (PCI-DSS, SOC2, GDPR).
- Establishing a baseline for secret detection in legacy codebases.

## When NOT to Use
- Detecting secrets in binary files or encrypted blobs.
- Real-time monitoring of live application memory for secrets.

## References
- [Skill Manual](references/secrets-gitleaks-manual.md)
- [Gitleaks Official Repo](https://github.com/gitleaks/gitleaks)
