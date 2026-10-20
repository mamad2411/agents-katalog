---
name: managing-aws-service-catalog
description: |
  Use when working with Aws Service Catalog — aWS Service Catalog portfolio and
  product management. Covers portfolio administration, product versioning,
  provisioned product inspection, launch constraints, tag options, and sharing
  across accounts. Use when managing self-service IT catalogs, provisioning
  products, reviewing portfolios, or auditing product usage across an
  organization.
connection_type: aws-service-catalog
preload: false
---

# AWS Service Catalog Management Skill

Manage AWS Service Catalog portfolios, products, provisioned resources, and constraints.

## MANDATORY: Discovery-First Pattern

**Always inspect portfolios and product status before provisioning or updating.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Portfolios ==="
aws servicecatalog list-portfolios --query 'PortfolioDetails[*].{Id:Id,Name:DisplayName,Provider:ProviderName}' --output table 2>/dev/null | head -15

echo ""
echo "=== Products ==="
aws servicecatalog search-products --query 'ProductViewSummaries[*].{Name:Name,Type:Type,Owner:Owner,Id:ProductId}' --output table 2>/dev/null | head -15

echo ""
echo "=== Provisioned Products ==="
aws servicecatalog search-provisioned-products --query 'ProvisionedProducts[*].{Name:Name,Status:Status,Type:Type,Id:Id}' --output table 2>/dev/null | head -15

echo ""
echo "=== Accepted Portfolio Shares ==="
aws servicecatalog list-accepted-portfolio-shares --query 'PortfolioDetails[*].{Id:Id,Name:DisplayName,Provider:ProviderName}' --output table 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
PORTFOLIO_ID="${1:-}"
PRODUCT_ID="${2:-}"

if [ -n "$PORTFOLIO_ID" ]; then
  echo "=== Portfolio Products ==="
  aws servicecatalog search-products-as-admin --portfolio-id "$PORTFOLIO_ID" --query 'ProductViewDetails[*].ProductViewSummary.{Name:Name,Type:Type,Status:Status}' --output table 2>/dev/null | head -15

  echo ""
  echo "=== Constraints ==="
  aws servicecatalog list-constraints-for-portfolio --portfolio-id "$PORTFOLIO_ID" --query 'ConstraintDetails[*].{Type:Type,Description:Description}' --output table 2>/dev/null | head -10

  echo ""
  echo "=== Portfolio Access ==="
  aws servicecatalog list-principals-for-portfolio --portfolio-id "$PORTFOLIO_ID" --query 'Principals[*].{ARN:PrincipalARN,Type:PrincipalType}' --output table 2>/dev/null | head -10
fi

if [ -n "$PRODUCT_ID" ]; then
  echo ""
  echo "=== Product Versions ==="
  aws servicecatalog list-provisioning-artifacts --product-id "$PRODUCT_ID" --query 'ProvisioningArtifactDetails[*].{Name:Name,Id:Id,Active:Active,Created:CreatedTime}' --output table 2>/dev/null | head -10
fi
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Show portfolio-product relationships concisely
- Summarize provisioned product statuses
- List constraints and access controls by portfolio

## Safety Rules
- **NEVER terminate provisioned products without explicit confirmation**
- **Test product provisioning** in a non-production portfolio first
- **Review launch constraints** before granting portfolio access
- **Validate CloudFormation templates** before creating product versions
- **Audit portfolio sharing** across accounts regularly

## Output Format

Present results as a structured report:
```
Managing Aws Service Catalog Report
═══════════════════════════════════
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

