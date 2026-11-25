---
name: managing-infracost
description: |
  Use when working with Infracost — infracost Terraform cost estimation and
  FinOps policy enforcement. Covers cost breakdown by resource, diff analysis
  between plan changes, CI/CD integration checks, policy validation, and cost
  forecasting. Use when estimating infrastructure cost impact, reviewing
  Terraform changes, or enforcing cost guardrails.
connection_type: infracost
preload: false
---

# Infracost Management Skill

Estimate and manage Terraform infrastructure costs with Infracost.

## MANDATORY: Discovery-First Pattern

**Always verify Infracost installation and configuration before running estimates.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Infracost Version ==="
infracost --version 2>/dev/null

echo ""
echo "=== Configuration ==="
infracost configure get api_key 2>/dev/null && echo "API key: configured" || echo "API key: NOT configured"
infracost configure get pricing_api_endpoint 2>/dev/null
infracost configure get currency 2>/dev/null || echo "Currency: USD (default)"

echo ""
echo "=== Terraform Project Detection ==="
find . -name "*.tf" -maxdepth 3 -exec dirname {} \; | sort -u | head -20
```

## Core Helper Functions

```bash
#!/bin/bash

infracost_breakdown() {
    local path="${1:-.}"
    local format="${2:-json}"
    infracost breakdown --path "$path" --format "$format" 2>/dev/null
}

