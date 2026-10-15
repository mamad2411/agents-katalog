---
name: aws-fis-experiment-execute
description: >
  Use when the user wants to deploy and run a prepared AWS FIS experiment.
  Triggers on "execute FIS experiment", "run FIS experiment", "start chaos experiment",
  "deploy FIS template", "启动 FIS 实验", "运行混沌实验", "执行故障注入实验",
  "deploy and run the experiment in [directory]". Expects a prepared experiment
  directory (from aws-fis-experiment-prepare or manually created) containing
  experiment-template.json, iam-policy.json, cfn-template.yaml, and alarm configs.
  Deploys resources via CLI or CloudFormation, starts the experiment with strict
  user confirmation, monitors progress, and generates results report.
---

# AWS FIS Experiment Execute

Deploy infrastructure, run an AWS FIS experiment, monitor its progress, and generate
a results report. Reads configuration files from a prepared experiment directory.

## Output Language Rule

Detect the language of the user's conversation and use the **same language** for all output.
- Chinese input -> Chinese output
- English input -> English output

## Prerequisites

Required tools:
- **AWS CLI** — `aws fis`, `aws iam`, `aws cloudwatch`, `aws cloudformation`
- A prepared experiment directory (from aws-fis-experiment-prepare skill)

## Workflow

```dot
digraph execute_flow {
    "Load experiment directory" [shape=box];
    "Validate files" [shape=box];
    "Choose deployment method" [shape=diamond];
    "CLI deployment" [shape=box];
    "CFN deployment" [shape=box];
    "User confirms deployment" [shape=diamond];
    "Deploy resources" [shape=box];
    "User confirms experiment start" [shape=diamond, style=bold, color=red];
    "Start experiment" [shape=box];
    "Monitor experiment" [shape=box];
    "Experiment complete?" [shape=diamond];
    "Generate results report" [shape=box];

    "Load experiment directory" -> "Validate files";
    "Validate files" -> "Choose deployment method";
    "Choose deployment method" -> "CLI deployment" [label="CLI"];
    "Choose deployment method" -> "CFN deployment" [label="CFN"];
    "CLI deployment" -> "User confirms deployment";
    "CFN deployment" -> "User confirms deployment";
    "User confirms deployment" -> "Deploy resources" [label="Yes"];
    "User confirms deployment" -> "Load experiment directory" [label="No, abort"];
    "Deploy resources" -> "User confirms experiment start";
    "User confirms experiment start" -> "Start experiment" [label="Yes, I confirm"];
    "User confirms experiment start" -> "Generate results report" [label="No, abort"];
    "Start experiment" -> "Monitor experiment";
    "Monitor experiment" -> "Experiment complete?" ;
    "Experiment complete?" -> "Monitor experiment" [label="No, poll again"];
    "Experiment complete?" -> "Generate results report" [label="Yes"];
}
```

### Step 1: Load and Validate Experiment Directory

The user provides the path to the experiment directory. Verify it contains the
required files:

```bash
EXPERIMENT_DIR="{USER_PROVIDED_PATH}"

# Required files
ls "${EXPERIMENT_DIR}/experiment-template.json"
ls "${EXPERIMENT_DIR}/iam-policy.json"
ls "${EXPERIMENT_DIR}/cfn-template.yaml"
ls "${EXPERIMENT_DIR}/README.md"
ls "${EXPERIMENT_DIR}/expected-behavior.md"

# Optional files
ls "${EXPERIMENT_DIR}/alarms/stop-condition-alarms.json" 2>/dev/null
ls "${EXPERIMENT_DIR}/alarms/dashboard.json" 2>/dev/null
```

Read `README.md` to understand the experiment and present a summary to the user:
- Scenario name
- Target region and AZ
- Affected resources
- Estimated duration

### Step 2: Choose Deployment Method

Ask the user:

> How would you like to deploy the experiment resources?
> 1. **AWS CLI** — Step-by-step deployment with individual commands
> 2. **CloudFormation** — All-in-one stack deployment

### Step 3: Deploy Resources

#### Path A: AWS CLI Deployment

Execute commands sequentially, showing each command before running it.
See `references/cli-commands.md` for the exact command sequence.

**3a. Create IAM Role**

```bash
# Show command to user, wait for confirmation
aws iam create-role \
  --role-name "FISExperimentRole-{SCENARIO}" \
  --assume-role-policy-document '{...}' \
  --region {REGION}

aws iam put-role-policy \
  --role-name "FISExperimentRole-{SCENARIO}" \
  --policy-name FISExperimentPolicy \
  --policy-document "file://${EXPERIMENT_DIR}/iam-policy.json"
```

**3b. Create CloudWatch Alarms (Stop Conditions)**

Read `alarms/stop-condition-alarms.json` and create each alarm:

