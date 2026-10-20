---
name: devops-deployment-safety-check
description: Validate deployment readiness and monitor canary rollout health. Use before deploying to production, after canary release, or when automated deployment gate reports failure. Covers pre-deploy validation, canary health monitoring, rollback criteria, and post-deploy verification.
version: 1.0.0
compatibility: "aws cli v2, kubectl, HERMES_LAB_MODE=mock|live, $DEPLOYMENT_TARGET, $AWS_DEFAULT_REGION"
metadata:
  hermes:
    category: devops
    tags: [deployment, canary, rollback, safety, cicd, production, ec2, kubernetes, ecs]
---

## When to Use

Use this skill when:

- CI/CD pipeline calls a pre-deployment gate (automated trigger: deployment approval webhook)
- Canary deployment reaches 10% traffic split and the health monitoring window starts
- Automated rollback system pages on-call: "Canary health check failed"
- Post-deployment smoke test reports an unexpected error rate increase

Do NOT use for: routine health monitoring without an active deployment (use `sre-ec2-health-check`), cost investigations, K8s pod restarts unrelated to a deployment, or executing deployments directly. This skill is a **gate**, not a deployer.

## Inputs

| Input | Source | Required | Description |
|-------|--------|----------|-------------|
| DEPLOYMENT_TARGET | `$DEPLOYMENT_TARGET` env var | YES | Target service name (e.g., `api-service`, `web-frontend`) |
| DEPLOYMENT_ENV | `$DEPLOYMENT_ENV` env var | YES | Environment: `staging` or `production` |
| AWS_DEFAULT_REGION | `$AWS_DEFAULT_REGION` env var | YES | AWS region (e.g., `us-east-1`) |
| HERMES_LAB_MODE | `$HERMES_LAB_MODE` env var | NO | `mock` or `live` (default: `live`) |
| CANARY_WEIGHT | `$CANARY_WEIGHT` env var | NO | Canary traffic percentage (default: `10`) |

## Prerequisites

- **Tools:** `aws cli v2`, `kubectl` (if K8s deployment target). For lab mode: use `mock-aws` and `mock-kubectl` wrappers in `course/infrastructure/wrappers/`
- **Permissions (read-only for pre-deploy gate):**
  - `elasticloadbalancing:DescribeTargetHealth`
  - `elasticloadbalancing:DescribeTargetGroups`
  - `cloudwatch:GetMetricStatistics`
  - `cloudwatch:DescribeAlarms`
  - `ec2:DescribeInstances`
- **Change window:** Pre-deployment gate requires an approved change ticket. Set `DEPLOYMENT_TICKET` env var to the ticket ID before running.
- **Environment setup:**
  ```bash
  export DEPLOYMENT_TARGET=api-service
  export DEPLOYMENT_ENV=production
  export AWS_DEFAULT_REGION=us-east-1
  ```
- **Lab mode:** Set `HERMES_LAB_MODE=mock` and add `course/infrastructure/wrappers/` to PATH. All mock commands emit a `[MOCK MODE]` banner at the top of every output.

## Procedure

### Phase 1: Pre-Deployment Validation [SCRIPTS ZONE — deterministic]

Run all steps before signaling the CI/CD pipeline to proceed. Record all outputs — they form the pre-deploy baseline for canary comparison.

**Step 1.1 — Target group health BEFORE deployment:**

```bash
aws elbv2 describe-target-health \
  --target-group-arn $(aws elbv2 describe-target-groups \
    --names "$DEPLOYMENT_TARGET-tg" \
    --query 'TargetGroups[0].TargetGroupArn' \
    --output text \
    --region $AWS_DEFAULT_REGION) \
  --region $AWS_DEFAULT_REGION
```

**Expected output (deployment safe):**
```json
{
  "TargetHealthDescriptions": [
    {"TargetHealth": {"State": "healthy"}},
    {"TargetHealth": {"State": "healthy"}}
  ]
}
```
All targets must show `State: "healthy"`. Any `draining`, `unhealthy`, or `unused` state blocks deployment.

---

**Step 1.2 — Current 5XX error rate baseline (5 minutes before deploy):**

