---
name: gitleaks
description: >
  Operate and configure Gitleaks — a SAST/secret-detection tool that scans git repositories,
  commit histories, and staged changes for leaked credentials, API keys, tokens, and private keys.
  Use when working with gitleaks/gitleaks, when the user needs to audit a repository for secrets,
  set up pre-commit hooks, integrate into CI/CD pipelines, write custom detection rules, or
  establish baselines to suppress known findings. Covers installation, detect/protect modes,
  .gitleaks.toml configuration, custom rules, allowlists, output formats, and CI/CD integration.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/gitleaks/gitleaks
  language: Go
---

# gitleaks Agent Skill

## When to Use This Skill

Use this skill when:
- Auditing a git repository for leaked secrets, tokens, or credentials
- Setting up a pre-commit hook to prevent secrets from being committed
- Integrating secret scanning into GitHub Actions, GitLab CI, or other pipelines
- Writing custom detection rules for organization-specific secret formats
- The user asks about gitleaks, secret scanning, or credential leakage in git
- Reducing false positives via allowlists or baseline files
- Scanning a specific commit range, branch, or PR diff

## What Gitleaks Does

Gitleaks scans git repository history (all commits, branches, tags) or staged/unstaged changes
for patterns matching known secret formats — AWS keys, GitHub tokens, private keys, generic
high-entropy strings, and hundreds of other types. It uses a TOML-based rule engine where each
rule is a named regex with optional entropy, keyword, and allowlist conditions. Results are
reported to stdout and optionally written to JSON, CSV, or SARIF files for integration with
SIEM, DAST pipelines, or code-review tooling.

## Installation

### Homebrew (macOS/Linux)
```bash
brew install gitleaks
```

### Go install
```bash
go install github.com/gitleaks/gitleaks/v8@latest
```

### Binary release
```bash
VERSION=8.21.2
curl -sSL https://github.com/gitleaks/gitleaks/releases/download/v${VERSION}/gitleaks_${VERSION}_linux_x64.tar.gz \
  | tar -xz gitleaks && chmod +x gitleaks && sudo mv gitleaks /usr/local/bin/
```

### Docker
```bash
docker pull zricethezav/gitleaks:latest
docker run --rm -v $(pwd):/repo zricethezav/gitleaks:latest detect --source /repo
```

### Kali / Debian
```bash
# Not in default repos — use Go install or binary release above
```

## Core Concepts

### Two Primary Commands
- **`detect`**: scan a git repository (local or remote) for secrets in history and working tree
- **`protect`**: scan staged changes before commit (pre-commit hook mode)

### Rule Engine
Each rule in `.gitleaks.toml` defines:
- `id` — unique rule identifier
- `description` — human-readable name
- `regex` — the detection pattern (applied to file content or git diff)
- `entropy` (optional) — minimum Shannon entropy threshold (0.0–8.0) to reduce false positives
- `keywords` — fast pre-filter strings (checked before regex for performance)
- `allowlist` — per-rule exceptions (regex on commit, path, or secret value)

### Default Rules
Gitleaks ships with ~160 built-in rules covering:
AWS access keys, secret keys, session tokens · GitHub/GitLab/Bitbucket tokens ·
Stripe, Twilio, SendGrid, Slack keys · JWT tokens · Private keys (RSA, EC, PGP) ·
Google API keys · Azure credentials · Generic high-entropy strings

## CLI Reference

### detect — scan a local repo
```bash
# Scan entire git history of current directory
gitleaks detect --source .

# Scan a specific directory
gitleaks detect --source /path/to/repo

# Scan only the last 30 commits
gitleaks detect --source . --log-opts="--since='30 days ago'"

# Scan a specific commit range
gitleaks detect --source . --log-opts="abc123..HEAD"

# Scan a specific branch
gitleaks detect --source . --log-opts="main..feature-branch"

# Include unstaged/untracked files (working tree scan)
gitleaks detect --source . --no-git

# Scan without git history (plain directory/file tree)
gitleaks detect --no-git --source /path/to/dir

# Verbose output
gitleaks detect --source . --verbose

# Exit code: 0 = no leaks, 1 = leaks found, 126 = error
```

### detect — output formats
```bash
# JSON report
gitleaks detect --source . --report-format json --report-path leaks.json

# CSV report
gitleaks detect --source . --report-format csv --report-path leaks.csv

# SARIF (for GitHub Code Scanning / security dashboards)
gitleaks detect --source . --report-format sarif --report-path leaks.sarif

# Pretty print to stdout only (default)
gitleaks detect --source .
```

