---
name: monitor-check
description: "Check runtime health and metrics from cloud monitoring platforms. Use for service health assessment, alert review, metric queries, or dashboard links. Trigger phrases: '监控检查', '服务健康度', '查看告警', 'check alerts', 'monitoring', 'metric query', '运行时监控', '云监控', 'CloudWatch', '阿里云监控', '阿里云告警'."
license: MIT
metadata:
  author: Orbit contributors
  version: "1.1.0"
---

# Monitor Check

Query runtime health, alerts, and metrics from cloud monitoring platforms via user-installed cloud CLIs. Support Alibaba Cloud (阿里云), Azure, and AWS. Provide structured health assessments and alert summaries without requiring a dedicated packaged CLI.

## Capability Dependencies

- External cloud CLI (scenario-only, not an Orbit packaged capability) — at least one installed and configured:
  - Alibaba Cloud CLI (`aliyun`) for CloudMonitor (云监控) / SLS (日志服务) / ARMS (应用实时监控)
  - AWS CLI (`aws`) for CloudWatch / CloudWatch Logs / CloudWatch Alarms
  - Azure CLI (`az`) for Azure Monitor / Log Analytics
- One `tracker` provider skill such as `jira` or `github-issue` (optional, only when alert → ticket escalation is requested)

This skill does **not** ship its own packaged CLI. It relies on the user's pre-installed cloud CLI and follows the **scenario-only pattern** — it orchestrates existing cloud CLI commands and does not wrap them in a launcher.

## Inputs

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `CLOUD_PROVIDER` | Conditional | Cloud provider: `aliyun`, `aws`, `azure`, or `auto`; when `auto`, detect from installed CLIs (default: `auto`) | `aliyun` |
| `SERVICE_IDENTIFIER` | Yes | Service or resource identifier to check (instance ID, app name, namespace, etc.) | `i-0abc1234` or `myapp-prod` |
| `CHECK_TYPE` | No | What to check: `health` (service status), `alerts` (active alarms), `metrics` (time-series query), or `all` (default: `all`) | `alerts` |
| `TIME_WINDOW` | No | Lookback window for metrics and alerts: `1h`, `6h`, `24h`, `7d` (default: `1h`) | `24h` |
| `METRIC_NAMES` | Conditional | Cloud-specific metric names to query; only when `CHECK_TYPE` includes `metrics` | `CPUUtilization,MemoryUtilization` |
| `ESCALATE_TO_TRACKER` | No | `true` to create tracker tickets for critical alerts; `false` to report only (default: `false`) | `true` |
| `TRACKER_PROJECT` | Conditional | Selected tracker project, workspace, or container key for the active provider (Jira project key, or GitHub Issue `owner/repo`); only when `ESCALATE_TO_TRACKER=true` | `PROJ` |

Follow the shared missing-input stop rule in `../using-orbit/references/safety-rules.md`.

Scenario-specific input rule:
- detect `CLOUD_PROVIDER` from installed CLIs when set to `auto`
- ask for `METRIC_NAMES` only when `CHECK_TYPE` includes `metrics` and no default metrics are known for the service
- ask for `TRACKER_PROJECT` only when `ESCALATE_TO_TRACKER=true`

## Missing-input collection rules

- Ask for missing inputs in one plain-text message, requesting only the smallest still-missing set for the current check.
- Use normalized shared field names from `../using-orbit/references/common-input-contract.md` whenever the input belongs to the shared capability contract (`TRACKER_PROJECT` for the tracker project identity).
- Defer tracker-provider questions until escalation is explicitly requested.

## Critical Prompt-Shape Override

When the user asks for a health check or alert review and provides `SERVICE_IDENTIFIER`, treat it as sufficient to start. Make the first live stop boundary the cloud CLI availability check — if no supported cloud CLI is installed, return: "No supported cloud CLI found. Install Alibaba Cloud CLI (`aliyun`), AWS CLI (`aws`), or Azure CLI (`az`) and configure credentials first." Defer all tracker-provider questions until escalation is explicitly requested.

## Before You Start

Before resolving the first stop boundary, read only the Missing-Input Stop Rule section of `../using-orbit/references/safety-rules.md`.

### Preflight Configuration Check

Verify that at least one supported cloud CLI is available:

```bash
which aliyun 2>/dev/null && echo "aliyun: available" || echo "aliyun: not found"
which aws 2>/dev/null && echo "aws: available" || echo "aws: not found"
which az 2>/dev/null && echo "az: available" || echo "az: not found"
```

If `CLOUD_PROVIDER` is `auto`, use the first available CLI. If `CLOUD_PROVIDER` is explicit, verify that CLI exists.

