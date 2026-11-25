---
name: managing-aws-sam
description: |
  Use when working with Aws Sam — aWS Serverless Application Model (SAM)
  management. Covers template validation, local testing, build and packaging,
  deployment orchestration, stack inspection, log tailing, and API Gateway
  debugging. Use when building serverless applications with SAM, testing
  locally, deploying Lambda functions, or troubleshooting API Gateway endpoints.
connection_type: aws-sam
preload: false
---

# AWS SAM Management Skill

Manage AWS SAM applications, build and deploy serverless stacks, test locally, and inspect deployments.

## MANDATORY: Discovery-First Pattern

**Always validate templates and check deployment status before operations.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== SAM Version ==="
sam --version 2>/dev/null

echo ""
echo "=== Template Validation ==="
sam validate 2>&1 | head -5

echo ""
echo "=== Template Resources ==="
if [ -f template.yaml ]; then
  grep "Type: AWS::" template.yaml | sort | uniq -c | sort -rn | head -15
elif [ -f template.yml ]; then
  grep "Type: AWS::" template.yml | sort | uniq -c | sort -rn | head -15
fi

echo ""
echo "=== Functions ==="
sam list resources --output json 2>/dev/null | jq -r '.[] | select(.LogicalResourceId | test("Function|Lambda")) | "\(.LogicalResourceId) | \(.PhysicalResourceId)"' 2>/dev/null | head -10

echo ""
echo "=== Deployed Endpoints ==="
sam list endpoints --output json 2>/dev/null | jq -r '.[] | "\(.LogicalResourceId) | \(.PhysicalResourceId)"' | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
STACK="${1:-}"
FUNCTION="${2:-}"

echo "=== Stack Status ==="
sam list resources ${STACK:+--stack-name "$STACK"} --output json 2>/dev/null | jq -r '.[] | "\(.LogicalResourceId) | \(.ResourceType) | \(.ResourceStatus)"' | head -20

echo ""
echo "=== Build ==="
sam build 2>&1 | tail -10

echo ""
if [ -n "$FUNCTION" ]; then
  echo "=== Function Logs (last 5 min) ==="
  sam logs -n "$FUNCTION" ${STACK:+--stack-name "$STACK"} --start-time "5min ago" 2>/dev/null | tail -20
fi

echo ""
echo "=== Stack Outputs ==="
aws cloudformation describe-stacks ${STACK:+--stack-name "$STACK"} --query 'Stacks[0].Outputs[*].{Key:OutputKey,Value:OutputValue}' --output table 2>/dev/null | head -15
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Summarize function counts and resource types
- Tail logs with time filters to avoid flooding
- Show endpoints and outputs, not full template dumps

## Safety Rules
- **NEVER deploy without `sam validate` and `sam build` first**
- **Use `sam deploy --guided`** for first-time deployments
- **Test locally with `sam local invoke`** before deploying
- **Review changeset** before confirming deployment
- **Use `--no-execute-changeset`** for dry-run deployments

## Output Format

Present results as a structured report:
```
Managing Aws Sam Report
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

