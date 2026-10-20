---
name: managing-cloudformation
description: |
  Use when working with Cloudformation — aWS CloudFormation stack management.
  Covers stack lifecycle, change sets, drift detection, template validation,
  nested stacks, stack sets, and event troubleshooting. Use when managing
  CloudFormation stacks, investigating deployment failures, detecting drift, or
  validating templates.
connection_type: cloudformation
preload: false
---

# CloudFormation Management Skill

Manage and inspect AWS CloudFormation stacks, change sets, and templates.

## MANDATORY: Discovery-First Pattern

**Always list stacks and check stack status before modifying infrastructure.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Active Stacks ==="
aws cloudformation list-stacks \
    --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE UPDATE_ROLLBACK_COMPLETE ROLLBACK_COMPLETE \
    --query 'StackSummaries[].{Name:StackName,Status:StackStatus,Updated:LastUpdatedTime}' \
    --output table 2>/dev/null | head -30

echo ""
echo "=== Failed Stacks ==="
aws cloudformation list-stacks \
    --stack-status-filter CREATE_FAILED UPDATE_FAILED DELETE_FAILED ROLLBACK_FAILED \
    --query 'StackSummaries[].{Name:StackName,Status:StackStatus,Reason:StackStatusReason}' \
    --output table 2>/dev/null

echo ""
echo "=== Stack Sets ==="
aws cloudformation list-stack-sets \
    --status ACTIVE \
    --query 'Summaries[].{Name:StackSetName,Status:Status}' \
    --output table 2>/dev/null | head -15
```

## Core Helper Functions

```bash
#!/bin/bash

# CloudFormation API wrapper
cfn_cmd() {
    aws cloudformation "$@" --output json 2>/dev/null
}

# Get stack status
cfn_status() {
    local stack="$1"
    cfn_cmd describe-stacks --stack-name "$stack" \
        --query 'Stacks[0].StackStatus' --output text
}