```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApplicationELB \
  --metric-name HTTPCode_Target_5XX_Count \
  --dimensions Name=LoadBalancer,Value="app/$DEPLOYMENT_TARGET-alb/abc123" \
  --start-time $(date -u -v-5M +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 60 \
  --statistics Sum \
  --region $AWS_DEFAULT_REGION
```

**Expected output (safe to deploy):** `Datapoints` array with Sum == 0 or Sum <= 5 across all 1-minute intervals. Record the exact values as the pre-deploy baseline.

---

**Step 1.3 — Active alarms that would block deployment:**

```bash
aws cloudwatch describe-alarms \
  --alarm-name-prefix "$DEPLOYMENT_TARGET-" \
  --state-value ALARM \
  --region $AWS_DEFAULT_REGION
```

**Expected output (clear to proceed):** Empty `MetricAlarms` array. Any alarm in `ALARM` state blocks the deployment.

---

**Step 1.4 — Minimum healthy instance count:**

```bash
aws ec2 describe-instances \
  --filters \
    "Name=tag:Service,Values=$DEPLOYMENT_TARGET" \
    "Name=instance-state-name,Values=running" \
  --query 'Reservations[*].Instances[*].InstanceId' \
  --output json \
  --region $AWS_DEFAULT_REGION
```

**Expected output:** JSON array with at least 2 instance IDs. A single-instance target group cannot safely absorb a rolling deployment.

---

### Phase 2: Monitor Canary Deployment [SCRIPTS ZONE — deterministic]

Run Steps 2.1 and 2.2 together every 2 minutes for a minimum 10-minute canary window. Compare each reading against the pre-deploy baseline captured in Phase 1.

**Step 2.1 — 5XX error rate during canary window:**

```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApplicationELB \
  --metric-name HTTPCode_Target_5XX_Count \
  --dimensions Name=LoadBalancer,Value="app/$DEPLOYMENT_TARGET-alb/abc123" \
  --start-time $(date -u -v-2M +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 60 \
  --statistics Sum \
  --region $AWS_DEFAULT_REGION
```

**Expected output (canary healthy):** Sum == 0 or within baseline ± 2 errors per minute. Record each reading with timestamp.

---

**Step 2.2 — Canary target response time (p95):**

```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApplicationELB \
  --metric-name TargetResponseTime \
  --dimensions Name=LoadBalancer,Value="app/$DEPLOYMENT_TARGET-alb/abc123" \
  --start-time $(date -u -v-5M +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 60 \
  --statistics p95 \
  --region $AWS_DEFAULT_REGION
```

**Expected output (acceptable):** p95 < 500ms. Alert threshold: p95 > 2000ms for 2 consecutive periods triggers rollback evaluation. Record each reading with timestamp.

---

### Phase 3: Gate and Rollback Decision [AGENTS ZONE — reasoning]

Review all Phase 1 and Phase 2 data. Apply the following gate decisions in order. All conditions are based on numeric thresholds or status values from collected outputs.

**Pre-deployment gate decisions:**

```
IF any MetricAlarms entry has StateValue == "ALARM" (from Step 1.3):
  THEN: BLOCK deployment.
  Do not proceed. Escalate with alarm names and current StateValue.
  NEVER deploy over an active production alarm.

IF any TargetHealthDescription has HealthStatus == "unhealthy" OR "unused" (from Step 1.1):
  THEN: BLOCK deployment.
  Target group is not healthy enough for a rolling deploy.
  Escalate: list which targets are unhealthy and their health check failure reasons.

IF 5XX error Sum > 5 in the 5 minutes before the deploy window (from Step 1.2):
  THEN: BLOCK deployment.
  Pre-existing errors must be resolved before introducing new code.
  Escalate: provide 5XX Sum readings with timestamps.

IF all alarms clear AND all targets healthy AND 5XX Sum <= 5 per minute:
  THEN: PRE-DEPLOYMENT GATE PASSED.
  Record baseline: exact 5XX Sum and p95 TargetResponseTime values for canary comparison.
  Signal CI/CD pipeline to begin canary deployment.
```

**Canary monitoring gate decisions:**