```bash
aws cloudwatch put-metric-alarm --cli-input-json '{...}' --region {REGION}
```

**3c. Create CloudWatch Dashboard (Optional)**

```bash
aws cloudwatch put-dashboard \
  --dashboard-name "FIS-{SCENARIO}" \
  --dashboard-body "file://${EXPERIMENT_DIR}/alarms/dashboard.json" \
  --region {REGION}
```

**3d. Update experiment-template.json with real ARNs**

After creating IAM role and alarms, update the experiment template with:
- Actual IAM role ARN
- Actual alarm ARNs for stop conditions

**3e. Create FIS Experiment Template**

```bash
aws fis create-experiment-template \
  --cli-input-json "file://${EXPERIMENT_DIR}/experiment-template.json" \
  --region {REGION}
```

Save the returned `experimentTemplate.id` for the next step.

#### Path B: CloudFormation Deployment

```bash
aws cloudformation deploy \
  --template-file "${EXPERIMENT_DIR}/cfn-template.yaml" \
  --stack-name "fis-{SCENARIO}-{TIMESTAMP}" \
  --capabilities CAPABILITY_NAMED_IAM \
  --region {REGION}
```

Wait for stack creation to complete:

```bash
aws cloudformation wait stack-create-complete \
  --stack-name "fis-{SCENARIO}-{TIMESTAMP}" \
  --region {REGION}
```

Extract the experiment template ID from stack outputs:

```bash
TEMPLATE_ID=$(aws cloudformation describe-stacks \
  --stack-name "fis-{SCENARIO}-{TIMESTAMP}" \
  --query 'Stacks[0].Outputs[?OutputKey==`ExperimentTemplateId`].OutputValue' \
  --output text --region {REGION})
```

### Step 4: Start Experiment (CRITICAL CONFIRMATION)

**This is the most dangerous step. The experiment WILL affect real resources.**

Before starting, present a clear warning:

```
⚠️  WARNING: Starting this FIS experiment will cause REAL impact:

Scenario:    {SCENARIO_NAME}
Region:      {REGION}
Target AZ:   {AZ_ID}
Duration:    {DURATION}

Resources that WILL be affected:
  - {list each affected resource type and count}

Stop Conditions:
  - {list each alarm that will stop the experiment}

Type "Yes, start experiment" to proceed, or "No" to abort.
```

**Only proceed if the user explicitly confirms.**

```bash
aws fis start-experiment \
  --experiment-template-id "{TEMPLATE_ID}" \
  --region {REGION}
```

Save the returned `experiment.id`.

### Step 5: Monitor Experiment

Poll the experiment status and display progress:

```bash
aws fis get-experiment \
  --id "{EXPERIMENT_ID}" \
  --region {REGION} \
  --query '{
    State: experiment.state.status,
    Reason: experiment.state.reason,
    StartTime: experiment.startTime,
    EndTime: experiment.endTime,
    Actions: experiment.actions
  }'
```

**Polling strategy:**
- Poll every 30 seconds for the first 5 minutes
- Poll every 60 seconds after that
- Show current status after each poll
- **Record timestamps** for each status change and action state transition — these
  feed into the per-service timeline in the final report
- **Track per-service events**: For each service in `expected-behavior.md`, note when
  it was impacted (action started), when it recovered, and any intermediate states.
  Query service-specific status (e.g., RDS instance status, ElastiCache replication
  group status, EKS node status) during monitoring to capture detailed observations.

**Status values:**
- `initiating` — Experiment is starting
- `running` — Experiment is in progress
- `completed` — Experiment finished successfully
- `stopping` — Experiment is being stopped (by user or stop condition)
- `stopped` — Experiment was stopped before completion
- `failed` — Experiment failed

**During monitoring, remind the user:**
- Check the CloudWatch dashboard for real-time metrics
- Read `expected-behavior.md` to compare actual vs expected behavior
- The experiment can be stopped at any time:
  ```bash
  aws fis stop-experiment --id "{EXPERIMENT_ID}" --region {REGION}
  ```

### Step 6: Save Results Report to Local File

After the experiment completes (any terminal state), generate a results report and
**write it directly to a local markdown file** instead of outputting the full content
to the terminal. Use the following file naming convention:

```bash
TIMESTAMP=$(date +%Y-%m-%d-%H-%M-%S)
SCENARIO_SLUG=$(echo "{SCENARIO_NAME}" | tr '[:upper:]' '[:lower:]' | tr ' :/' '-')
# File name: ${TIMESTAMP}-${SCENARIO_SLUG}-experiment-results.md
# Save the file in the experiment directory (${EXPERIMENT_DIR})
```

