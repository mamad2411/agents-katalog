---
name: managing-aws-codepipeline
description: |
  Use when working with Aws Codepipeline — aWS CodePipeline CI/CD pipeline
  management and execution analysis. Covers pipeline inventory, stage and action
  status, execution history, pipeline triggers, artifact stores, and action type
  configurations. Use when inspecting pipeline health, debugging failed stages,
  reviewing execution history, or auditing pipeline configurations.
connection_type: aws
preload: false
---

# AWS CodePipeline Management Skill

Analyze and manage AWS CodePipeline pipelines, stages, and execution history.

## MANDATORY: Discovery-First Pattern

**Always list pipelines before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== CodePipeline Inventory ==="
aws codepipeline list-pipelines --output text \
  --query 'pipelines[].[name,version,created,updated]'

echo ""
echo "=== Pipeline States ==="
for pipeline in $(aws codepipeline list-pipelines --output text --query 'pipelines[].name'); do
  aws codepipeline get-pipeline-state --name "$pipeline" --output text \
    --query "stageStates[].[\"$pipeline\",stageName,latestExecution.status]" &
done
wait
```

### Phase 2: Analysis

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== Recent Executions ==="
for pipeline in $(aws codepipeline list-pipelines --output text --query 'pipelines[].name'); do
  aws codepipeline list-pipeline-executions --pipeline-name "$pipeline" --max-items 3 --output text \
    --query "pipelineExecutionSummaries[].[\"$pipeline\",pipelineExecutionId,status,startTime,trigger.triggerType]" &
done
wait | head -30

echo ""
echo "=== Failed Stages ==="
for pipeline in $(aws codepipeline list-pipelines --output text --query 'pipelines[].name'); do
  aws codepipeline get-pipeline-state --name "$pipeline" --output text \
    --query "stageStates[?latestExecution.status=='Failed'].[\"$pipeline\",stageName,latestExecution.status,actionStates[0].latestExecution.summary]" &
done
wait

echo ""
echo "=== Pipeline Structure ==="
for pipeline in $(aws codepipeline list-pipelines --output text --query 'pipelines[].name'); do
  aws codepipeline get-pipeline --name "$pipeline" --output text \
    --query "pipeline.stages[].[\"$pipeline\",name,actions[].actionTypeId.provider]" &
done
wait

echo ""
echo "=== Action Executions (last failed) ==="
for pipeline in $(aws codepipeline list-pipelines --output text --query 'pipelines[].name'); do
  aws codepipeline list-action-executions --pipeline-name "$pipeline" \
    --filter pipelineExecutionId=$(aws codepipeline list-pipeline-executions --pipeline-name "$pipeline" --max-items 1 --output text --query 'pipelineExecutionSummaries[0].pipelineExecutionId') \
    --output text \
    --query "actionExecutionDetails[?status=='Failed'].[\"$pipeline\",stageName,actionName,status,output.executionResult.externalExecutionSummary]" 2>/dev/null &
done
wait | head -15
```

## Output Format

- Target ≤50 lines per output
- Use `--output text --query` for all commands
- Tab-delimited fields: PipelineName, Stage, Action, Status
- Aggregate execution counts by status for busy pipelines
- Never dump full pipeline definitions -- show stage/action summary

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

- **Execution status values**: InProgress, Stopped, Stopping, Succeeded, Superseded, Failed
- **Stage vs action status**: A stage fails if any action fails -- check action-level for root cause
- **Superseded executions**: Newer commits can supersede in-progress executions -- not a failure
- **Artifact store**: Pipelines use S3 for artifacts -- check bucket permissions if stages fail
- **Cross-region actions**: Some actions can run in different regions -- check `region` field
- **Manual approval**: Stages with manual approval actions will show InProgress until approved/rejected
- **Trigger types**: Can be webhook, CloudWatch Event, manual, or polling -- check pipeline trigger configuration
