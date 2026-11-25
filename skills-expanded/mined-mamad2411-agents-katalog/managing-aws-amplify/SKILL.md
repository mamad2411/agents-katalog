---
name: managing-aws-amplify
description: |
  Use when working with Aws Amplify — aWS Amplify application management and
  deployment analysis. Covers Amplify apps, branches, backend environments,
  build status, domain associations, and webhook configurations. Use when
  inspecting Amplify deployments, debugging build failures, reviewing hosting
  configurations, or auditing Amplify app settings.
connection_type: aws
preload: false
---

# AWS Amplify Management Skill

Analyze and manage AWS Amplify applications, deployments, and hosting configurations.

## MANDATORY: Discovery-First Pattern

**Always list apps and branches before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== Amplify Apps ==="
aws amplify list-apps --output text \
  --query 'apps[].[appId,name,defaultDomain,platform,repository]'

echo ""
echo "=== App Branches ==="
for app_id in $(aws amplify list-apps --output text --query 'apps[].appId'); do
  aws amplify list-branches --app-id "$app_id" --output text \
    --query "branchSummaries[].[\"$app_id\",branchName,stage,activeJobId,lastDeployTime]" &
done
wait

echo ""
echo "=== Domain Associations ==="
for app_id in $(aws amplify list-apps --output text --query 'apps[].appId'); do
  aws amplify list-domain-associations --app-id "$app_id" --output text \
    --query "domainAssociations[].[\"$app_id\",domainName,domainStatus,certificateVerificationDNSRecord]" &
done
wait
```

### Phase 2: Analysis

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== Recent Build Jobs ==="
for app_id in $(aws amplify list-apps --output text --query 'apps[].appId'); do
  for branch in $(aws amplify list-branches --app-id "$app_id" --output text --query 'branchSummaries[].branchName'); do
    aws amplify list-jobs --app-id "$app_id" --branch-name "$branch" --max-items 3 --output text \
      --query "jobSummaries[].[\"$app_id\",\"$branch\",jobId,status,startTime,endTime]" &
  done
done
wait

echo ""
echo "=== Backend Environments ==="
for app_id in $(aws amplify list-apps --output text --query 'apps[].appId'); do
  aws amplify list-backend-environments --app-id "$app_id" --output text \
    --query "backendEnvironments[].[\"$app_id\",environmentName,stackName,deploymentArtifacts]" 2>/dev/null &
done
wait

echo ""
echo "=== Webhooks ==="
for app_id in $(aws amplify list-apps --output text --query 'apps[].appId'); do
  aws amplify list-webhooks --app-id "$app_id" --output text \
    --query "webhooks[].[\"$app_id\",webhookId,branchName,webhookUrl]" 2>/dev/null &
done
wait
```

## Output Format

- Target ≤50 lines per output
- Use `--output text --query` for all commands
- Tab-delimited fields: AppId, Name, Branch, Status
- Aggregate build results by status when listing many jobs
- Never dump full build logs -- extract key error lines only

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

- **Build logs**: Use `get-job` to retrieve build steps, not CloudWatch Logs
- **Branch auto-detection**: Amplify may auto-detect branches from repo -- check `enableAutoBranchCreation`
- **Custom domains**: Domain verification can take time -- check `domainStatus` before assuming failure
- **Webhooks**: Each branch can have its own webhook -- list per branch, not per app
- **Platform field**: Values are `WEB` (static) or `WEB_DYNAMIC` (SSR) -- affects build behavior
