---
name: aws-systems-manager
description: |
  Use when working with Aws Systems Manager — aWS Systems Manager parameter
  store management, session management, patch compliance tracking, and Run
  Command analysis. Covers parameter inventory, managed instance status,
  automation execution, maintenance windows, and inventory collection.
connection_type: aws
preload: false
---

# AWS Systems Manager Skill

Analyze AWS Systems Manager resources with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-systems-manager/` → SSM-specific analysis (parameters, sessions, patches, commands)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

for instance in $instances; do
  get_patch_compliance "$instance" &
done
wait
```

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# List parameters (paginated)
list_parameters() {
  aws ssm describe-parameters --max-results 50 \
    --output text \
    --query 'Parameters[].[Name,Type,LastModifiedDate,Version]'
}

# Get parameter value
get_parameter() {
  local name=$1
  aws ssm get-parameter --name "$name" --with-decryption \
    --output text \
    --query 'Parameter.[Name,Type,Value,Version,LastModifiedDate]'
}

# List parameters by path
get_parameters_by_path() {
  local path=$1
  aws ssm get-parameters-by-path --path "$path" --recursive \
    --output text \
    --query 'Parameters[].[Name,Type,Version,LastModifiedDate]'
}

# List managed instances
list_managed_instances() {
  aws ssm describe-instance-information \
    --output text \
    --query 'InstanceInformationList[].[InstanceId,PingStatus,PlatformType,PlatformName,AgentVersion,IsLatestVersion]'
}

# Get patch compliance for an instance
get_patch_compliance() {
  local instance_id=$1
  aws ssm describe-instance-patch-states --instance-ids "$instance_id" \
    --output text \
    --query 'InstancePatchStates[].[InstanceId,PatchGroup,InstalledCount,MissingCount,FailedCount,InstalledRejectedCount,OperationEndTime]'
}

# List recent command invocations
list_commands() {
  aws ssm list-commands --max-results 20 \
    --output text \
    --query 'Commands[].[CommandId,DocumentName,Status,InstanceIds[0],RequestedDateTime]'
}
```

## Common Operations

### 1. Parameter Store Inventory

```bash
#!/bin/bash
export AWS_PAGER=""
aws ssm describe-parameters --max-results 50 \
  --output text \
  --query 'Parameters[].[Name,Type,LastModifiedDate,Version,Tier]' | sort -k1
```

### 2. Managed Instance Health

```bash
#!/bin/bash
export AWS_PAGER=""
aws ssm describe-instance-information \
  --output text \
  --query 'InstanceInformationList[].[InstanceId,PingStatus,PlatformType,PlatformName,AgentVersion,IsLatestVersion,LastPingDateTime]' \
  | sort -k2
```

### 3. Patch Compliance Summary

```bash
#!/bin/bash
export AWS_PAGER=""
INSTANCES=$(aws ssm describe-instance-information --output text --query 'InstanceInformationList[].InstanceId')
for inst in $INSTANCES; do
  aws ssm describe-instance-patch-states --instance-ids "$inst" \
    --output text \
    --query 'InstancePatchStates[].[InstanceId,InstalledCount,MissingCount,FailedCount,NotApplicableCount,OperationEndTime]' &
done
wait
```

### 4. Run Command History

```bash
#!/bin/bash
export AWS_PAGER=""
aws ssm list-commands --max-results 20 \
  --output text \
  --query 'Commands[].[CommandId,DocumentName,Status,StatusDetails,TargetCount,CompletedCount,ErrorCount,RequestedDateTime]' | sort -k8 -r
```

### 5. Session Manager Activity

```bash
#!/bin/bash
export AWS_PAGER=""
aws ssm describe-sessions --state Active \
  --output text \
  --query 'Sessions[].[SessionId,Target,Status,StartDate,Owner]' &

aws ssm describe-sessions --state History --max-results 20 \
  --output text \
  --query 'Sessions[].[SessionId,Target,Status,StartDate,EndDate,Owner]' &
wait
```

## Anti-Hallucination Rules

1. **SecureString parameters are encrypted** - `get-parameter` without `--with-decryption` returns encrypted values for SecureString. Always use `--with-decryption` for readable values.
2. **PingStatus reflects SSM agent** - PingStatus "Online" means the SSM agent is responding, not that the instance is healthy. "ConnectionLost" means no agent response in 5+ minutes.
3. **Parameter tiers** - Standard (free, 4KB, 10K max), Advanced ($0.05/month, 8KB, 100K max), Intelligent-Tiering (auto). Tier affects cost.
4. **Patch baselines are OS-specific** - Each OS has a separate default patch baseline. Custom baselines must match the target OS.
5. **Run Command != SSH** - Run Command executes documents via SSM agent, not SSH. No SSH keys or open ports required.

## Output Format

Present results as a structured report:
```
Aws Systems Manager Report
══════════════════════════
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

- **Parameter path hierarchy**: Parameters use `/` path separators. `get-parameters-by-path` with `--recursive` fetches all under a path prefix.
- **Parameter versions**: Each update creates a new version. Use `:version` suffix to reference specific versions (e.g., `/app/config:3`).
- **Patch group assignment**: Instances must have a `Patch Group` tag to be associated with a patch baseline. Untagged instances use the default baseline.
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum`.
- **Document permissions**: SSM documents can be shared with specific accounts or publicly. Audit with `describe-document-permission`.
