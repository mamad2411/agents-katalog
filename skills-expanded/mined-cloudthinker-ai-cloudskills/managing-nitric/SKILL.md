---
name: managing-nitric
description: |
  Use when working with Nitric — nitric cloud application framework management.
  Covers service definition, local development, deployment to AWS/Azure/GCP,
  resource inspection, stack management, and provider configuration. Use when
  building cloud applications with Nitric, deploying services, managing stacks,
  or debugging resource bindings.
connection_type: nitric
preload: false
---

# Nitric Management Skill

Manage Nitric applications, deploy services, inspect resources, and configure cloud providers.

## MANDATORY: Discovery-First Pattern

**Always inspect Nitric project structure and stack configuration before deploying.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Nitric Version ==="
nitric version 2>/dev/null

echo ""
echo "=== Project Config ==="
cat nitric.yaml 2>/dev/null | head -15

echo ""
echo "=== Services ==="
ls services/ 2>/dev/null || ls functions/ 2>/dev/null | head -10

echo ""
echo "=== Stacks ==="
nitric stack list 2>/dev/null | head -10

echo ""
echo "=== Stack Files ==="
ls nitric-*.yaml 2>/dev/null || ls nitric.*.yaml 2>/dev/null
```

### Phase 2: Analysis

```bash
#!/bin/bash
STACK="${1:-dev}"

echo "=== Stack Config ==="
cat "nitric-${STACK}.yaml" 2>/dev/null || cat "nitric.${STACK}.yaml" 2>/dev/null | head -20

echo ""
echo "=== Resource Declarations ==="
grep -rn "nitric\.\(api\|bucket\|topic\|queue\|secret\|schedule\|websocket\)" --include="*.ts" --include="*.py" --include="*.go" . 2>/dev/null | head -20

echo ""
echo "=== Deployment Status ==="
nitric stack up --stack "$STACK" --dry-run 2>&1 | tail -20

echo ""
echo "=== Deployed Resources ==="
nitric stack describe --stack "$STACK" 2>/dev/null | head -15
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Show resource declarations, not full service code
- Summarize stack configuration concisely
- List services with their resource bindings

## Safety Rules
- **NEVER run `nitric stack up` without `--dry-run` first**
- **Use `nitric start`** for local development and testing
- **Review resource permissions** before deploying
- **Check provider configuration** matches target cloud
- **Confirm stack name** before deployment to avoid wrong-environment deploys

## Output Format

Present results as a structured report:
```
Managing Nitric Report
══════════════════════
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

