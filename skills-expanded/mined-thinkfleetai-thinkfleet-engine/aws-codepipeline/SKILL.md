---
name: aws-codepipeline
description: "Manage AWS CodePipeline CI/CD pipelines."
metadata: {"thinkfleetbot":{"emoji":"🔄","requires":{"bins":["aws","jq"],"env":["AWS_ACCESS_KEY_ID","AWS_SECRET_ACCESS_KEY"]}}}
---

# AWS CodePipeline

Manage CI/CD pipelines.

## List pipelines

```bash
aws codepipeline list-pipelines --query 'pipelines[].{Name:name,Created:created,Updated:updated}' --output table
```

## Get pipeline state

```bash
aws codepipeline get-pipeline-state --name my-pipeline | jq '.stageStates[] | {Stage: .stageName, Status: .latestExecution.status, Action: .actionStates[0].latestExecution.status}'
```

## Get pipeline details

```bash
aws codepipeline get-pipeline --name my-pipeline | jq '.pipeline | {Name: .name, Stages: [.stages[].name]}'
```

## Start pipeline execution

```bash
aws codepipeline start-pipeline-execution --name my-pipeline | jq '{PipelineExecutionId}'
```

## List executions

```bash
aws codepipeline list-pipeline-executions --pipeline-name my-pipeline --max-items 10 \
  --query 'pipelineExecutionSummaries[].{Id:pipelineExecutionId,Status:status,Trigger:trigger.triggerType,Started:startTime}' --output table
```

## Get execution details

```bash
aws codepipeline get-pipeline-execution --pipeline-name my-pipeline \
  --pipeline-execution-id abc-123 | jq '{Status: .pipelineExecution.status, Artifacts: .pipelineExecution.artifactRevisions}'
```

## Retry failed stage

```bash
aws codepipeline retry-stage-execution --pipeline-name my-pipeline \
  --stage-name Deploy --pipeline-execution-id abc-123 \
  --retry-mode FAILED_ACTIONS | jq '{PipelineExecutionId}'
```

## Notes

- Pipelines execute sequentially through stages.
- Confirm before starting executions or retrying stages.
