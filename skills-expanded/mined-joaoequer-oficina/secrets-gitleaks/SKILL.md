---
name: secrets-gitleaks
description: >
  Hardcoded secret detection and prevention in git repositories and codebases using Gitleaks.
  Identifies passwords, API keys, tokens, and credentials through regex-based pattern matching
  and entropy analysis. Use when: (1) Scanning repositories for exposed secrets and credentials,
  (2) Implementing pre-commit hooks to prevent secret leakage, (3) Integrating secret detection
  into CI/CD pipelines, (4) Auditing codebases for compliance violations (PCI-DSS, SOC2, GDPR),
  (5) Establishing baseline secret detection and tracking new exposures, (6) Remediating
  historical secret exposures in git history.
version: 0.1.0
maintainer: SirAppSec
category: devsecops
tags: [secrets, gitleaks, secret-scanning, devsecops, ci-cd, credentials, api-keys, compliance]
frameworks: [OWASP, CWE, PCI-DSS, SOC2, GDPR]
dependencies:
  tools: [gitleaks, git]
references:
  - https://github.com/gitleaks/gitleaks
  - https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
  - https://cwe.mitre.org/data/definitions/798.html
---

<!-- Fonte: github.com/majiayu000/claude-skill-registry-data, security/secrets-gitleaks/SKILL.md
     (autor atribuído: SirAppSec; repo agregador sem LICENSE próprio detectado no GitHub — conteúdo é
     documentação de uso de uma ferramenta open-source real, gitleaks/gitleaks, sem claim de autoria
     original sobre o gitleaks em si). Copiado verbatim 2026-09-01 após leitura completa (duas vezes,
     mesmo veredito). Ver skills-radar.md (seção H).

     CAVEAT confirmado na cópia: a seção "Bundled Resources" abaixo lista scripts/references/assets
     que NÃO EXISTEM no repo de origem (só SKILL.md + metadata.json de fato existem) — são aspiracionais,
     não copiados aqui. Os comandos inline (gitleaks CLI, YAML de CI, pre-commit manual) são reais e
     usáveis como estão; não tente rodar `./scripts/install_precommit.sh` — escreva o hook inline
     seguindo o exemplo em "Pre-Commit Hook Protection" abaixo. -->

# Secrets Detection with Gitleaks

## Overview

Gitleaks is a secret detection tool that scans git repositories, files, and directories for hardcoded credentials including passwords, API keys, tokens, and other sensitive information. It uses regex-based pattern matching combined with Shannon entropy analysis to identify secrets that could lead to unauthorized access if exposed.

This skill provides comprehensive guidance for integrating Gitleaks into DevSecOps workflows, from pre-commit hooks to CI/CD pipelines, with emphasis on preventing secret leakage before code reaches production.

## Quick Start

Scan current repository for secrets:

```bash
# Install gitleaks
brew install gitleaks  # macOS
# or: docker pull zricethezav/gitleaks:latest

# Scan current git repository
gitleaks detect -v

# Scan specific directory
gitleaks detect --source /path/to/code -v

# Generate report
gitleaks detect --report-path gitleaks-report.json --report-format json
```

## Core Workflows

### 1. Repository Scanning

Scan existing repositories to identify exposed secrets:

```bash
# Full repository scan with verbose output
gitleaks detect -v --source /path/to/repo

# Scan with custom configuration
gitleaks detect --config .gitleaks.toml -v

# Generate JSON report for further analysis
gitleaks detect --report-path findings.json --report-format json

# Generate SARIF report for GitHub/GitLab integration
gitleaks detect --report-path findings.sarif --report-format sarif
```

**When to use**: Initial security audit, compliance checks, incident response.

### 2. Pre-Commit Hook Protection

Prevent secrets from being committed in the first place:

```bash
# Install pre-commit hook (run in repository root)
cat << 'EOF' > .git/hooks/pre-commit
#!/bin/sh
gitleaks protect --verbose --redact --staged
EOF

chmod +x .git/hooks/pre-commit
```

**When to use**: Developer workstation setup, team onboarding, mandatory security controls.

### 3. CI/CD Pipeline Integration

#### GitHub Actions

```yaml
name: gitleaks
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

#### GitLab CI

```yaml
gitleaks:
  image: zricethezav/gitleaks:latest
  stage: test
  script:
    - gitleaks detect --report-path gitleaks.json --report-format json --verbose
  artifacts:
    paths:
      - gitleaks.json
    when: always
  allow_failure: false
```

**When to use**: Automated security gates, pull request checks, release validation.

### 4. Baseline and Incremental Scanning

Establish security baseline and track only new secrets:

```bash
# Create initial baseline
gitleaks detect --report-path baseline.json --report-format json

