---
name: managing-infracost-deep
description: |
  Use when working with Infracost Deep — advanced Infracost cost estimation and
  FinOps management. Covers multi-project cost breakdown, diff analysis between
  branches, CI/CD integration inspection, policy enforcement with OPA/Sentinel,
  usage-based estimation, cost anomaly detection, and Infracost Cloud dashboard
  analysis. Use for deep cost analysis, cross-project comparison, policy-driven
  cost guardrails, or usage file configuration.
connection_type: infracost
preload: false
---

# Infracost Deep Management Skill

Advanced cost estimation, policy enforcement, and FinOps analysis with Infracost.

## MANDATORY: Discovery-First Pattern

**Always generate a baseline cost breakdown before comparing or enforcing policies.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Infracost Version ==="
infracost --version 2>/dev/null

echo ""
echo "=== Configuration ==="
infracost configure get api_key 2>/dev/null | sed 's/./*/g' | head -1
infracost configure get pricing_api_endpoint 2>/dev/null
infracost configure get currency 2>/dev/null

echo ""
echo "=== Project Detection ==="
if [ -f infracost.yml ]; then
    cat infracost.yml | head -20
elif [ -f terraform.tf ] || [ -f main.tf ]; then
    echo "Terraform project detected"
    ls *.tf 2>/dev/null | head -10
fi

echo ""
echo "=== Baseline Breakdown ==="
infracost breakdown --path . --format table 2>/dev/null | tail -25
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Detailed Cost Breakdown ==="
infracost breakdown --path . --format json 2>/dev/null | jq '{
    totalMonthlyCost: .totalMonthlyCost,
    totalHourlyCost: .totalHourlyCost,
    currency: .currency,
    projects: [.projects[] | {
        name: .name,
        monthlyCost: .pastBreakdown.totalMonthlyCost,
        resourceCount: (.pastBreakdown.resources // []) | length
    }],
    topResources: [.projects[].pastBreakdown.resources[]? | {name: .name, monthlyCost: .monthlyCost}] | sort_by(-.monthlyCost) | .[0:10]
}' 2>/dev/null | head -40

echo ""
echo "=== Cost Diff (vs main) ==="
infracost diff --path . --compare-to infracost-base.json --format table 2>/dev/null | tail -20 || echo "No baseline file for comparison. Generate one with: infracost breakdown --path . --format json --out-file infracost-base.json"

echo ""
echo "=== Usage Estimation ==="
if [ -f infracost-usage.yml ]; then
    echo "Usage file found:"
    cat infracost-usage.yml | head -20
else
    echo "No usage file found. Create infracost-usage.yml for usage-based estimates."
fi

echo ""
echo "=== Policy Check ==="
if [ -f infracost-policy.rego ]; then
    infracost breakdown --path . --format json 2>/dev/null | infracost output --format json --policy-path infracost-policy.rego 2>&1 | tail -10
else
    echo "No policy file found. Create .rego files for cost guardrails."
fi
```

## Output Format

```
INFRACOST DEEP STATUS: <project>
Monthly Cost: $<amount>/mo | Hourly: $<amount>/hr
Currency: <USD|EUR|etc>
Projects: <count> | Resources: <count>
Top Cost Drivers:
  1. <resource>: $<amount>/mo
  2. <resource>: $<amount>/mo
  3. <resource>: $<amount>/mo
Diff: +$<amount>/mo (+<percentage>%) vs baseline
Policy: <passed|failed> (<violations> violations)
Issues: <any cost spikes, policy violations, or missing usage data>
```

## Safety Rules

- **Infracost is read-only** -- it estimates costs but does not modify infrastructure
- **Review cost estimates carefully** -- estimates depend on accurate usage files for usage-based resources
- **Always generate a baseline** before comparing -- stale baselines produce misleading diffs
- **Policy violations should block PRs** only after thorough testing

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

- **Usage-based resources**: Resources like data transfer, API calls, and storage have zero cost without usage files
- **Module support**: Some Terraform modules may not be fully parsed -- check for warnings in output
- **Currency configuration**: Default is USD -- set currency before comparing across teams
- **Baseline staleness**: Old baseline files produce incorrect diffs -- regenerate regularly
- **Multi-project configs**: infracost.yml must list all project paths correctly for aggregate costs
- **Free tier exclusion**: Infracost does not account for AWS/GCP/Azure free tiers -- actual costs may be lower
- **Spot/reserved pricing**: Estimates use on-demand pricing by default -- use usage files to specify commitment discounts