**Timeline emphasis:** Timestamps in the report header (Start Time, End Time) use full
ISO 8601 with timezone (e.g., `2025-03-30T14:05:32+08:00`). However, in timeline tables
and action results, use **time-only format in UTC** (e.g., `05:05:32`) — the report date
is already in the header, so repeating the date on every row adds clutter. Mark the
column header as "Time (UTC)" so the timezone is clear. No milliseconds anywhere. Timeline events are embedded directly
into each service's impact analysis section — do NOT create a separate standalone
timeline section. This allows readers to see the full picture (timeline + impact +
findings) for each service without jumping between sections.

**Per-service analysis:** Read `expected-behavior.md` from the experiment directory to
identify all services under test. For each service, create a sub-section under
"Per-Service Impact Analysis" that includes: (1) the timeline events relevant to that
service, (2) observed behavior from monitoring, (3) key findings. Also check for
indirectly affected services (e.g., MSK affected by network disruption) and include
them.

The results report file must include:

```markdown
## FIS Experiment Results

**Experiment ID:** {EXPERIMENT_ID}
**Template ID:**   {TEMPLATE_ID}
**Status:**        {FINAL_STATUS}
**Start Time:**    {START_TIME}
**End Time:**      {END_TIME}
**Duration:**      {ACTUAL_DURATION}

### Action Results

| Action | Action ID | Status | Start (UTC) | End (UTC) | Duration |
|---|---|---|---|---|---|
| {action_name} | {action_id} | {status} | {HH:MM:SS} | {HH:MM:SS} | {duration} |

### Stop Condition Alarms

| Alarm | Final Status |
|---|---|
| {alarm_name} | {OK/ALARM} |

### Per-Service Impact Analysis

For EACH service listed in expected-behavior.md, create a sub-section below.
Also include indirectly affected services (e.g., services impacted by network
disruption even without a dedicated FIS action).

#### {Service Name} ({resource_identifier})

| Time (UTC) | Event | Observation |
|---|---|---|
| {HH:MM:SS} | {event} | {what was observed at this point} |
| {HH:MM:SS} | {event} | {observed result / status change} |
| ... | ... | ... |

**Key Findings:**
- {finding_1 — what happened and why}
- {finding_2 — recovery behavior}

(Repeat for each service)

### Recovery Status Summary

| Resource | Recovery Status | Notes |
|---|---|---|
| {service} | {Recovered / Partially Recovered / Recovering} | {details} |

### Issues Requiring Attention

#### 1. {Issue title}
- **Problem:** {description}
- **Recommendation:** {action to take, with CLI command if applicable}

### Cleanup

{cleanup instructions with CLI commands}
```

After saving the file, print a brief summary to the terminal listing only:
- The file path of the saved results report
- Experiment ID and final status
- Start time, end time, and duration (all timestamps in ISO 8601 with timezone)
- Per-action status (one line each)
- Per-service recovery status (one line each)
- Issues requiring attention (if any)
- Cleanup instructions

## Safety Rules

1. **Never auto-start experiments.** Always require explicit user confirmation.
2. **Show every CLI command** before executing it.
3. **Display impact warning** before experiment start with specific resource list.
4. **Provide abort instructions** at every step.
5. **Never delete resources** without user confirmation.
6. **Recommend dry-run first** — suggest the user review all files before deploying.

## Cleanup Guide

After the experiment, offer cleanup:

### CLI Cleanup
```bash
# Delete experiment template
aws fis delete-experiment-template --id "{TEMPLATE_ID}" --region {REGION}

# Delete CloudWatch alarms
aws cloudwatch delete-alarms --alarm-names "FIS-StopCondition-{SCENARIO}-{SERVICE}" --region {REGION}

# Delete CloudWatch dashboard
aws cloudwatch delete-dashboards --dashboard-names "FIS-{SCENARIO}" --region {REGION}

# Delete IAM role
aws iam delete-role-policy --role-name "FISExperimentRole-{SCENARIO}" --policy-name FISExperimentPolicy
aws iam delete-role --role-name "FISExperimentRole-{SCENARIO}"
```

### CFN Cleanup
```bash
aws cloudformation delete-stack --stack-name "fis-{SCENARIO}-{TIMESTAMP}" --region {REGION}
```

## Error Handling

| Error | Cause | Resolution |
|---|---|---|
| `AccessDeniedException` | Insufficient permissions | Check IAM policy in iam-policy.json |
| `ValidationException` on template | Invalid template JSON | Validate with `aws fis create-experiment-template --cli-input-json --generate-cli-skeleton` |
| `ResourceNotFoundException` on targets | Tagged resources not found | Verify resource tags match template |
| Alarm creation fails | Metric/namespace mismatch | Check metric name and namespace exist |
| Stack creation fails | CFN template validation error | Run `aws cloudformation validate-template` first |
| Experiment stuck in `initiating` | IAM role propagation delay | Wait 30 seconds and check again |
