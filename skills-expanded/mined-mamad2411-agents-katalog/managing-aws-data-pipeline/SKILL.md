---
name: managing-aws-data-pipeline
description: |
  Use when working with Aws Data Pipeline — aWS Data Pipeline workflow
  management and execution analysis. Covers pipeline inventory, pipeline
  definitions, execution status, object status, task runner health, and pipeline
  scheduling. Use when inspecting data pipeline health, debugging failed
  executions, reviewing pipeline definitions, or auditing pipeline schedules.
connection_type: aws
preload: false
---

# AWS Data Pipeline Management Skill

Analyze and manage AWS Data Pipeline workflows, definitions, and execution status.

## MANDATORY: Discovery-First Pattern

**Always list pipelines before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== Data Pipelines ==="
aws datapipeline list-pipelines --output text \
  --query 'pipelineIdList[].[id,name]'

echo ""
echo "=== Pipeline Details ==="
PIPELINE_IDS=$(aws datapipeline list-pipelines --output text --query 'pipelineIdList[].id')
if [ -n "$PIPELINE_IDS" ]; then
  aws datapipeline describe-pipelines --pipeline-ids $PIPELINE_IDS --output text \
    --query 'pipelineDescriptionList[].[pipelineId,name,fields[?key==`@pipelineState`].stringValue|[0]]' | head -20
fi
```

### Phase 2: Analysis

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== Pipeline Run Status ==="
for pipeline_id in $(aws datapipeline list-pipelines --output text --query 'pipelineIdList[].id'); do
  aws datapipeline list-runs --pipeline-id "$pipeline_id" --output text \
    --query "[:5]" 2>/dev/null | head -5 &
done
wait

echo ""
echo "=== Pipeline Object Status ==="
for pipeline_id in $(aws datapipeline list-pipelines --output text --query 'pipelineIdList[].id'); do
  aws datapipeline query-objects --pipeline-id "$pipeline_id" --objects-query '{"selectors":[]}' --sphere INSTANCE --output text \
    --query "ids[:5]" 2>/dev/null &
done
wait

echo ""
echo "=== Pipeline Definitions ==="
for pipeline_id in $(aws datapipeline list-pipelines --output text --query 'pipelineIdList[].id'); do
  aws datapipeline get-pipeline-definition --pipeline-id "$pipeline_id" --output text \
    --query "pipelineObjects[:5].[id,name,fields[?key==`type`].stringValue|[0]]" 2>/dev/null &
done
wait

echo ""
echo "=== Pipeline Tags ==="
PIPELINE_IDS=$(aws datapipeline list-pipelines --output text --query 'pipelineIdList[].id')
if [ -n "$PIPELINE_IDS" ]; then
  aws datapipeline describe-pipelines --pipeline-ids $PIPELINE_IDS --output text \
    --query 'pipelineDescriptionList[].[pipelineId,tags[].{k:key,v:value}]' 2>/dev/null | head -15
fi
```

## Output Format

- Target ≤50 lines per output
- Use `--output text --query` for all commands
- Tab-delimited fields: PipelineId, Name, State, Status
- Aggregate run counts by status for busy pipelines
- Never dump full pipeline definitions -- show object types and names only

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

- **Service status**: AWS Data Pipeline is a legacy service -- consider Step Functions or Glue for new workflows
- **Pipeline states**: PENDING, SCHEDULING, RUNNING, SHUTTING_DOWN, FINISHED -- check `@pipelineState` field
- **Object spheres**: COMPONENT (definition), INSTANCE (execution), ATTEMPT (retry) -- specify correct sphere
- **Scheduling**: Pipelines can use cron-like schedules or on-demand activation -- check schedule object
- **Task runners**: Default uses AWS-managed runners; custom runners need health monitoring
- **Health status**: Check `@healthStatus` field for ERROR, ERROR_COUNT thresholds
- **Backfill**: Activating with past start dates triggers backfill runs -- can be expensive