infracost_diff() {
    local path="${1:-.}"
    local compare="${2:-}"
    if [ -n "$compare" ]; then
        infracost diff --path "$path" --compare-to "$compare" --format json 2>/dev/null
    else
        infracost diff --path "$path" --format json 2>/dev/null
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines per output
- Use `--format json` with jq for structured extraction
- Round monthly costs to 2 decimal places

## Common Operations

### Cost Breakdown by Resource

```bash
#!/bin/bash
TF_PATH="${1:-.}"

echo "=== Infrastructure Cost Breakdown ==="
infracost breakdown --path "$TF_PATH" --format json 2>/dev/null | jq -r '
    .projects[0].breakdown.resources[] |
    "\(.name)\t$\(.monthlyCost // "0.00")/mo\t\(.resourceType)"
' | sort -t'$' -k2 -rn | column -t | head -25

echo ""
echo "=== Total Monthly Cost ==="
infracost breakdown --path "$TF_PATH" --format json 2>/dev/null | jq '{
    totalMonthlyCost: .totalMonthlyCost,
    totalHourlyCost: .totalHourlyCost,
    resourceCount: (.projects[0].breakdown.resources | length),
    currency: .currency
}'
```

### Diff Analysis (Plan Cost Impact)

```bash
#!/bin/bash
TF_PATH="${1:-.}"
BASELINE="${2:-infracost-base.json}"

echo "=== Cost Diff Analysis ==="
if [ -f "$BASELINE" ]; then
    infracost diff --path "$TF_PATH" --compare-to "$BASELINE" --format json 2>/dev/null | jq '{
        totalMonthlyCostBefore: .projects[0].diff.totalMonthlyCost,
        totalMonthlyCostAfter: .totalMonthlyCost,
        diffTotalMonthlyCost: .diffTotalMonthlyCost,
        summary: .summary
    }'
else
    echo "No baseline found. Generating baseline..."
    infracost breakdown --path "$TF_PATH" --format json --out-file "$BASELINE" 2>/dev/null
    echo "Baseline saved to $BASELINE. Run again after making changes."
fi

echo ""
echo "=== Changed Resources ==="
infracost diff --path "$TF_PATH" --compare-to "$BASELINE" --format json 2>/dev/null | jq -r '
    .projects[0].diff.resources[]? |
    select(.diff != null) |
    "\(.name)\tBefore: $\(.monthlyCostBefore // "0")\tAfter: $\(.monthlyCostAfter // "0")\tDiff: $\(.diff.totalMonthlyCost // "0")"
' | column -t | head -15
```

### Policy Check (Cost Guardrails)

```bash
#!/bin/bash
TF_PATH="${1:-.}"
POLICY_FILE="${2:-infracost-policy.rego}"

echo "=== Cost Policy Evaluation ==="
if [ -f "$POLICY_FILE" ]; then
    infracost breakdown --path "$TF_PATH" --format json 2>/dev/null \
        | infracost comment --format json --policy-path "$POLICY_FILE" --dry-run 2>/dev/null
else
    echo "No policy file found. Running basic cost checks..."
    RESULT=$(infracost breakdown --path "$TF_PATH" --format json 2>/dev/null)
    TOTAL=$(echo "$RESULT" | jq -r '.totalMonthlyCost // "0"')
    echo "Total monthly cost: \$$TOTAL"
    echo ""
    echo "=== Expensive Resources (>$100/mo) ==="
    echo "$RESULT" | jq -r '
        .projects[].breakdown.resources[] |
        select((.monthlyCost // "0" | tonumber) > 100) |
        "\(.name)\t$\(.monthlyCost)/mo\t\(.resourceType)"
    ' | sort -t'$' -k2 -rn | column -t | head -15
fi
```

### CI Integration Output

```bash
#!/bin/bash
TF_PATH="${1:-.}"

echo "=== Generating CI Comment ==="
infracost breakdown --path "$TF_PATH" --format json --out-file /tmp/infracost-report.json 2>/dev/null

echo ""
echo "=== Cost Summary for PR ==="
jq '{
    total_monthly: .totalMonthlyCost,
    total_hourly: .totalHourlyCost,
    projects: [.projects[] | {
        name: .metadata.path,
        monthly_cost: .breakdown.totalMonthlyCost,
        resource_count: (.breakdown.resources | length)
    }]
}' /tmp/infracost-report.json

echo ""
echo "=== Top 5 Costliest Resources ==="
jq -r '.projects[].breakdown.resources[] |
    "\(.name)\t$\(.monthlyCost // "0")/mo"
' /tmp/infracost-report.json | sort -t'$' -k2 -rn | head -5
```

### Multi-Project Cost Report

```bash
#!/bin/bash
CONFIG_FILE="${1:-infracost.yml}"

echo "=== Multi-Project Cost Report ==="
if [ -f "$CONFIG_FILE" ]; then
    infracost breakdown --config-file "$CONFIG_FILE" --format json 2>/dev/null | jq -r '
        .projects[] | "\(.metadata.path)\t$\(.breakdown.totalMonthlyCost // "0")/mo\tResources: \(.breakdown.resources | length)"
    ' | column -t
else
    echo "No config file found. Scanning subdirectories..."
    for dir in $(find . -name "*.tf" -maxdepth 3 -exec dirname {} \; | sort -u); do
        COST=$(infracost breakdown --path "$dir" --format json 2>/dev/null | jq -r '.totalMonthlyCost // "0"')
        echo "$dir: \$$COST/mo"
    done | head -15
fi
```

## Safety Rules
- **Read-only tool**: Infracost only estimates costs -- it never modifies infrastructure
- **API key protection**: Never log or expose the Infracost API key in CI outputs
- **Baseline management**: Always generate a baseline before comparing diffs
- **Plan file usage**: Prefer using Terraform plan files for accuracy over HCL parsing

## Output Format

Present results as a structured report:
```
Managing Infracost Report
═════════════════════════
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
- **Usage-based costs**: Resources like data transfer, API calls, and storage I/O cannot be estimated without usage data
- **Free tier**: Infracost does not account for free tier allowances -- estimates may be higher than actual
- **Module support**: Nested modules require `--path` to point to root module
- **State vs plan**: Breakdown from HCL may differ from plan-based estimates -- plan is more accurate
- **Currency**: Default is USD -- set `infracost configure set currency EUR` for other currencies
- **Provider pricing**: Prices are based on on-demand rates -- reserved/spot pricing requires usage file
