---
name: gcp-cloud-deploy
description: |
  Use when working with Gcp Cloud Deploy — google Cloud Deploy delivery pipeline
  management, release tracking, rollout status monitoring, approval workflows,
  and deployment diagnostics via gcloud CLI.
connection_type: gcp
preload: false
---

# Cloud Deploy Skill

Manage and analyze Google Cloud Deploy pipelines using `gcloud deploy` commands.

## Discovery-First Rule

**ALWAYS discover before acting.** Never assume pipeline names, release names, rollout names, or target names.

```bash
# Discover delivery pipelines
gcloud deploy delivery-pipelines list --format=json \
  | jq '[.[] | {name: .name | split("/") | last, uid: .uid, createTime: .createTime, stages: [.serialPipeline.stages[] | {target: .targetId, strategy: .strategy.standard.verify // .strategy.canary}]}]'
```

## Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
for pipeline in $(gcloud deploy delivery-pipelines list --format="value(name)" | xargs -I{} basename {}); do
  {
    gcloud deploy delivery-pipelines describe "$pipeline" --region="$REGION" --format=json
  } &
done
wait
```

## Helper Functions

```bash
# Get pipeline details
get_pipeline() {
  local pipeline="$1" region="$2"
  gcloud deploy delivery-pipelines describe "$pipeline" --region="$region" --format=json \
    | jq '{name: .name | split("/") | last, stages: [.serialPipeline.stages[] | {target: .targetId, profiles: .profiles, strategy: .strategy}], condition: .condition}'
}

# List releases for a pipeline
list_releases() {
  local pipeline="$1" region="$2" limit="${3:-10}"
  gcloud deploy releases list --delivery-pipeline="$pipeline" --region="$region" --format=json --limit="$limit" \
    | jq '[.[] | {name: .name | split("/") | last, createTime: .createTime, renderState: .renderState, condition: .condition, targetSnapshots: [.targetSnapshots[]? | .name | split("/") | last]}]'
}

# List rollouts for a release
list_rollouts() {
  local release="$1" pipeline="$2" region="$3"
  gcloud deploy rollouts list --release="$release" --delivery-pipeline="$pipeline" --region="$region" --format=json \
    | jq '[.[] | {name: .name | split("/") | last, target: .targetId, state: .state, approvalState: .approvalState, deployStartTime: .deployStartTime, deployEndTime: .deployEndTime, failureReason: .failureReason}]'
}

# List targets
list_targets() {
  local region="$1"
  gcloud deploy targets list --region="$region" --format=json \
    | jq '[.[] | {name: .name | split("/") | last, gke: .gke, cloudRun: .run, executionConfigs: .executionConfigs}]'
}
```

## Common Operations

### 1. Pipeline Overview

```bash
pipelines=$(gcloud deploy delivery-pipelines list --region="$REGION" --format="value(name)" | xargs -I{} basename {})
for pipeline in $pipelines; do
  {
    echo "=== Pipeline: $pipeline ==="
    get_pipeline "$pipeline" "$REGION"
    list_releases "$pipeline" "$REGION" 5
  } &
done
wait
```

### 2. Release Management

```bash
# Latest release details
gcloud deploy releases list --delivery-pipeline="$PIPELINE" --region="$REGION" --limit=1 --format=json \
  | jq '.[0] | {name: .name | split("/") | last, renderState: .renderState, buildArtifacts: .buildArtifacts, deliveryPipelineSnapshot: .deliveryPipelineSnapshot.serialPipeline.stages | length}'

# Release render status
gcloud deploy releases describe "$RELEASE" --delivery-pipeline="$PIPELINE" --region="$REGION" --format=json \
  | jq '{renderState: .renderState, renderStartTime: .renderStartTime, renderEndTime: .renderEndTime, targetRenders: .targetRenders}'
```

### 3. Rollout Status

```bash
# Current rollouts across all releases
releases=$(gcloud deploy releases list --delivery-pipeline="$PIPELINE" --region="$REGION" --limit=5 --format="value(name)" | xargs -I{} basename {})
for release in $releases; do
  {
    echo "Release: $release"
    list_rollouts "$release" "$PIPELINE" "$REGION"
  } &
done
wait

# Detailed rollout status
gcloud deploy rollouts describe "$ROLLOUT" --release="$RELEASE" --delivery-pipeline="$PIPELINE" --region="$REGION" --format=json \
  | jq '{state: .state, approvalState: .approvalState, targetId: .targetId, phases: .phases, metadata: .metadata}'
```

### 4. Approval Workflows

```bash
# Find rollouts pending approval
for pipeline in $(gcloud deploy delivery-pipelines list --region="$REGION" --format="value(name)" | xargs -I{} basename {}); do
  {
    releases=$(gcloud deploy releases list --delivery-pipeline="$pipeline" --region="$REGION" --limit=3 --format="value(name)" | xargs -I{} basename {})
    for release in $releases; do
      gcloud deploy rollouts list --release="$release" --delivery-pipeline="$pipeline" --region="$REGION" --format=json \
        | jq --arg p "$pipeline" --arg r "$release" '[.[] | select(.approvalState=="NEEDS_APPROVAL") | {pipeline: $p, release: $r, rollout: .name | split("/") | last, target: .targetId}]'
    done
  } &
done
wait
```

### 5. Target Configuration

```bash
# List all targets with their runtime config
list_targets "$REGION"

# Check target execution environment
gcloud deploy targets describe "$TARGET" --region="$REGION" --format=json \
  | jq '{name: .name | split("/") | last, gke: .gke, run: .run, requireApproval: .requireApproval, executionConfigs: [.executionConfigs[] | {usages: .usages, workerPool: .workerPool, serviceAccount: .serviceAccount, artifactStorage: .artifactStorage}]}'
```

## Output Format

Present results as a structured report:
```
Gcp Cloud Deploy Report
═══════════════════════
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

1. **Render vs deploy**: A release must render successfully before rollouts can begin. Check `renderState` before investigating rollout failures.
2. **Approval timeout**: Rollouts pending approval do not time out by default. Stale approvals can block the pipeline indefinitely.
3. **Target ordering**: Pipeline stages are sequential. A rollout to stage N requires successful completion of stage N-1. Cannot skip stages.
4. **Skaffold version**: Cloud Deploy uses Skaffold for rendering. Skaffold version mismatches between local development and Cloud Deploy can cause render failures.
5. **Service account permissions**: The execution service account needs permissions to deploy to GKE or Cloud Run targets. Check IAM bindings on the target.
