---
name: analyzing-checkov
description: |
  Use when working with Checkov — checkov infrastructure-as-code security
  scanning. Covers Terraform, CloudFormation, Kubernetes, and Dockerfile
  scanning, policy management, custom checks, compliance frameworks, and
  suppression management. Use when scanning IaC for security misconfigurations,
  evaluating compliance, managing custom policies, or reviewing scan results.
connection_type: checkov
preload: false
---

# Checkov IaC Security Analysis Skill

Analyze infrastructure-as-code security using Checkov across Terraform, CloudFormation, Kubernetes, and more.

## MANDATORY: Discovery-First Pattern

**Always check Checkov version and available frameworks before running scans.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Checkov Version ==="
checkov --version 2>/dev/null

echo ""
echo "=== Supported Frameworks ==="
echo "terraform, cloudformation, kubernetes, dockerfile, helm,"
echo "arm, bicep, serverless, github_actions, gitlab_ci, bitbucket_pipelines"

echo ""
echo "=== Available Check Count ==="
checkov --list --output json 2>/dev/null | jq 'length' | xargs -I{} echo "{} checks available"

echo ""
echo "=== IaC Files Detected ==="
find . -maxdepth 3 \( -name "*.tf" -o -name "*.yaml" -o -name "*.yml" -o -name "Dockerfile" -o -name "*.json" \) -not -path "*/.terraform/*" -not -path "*/node_modules/*" 2>/dev/null | head -20
```

## Core Helper Functions

```bash
#!/bin/bash

# Checkov wrapper with JSON output
checkov_cmd() {
    checkov "$@" --output json --compact --quiet 2>/dev/null
}

# Run specific framework
checkov_framework() {
    local framework="$1"
    local directory="${2:-.}"
    checkov --framework "$framework" --directory "$directory" --output json --compact --quiet 2>/dev/null
}

# Summary extractor
checkov_summary() {
    jq '{
        passed: .summary.passed,
        failed: .summary.failed,
        skipped: .summary.skipped,
        parsing_errors: .summary.parsing_errors
    }'
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `--output json --compact` for structured results
- Use `--check` or `--skip-check` to focus scans
- Group findings by severity and category

## Common Operations

### Full Directory Scan

```bash
#!/bin/bash
TARGET="${1:-.}"

echo "=== Checkov Full Scan ==="
checkov --directory "$TARGET" --output json --compact --quiet 2>/dev/null | jq '{
    summary: .summary,
    failed_checks: [.results.failed_checks[:10][] | {
        check_id: .check_id,
        check_name: .name,
        resource: .resource,
        file: .file_path,
        guideline: .guideline
    }],
    framework: .check_type
}'
```

### Terraform-Specific Scan

```bash
#!/bin/bash
TARGET="${1:-.}"

echo "=== Terraform Security Scan ==="
checkov --framework terraform --directory "$TARGET" --output json --compact --quiet 2>/dev/null | jq '{
    summary: .summary,
    top_failures: [.results.failed_checks[] | {
        id: .check_id,
        name: .name,
        resource: .resource,
        file: .file_path,
        severity: .severity
    }] | group_by(.id) | map({
        check: .[0].id,
        name: .[0].name,
        severity: .[0].severity,
        occurrences: length
    }) | sort_by(-.occurrences) | .[0:10]
}'
```

### Compliance Framework Scan

```bash
#!/bin/bash
FRAMEWORK="${1:-CIS}"
TARGET="${2:-.}"

echo "=== Compliance Scan: $FRAMEWORK ==="
echo "Available frameworks: CIS, SOC2, HIPAA, PCI-DSS, NIST-800-53, ISO27001"
echo ""

checkov --directory "$TARGET" --output json --compact --quiet 2>/dev/null | jq --arg fw "$FRAMEWORK" '{
    framework: $fw,
    summary: .summary,
    compliance_failures: [.results.failed_checks[] |
        select(.check_id | test("CK_")) |
        {id: .check_id, name: .name, resource: .resource, file: .file_path}
    ] | .[0:15]
}'
```

### Custom Check Management

```bash
#!/bin/bash
echo "=== External Checks ==="
CUSTOM_DIR="${1:-}"
if [ -n "$CUSTOM_DIR" ]; then
    echo "Running with custom checks from: $CUSTOM_DIR"
    checkov --directory . --external-checks-dir "$CUSTOM_DIR" --output json --compact --quiet 2>/dev/null | jq '.summary'
fi

echo ""
echo "=== Inline Suppressions ==="
grep -rn 'checkov:skip=' . --include="*.tf" --include="*.yaml" 2>/dev/null | head -15

echo ""
echo "=== Skip Configuration ==="
cat .checkov.yaml 2>/dev/null || cat .checkov.yml 2>/dev/null || echo "No .checkov.yaml found"
```

### Scan Results Comparison

```bash
#!/bin/bash
TARGET="${1:-.}"

echo "=== Scan by Framework ==="
for fw in terraform cloudformation kubernetes dockerfile; do
    RESULT=$(checkov --framework "$fw" --directory "$TARGET" --output json --compact --quiet 2>/dev/null | jq '.summary // empty')
    if [ -n "$RESULT" ]; then
        echo "--- $fw ---"
        echo "$RESULT" | jq '{passed: .passed, failed: .failed}'
    fi
done

echo ""
echo "=== Severity Distribution ==="
checkov --directory "$TARGET" --output json --compact --quiet 2>/dev/null | jq '
    [.results.failed_checks[] | .severity // "UNKNOWN"] |
    group_by(.) | map({severity: .[0], count: length}) | sort_by(-.count)
'
```

## Safety Rules

- **Scans are read-only** -- Checkov never modifies scanned files
- **Use `--skip-check`** for known false positives rather than removing checks entirely
- **Custom checks should be version-controlled** and reviewed before deployment
- **CI/CD integration** should use `--soft-fail` initially to avoid blocking pipelines
- **Suppressions should have justification** comments explaining why checks are skipped

## Output Format

Present results as a structured report:
```
Analyzing Checkov Report
════════════════════════
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

- **Python version**: Checkov requires Python 3.7+ -- version conflicts cause import errors
- **Large repositories**: Scanning large repos can be slow -- use `--framework` to target specific IaC types
- **Variable resolution**: Checkov may not resolve all Terraform variables -- some checks produce false positives
- **Module scanning**: Remote modules are not downloaded by default -- use `--download-external-modules true`
- **YAML parsing**: Mixed YAML formats (K8s, CloudFormation, Ansible) can cause parser confusion
- **Check ID changes**: Checkov check IDs can change between versions -- pin version in CI
- **Baseline drift**: Running without `--baseline` causes re-reporting of known issues
- **Graph-based checks**: Some checks require the full resource graph -- scanning individual files may miss context
