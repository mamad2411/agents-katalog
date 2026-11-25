---
name: managing-encore
description: |
  Use when working with Encore — encore cloud application platform management.
  Covers service architecture, API inspection, infrastructure provisioning,
  environment management, deployment history, and local development. Use when
  building backend applications with Encore, inspecting service APIs, managing
  environments, or reviewing deployment status.
connection_type: encore
preload: false
---

# Encore Management Skill

Manage Encore applications, inspect services, review deployments, and configure environments.

## MANDATORY: Discovery-First Pattern

**Always inspect Encore app structure and environment status before operations.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Encore Version ==="
encore version 2>/dev/null

echo ""
echo "=== App Config ==="
cat encore.app 2>/dev/null | head -10

echo ""
echo "=== Services ==="
find . -name "encore.service.ts" -o -name "encore.service.go" 2>/dev/null | head -15

echo ""
echo "=== API Endpoints ==="
grep -rn "//encore:api\|@api\|api\.NewEndpoint" --include="*.go" --include="*.ts" . 2>/dev/null | head -15

echo ""
echo "=== Environments ==="
encore env list 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
ENV="${1:-staging}"

echo "=== App Metadata ==="
encore app show 2>/dev/null | head -10

echo ""
echo "=== Service Diagram ==="
encore diagram 2>/dev/null | head -20

echo ""
echo "=== Deployment History ==="
encore deploy list --env "$ENV" 2>/dev/null | head -10

echo ""
echo "=== Infrastructure Resources ==="
encore infra list --env "$ENV" 2>/dev/null | head -15

echo ""
echo "=== Secrets ==="
encore secret list 2>/dev/null | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Show service topology and API endpoints concisely
- Summarize deployment history with status
- List infrastructure resources by type

## Safety Rules
- **NEVER deploy to production without reviewing changes**
- **Use `encore run`** for local development and testing
- **Review service dependencies** before deployments
- **Check environment configuration** matches target
- **Use Encore dashboard** for detailed observability

## Output Format

Present results as a structured report:
```
Managing Encore Report
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

