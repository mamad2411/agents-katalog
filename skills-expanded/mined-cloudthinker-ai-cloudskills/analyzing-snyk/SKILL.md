---
name: analyzing-snyk
description: |
  Use when working with Snyk — snyk security scanning and vulnerability
  analysis. Covers dependency vulnerability scanning, container image scanning,
  IaC security scanning, code analysis, license compliance, and fix
  recommendations. Use when scanning for vulnerabilities, analyzing dependency
  risks, reviewing container security, or auditing IaC configurations.
connection_type: snyk
preload: false
---

# Snyk Security Analysis Skill

Analyze and manage vulnerabilities using Snyk across dependencies, containers, IaC, and code.

## MANDATORY: Discovery-First Pattern

**Always check authentication and project list before running scans.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Snyk Version ==="
snyk --version 2>/dev/null

echo ""
echo "=== Authentication Status ==="
snyk auth --check 2>/dev/null || snyk whoami 2>/dev/null

echo ""
echo "=== Monitored Projects ==="
snyk monitor --dry-run 2>/dev/null || echo "Run 'snyk monitor' to add project"

echo ""
echo "=== Snyk Organizations ==="
snyk config get org 2>/dev/null || echo "Using default org"
```

## Core Helper Functions

```bash
#!/bin/bash

# Snyk CLI wrapper with JSON output
snyk_cmd() {
    snyk "$@" --json 2>/dev/null
}

# Snyk API call
snyk_api() {
    local endpoint="$1"
    curl -s -H "Authorization: token $SNYK_TOKEN" \
        "https://api.snyk.io/rest/${endpoint}"
}

# Parse vulnerability severity
snyk_severity_summary() {
    jq '{
        critical: [.vulnerabilities[]? | select(.severity == "critical")] | length,
        high: [.vulnerabilities[]? | select(.severity == "high")] | length,
        medium: [.vulnerabilities[]? | select(.severity == "medium")] | length,
        low: [.vulnerabilities[]? | select(.severity == "low")] | length
    }'
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `--json` output with jq for structured results
- Summarize by severity instead of listing all vulnerabilities
- Use `--severity-threshold` to focus on critical/high issues

## Common Operations

### Dependency Vulnerability Scan

```bash
#!/bin/bash
PROJECT_DIR="${1:-.}"

echo "=== Open Source Vulnerability Scan ==="
snyk test --json "$PROJECT_DIR" 2>/dev/null | jq '{
    project: .projectName,
    package_manager: .packageManager,
    vulnerability_summary: {
        total: (.vulnerabilities | length),
        critical: [.vulnerabilities[] | select(.severity == "critical")] | length,
        high: [.vulnerabilities[] | select(.severity == "high")] | length,
        medium: [.vulnerabilities[] | select(.severity == "medium")] | length,
        fixable: [.vulnerabilities[] | select(.isUpgradable or .isPatchable)] | length
    },
    top_vulnerabilities: [.vulnerabilities | sort_by(-.cvssScore)[:5][] | {
        id: .id,
        title: .title,
        severity: .severity,
        cvss: .cvssScore,
        package: .packageName,
        version: .version,
        fixedIn: .fixedIn
    }]
}'
```

### Container Image Scan

```bash
#!/bin/bash
IMAGE="${1:?Container image required}"

echo "=== Container Scan: $IMAGE ==="
snyk container test "$IMAGE" --json 2>/dev/null | jq '{
    image: .docker.image,
    base_image: .docker.baseImage,
    platform: .platform,
    vulnerability_summary: {
        total: (.vulnerabilities | length),
        critical: [.vulnerabilities[] | select(.severity == "critical")] | length,
        high: [.vulnerabilities[] | select(.severity == "high")] | length
    },
    base_image_remediation: .docker.baseImageRemediation,
    top_issues: [.vulnerabilities | sort_by(-.cvssScore)[:5][] | {
        id: .id,
        title: .title,
        severity: .severity,
        package: .packageName,
        nearestFixedIn: .nearestFixedInVersion
    }]
}'
```

### IaC Security Scan

```bash
#!/bin/bash
TARGET="${1:-.}"

echo "=== IaC Security Scan ==="
snyk iac test "$TARGET" --json 2>/dev/null | jq '{
    target_file: .targetFile,
    project_type: .projectType,
    issue_summary: {
        total: (.infrastructureAsCodeIssues | length),
        critical: [.infrastructureAsCodeIssues[] | select(.severity == "critical")] | length,
        high: [.infrastructureAsCodeIssues[] | select(.severity == "high")] | length,
        medium: [.infrastructureAsCodeIssues[] | select(.severity == "medium")] | length
    },
    top_issues: [.infrastructureAsCodeIssues | sort_by(-.severity)[:10][] | {
        id: .id,
        title: .title,
        severity: .severity,
        path: .path,
        resolve: .resolve
    }]
}'
```

### License Compliance

```bash
#!/bin/bash
echo "=== License Analysis ==="
snyk test --json 2>/dev/null | jq '{
    licenses: [.vulnerabilities[] | select(.type == "license") | {
        package: .packageName,
        license: .license,
        severity: .severity
    }] | unique_by(.package) | .[0:15]
}'

echo ""
echo "=== License Policy ==="
snyk_api "orgs/$(snyk config get org 2>/dev/null)/settings/license-policy" 2>/dev/null | jq '.' | head -20
```

### Fix Recommendations

```bash
#!/bin/bash
echo "=== Fixable Vulnerabilities ==="
snyk test --json 2>/dev/null | jq '{
    upgradable: [.vulnerabilities[] | select(.isUpgradable) | {
        package: .packageName,
        current: .version,
        upgrade_to: .upgradePath[-1],
        fixes: .id
    }] | unique_by(.package) | .[0:10],
    patchable: [.vulnerabilities[] | select(.isPatchable) | {
        package: .packageName,
        patch: .patches[0].id
    }] | unique_by(.package) | .[0:5]
}'

echo ""
echo "=== Auto-Fix Preview ==="
echo "Run: snyk wizard  # Interactive fix wizard"
echo "Run: snyk fix     # Auto-apply fixes (Snyk CLI v2)"
```

## Safety Rules

- **Scans are read-only** -- they do not modify code or dependencies
- **`snyk monitor` uploads dependency graph to Snyk cloud** -- ensure compliance with data policies
- **Container scans pull images** -- ensure registry credentials are configured
- **IaC scans may contain sensitive paths** -- review output before sharing
- **Fix commands modify package files** -- review changes before committing

## Output Format

Present results as a structured report:
```
Analyzing Snyk Report
═════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Authentication errors**: Token may be expired or scoped to wrong org -- check with `snyk auth`
- **Missing lockfiles**: Snyk needs lockfiles (package-lock.json, Gemfile.lock) for accurate dependency trees
- **Private registries**: Container scans need registry auth -- configure Docker credentials first
- **Monorepo scanning**: Use `--all-projects` for monorepos or scan each project directory individually
- **False positives**: Some vulnerabilities may not be reachable in your code -- use `--reachable-vulns` for better accuracy
- **Rate limiting**: Heavy API usage can trigger rate limits -- batch operations appropriately
- **Severity thresholds**: CI pipelines should use `--severity-threshold=high` to avoid failing on low-severity issues
- **Snyk Code vs Test**: `snyk code test` scans source code (SAST); `snyk test` scans dependencies (SCA)
