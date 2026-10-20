---
name: managing-aws-organizations-deep
description: |
  Use when working with Aws Organizations Deep — aWS Organizations deep
  management. Covers organizational unit hierarchy, account management, service
  control policies (SCPs), tag policies, backup policies, delegated
  administrators, and organizational service integrations. Use when managing
  multi-account AWS environments, reviewing SCPs, auditing OU structures, or
  analyzing organizational policies.
connection_type: aws-organizations
preload: false
---

# AWS Organizations Deep Management Skill

Deep management of AWS Organizations OUs, accounts, SCPs, and organizational policies.

## MANDATORY: Discovery-First Pattern

**Always inspect organization structure and policy assignments before changes.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Organization ==="
aws organizations describe-organization --query 'Organization.{Id:Id,MasterAccountId:MasterAccountId,FeatureSet:FeatureSet}' --output table 2>/dev/null

echo ""
echo "=== Root ==="
ROOT_ID=$(aws organizations list-roots --query 'Roots[0].Id' --output text 2>/dev/null)
echo "Root ID: $ROOT_ID"

echo ""
echo "=== Organizational Units ==="
aws organizations list-organizational-units-for-parent --parent-id "$ROOT_ID" --query 'OrganizationalUnits[*].{Name:Name,Id:Id}' --output table 2>/dev/null | head -15

echo ""
echo "=== Accounts ==="
aws organizations list-accounts --query 'Accounts[*].{Name:Name,Id:Id,Email:Email,Status:Status}' --output table 2>/dev/null | head -20

echo ""
echo "=== Enabled Policy Types ==="
aws organizations list-roots --query 'Roots[0].PolicyTypes[*].{Type:Type,Status:Status}' --output table 2>/dev/null
```

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== Service Control Policies ==="
aws organizations list-policies --filter SERVICE_CONTROL_POLICY --query 'Policies[*].{Name:Name,Id:Id,AwsManaged:AwsManaged}' --output table 2>/dev/null | head -15

echo ""
echo "=== SCP Targets ==="
for policy_id in $(aws organizations list-policies --filter SERVICE_CONTROL_POLICY --query 'Policies[*].Id' --output text 2>/dev/null); do
  POLICY_NAME=$(aws organizations describe-policy --policy-id "$policy_id" --query 'Policy.PolicySummary.Name' --output text 2>/dev/null)
  TARGETS=$(aws organizations list-targets-for-policy --policy-id "$policy_id" --query 'Targets[*].Name' --output text 2>/dev/null)
  echo "$POLICY_NAME -> $TARGETS"
done | head -10

echo ""
echo "=== Tag Policies ==="
aws organizations list-policies --filter TAG_POLICY --query 'Policies[*].{Name:Name,Id:Id}' --output table 2>/dev/null | head -10

echo ""
echo "=== Delegated Administrators ==="
aws organizations list-delegated-administrators --query 'DelegatedAdministrators[*].{AccountId:Id,Name:Name,ServicePrincipal:DelegationEnabledDate}' --output table 2>/dev/null | head -10

echo ""
echo "=== Enabled Services ==="
aws organizations list-aws-service-access-for-organization --query 'EnabledServicePrincipals[*].ServicePrincipal' --output table 2>/dev/null | head -15
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Show OU hierarchy as a tree when possible
- Summarize SCP targets and effects
- List accounts with OU membership

## Safety Rules
- **NEVER modify SCPs without reviewing the policy document**
- **NEVER detach the FullAWSAccess SCP** from the root without replacement
- **Test SCPs on non-production OUs first**
- **Review account move impacts** on inherited policies
- **Check delegated admin permissions** before changes
- **Audit service integrations** before disabling

## Output Format

Present results as a structured report:
```
Managing Aws Organizations Deep Report
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

