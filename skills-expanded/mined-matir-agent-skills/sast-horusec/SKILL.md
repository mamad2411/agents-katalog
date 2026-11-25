---
name: sast-horusec
description: Multi-language Static Application Security Testing (SAST) using the Horusec scanner.
metadata:
  version: 0.2.0
  category: secsdlc
---
# Horusec SAST Scanner

## Quick Start
```bash
# Using Docker (recommended)
docker run -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd):/src horuszup/horusec-cli:latest horusec start -p /src -P $(pwd)

# Local installation
horusec start -p ./path/to/project
```

## Workflow
1. **Execution**: Run Horusec start on the project directory (Docker or local).
2. **Secret Scanning**: Enable `--enable-git-history-analysis` to detect exposed credentials.
3. **Reporting**: Configure output formats (text, json, sonarqube) for analysis.
4. **False Positive Management**: Use `.horusec/config.json` to ignore non-vulnerable findings.
5. **Gating**: Set `--severity-threshold` and `--return-error-if-found-vulnerability` for CI/CD gating.

## Rules & Constraints
- **RULE-1**: Ensure Docker socket access or install all security tool dependencies locally.
- **RULE-2**: Store scan results securely; they may contain sensitive secret findings.
- **RULE-3**: Review and rotate any credentials found in git history analysis.
- **RULE-4**: Exclude test and vendor directories to reduce noise.

## When to Use
- Analyzing code for vulnerabilities across multiple languages simultaneously.
- Detecting exposed secrets and credentials in git history.
- Integrating SAST into CI/CD pipelines.

## When NOT to Use
- Dynamic analysis (DAST) requirements.
- Binary-only analysis (needs source code).
- Production runtime monitoring.

## References
- [Skill Manual](references/sast-horusec-manual.md)
- [Official Documentation](https://docs.horusec.io/)
- [Vulnerability Management](https://github.com/ZupIT/horusec-platform)
