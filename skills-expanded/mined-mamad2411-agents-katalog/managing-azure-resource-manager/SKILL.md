---
name: managing-azure-resource-manager
description: |
  Use when working with Azure Resource Manager — azure Resource Manager (ARM)
  template and deployment management. Covers template validation, deployment
  operations, resource group inspection, what-if analysis, deployment history,
  and template spec management. Use when deploying ARM templates, reviewing
  deployment status, analyzing resource groups, or troubleshooting failed
  deployments.
connection_type: azure-resource-manager
preload: false
---

# Azure Resource Manager Management Skill

Manage ARM template deployments, resource groups, deployment history, and template specs.

## MANDATORY: Discovery-First Pattern

**Always inspect resource groups and deployment status before operations.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Current Account ==="
az account show --query '{Name:name,Id:id,TenantId:tenantId}' -o table 2>/dev/null

echo ""
echo "=== Resource Groups ==="
az group list --query '[*].{Name:name,Location:location,State:properties.provisioningState}' -o table 2>/dev/null | head -20

echo ""
echo "=== Recent Deployments ==="
az deployment sub list --query '[*].{Name:name,State:properties.provisioningState,Timestamp:properties.timestamp}' -o table 2>/dev/null | head -10

echo ""
echo "=== Template Specs ==="
az ts list --query '[*].{Name:name,Version:versions[-1].name,Location:location}' -o table 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
RG="${1:?Resource group name required}"

echo "=== Resource Group Resources ==="
az resource list -g "$RG" --query '[*].{Name:name,Type:type,Location:location}' -o table 2>/dev/null | head -20

echo ""
echo "=== Deployment History ==="
az deployment group list -g "$RG" --query '[*].{Name:name,State:properties.provisioningState,Timestamp:properties.timestamp,Mode:properties.mode}' -o table 2>/dev/null | head -10

echo ""
echo "=== Failed Deployments ==="
az deployment group list -g "$RG" --query "[?properties.provisioningState=='Failed'].{Name:name,Error:properties.error.message}" -o table 2>/dev/null | head -10

echo ""
echo "=== What-If (if template provided) ==="
TEMPLATE="${2:-}"
if [ -n "$TEMPLATE" ]; then
  az deployment group what-if -g "$RG" --template-file "$TEMPLATE" 2>&1 | tail -20
fi
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Show resource counts by type, not full resource listings
- Summarize deployment states and highlight failures
- Use what-if output for change previews

## Safety Rules
- **NEVER deploy in Complete mode without explicit confirmation** (deletes unmanaged resources)
- **Always run `what-if`** before deploying templates
- **Use Incremental mode** by default
- **Review deployment error details** before retrying
- **Validate templates** with `az deployment group validate` before deploying

## Output Format

Present results as a structured report:
```
Managing Azure Resource Manager Report
══════════════════════════════════════
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

