---
name: analyzing-prowler
description: |
  Use when working with Prowler — prowler cloud security assessment tool. Covers
  AWS, Azure, and GCP security posture assessment, CIS benchmark evaluation,
  compliance frameworks (PCI-DSS, HIPAA, SOC2), multi-account scanning, and
  remediation guidance. Use when assessing cloud security posture, running
  compliance audits, or investigating security findings across cloud providers.
connection_type: prowler
preload: false
---

# Prowler Cloud Security Assessment Skill

Assess cloud security posture across AWS, Azure, and GCP using Prowler.

## MANDATORY: Discovery-First Pattern

**Always check credentials and available checks before running assessments.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Prowler Version ==="
prowler --version 2>/dev/null

echo ""
echo "=== Available Providers ==="
prowler --list-providers 2>/dev/null || echo "aws, azure, gcp"

echo ""
echo "=== AWS Identity ==="
aws sts get-caller-identity 2>/dev/null | jq '{Account: .Account, Arn: .Arn}'

echo ""
echo "=== Available Check Count ==="
prowler aws --list-checks-json 2>/dev/null | jq 'length' | xargs -I{} echo "{} checks available for AWS"

echo ""
echo "=== Compliance Frameworks ==="
prowler aws --list-compliance 2>/dev/null | head -15
```

## Core Helper Functions

```bash
#!/bin/bash

# Prowler wrapper
prowler_cmd() {
    prowler "$@" --no-banner 2>/dev/null
}

# Parse Prowler JSON output
prowler_parse() {
    local output_file="$1"
    jq -r '.[] | "\(.Status)\t\(.Severity)\t\(.CheckID)\t\(.ResourceId)\t\(.StatusExtended[:60])"' "$output_file"
}

# Summary from output
prowler_summary() {
    local output_file="$1"
    jq '{
        total: length,
        pass: [.[] | select(.Status == "PASS")] | length,
        fail: [.[] | select(.Status == "FAIL")] | length,
        info: [.[] | select(.Status == "INFO")] | length
    }' "$output_file"
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `--output-formats json` for structured results
- Use `--severity` to focus on critical/high findings
- Use `--compliance` to scope to specific frameworks

## Common Operations

### AWS Security Assessment

```bash
#!/bin/bash
SERVICES="${1:-}"
SEVERITY="${2:-critical high}"

echo "=== AWS Security Scan ==="
if [ -n "$SERVICES" ]; then
    prowler aws --services "$SERVICES" --severity "$SEVERITY" --output-formats json --no-banner 2>/dev/null
else
    prowler aws --severity "$SEVERITY" --output-formats json --no-banner 2>/dev/null
fi

echo ""
echo "=== Results Summary ==="
OUTPUT_DIR=$(ls -td output/prowler-output-* 2>/dev/null | head -1)
if [ -n "$OUTPUT_DIR" ]; then
    cat "${OUTPUT_DIR}"/*.json 2>/dev/null | jq -s 'flatten | {
        total: length,
        pass: [.[] | select(.Status == "PASS")] | length,
        fail: [.[] | select(.Status == "FAIL")] | length,
        by_severity: (group_by(.Severity) | map({severity: .[0].Severity, fail: ([.[] | select(.Status == "FAIL")] | length)})),
        top_failing: [.[] | select(.Status == "FAIL")] | group_by(.CheckID) | map({check: .[0].CheckID, count: length, severity: .[0].Severity}) | sort_by(-.count) | .[0:10]
    }'
fi
```

### CIS Benchmark Assessment

```bash
#!/bin/bash
PROVIDER="${1:-aws}"
CIS_VERSION="${2:-cis_2.0_aws}"

echo "=== CIS Benchmark: $CIS_VERSION ==="
prowler "$PROVIDER" --compliance "$CIS_VERSION" --output-formats json --no-banner 2>/dev/null

OUTPUT_DIR=$(ls -td output/prowler-output-* 2>/dev/null | head -1)
if [ -n "$OUTPUT_DIR" ]; then
    echo ""
    echo "=== CIS Compliance Summary ==="
    cat "${OUTPUT_DIR}"/*.json 2>/dev/null | jq -s 'flatten | {
        total_checks: length,
        passing: [.[] | select(.Status == "PASS")] | length,
        failing: [.[] | select(.Status == "FAIL")] | length,
        compliance_pct: (([.[] | select(.Status == "PASS")] | length) / length * 100 | floor),
        failing_sections: [.[] | select(.Status == "FAIL") | .CheckID[:5]] | group_by(.) | map({section: .[0], count: length}) | sort_by(-.count)
    }'
fi
```