### detect — remote repos
```bash
# Scan a GitHub repo directly (clones to temp dir)
gitleaks detect --source https://github.com/org/repo --verbose

# With GitHub token (avoids rate limits, access private repos)
GITHUB_TOKEN=ghp_xxx gitleaks detect --source https://github.com/org/repo
```

### protect — pre-commit mode
```bash
# Scan staged changes (run before git commit)
gitleaks protect --staged

# Scan unstaged changes
gitleaks protect

# Verbose
gitleaks protect --staged --verbose

# Exit code: 0 = clean, 1 = secrets found (blocks commit when used as hook)
```

### baseline — suppress known findings
```bash
# Generate a baseline from current findings (existing known secrets)
gitleaks detect --source . --report-format json --report-path baseline.json

# Future scans: only report NEW findings not in baseline
gitleaks detect --source . --baseline-path baseline.json
```

### Config file selection
```bash
# Use a specific config file
gitleaks detect --source . --config /path/to/.gitleaks.toml

# Gitleaks searches for config in this order:
# 1. --config flag
# 2. GITLEAKS_CONFIG env var
# 3. .gitleaks.toml in repo root
# 4. ~/.config/gitleaks/config.toml
# 5. Built-in default rules
```

## .gitleaks.toml Configuration

### Full structure
```toml
title = "My Gitleaks Config"

[extend]
# Inherit built-in rules and add your own
useDefault = true

[allowlist]
description = "Global allowlist"
commits = ["abc123deadbeef"]   # Ignore specific commits
paths   = ['''(?i)test''']     # Ignore paths matching regex
regexes = ['''EXAMPLE_KEY''']  # Ignore secrets matching regex

[[rules]]
id          = "my-internal-api-key"
description = "Internal API Key"
regex       = '''MYCO-[A-Z0-9]{32}'''
entropy     = 3.5
keywords    = ["MYCO-"]

  [rules.allowlist]
  description = "Allow test fixtures"
  paths       = ['''(?i)(test|fixture|mock|fake)''']
  regexes     = ['''MYCO-TESTKEY00000000000000000000''']

[[rules]]
id          = "slack-webhook"
description = "Slack Incoming Webhook"
regex       = '''https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+'''
keywords    = ["hooks.slack.com"]
```

### Extend-only (add rules without losing defaults)
```toml
title = "Org Config"

[extend]
useDefault = true

[[rules]]
id      = "internal-jwt-secret"
description = "Internal JWT signing key prefix"
regex   = '''jwt_secret\s*=\s*["']?[A-Za-z0-9+/]{40,}'''
entropy = 4.0
keywords = ["jwt_secret"]
```

### Suppress a noisy built-in rule
```toml
[extend]
useDefault = true

# Override a specific rule by re-defining it with a no-match regex
# or add its ID to an allowlist at the rule level
[allowlist]
rules = ["generic-api-key"]   # Disable a built-in rule by ID
```

## Custom Rules: Writing Patterns

### High-entropy generic string
```toml
[[rules]]
id          = "high-entropy-env-var"
description = "High entropy value assigned in env"
regex       = '''(?i)(api_key|secret|token|password)\s*=\s*["']?([A-Za-z0-9+/=!@#$%^&*]{20,})'''
entropy     = 4.5
keywords    = ["api_key", "secret", "token", "password"]
```

### Private key block
```toml
[[rules]]
id          = "pem-private-key"
description = "PEM Private Key"
regex       = '''-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----'''
keywords    = ["BEGIN", "PRIVATE KEY"]
```

### AWS-style pattern (already in defaults, shown for reference)
```toml
[[rules]]
id      = "aws-access-key"
description = "AWS Access Key"
regex   = '''(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}'''
keywords = ["AKIA", "ASIA"]
```

## CI/CD Integration

### GitHub Actions
```yaml
name: Secret Scan
on: [push, pull_request]
jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0          # Full history required

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          # GITLEAKS_LICENSE required for organizations (free for public repos)
          GITLEAKS_ENABLE_COMMENTS: true    # Post PR comments on findings
```

