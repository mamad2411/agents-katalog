---
name: managing-aws-proton
description: |
  Use when working with Aws Proton — aWS Proton service and environment template
  management. Covers environment templates, service templates, service
  instances, pipeline management, component inspection, and template sync
  configuration. Use when managing Proton environments, deploying services from
  templates, inspecting provisioned resources, or auditing template versions.
connection_type: aws-proton
preload: false
---

# AWS Proton Management Skill

Manage AWS Proton environments, service templates, service instances, and deployment pipelines.

## MANDATORY: Discovery-First Pattern

**Always inspect Proton environment and template status before operations.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Environment Templates ==="
aws proton list-environment-templates --query 'templates[*].{Name:name,DisplayName:displayName,Status:recommendedVersion}' --output table 2>/dev/null | head -15

echo ""
echo "=== Environments ==="
aws proton list-environments --query 'environments[*].{Name:name,Template:templateName,Status:deploymentStatus,LastModified:lastDeploymentSucceededAt}' --output table 2>/dev/null | head -15

echo ""
echo "=== Service Templates ==="
aws proton list-service-templates --query 'templates[*].{Name:name,DisplayName:displayName,Pipeline:pipelineProvisioning}' --output table 2>/dev/null | head -15

echo ""
echo "=== Services ==="
aws proton list-services --query 'services[*].{Name:name,Template:templateName,Status:status}' --output table 2>/dev/null | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash
SERVICE="${1:-}"
ENV="${2:-}"

if [ -n "$SERVICE" ]; then
  echo "=== Service Detail ==="
  aws proton get-service --name "$SERVICE" --query 'service.{Name:name,Status:status,Template:templateName,Version:templateMajorVersion,Pipeline:pipeline.status}' --output table 2>/dev/null

  echo ""
  echo "=== Service Instances ==="
  aws proton list-service-instances --service-name "$SERVICE" --query 'serviceInstances[*].{Name:name,Env:environmentName,Status:deploymentStatus}' --output table 2>/dev/null | head -15
fi

if [ -n "$ENV" ]; then
  echo ""
  echo "=== Environment Detail ==="
  aws proton get-environment --name "$ENV" --query 'environment.{Name:name,Status:deploymentStatus,Template:templateName,Provisioning:provisioning}' --output table 2>/dev/null

  echo ""
  echo "=== Environment Outputs ==="
  aws proton get-environment --name "$ENV" --query 'environment.spec' --output text 2>/dev/null | head -15
fi

echo ""
echo "=== Components ==="
aws proton list-components --query 'components[*].{Name:name,Service:serviceName,Env:environmentName,Status:deploymentStatus}' --output table 2>/dev/null | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Show template versions and deployment statuses
- Summarize service instances by environment
- List components with their parent service/environment

## Safety Rules
- **NEVER update production templates without testing in staging first**
- **Review template diffs** before publishing new versions
- **Check service instance status** before triggering updates
- **Validate template schemas** before registration
- **Monitor pipeline status** after deployments

## Output Format

Present results as a structured report:
```
Managing Aws Proton Report
══════════════════════════
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