### Multi-Account Scanning

```bash
#!/bin/bash
echo "=== Multi-Account Scan ==="
ROLE_NAME="${1:-ProwlerScanRole}"

echo "Scanning with cross-account role: $ROLE_NAME"
prowler aws --role "arn:aws:iam::role/$ROLE_NAME" \
    --severity "critical high" \
    --output-formats json --no-banner 2>/dev/null | tail -10

echo ""
echo "=== Account Comparison ==="
for output in output/prowler-output-*/; do
    ACCOUNT=$(basename "$output" | grep -oP '\d{12}')
    FAILS=$(cat "${output}"*.json 2>/dev/null | jq -s '[flatten[] | select(.Status == "FAIL")] | length')
    echo "Account $ACCOUNT: $FAILS findings"
done | head -10
```

### Service-Specific Deep Dive

```bash
#!/bin/bash
SERVICE="${1:?Service required (e.g., iam, s3, ec2)}"

echo "=== $SERVICE Security Assessment ==="
prowler aws --services "$SERVICE" --output-formats json --no-banner 2>/dev/null

OUTPUT_DIR=$(ls -td output/prowler-output-* 2>/dev/null | head -1)
if [ -n "$OUTPUT_DIR" ]; then
    cat "${OUTPUT_DIR}"/*.json 2>/dev/null | jq -s "flatten | [.[] | select(.Status == \"FAIL\")] | {
        service: \"$SERVICE\",
        failures: length,
        by_check: (group_by(.CheckID) | map({check: .[0].CheckID, description: .[0].CheckTitle, count: length, resources: [.[].ResourceId][:3]}) | sort_by(-.count))
    }"
fi
```

### Remediation Report

```bash
#!/bin/bash
echo "=== Top Remediation Actions ==="
OUTPUT_DIR=$(ls -td output/prowler-output-* 2>/dev/null | head -1)
if [ -n "$OUTPUT_DIR" ]; then
    cat "${OUTPUT_DIR}"/*.json 2>/dev/null | jq -s 'flatten |
        [.[] | select(.Status == "FAIL")] |
        group_by(.CheckID) | map({
            check: .[0].CheckID,
            severity: .[0].Severity,
            title: .[0].CheckTitle,
            affected_resources: length,
            remediation: .[0].Remediation.Recommendation.Text,
            url: .[0].Remediation.Recommendation.Url
        }) | sort_by(-.affected_resources) | .[0:10]
    '
fi
```

## Safety Rules

- **Prowler is read-only** -- it uses describe/list API calls only, never modifies resources
- **IAM permissions required** -- ensure scanning role has SecurityAudit and ViewOnlyAccess policies
- **API rate limiting** -- large accounts may trigger AWS API throttling -- use `--services` to scope
- **Multi-account scanning** requires cross-account IAM roles configured in advance
- **Output files may contain resource identifiers** -- handle with appropriate security

## Output Format

Present results as a structured report:
```
Analyzing Prowler Report
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

- **Credential scope**: Prowler scans the account/subscription tied to active credentials -- verify identity first
- **Region coverage**: Default may scan only one region -- use `--region` or `--all-regions` for full coverage
- **False positives**: Some checks have expected failures (e.g., root account MFA in org member accounts)
- **Scan duration**: Full AWS account scan can take 30-60 minutes -- use `--services` for targeted scans
- **Output directory**: Previous scan outputs accumulate -- clean up old output directories
- **Compliance mapping**: Not all checks map to all frameworks -- some compliance requirements need manual verification
- **Custom checks**: Custom checks require specific directory structure -- follow Prowler check template
- **Version differences**: Prowler v3 vs v4 have different CLI syntax and output formats