If no supported CLI is found, STOP. Output: "No supported cloud CLI found. Install and configure a cloud CLI (Alibaba Cloud CLI, AWS CLI, or Azure CLI) before using this skill."

If tracker escalation is requested, also follow the preflight protocol in `../using-orbit/references/safety-rules.md` for the selected **tracker** provider.

### After boundary resolved

Read `../using-orbit/references/safety-rules.md`, `../using-orbit/references/cli-patterns.md`, and `../using-orbit/references/output-conventions.md` first.
Use those shared references for common execution policy. This skill file remains responsible for the cloud-CLI-specific query patterns and health assessment logic.

## Cloud CLI Command Patterns

This section defines the command patterns for each supported cloud provider. Adapt flags and identifiers to the user's actual environment.

### Alibaba Cloud (CloudMonitor 云监控)

**Service health check** (ECS instance):
```bash
aliyun ecs DescribeInstanceStatus --InstanceId.1 {{SERVICE_IDENTIFIER}}
```

**Active alarms**:
```bash
aliyun cms DescribeActiveAlertRule --Namespace acs_ecs_dashboard
```

**Metric query**:
```bash
aliyun cms QueryMetricList --Namespace acs_ecs_dashboard --MetricName {{METRIC_NAME}} --Dimensions '{"instanceId":"{{SERVICE_IDENTIFIER}}"}' --StartTime <epoch-ms> --EndTime <epoch-ms> --Period 300
```

Common ECS metric names:
- `CPUUtilization` — CPU 使用率
- `memory_usedutilization` — 内存使用率
- `diskusage_utilization` — 磁盘使用率
- `networkin_rate` / `networkout_rate` — 网络流入/流出速率

**Recent log entries** (SLS 日志服务, for error investigation):
```bash
aliyun sls GetLogs --project {{SLS_PROJECT}} --logstore {{SLS_LOGSTORE}} --query "ERROR" --from <epoch-s> --to <epoch-s>
```

**ARMS application health** (for APM):
```bash
aliyun arms SearchTraces --pid {{ARMS_PID}} --startTime <epoch-ms> --endTime <epoch-ms>
```

### AWS (CloudWatch)

**Service health check**:
```bash
aws ec2 describe-instance-status --instance-ids {{SERVICE_IDENTIFIER}} --query 'InstanceStatuses[0].[InstanceStatus.Status,SystemStatus.Status]' --output text
```

**Active alarms**:
```bash
aws cloudwatch describe-alarms --state-value ALARM --query 'MetricAlarms[?Namespace==`{{NAMESPACE}}`].[AlarmName,StateValue,MetricName,Statistic,ComparisonOperator,Threshold]' --output table
```

**Recent alarm history** (within `TIME_WINDOW`):
```bash
aws cloudwatch describe-alarm-history --alarm-name {{ALARM_NAME}} --history-type StateUpdate --start-time $(date -u -v-{{TIME_WINDOW}} +%Y-%m-%dT%H:%M:%SZ) --max-records 10 --output table
```

**Metric query**:
```bash
aws cloudwatch get-metric-statistics --namespace {{NAMESPACE}} --metric-name {{METRIC_NAME}} --dimensions Name=InstanceId,Value={{SERVICE_IDENTIFIER}} --start-time $(date -u -v-{{TIME_WINDOW}} +%Y-%m-%dT%H:%M:%SZ) --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) --period 300 --statistics Average --output json
```

**Recent log entries** (for error investigation):
```bash
aws logs tail /aws/{{LOG_GROUP}} --since {{TIME_WINDOW}} --filter-pattern "ERROR" --limit 50
```

### Azure (Azure Monitor)

**Service health check**:
```bash
az resource show --ids {{SERVICE_IDENTIFIER}} --query 'properties.provisioningState' --output tsv
```

**Active alerts**:
```bash
az monitor activity-log alert list --query "[?contains(name, '{{SERVICE_IDENTIFIER}}')].{Name:name, Enabled:enabled, Condition:condition}" --output table
```

**Metric query**:
```bash
az monitor metrics list --resource {{SERVICE_IDENTIFIER}} --metric "{{METRIC_NAMES}}" --interval PT5M --start-time $(date -u -v-{{TIME_WINDOW}} +%Y-%m-%dT%H:%M:%SZ) --output table
```

## Workflow

### Step 1: Detect Cloud Provider

If `CLOUD_PROVIDER` is `auto`, detect from installed CLIs. If multiple are available, ask the user which to use.

Record the provider for subsequent steps.