```
IF 5XX Count during canary window > (baseline 5XX * 3) for 2 consecutive 2-minute windows:
  THEN: ROLLBACK. Error rate tripled relative to baseline.
  Canary is degraded. Escalate immediately with 5XX readings and baseline comparison.

IF p95 TargetResponseTime > 2000ms for 2 consecutive 5-minute measurement windows:
  THEN: ROLLBACK. Latency severely degraded. Canary is unhealthy.
  Escalate: provide p95 time series for last 10 minutes.

IF 5XX Sum <= (baseline * 1.2) AND p95 < 500ms sustained across the full 10-minute canary window:
  THEN: CANARY HEALTHY. Recommend proceeding to full rollout.
  Document: final 5XX Sum and p95 readings with timestamps. Record gate PASS decision.
```

## Escalation Rules

Escalate to deployment owner or on-call engineer when:

- Pre-deployment gate fails (specify which condition blocked it)
- Canary rollback is triggered (specify which threshold was breached)
- Unable to retrieve target group health (permission error or missing ALB — possible misconfiguration)
- Deployment ticket (`$DEPLOYMENT_TICKET`) is missing or expired

**Include in every escalation handoff:**
1. Pre-deploy baseline: 5XX Sum (Step 1.2) and p95 TargetResponseTime (Step 2.2 first reading)
2. Canary readings: 5XX Sum and p95 from each 2-minute polling window
3. Gate decision: exact condition that triggered BLOCK or ROLLBACK, with timestamps
4. CloudWatch alarm names in `ALARM` state (Step 1.3 output)
5. Recommended action: "Block deployment" or "Execute rollback" — do NOT take action without acknowledgment

## NEVER DO

- **NEVER approve a deployment when any production alarm is in `ALARM` state** — even if the alarm seems unrelated. Unknown blast radius.
- **NEVER modify load balancer weights, target group configurations, or security groups** as part of this skill. This skill is a gate, not a deployer. All configuration changes go through the CI/CD pipeline.
- **NEVER initiate rollback without first recording the canary metrics that triggered it** — evidence is required for incident post-mortem.
- **NEVER execute deployment commands directly** — this skill outputs gate PASS/BLOCK/ROLLBACK decisions. The CI/CD pipeline executes them. Running deployment commands outside the pipeline bypasses change controls.
- **NEVER mark the canary as healthy based on a single 1-minute window** — transient spikes and recovery can mask real issues. Minimum 2 consecutive clean windows required for PASS.

## Rollback Procedure

If rollback is triggered by this skill's gate decision:

1. Signal CI/CD pipeline rollback — requires on-call approval:
   ```bash
   # This command requires DEPLOYMENT_ID from the CI/CD pipeline output
   aws codedeploy stop-deployment \
     --deployment-id $DEPLOYMENT_ID \
     --region $AWS_DEFAULT_REGION
   ```
   Do NOT run this without explicit approval from the on-call engineer.

2. Verify original target group is restored within 5 minutes — re-run Step 1.1:
   ```bash
   aws elbv2 describe-target-health \
     --target-group-arn $(aws elbv2 describe-target-groups \
       --names "$DEPLOYMENT_TARGET-tg" \
       --query 'TargetGroups[0].TargetGroupArn' \
       --output text \
       --region $AWS_DEFAULT_REGION) \
     --region $AWS_DEFAULT_REGION
   ```
   Expected: all targets return to `State: "healthy"`.

3. Verify 5XX error rate returns to pre-deploy baseline within 5 minutes — re-run Step 1.2. Expected: Sum <= baseline value captured before deployment.

4. Log the rollback: deployment ID, rollback trigger condition and metric values, timestamp, on-call engineer who approved the rollback action.

## Verification

Deployment gate is complete when all of the following are satisfied:

- [ ] Pre-deployment baseline captured: 5XX Sum and p95 TargetResponseTime recorded before deploy
- [ ] All active alarms checked — none in `ALARM` state for `$DEPLOYMENT_TARGET` service prefix
- [ ] All target group instances verified healthy before rolling deploy begins
- [ ] Minimum 2 healthy instances confirmed (Step 1.4 complete)
- [ ] Canary ran for full 10-minute monitoring window OR rollback was executed
- [ ] Gate decision documented: PASS or ROLLBACK with supporting metric values and timestamps
- [ ] Mock mode: `[MOCK MODE]` banner confirmed visible in all command outputs if `HERMES_LAB_MODE=mock`
