---
name: managing-aws-appconfig
description: |
  Use when working with Aws Appconfig — aWS AppConfig configuration management
  and deployment analysis. Covers applications, environments, configuration
  profiles, deployment strategies, hosted configurations, and deployment status
  monitoring. Use when inspecting AppConfig deployments, reviewing feature
  flags, auditing configuration profiles, or debugging deployment rollbacks.
connection_type: aws
preload: false
---

# AWS AppConfig Management Skill

Analyze and manage AWS AppConfig applications, configurations, and deployments.

## MANDATORY: Discovery-First Pattern

**Always list applications and environments before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== AppConfig Applications ==="
aws appconfig list-applications --output text \
  --query 'Items[].[Id,Name,Description]'

echo ""
echo "=== Environments ==="
for app_id in $(aws appconfig list-applications --output text --query 'Items[].Id'); do
  aws appconfig list-environments --application-id "$app_id" --output text \
    --query "Items[].[\"$app_id\",Id,Name,State]" &
done
wait

echo ""
echo "=== Configuration Profiles ==="
for app_id in $(aws appconfig list-applications --output text --query 'Items[].Id'); do
  aws appconfig list-configuration-profiles --application-id "$app_id" --output text \
    --query "Items[].[\"$app_id\",Id,Name,Type,LocationUri]" &
done
wait

echo ""
echo "=== Deployment Strategies ==="
aws appconfig list-deployment-strategies --output text \
  --query 'Items[].[Id,Name,DeploymentDurationInMinutes,GrowthFactor,FinalBakeTimeInMinutes,ReplicateTo]'
```

### Phase 2: Analysis

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== Active Deployments ==="
for app_id in $(aws appconfig list-applications --output text --query 'Items[].Id'); do
  for env_id in $(aws appconfig list-environments --application-id "$app_id" --output text --query 'Items[].Id'); do
    aws appconfig list-deployments --application-id "$app_id" --environment-id "$env_id" --output text \
      --query "Items[:3].[\"$app_id\",\"$env_id\",DeploymentNumber,ConfigurationName,State,PercentageComplete,StartedAt]" &
  done
done
wait

echo ""
echo "=== Hosted Configuration Versions ==="
for app_id in $(aws appconfig list-applications --output text --query 'Items[].Id'); do
  for profile_id in $(aws appconfig list-configuration-profiles --application-id "$app_id" --output text --query 'Items[].Id'); do
    aws appconfig list-hosted-configuration-versions --application-id "$app_id" --configuration-profile-id "$profile_id" \
      --output text --query "Items[:3].[\"$app_id\",\"$profile_id\",VersionNumber,ContentType]" 2>/dev/null &
  done
done
wait
```

## Output Format

- Target ≤50 lines per output
- Use `--output text --query` for all commands
- Tab-delimited fields: AppId, EnvId, ProfileName, State
- Summarize deployment status with percentage complete
- Never dump full configuration content -- show metadata only

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

- **Deployment state**: States are BAKING, VALIDATING, DEPLOYING, COMPLETE, ROLLING_BACK -- only COMPLETE is stable
- **Configuration profile types**: `AWS.Freeform` for custom configs, `AWS.AppConfig.FeatureFlags` for feature flags
- **Hosted vs external**: Hosted configurations are stored in AppConfig; external use SSM Parameter Store or S3
- **Validators**: Profiles can have JSON Schema or Lambda validators -- check before deployment
- **Rollback triggers**: CloudWatch alarms can trigger automatic rollback -- check environment monitors
- **Growth factor**: Linear deployment grows by this percentage each interval -- 100% means instant deployment