# Subsequent scans detect only new secrets
gitleaks detect --baseline-path baseline.json --report-path new-findings.json -v
```

**When to use**: Legacy codebase remediation, phased rollout, compliance tracking.

### 5. Configuration Customization

Create custom `.gitleaks.toml` configuration:

```toml
title = "Custom Gitleaks Configuration"

[extend]
# Extend default config with custom rules
useDefault = true

[[rules]]
id = "custom-api-key"
description = "Custom API Key Pattern"
regex = '''(?i)(custom_api_key|custom_secret)[\s]*[=:][\s]*['"][a-zA-Z0-9]{32,}['"]'''
tags = ["api-key", "custom"]

[allowlist]
description = "Global allowlist"
paths = [
  '''\.md$''',           # Ignore markdown files
  '''test/fixtures/''',  # Ignore test fixtures
]
stopwords = [
  '''EXAMPLE''',         # Ignore example keys
  '''PLACEHOLDER''',
]
```

**When to use**: Reducing false positives, adding proprietary secret patterns, organizational standards.

## Security Considerations

### Sensitive Data Handling

- **Secret Redaction**: Always use `--redact` flag in logs and reports to prevent accidental secret exposure
- **Report Security**: Gitleaks reports contain detected secrets - treat as confidential, encrypt at rest
- **Git History**: Detected secrets in git history require complete removal using tools like `git filter-repo` or `BFG Repo-Cleaner`
- **Credential Rotation**: All exposed secrets must be rotated immediately, even if removed from code

### Access Control

- **CI/CD Permissions**: Gitleaks scans require read access to repository content and git history
- **Report Access**: Restrict access to scan reports containing sensitive findings
- **Baseline Files**: Baseline JSON files contain secret metadata - protect with same controls as findings

### Audit Logging

Log the following for compliance and incident response:
- Scan execution timestamps and scope (repository, branch, commit range)
- Number and types of secrets detected
- Remediation actions taken (credential rotation, commit history cleanup)
- False positive classifications and allowlist updates

### Compliance Requirements

- **PCI-DSS 3.2.1**: Requirement 6.5.3 - Prevent hardcoded credentials in payment applications
- **SOC2**: CC6.1 - Logical access controls prevent unauthorized credential exposure
- **GDPR**: Article 32 - Appropriate security measures for processing personal data credentials
- **CWE-798**: Use of Hard-coded Credentials
- **CWE-259**: Use of Hard-coded Password
- **OWASP A07:2021**: Identification and Authentication Failures

## Common Patterns

### Pattern 1: Initial Repository Audit

First-time secret scanning for security assessment:

```bash
# 1. Clone repository with full history
git clone --mirror https://github.com/org/repo.git audit-repo
cd audit-repo

# 2. Run comprehensive scan
gitleaks detect --report-path audit-report.json --report-format json -v

# 3. Review findings and classify false positives
# Edit .gitleaks.toml to add allowlist entries

# 4. Create baseline for future scans
cp audit-report.json baseline.json
```

### Pattern 2: Developer Workstation Setup

Protect developers from accidental secret commits:

```bash
# 1. Install gitleaks locally
brew install gitleaks  # macOS
# or use package manager for your OS

# 2. Install pre-commit hook (see "Pre-Commit Hook Protection" above)

# 3. Test hook with dummy commit
echo "api_key = 'EXAMPLE_KEY_12345'" > test.txt
git add test.txt
git commit -m "test"  # Should be blocked by gitleaks

# 4. Clean up test
git reset HEAD~1
rm test.txt
```

### Pattern 3: CI/CD Pipeline with Baseline

Progressive secret detection in continuous integration:

```bash
# In CI pipeline script:

# 1. Check if baseline exists
if [ -f ".gitleaks-baseline.json" ]; then
  # Incremental scan - only new secrets
  gitleaks detect \
    --baseline-path .gitleaks-baseline.json \
    --report-path new-findings.json \
    --report-format json \
    --exit-code 1  # Fail on new secrets
else
  # Initial scan - create baseline
  gitleaks detect \
    --report-path .gitleaks-baseline.json \
    --report-format json \
    --exit-code 0  # Don't fail on first scan
fi

# 2. Generate SARIF for GitHub Security tab
if [ -f "new-findings.json" ] && [ -s "new-findings.json" ]; then
  gitleaks detect \
    --baseline-path .gitleaks-baseline.json \
    --report-path results.sarif \
    --report-format sarif
fi
```

### Pattern 4: Custom Rule Development

Add organization-specific secret patterns:

```toml
# Add to .gitleaks.toml

[[rules]]
id = "acme-corp-api-key"
description = "ACME Corp Internal API Key"
regex = '''(?i)acme[_-]?api[_-]?key[\s]*[=:][\s]*['"]?([a-f0-9]{40})['"]?'''
secretGroup = 1
tags = ["api-key", "acme-internal"]

