---
name: analyzing-tfsec
description: |
  Use when working with Tfsec — tfsec Terraform security scanning. Covers static
  analysis of Terraform code, custom rule creation, CI integration, severity
  filtering, module scanning, and remediation guidance. Use when scanning
  Terraform configurations for security issues, creating custom security rules,
  or integrating security checks into CI pipelines.
connection_type: tfsec
preload: false
---

# tfsec Terraform Security Scanning Skill

Analyze Terraform configurations for security misconfigurations using tfsec.

## MANDATORY: Discovery-First Pattern

**Always check tfsec version and scan scope before running analysis.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== tfsec Version ==="
tfsec --version 2>/dev/null

echo ""
echo "=== Terraform Files Found ==="
find . -name "*.tf" -not -path "*/.terraform/*" 2>/dev/null | wc -l | xargs -I{} echo "{} Terraform files"

echo ""
echo "=== Module References ==="
grep -rh 'source\s*=' *.tf modules/ 2>/dev/null | sort -u | head -10

echo ""
echo "=== Custom Rules ==="
ls .tfsec/ 2>/dev/null || echo "No custom rules directory found"
cat .tfsec.yml 2>/dev/null || echo "No tfsec config found"
```

## Core Helper Functions

```bash
#!/bin/bash

# tfsec wrapper with JSON output
tfsec_cmd() {
    tfsec "$@" --format json --no-color 2>/dev/null
}

# Scan with severity filter
tfsec_critical() {
    tfsec "$@" --minimum-severity HIGH --format json --no-color 2>/dev/null
}

# Summary extractor
tfsec_summary() {
    jq '{
        total: (.results | length),
        critical: [.results[] | select(.severity == "CRITICAL")] | length,
        high: [.results[] | select(.severity == "HIGH")] | length,
        medium: [.results[] | select(.severity == "MEDIUM")] | length,
        low: [.results[] | select(.severity == "LOW")] | length
    }'
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `--format json` with jq for structured results
- Use `--minimum-severity` to focus on critical findings
- Group results by rule ID for deduplication

## Common Operations

### Full Security Scan

```bash
#!/bin/bash
TARGET="${1:-.}"

echo "=== tfsec Security Scan ==="
tfsec "$TARGET" --format json --no-color 2>/dev/null | jq '{
    summary: {
        total: (.results | length),
        critical: [.results[] | select(.severity == "CRITICAL")] | length,
        high: [.results[] | select(.severity == "HIGH")] | length,
        medium: [.results[] | select(.severity == "MEDIUM")] | length,
        low: [.results[] | select(.severity == "LOW")] | length
    },
    top_findings: [.results | sort_by(.severity) | .[:10][] | {
        rule_id: .rule_id,
        severity: .severity,
        description: .rule_description,
        resource: .resource,
        location: "\(.location.filename):\(.location.start_line)",
        resolution: .resolution
    }]
}'
```

### Scan by Severity

```bash
#!/bin/bash
TARGET="${1:-.}"
SEVERITY="${2:-HIGH}"

echo "=== Findings >= $SEVERITY ==="
tfsec "$TARGET" --minimum-severity "$SEVERITY" --format json --no-color 2>/dev/null | jq '{
    count: (.results | length),
    by_rule: [.results | group_by(.rule_id) | .[] | {
        rule: .[0].rule_id,
        severity: .[0].severity,
        description: .[0].rule_description,
        occurrences: length,
        files: [.[].location.filename] | unique
    }] | sort_by(-.occurrences)
}'
```

### Module Security Scan

```bash
#!/bin/bash
echo "=== Module Scan ==="
tfsec . --include-ignored --include-passed --format json --no-color 2>/dev/null | jq '{
    passed: [.results[] | select(.status == 0)] | length,
    failed: [.results[] | select(.status != 0)] | length,
    module_findings: [.results[] | select(.resource | contains("module."))] | {
        count: length,
        modules: [.[].resource | split(".")[1]] | unique
    }
}'

echo ""
echo "=== Ignored Findings ==="
grep -rn 'tfsec:ignore' . --include="*.tf" 2>/dev/null | head -15
```

### Custom Rule Management

```bash
#!/bin/bash
echo "=== Custom Rules ==="
if [ -d ".tfsec" ]; then
    for rule_file in .tfsec/*.json .tfsec/*.yaml .tfsec/*.yml; do
        [ -f "$rule_file" ] && echo "--- $rule_file ---"
        cat "$rule_file" 2>/dev/null | head -15
    done
else
    echo "No .tfsec directory found"
    echo ""
    echo "To create custom rules, add YAML/JSON files to .tfsec/"
    echo "Example structure:"
    echo "  .tfsec/custom_check.yaml"
fi

echo ""
echo "=== tfsec Configuration ==="
cat .tfsec.yml 2>/dev/null || cat tfsec.yml 2>/dev/null || echo "No config file"
```

### CI Integration Report

```bash
#!/bin/bash
TARGET="${1:-.}"

echo "=== CI Report ==="
tfsec "$TARGET" --format json --no-color 2>/dev/null | jq '{
    pass: ((.results | length) == 0),
    findings: (.results | length),
    critical_high: ([.results[] | select(.severity == "CRITICAL" or .severity == "HIGH")] | length),
    files_affected: ([.results[].location.filename] | unique | length),
    rules_triggered: ([.results[].rule_id] | unique | length),
    remediation: [.results | group_by(.rule_id) | .[:5][] | {
        rule: .[0].rule_id,
        count: length,
        fix: .[0].resolution
    }]
}'

echo ""
echo "=== Exit Code Behavior ==="
echo "tfsec exits 1 on findings -- use --soft-fail for non-blocking CI"
```

## Safety Rules

- **Scans are read-only** -- tfsec never modifies Terraform files
- **Use `--exclude` for known false positives** rather than ignoring all findings
- **Inline ignores (`tfsec:ignore`) should include justification** comments
- **CI pipelines** should start with `--soft-fail` and tighten over time
- **Custom rules** should be reviewed and tested before adding to CI

## Output Format

Present results as a structured report:
```
Analyzing Tfsec Report
══════════════════════
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

- **tfsec is now part of Trivy**: tfsec is maintained but Aqua recommends migrating to `trivy config`
- **Variable resolution**: tfsec may not resolve all variable types -- complex expressions may cause false positives
- **Module sources**: Remote modules are not scanned by default -- clone locally first
- **Terraform version**: tfsec supports HCL2 only -- Terraform 0.11 syntax is not supported
- **Override files**: `_override.tf` files may not be processed correctly in all cases
- **Plan scanning**: tfsec scans HCL, not plan output -- some runtime values are unknown at scan time
- **Workspace variables**: Different workspace variable values may change security posture -- scan each configuration
- **Rule deprecation**: Some rule IDs change between versions -- update CI configurations after upgrades
