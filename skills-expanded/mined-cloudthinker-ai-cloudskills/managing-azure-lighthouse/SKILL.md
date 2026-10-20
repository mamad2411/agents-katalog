---
name: managing-azure-lighthouse
description: |
  Use when working with Azure Lighthouse — azure Lighthouse delegated resource
  management. Covers delegation assignments, managed service offers, customer
  tenant access, cross-tenant resource visibility, role assignments, and
  delegation auditing. Use when managing multi-tenant Azure environments,
  reviewing delegated access, auditing cross-tenant permissions, or configuring
  managed service registrations.
connection_type: azure-lighthouse
preload: false
---

# Azure Lighthouse Management Skill

Manage Azure Lighthouse delegations, cross-tenant access, managed service offers, and role assignments.

## MANDATORY: Discovery-First Pattern

**Always inspect delegation assignments and tenant context before operations.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Current Tenant ==="
az account show --query '{TenantId:tenantId,Name:name,Id:id}' -o table 2>/dev/null

echo ""
echo "=== Delegated Subscriptions ==="
az account list --query '[*].{Name:name,Id:id,TenantId:tenantId,State:state}' -o table 2>/dev/null | head -15

echo ""
echo "=== Registration Assignments ==="
az managedservices assignment list --query '[*].{Name:name,State:properties.provisioningState,Registration:properties.registrationDefinitionId}' -o table 2>/dev/null | head -15

echo ""
echo "=== Registration Definitions ==="
az managedservices definition list --query '[*].{Name:properties.registrationDefinitionName,ManagedBy:properties.managedByTenantId,State:properties.provisioningState}' -o table 2>/dev/null | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== Delegation Details ==="
az managedservices definition list --query '[*].{Name:properties.registrationDefinitionName,ManagedTenant:properties.managedByTenantId,Description:properties.description}' -o table 2>/dev/null | head -10

echo ""
echo "=== Authorization Details ==="
az managedservices definition list -o json 2>/dev/null | jq '.[].properties.authorizations[] | {principalId, roleDefinitionId, principalIdDisplayName}' | head -25

echo ""
echo "=== Eligible Authorizations ==="
az managedservices definition list -o json 2>/dev/null | jq '.[].properties.eligibleAuthorizations[]? | {principalId, roleDefinitionId, justInTimeAccessPolicy}' | head -15

echo ""
echo "=== Cross-Tenant Resources ==="
for sub in $(az account list --query '[?tenantId!=`'$(az account show --query tenantId -o tsv)'`].id' -o tsv 2>/dev/null | head -5); do
  echo "--- Subscription: $sub ---"
  az resource list --subscription "$sub" --query '[*].{Type:type}' -o tsv 2>/dev/null | sort | uniq -c | sort -rn | head -5
done
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Show delegation relationships concisely
- Summarize authorization roles, not full role definition IDs
- List cross-tenant resources by type

## Safety Rules
- **NEVER modify delegations without tenant owner confirmation**
- **Review authorization roles** before accepting managed service offers
- **Audit cross-tenant access** regularly
- **Use eligible authorizations** with JIT access for elevated roles
- **Verify managed-by tenant ID** before accepting registrations

## Output Format

Present results as a structured report:
```
Managing Azure Lighthouse Report
════════════════════════════════
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

