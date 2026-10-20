---
name: managing-aws-control-tower
description: |
  Use when working with Aws Control Tower — aWS Control Tower landing zone and
  account management. Covers landing zone status, enrolled accounts, guardrails
  (controls), organizational units, baseline configurations, and drift
  detection. Use when auditing landing zone health, reviewing guardrail
  compliance, inspecting account enrollment, or troubleshooting Control Tower
  drift.
connection_type: aws
preload: false
---

# AWS Control Tower Management Skill

Analyze and manage AWS Control Tower landing zones, accounts, and guardrails.

## MANDATORY: Discovery-First Pattern

**Always check landing zone status before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== Landing Zone Status ==="
aws controltower list-landing-zones --output text \
  --query 'landingZones[].[arn,status]' 2>/dev/null

echo ""
echo "=== Enabled Controls (Guardrails) ==="
# List OUs first from Organizations
OU_IDS=$(aws organizations list-organizational-units-for-parent \
  --parent-id $(aws organizations list-roots --output text --query 'Roots[0].Id') \
  --output text --query 'OrganizationalUnits[].Id' 2>/dev/null)

for ou_id in $OU_IDS; do
  ou_arn="arn:aws:organizations::$(aws sts get-caller-identity --output text --query 'Account'):ou/$ou_id"
  aws controltower list-enabled-controls --target-identifier "$ou_arn" --output text \
    --query "enabledControls[].[controlIdentifier]" 2>/dev/null &
done
wait | head -20

echo ""
echo "=== Organizational Units ==="
ROOT_ID=$(aws organizations list-roots --output text --query 'Roots[0].Id' 2>/dev/null)
aws organizations list-organizational-units-for-parent --parent-id "$ROOT_ID" --output text \
  --query 'OrganizationalUnits[].[Id,Name]' 2>/dev/null

echo ""
echo "=== Enrolled Accounts ==="
aws organizations list-accounts --output text \
  --query 'Accounts[].[Id,Name,Email,Status,JoinedTimestamp]' 2>/dev/null | head -20
```

### Phase 2: Analysis

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== Account Status ==="
aws organizations list-accounts --output text \
  --query 'Accounts[?Status!=`ACTIVE`].[Id,Name,Status]' 2>/dev/null

echo ""
echo "=== Control Tower Baselines ==="
aws controltower list-baselines --output text \
  --query 'baselines[].[arn,name,description]' 2>/dev/null | head -15

echo ""
echo "=== Enabled Baselines ==="
aws controltower list-enabled-baselines --output text \
  --query 'enabledBaselines[].[arn,baselineIdentifier,statusSummary.status]' 2>/dev/null | head -15

echo ""
echo "=== Landing Zone Operations (recent) ==="
aws controltower list-landing-zone-operations --output text \
  --query 'landingZoneOperations[:5].[operationIdentifier,operationType,status]' 2>/dev/null

echo ""
echo "=== SCPs on OUs ==="
ROOT_ID=$(aws organizations list-roots --output text --query 'Roots[0].Id' 2>/dev/null)
for ou_id in $(aws organizations list-organizational-units-for-parent --parent-id "$ROOT_ID" --output text --query 'OrganizationalUnits[].Id' 2>/dev/null); do
  aws organizations list-policies-for-target --target-id "$ou_id" --filter SERVICE_CONTROL_POLICY --output text \
    --query "Policies[].[\"$ou_id\",Name,Id]" 2>/dev/null &
done
wait
```

## Output Format

- Target ≤50 lines per output
- Use `--output text --query` for all commands
- Tab-delimited fields: AccountId, OUName, ControlId, Status
- Summarize guardrail counts per OU rather than listing all
- Never dump full SCP documents -- show policy names only

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

- **API availability**: Control Tower APIs require the management account and the home region
- **Guardrail types**: Preventive (SCP-based), Detective (Config rules), Proactive (CloudFormation hooks)
- **Drift detection**: Drift can occur from manual changes to SCPs, OUs, or accounts -- check regularly
- **Landing zone versions**: Upgrades are not automatic -- check `version` against latest available
- **Account factory**: Uses Service Catalog under the hood -- check Service Catalog for provisioned products
- **Region deny**: Control Tower applies region-deny SCPs -- new regions need explicit enablement
- **Nested OUs**: Control Tower supports nested OUs -- recurse through the hierarchy for complete view