# Get stack events (most recent)
cfn_events() {
    local stack="$1"
    local limit="${2:-10}"
    cfn_cmd describe-stack-events --stack-name "$stack" \
        --query "StackEvents[:${limit}]"
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `--query` (JMESPath) to filter AWS CLI output
- Use `--output table` for human-readable summaries
- Never dump full templates -- extract specific resources

## Common Operations

### Stack Inspection and Resources

```bash
#!/bin/bash
STACK_NAME="${1:?Stack name required}"

echo "=== Stack Details ==="
aws cloudformation describe-stacks --stack-name "$STACK_NAME" \
    --query 'Stacks[0].{Name:StackName,Status:StackStatus,Created:CreationTime,Updated:LastUpdatedTime,Description:Description}' \
    --output table 2>/dev/null

echo ""
echo "=== Stack Resources ==="
aws cloudformation list-stack-resources --stack-name "$STACK_NAME" \
    --query 'StackResourceSummaries[].{Logical:LogicalResourceId,Type:ResourceType,Status:ResourceStatus}' \
    --output table 2>/dev/null | head -30

echo ""
echo "=== Stack Outputs ==="
aws cloudformation describe-stacks --stack-name "$STACK_NAME" \
    --query 'Stacks[0].Outputs[].{Key:OutputKey,Value:OutputValue}' \
    --output table 2>/dev/null

echo ""
echo "=== Stack Parameters ==="
aws cloudformation describe-stacks --stack-name "$STACK_NAME" \
    --query 'Stacks[0].Parameters[].{Key:ParameterKey,Value:ParameterValue}' \
    --output table 2>/dev/null
```

### Change Set Management

```bash
#!/bin/bash
STACK_NAME="${1:?Stack name required}"
TEMPLATE="${2:?Template file or URL required}"

echo "=== Creating Change Set ==="
CHANGE_SET_NAME="review-$(date +%s)"
aws cloudformation create-change-set \
    --stack-name "$STACK_NAME" \
    --change-set-name "$CHANGE_SET_NAME" \
    --template-body "file://${TEMPLATE}" \
    --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
    --output json 2>/dev/null | jq '{Id: .Id, StackId: .StackId}'

echo "Waiting for change set to be created..."
aws cloudformation wait change-set-create-complete \
    --stack-name "$STACK_NAME" \
    --change-set-name "$CHANGE_SET_NAME" 2>/dev/null

echo ""
echo "=== Change Set Details ==="
aws cloudformation describe-change-set \
    --stack-name "$STACK_NAME" \
    --change-set-name "$CHANGE_SET_NAME" \
    --query 'Changes[].{Action:ResourceChange.Action,Resource:ResourceChange.LogicalResourceId,Type:ResourceChange.ResourceType,Replacement:ResourceChange.Replacement}' \
    --output table 2>/dev/null
```

### Drift Detection

```bash
#!/bin/bash
STACK_NAME="${1:?Stack name required}"

echo "=== Initiating Drift Detection ==="
DETECT_ID=$(aws cloudformation detect-stack-drift \
    --stack-name "$STACK_NAME" \
    --query 'StackDriftDetectionId' --output text 2>/dev/null)

echo "Detection ID: $DETECT_ID"
echo "Waiting for detection to complete..."
sleep 10

echo ""
echo "=== Drift Status ==="
aws cloudformation describe-stack-drift-detection-status \
    --stack-drift-detection-id "$DETECT_ID" \
    --query '{Status:DetectionStatus,DriftStatus:StackDriftStatus,DriftedResources:DriftedStackResourceCount}' \
    --output table 2>/dev/null

echo ""
echo "=== Drifted Resources ==="
aws cloudformation describe-stack-resource-drifts \
    --stack-name "$STACK_NAME" \
    --stack-resource-drift-status-filters MODIFIED DELETED \
    --query 'StackResourceDrifts[].{Resource:LogicalResourceId,Type:ResourceType,Status:StackResourceDriftStatus}' \
    --output table 2>/dev/null
```

### Template Validation

```bash
#!/bin/bash
TEMPLATE="${1:?Template file required}"

echo "=== Template Validation ==="
aws cloudformation validate-template \
    --template-body "file://${TEMPLATE}" \
    --query '{Parameters:Parameters[].ParameterKey,Capabilities:Capabilities,Description:Description}' \
    --output json 2>/dev/null

echo ""
echo "=== Resource Types in Template ==="
cat "$TEMPLATE" | python3 -c "
import sys, json, yaml
try:
    tpl = yaml.safe_load(sys.stdin) or json.load(open('$TEMPLATE'))
except:
    tpl = json.load(open('$TEMPLATE'))
resources = tpl.get('Resources', {})
for name, r in resources.items():
    print(f\"{name}: {r['Type']}\")
" 2>/dev/null | head -30
```

### Event Troubleshooting

```bash
#!/bin/bash
STACK_NAME="${1:?Stack name required}"

echo "=== Recent Stack Events ==="
aws cloudformation describe-stack-events --stack-name "$STACK_NAME" \
    --query 'StackEvents[:20].{Time:Timestamp,Resource:LogicalResourceId,Status:ResourceStatus,Reason:ResourceStatusReason}' \
    --output table 2>/dev/null

echo ""
echo "=== Failed Events ==="
aws cloudformation describe-stack-events --stack-name "$STACK_NAME" \
    --query 'StackEvents[?contains(ResourceStatus,`FAILED`)].{Time:Timestamp,Resource:LogicalResourceId,Reason:ResourceStatusReason}' \
    --output table 2>/dev/null | head -20
```

## Safety Rules

- **NEVER delete stacks without explicit user confirmation** -- use `--retain-resources` if needed
- **Always use change sets** for production stacks instead of direct `update-stack`
- **Enable termination protection** on critical stacks
- **Use `--capabilities CAPABILITY_IAM`** only when template creates IAM resources
- **Review change set before executing** -- replacement operations destroy and recreate resources

## Output Format

Present results as a structured report:
```
Managing Cloudformation Report
══════════════════════════════
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

- **ROLLBACK_COMPLETE state**: Stack cannot be updated -- must be deleted and recreated
- **Circular dependencies**: Resources referencing each other cause creation failures -- use `DependsOn` carefully
- **Resource limits**: AWS has limits on resources per stack (500) -- use nested stacks for large deployments
- **IAM capabilities**: Forgetting `CAPABILITY_IAM` causes immediate failure on IAM-containing templates
- **Export/Import dependencies**: Cannot delete a stack whose exports are imported by other stacks
- **Drift false positives**: Some resources show drift due to AWS-managed fields (e.g., default security group rules)
- **Template size limit**: Direct upload limited to 51,200 bytes -- use S3 for larger templates
- **Stack set drift**: Individual stack instances in a stack set can drift independently
