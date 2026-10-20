---
name: managing-azure-policy-deep
description: |
  Use when working with Azure Policy Deep — azure Policy deep compliance and
  governance management. Covers policy definitions, initiatives, assignments,
  compliance evaluation, exemptions, remediation tasks, custom policies, and
  regulatory compliance. Use when managing Azure governance at scale, reviewing
  compliance states, creating custom policies, or troubleshooting policy
  evaluation results.
connection_type: azure-policy
preload: false
---

# Azure Policy Deep Management Skill

Deep management of Azure Policy definitions, initiatives, assignments, compliance, and remediation.

## MANDATORY: Discovery-First Pattern

**Always inspect policy assignments and compliance state before changes.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Policy Assignments (Subscription) ==="
az policy assignment list --query '[*].{Name:name,Policy:policyDefinitionId,Enforcement:enforcementMode,Scope:scope}' -o table 2>/dev/null | head -15

echo ""
echo "=== Compliance Summary ==="
az policy state summarize --query '{total: results.resourceDetails[].count, nonCompliant: results.nonCompliantResources, policyAssignments: policyAssignments[:5] | [*].{Name:policyAssignmentId,NonCompliant:results.nonCompliantResources}}' -o json 2>/dev/null | jq '.' | head -15

echo ""
echo "=== Initiatives ==="
az policy set-definition list --custom-only --query '[*].{Name:displayName,Policies:policyDefinitions | length(@)}' -o table 2>/dev/null | head -10

echo ""
echo "=== Exemptions ==="
az policy exemption list --query '[*].{Name:name,Category:exemptionCategory,Policy:policyAssignmentId,Expiry:expiresOn}' -o table 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
ASSIGNMENT="${1:-}"

echo "=== Non-Compliant Resources ==="
if [ -n "$ASSIGNMENT" ]; then
  az policy state list --policy-assignment "$ASSIGNMENT" --filter "complianceState eq 'NonCompliant'" --query '[*].{Resource:resourceId,Policy:policyDefinitionName,Reason:policyDefinitionAction}' -o table 2>/dev/null | head -15
else
  az policy state list --filter "complianceState eq 'NonCompliant'" --query '[*].{Resource:resourceId,Policy:policyDefinitionName}' -o table 2>/dev/null | head -15
fi

echo ""
echo "=== Remediation Tasks ==="
az policy remediation list --query '[*].{Name:name,Policy:policyAssignmentId,Status:provisioningState,Created:createdOn}' -o table 2>/dev/null | head -10

echo ""
echo "=== Policy Evaluation Details ==="
if [ -n "$ASSIGNMENT" ]; then
  az policy state list --policy-assignment "$ASSIGNMENT" --top 5 --query '[*].{Resource:resourceId,State:complianceState,Reason:complianceReasonCode}' -o table 2>/dev/null
fi

echo ""
echo "=== Regulatory Compliance ==="
az policy state summarize --management-group "$(az account show --query tenantId -o tsv 2>/dev/null)" --query 'policyAssignments[:5] | [*].{Name:policyAssignmentId,NonCompliant:results.nonCompliantResources}' -o table 2>/dev/null | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Show compliance summaries, not per-resource details
- Highlight non-compliant resource counts by policy
- Summarize remediation task statuses

## Safety Rules
- **NEVER enforce Deny policies without testing in Audit mode first**
- **Review non-compliant resources** before triggering remediation
- **Test custom policy definitions** with DoNotEnforce mode
- **Set exemption expiry dates** to prevent permanent exceptions
- **Validate initiative definitions** before assignment
- **Check scope inheritance** before management-group-level assignments

## Output Format

Present results as a structured report:
```
Managing Azure Policy Deep Report
═════════════════════════════════
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

