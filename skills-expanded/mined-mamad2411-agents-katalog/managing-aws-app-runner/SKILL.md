---
name: managing-aws-app-runner
description: |
  Use when working with Aws App Runner — aWS App Runner service management and
  health analysis. Covers service inventory, deployment status, auto-scaling
  configurations, custom domain associations, VPC connector settings, and
  observability configurations. Use when inspecting App Runner services,
  debugging deployment failures, reviewing scaling behavior, or auditing service
  configurations.
connection_type: aws
preload: false
---

# AWS App Runner Management Skill

Analyze and manage AWS App Runner services, deployments, and scaling configurations.

## MANDATORY: Discovery-First Pattern

**Always list services before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== App Runner Services ==="
aws apprunner list-services --output text \
  --query 'ServiceSummaryList[].[ServiceName,ServiceArn,Status,ServiceUrl]'

echo ""
echo "=== Service Details ==="
for arn in $(aws apprunner list-services --output text --query 'ServiceSummaryList[].ServiceArn'); do
  aws apprunner describe-service --service-arn "$arn" --output text \
    --query 'Service.[ServiceName,Status,SourceConfiguration.ImageRepository.ImageIdentifier,InstanceConfiguration.Cpu,InstanceConfiguration.Memory]' &
done
wait

echo ""
echo "=== Auto Scaling Configurations ==="
aws apprunner list-auto-scaling-configurations --output text \
  --query 'AutoScalingConfigurationSummaryList[].[AutoScalingConfigurationName,AutoScalingConfigurationRevision,Status]'
```

### Phase 2: Analysis

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== Service Health ==="
for arn in $(aws apprunner list-services --output text --query 'ServiceSummaryList[].ServiceArn'); do
  {
    name=$(aws apprunner describe-service --service-arn "$arn" --output text --query 'Service.ServiceName')
    status=$(aws apprunner describe-service --service-arn "$arn" --output text --query 'Service.Status')
    printf "%s\t%s\n" "$name" "$status"
  } &
done
wait

echo ""
echo "=== Recent Operations ==="
for arn in $(aws apprunner list-services --output text --query 'ServiceSummaryList[].ServiceArn'); do
  aws apprunner list-operations --service-arn "$arn" --output text \
    --query "OperationSummaryList[:3].[\"$(echo $arn | awk -F/ '{print $NF}')\",Type,Status,StartedAt,EndedAt]" &
done
wait

echo ""
echo "=== Custom Domains ==="
for arn in $(aws apprunner list-services --output text --query 'ServiceSummaryList[].ServiceArn'); do
  aws apprunner describe-custom-domains --service-arn "$arn" --output text \
    --query "CustomDomains[].[DomainName,Status,CertificateValidationRecords[0].Value]" 2>/dev/null &
done
wait

echo ""
echo "=== VPC Connectors ==="
aws apprunner list-vpc-connectors --output text \
  --query 'VpcConnectors[].[VpcConnectorName,Status,Subnets[0],SecurityGroups[0]]' 2>/dev/null
```

## Output Format

- Target ≤50 lines per output
- Use `--output text --query` for all commands
- Tab-delimited fields: ServiceName, Status, Source, CPU, Memory
- Aggregate deployment operations by status
- Never dump full service configuration -- extract key fields only

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

- **Service ARN required**: Most describe/update operations need the full ARN, not just service name
- **Source types**: Services can use image registry or code repository -- check `SourceConfiguration` type
- **Auto-scaling revisions**: Each config change creates a new revision -- check `LatestRevision` vs active
- **VPC connector**: Required for accessing private resources -- check `EgressConfiguration` settings
- **Paused services**: Paused services don't incur compute charges but retain configuration -- check `Status`
- **Deployment triggers**: Auto-deploy can be enabled per service -- check `AutoDeploymentsEnabled`