### Step 2: Run Health Checks

Execute the health check commands for the detected provider.

**If the service is unhealthy**, note the specific failure:
- Alibaba Cloud: `Status != Running` or health check failed
- AWS: `InstanceStatus.Status != ok` or `SystemStatus.Status != ok`
- Azure: `provisioningState != Succeeded`

**If the service is not found**, STOP. Output: "Service '{{SERVICE_IDENTIFIER}}' not found. Verify the identifier and cloud provider."

### Step 3: Check Active Alerts

Execute the alert query commands.

For each active alarm/alert, extract:
- Name
- State (ALARM / OK / INSUFFICIENT_DATA)
- Metric name
- Threshold condition
- Last state change time

**Categorize alerts by severity**:
- 🔴 **Critical**: alarms in ALARM state that directly affect service availability
- 🟡 **Warning**: alarms in ALARM state for performance degradation
- 🔵 **Info**: alarms in INSUFFICIENT_DATA or recently resolved

### Step 4: Query Metrics (conditional)

Only execute when `CHECK_TYPE` includes `metrics` and `METRIC_NAMES` is provided.

Execute the metric query commands. For each metric:
- Extract average, min, max values
- Identify any anomalies (sudden spikes or drops)
- Compare against typical thresholds where known

Default thresholds (override when user provides specific thresholds):
- CPU Utilization: warning > 80%, critical > 95%
- Memory Utilization: warning > 85%, critical > 95%
- Error Rate: warning > 1%, critical > 5%
- Latency (p99): warning > 2s, critical > 5s

### Step 5: Compile Health Assessment

Combine all check results into a structured health assessment.

### Step 6: Escalate to tracker (conditional, requires user confirmation)

Only execute when `ESCALATE_TO_TRACKER=true` and there are critical alerts.

**Follow `../using-orbit/references/safety-rules.md` write confirmation protocol.**

Display the planned tracker tickets before creating. For each critical alert, offer to create a tracker ticket.

Jira example:
```
jira issue create --project {{TRACKER_PROJECT}} --type Bug --summary "[Monitor] {{ALARM_NAME}} — {{ALARM_DESCRIPTION}}" --description "{{ALARM_DETAILS}}" --fields-json '{"priority": "High", "labels": ["monitoring-alert", "{{CLOUD_PROVIDER}}"]}'
```

GitHub Issue example:
```
github-issue issue create --namespace {{TRACKER_PROJECT}} --repo {{TRACKER_REPO}} --title "[Monitor] {{ALARM_NAME}} — {{ALARM_DESCRIPTION}}" --description "{{ALARM_DETAILS}}" --labels "monitoring-alert,{{CLOUD_PROVIDER}}"
```

For GitHub Issue, `TRACKER_PROJECT` carries the `owner/repo` form per `common-input-contract.md`; split it into `--namespace`/`--repo` when invoking the launcher.

## Output

```
## Monitor Check — {{SERVICE_IDENTIFIER}}

### Provider
- Cloud: {{CLOUD_PROVIDER}}

### Service Health
| Check | Status |
|-------|--------|
| Instance/System | ✓ OK |

### Active Alerts
| Severity | Alarm | Metric | State | Since |
|----------|-------|--------|-------|-------|
| 🔴 Critical | HighCPU | CPUUtilization > 95% | ALARM | 2026-06-12 10:30 |
| 🟡 Warning | HighLatency | LatencyP99 > 2s | ALARM | 2026-06-12 10:15 |

### Metrics ({{TIME_WINDOW}})
| Metric | Avg | Min | Max | Status |
|--------|-----|-----|-----|--------|
| CPUUtilization | 82% | 45% | 97% | ⚠ Warning |
| ErrorRate | 0.3% | 0% | 1.2% | ✓ Normal |

### Overall Health: ⚠ DEGRADED
- 1 critical alert, 1 warning alert
- CPUUtilization exceeded 95% threshold within the monitoring window
```

## Local Persistence

Local state is stored under `~/.config/monitor-check/`:
```
~/.config/monitor-check/
  runs/
    <service-identifier>-<timestamp>.json
```

Internal local-state persistence under `~/.config/monitor-check/` is allowed without extra confirmation.

## Allowed Automatic Writes

- Local state persistence under `~/.config/monitor-check/`
- Cloud CLI read operations (health checks, metric queries, alert listing)

## Forbidden Automatic Writes

- Tracker issue create without confirmation
- Any cloud resource modifications (scale up/down, restart, etc.)
- Any alarm state changes (acknowledge, silence, etc.)
- Docs writes without confirmation and dedup check
