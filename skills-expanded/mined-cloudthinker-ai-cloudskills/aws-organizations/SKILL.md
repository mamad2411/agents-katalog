---
name: aws-organizations
description: |
  Use when working with Aws Organizations — aWS Organizations account
  management, OU structure analysis, SCP policy review, and service access
  control. Covers organizational hierarchy, account inventory, policy
  inheritance analysis, delegated administrator status, and service control
  boundary assessment.
connection_type: aws
preload: false
---

# AWS Organizations Skill

Analyze AWS Organizations structure and policies with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-organizations/` → Organizations-specific analysis (accounts, OUs, SCPs)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

for ou_id in $ous; do
  list_accounts_in_ou "$ou_id" &
done
wait
```

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# Get organization details
describe_organization() {
  aws organizations describe-organization \
    --output text \
    --query 'Organization.[Id,MasterAccountId,MasterAccountEmail,AvailablePolicyTypes[].Type]'
}

# List all accounts
list_accounts() {
  aws organizations list-accounts \
    --output text \
    --query 'Accounts[].[Id,Name,Email,Status,JoinedTimestamp]'
}

# List organizational units under a parent
list_ous() {
  local parent_id=$1
  aws organizations list-organizational-units-for-parent --parent-id "$parent_id" \
    --output text \
    --query 'OrganizationalUnits[].[Id,Name]'
}

# List accounts in an OU
list_accounts_in_ou() {
  local parent_id=$1
  aws organizations list-accounts-for-parent --parent-id "$parent_id" \
    --output text \
    --query 'Accounts[].[Id,Name,Status]'
}

# List policies of a type
list_policies() {
  local policy_type=${1:-SERVICE_CONTROL_POLICY}
  aws organizations list-policies --filter "$policy_type" \
    --output text \
    --query 'Policies[].[Id,Name,Type,AwsManaged]'
}

# List policies attached to a target
list_target_policies() {
  local target_id=$1 policy_type=${2:-SERVICE_CONTROL_POLICY}
  aws organizations list-policies-for-target --target-id "$target_id" --filter "$policy_type" \
    --output text \
    --query 'Policies[].[Id,Name,Type]'
}

# Get policy content
describe_policy() {
  local policy_id=$1
  aws organizations describe-policy --policy-id "$policy_id" \
    --output text \
    --query 'Policy.[PolicySummary.Name,PolicySummary.Type,Content]'
}
```

## Common Operations

### 1. Organization Overview

```bash
#!/bin/bash
export AWS_PAGER=""
aws organizations describe-organization \
  --output text \
  --query 'Organization.[Id,MasterAccountId,MasterAccountEmail,FeatureSet,AvailablePolicyTypes[].Type]'

echo "=== Account Count ==="
aws organizations list-accounts --output text --query 'length(Accounts)'

echo "=== Active vs Suspended ==="
aws organizations list-accounts --output text --query 'Accounts[].Status' | tr '\t' '\n' | sort | uniq -c
```

### 2. OU Hierarchy Tree

```bash
#!/bin/bash
export AWS_PAGER=""
ROOT_ID=$(aws organizations list-roots --output text --query 'Roots[0].Id')

list_ou_recursive() {
  local parent_id=$1 depth=$2
  local indent=$(printf '%*s' $((depth * 2)) '')
  local ous=$(aws organizations list-organizational-units-for-parent --parent-id "$parent_id" \
    --output text --query 'OrganizationalUnits[].[Id,Name]')
  echo "$ous" | while read ou_id ou_name; do
    [ -z "$ou_id" ] && continue
    acct_count=$(aws organizations list-accounts-for-parent --parent-id "$ou_id" \
      --output text --query 'length(Accounts)')
    printf "%s%s (%s) [%s accounts]\n" "$indent" "$ou_name" "$ou_id" "$acct_count"
    list_ou_recursive "$ou_id" $((depth + 1))
  done
}

printf "Root (%s)\n" "$ROOT_ID"
list_ou_recursive "$ROOT_ID" 1
```

### 3. SCP Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
POLICIES=$(aws organizations list-policies --filter SERVICE_CONTROL_POLICY \
  --output text --query 'Policies[].[Id,Name,AwsManaged]')
echo "$POLICIES" | while read policy_id name managed; do
  {
    targets=$(aws organizations list-targets-for-policy --policy-id "$policy_id" \
      --output text --query 'Targets[].[TargetId,Name,Type]')
    printf "POLICY:%s\tManaged:%s\nTargets:\n%s\n" "$name" "$managed" "$targets"
  } &
done
wait
```

### 4. Service Access Status

```bash
#!/bin/bash
export AWS_PAGER=""
aws organizations list-aws-service-access-for-organization \
  --output text \
  --query 'EnabledServicePrincipals[].[ServicePrincipal,DateEnabled]' | sort -k1
```

### 5. Delegated Administrator Accounts

```bash
#!/bin/bash
export AWS_PAGER=""
SERVICES=$(aws organizations list-aws-service-access-for-organization \
  --output text --query 'EnabledServicePrincipals[].ServicePrincipal')
for svc in $SERVICES; do
  aws organizations list-delegated-administrators --service-principal "$svc" \
    --output text \
    --query "DelegatedAdministrators[].[\"$svc\",Id,Name,Status]" 2>/dev/null &
done
wait
```

## Anti-Hallucination Rules

1. **Management account only** - Most Organizations API calls only work from the management (payer) account. Member accounts get AccessDenied.
2. **SCP does not grant permissions** - SCPs only restrict. They set the maximum permissions boundary. IAM policies still required for access.
3. **FullAWSAccess SCP** - Every OU and account has the FullAWSAccess SCP by default. Removing it without attaching a replacement denies ALL actions.
4. **Policy types must be enabled** - SCPs, tag policies, backup policies, and AI services opt-out policies must be explicitly enabled in the organization.
5. **Account status** - Valid statuses: ACTIVE, SUSPENDED, PENDING_CLOSURE. Suspended accounts still incur some charges.

## Output Format

Present results as a structured report:
```
Aws Organizations Report
════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Root vs management account**: The organization root (r-xxxx) is the top of the OU hierarchy. The management account is the account that created the organization. Different concepts.
- **SCP inheritance**: SCPs are inherited down the OU tree. An effective SCP is the intersection of all inherited SCPs from root to the account.
- **Account limits**: Default is 10 accounts per organization. Increase via service quotas.
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum`.
- **Closing accounts**: Account closure has a 90-day grace period. During this time, the account can be reopened.