### GitHub Actions (binary, more control)
```yaml
      - name: Install Gitleaks
        run: |
          curl -sSL https://github.com/gitleaks/gitleaks/releases/download/v8.21.2/gitleaks_8.21.2_linux_x64.tar.gz \
            | tar -xz && chmod +x gitleaks && sudo mv gitleaks /usr/local/bin/

      - name: Scan
        run: gitleaks detect --source . --report-format sarif --report-path gitleaks.sarif || true

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: gitleaks.sarif
```

### GitLab CI
```yaml
gitleaks:
  image: zricethezav/gitleaks:latest
  stage: test
  script:
    - gitleaks detect --source . --report-format json --report-path gl-secret-detection-report.json
  artifacts:
    reports:
      secret_detection: gl-secret-detection-report.json
    when: always
```

### Pre-commit Hook (local enforcement)
```bash
# Method 1: gitleaks protect as git hook
cat > .git/hooks/pre-commit <<'EOF'
#!/bin/sh
gitleaks protect --staged --verbose
if [ $? -ne 0 ]; then
  echo "[BLOCKED] Gitleaks found secrets. Fix before committing."
  exit 1
fi
EOF
chmod +x .git/hooks/pre-commit

# Method 2: pre-commit framework
# .pre-commit-config.yaml
# repos:
# - repo: https://github.com/gitleaks/gitleaks
#   rev: v8.21.2
#   hooks:
#   - id: gitleaks
```

## Scanning Specific Commits and Branches

```bash
# Single commit
gitleaks detect --source . --log-opts="-1 abc123"

# All commits since a tag
gitleaks detect --source . --log-opts="v1.0.0..HEAD"

# Feature branch diff vs main
gitleaks detect --source . --log-opts="main..feature/my-branch"

# Last N commits
gitleaks detect --source . --log-opts="-50"

# All commits by a specific author
gitleaks detect --source . --log-opts='--author="dev@example.com"'

# Scan a specific file across all history
gitleaks detect --source . --log-opts="-- config/secrets.yml"
```

## Secret Types Detected (Built-in)

| Category | Examples |
|---|---|
| AWS | Access Key IDs (AKIA…), Secret Access Keys, Session Tokens |
| GitHub | PATs (ghp_…), OAuth tokens (gho_…), App tokens (ghs_…) |
| GitLab | Project/Group tokens (glpat-…) |
| Azure | Storage keys, SAS tokens, AD client secrets |
| GCP | Service account keys (JSON), API keys (AIza…) |
| Stripe | Publishable (pk_live_…) and secret (sk_live_…) keys |
| Twilio | Auth tokens, API keys |
| Slack | Bot tokens (xoxb-…), Webhook URLs |
| JWT | JSON Web Tokens (eyJ…) |
| Private Keys | RSA, EC, DSA, OPENSSH PEM blocks |
| Generic | High-entropy strings in variable assignments |
| Database | Connection strings with embedded passwords |
| SendGrid | API keys (SG.…) |

## Advanced Techniques

### Audit an entire GitHub organization
```bash
# Use gh CLI to list repos, then scan each
gh repo list MY_ORG --limit 200 --json nameWithOwner -q '.[].nameWithOwner' | \
  while read repo; do
    echo "=== Scanning $repo ==="
    gitleaks detect \
      --source "https://github.com/$repo" \
      --report-format json \
      --report-path "reports/${repo//\//_}.json" 2>/dev/null
  done
```

### Merge all JSON reports
```bash
jq -s '[.[] | .[]]' reports/*.json > all-findings.json
jq 'group_by(.RuleID) | map({rule: .[0].RuleID, count: length})' all-findings.json
```

### Find secrets in Docker image layers
```bash
# Save image layers as tar, mount and scan
docker save myimage:latest -o image.tar
mkdir image-fs && tar -xf image.tar -C image-fs
gitleaks detect --no-git --source image-fs/
```

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| No config file found warning | No .gitleaks.toml in repo | Create one or pass --config |
| Too many false positives | Overly broad rules | Add allowlist regexes or raise entropy threshold |
| `fatal: bad object` log-opts error | Invalid commit ref | Verify the commit hash exists |
| Slow scan on large repos | Massive history | Limit with --log-opts="-500" for initial run |
| Docker permission denied | Volume mount | Use `--user $(id -u):$(id -g)` with Docker |
| pre-commit hook not triggering | Hook not executable | `chmod +x .git/hooks/pre-commit` |
| Baseline not suppressing findings | Baseline generated from different scan | Regenerate baseline with same config |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