# Test custom rules
# gitleaks detect --config .gitleaks.toml -v
```

## Integration Points

### CI/CD Integration

- **GitHub Actions**: Use `gitleaks/gitleaks-action@v2` for native integration with Security tab
- **GitLab CI**: Docker-based scanning with artifact retention for audit trails
- **Jenkins**: Execute via Docker or installed binary in pipeline stages
- **CircleCI**: Docker executor with orb support
- **Azure Pipelines**: Task-based integration with results publishing

### Security Tools Ecosystem

- **SIEM Integration**: Export JSON findings to Splunk, ELK, or Datadog for centralized monitoring
- **Vulnerability Management**: Import SARIF reports into Snyk, SonarQube, or Checkmarx
- **Secret Management**: Integrate findings with HashiCorp Vault or AWS Secrets Manager rotation workflows
- **Ticketing Systems**: Automated Jira/ServiceNow ticket creation for remediation tracking

## Troubleshooting

### Issue: Too Many False Positives

**Solution**:
1. Review findings to identify patterns: `grep -i "example\|test\|placeholder" gitleaks-report.json`
2. Add to allowlist in `.gitleaks.toml`:
   ```toml
   [allowlist]
   paths = ['''test/''', '''examples/''', '''\.md$''']
   stopwords = ["EXAMPLE", "PLACEHOLDER", "YOUR_API_KEY_HERE"]
   ```
3. Use commit allowlists for specific false positives:
   ```toml
   [allowlist]
   commits = ["commit-sha-here"]
   ```

### Issue: Performance Issues on Large Repositories

**Solution**:
1. Use `--log-opts` to limit git history: `gitleaks detect --log-opts="--since=2024-01-01"`
2. Scan specific branches: `gitleaks detect --log-opts="origin/main"`
3. Use baseline approach to scan only recent changes
4. Consider shallow clone for initial scans: `git clone --depth=1000`

### Issue: Pre-commit Hook Blocking Valid Commits

**Solution**:
1. Add inline comment to bypass hook: `# gitleaks:allow`
2. Update `.gitleaks.toml` allowlist for the specific pattern
3. Use `--redact` to safely review findings: `gitleaks protect --staged --redact`
4. Temporary bypass (use with caution): `git commit --no-verify`
5. Review with security team if pattern is genuinely needed

### Issue: Secrets Found in Git History

**Solution**:
1. Rotate compromised credentials immediately (highest priority)
2. For public repositories, consider full history rewrite using:
   - `git filter-repo` (recommended): `git filter-repo --path-glob '*.env' --invert-paths`
   - BFG Repo-Cleaner: `bfg --delete-files credentials.json`
3. Force-push cleaned history: `git push --force`
4. Notify all contributors to rebase/re-clone
5. Document incident in security audit log

### Issue: Custom Secret Patterns Not Detected

**Solution**:
1. Develop regex pattern: Test at regex101.com with sample secrets
2. Add custom rule to `.gitleaks.toml`
3. Test pattern: `gitleaks detect --config .gitleaks.toml -v --no-git`
4. Consider entropy threshold if pattern is ambiguous:
   ```toml
   [[rules.Entropies]]
   Min = "3.5"
   Max = "7.0"
   Group = "1"
   ```

## Advanced Configuration

### Entropy-Based Detection

For secrets without clear patterns, use Shannon entropy analysis:

```toml
[[rules]]
id = "high-entropy-strings"
description = "High entropy strings that may be secrets"
regex = '''[a-zA-Z0-9]{32,}'''
entropy = 4.5  # Shannon entropy threshold
secretGroup = 0
```

### Composite Rules (v8.28.0+)

Detect secrets spanning multiple lines or requiring context:

```toml
[[rules]]
id = "multi-line-secret"
description = "API key with usage context"
regex = '''api_key[\s]*='''

[[rules.composite]]
pattern = '''initialize_client'''
location = "line"  # Must be within same line proximity
distance = 5       # Within 5 lines
```

### Global vs Rule-Specific Allowlists

```toml
# Global allowlist (highest precedence)
[allowlist]
description = "Organization-wide exceptions"
paths = ['''vendor/''', '''node_modules/''']

# Rule-specific allowlist
[[rules]]
id = "generic-api-key"
[rules.allowlist]
description = "Exceptions only for this rule"
regexes = ['''key\s*=\s*EXAMPLE''']
```

## References

- [Gitleaks Official Documentation](https://github.com/gitleaks/gitleaks)
- [OWASP A07:2021 - Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)
- [CWE-798: Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
- [CWE-259: Use of Hard-coded Password](https://cwe.mitre.org/data/definitions/259.html)
- [CWE-321: Use of Hard-coded Cryptographic Key](https://cwe.mitre.org/data/definitions/321.html)
