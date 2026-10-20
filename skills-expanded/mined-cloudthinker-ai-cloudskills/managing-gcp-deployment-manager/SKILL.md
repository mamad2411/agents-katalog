---
name: managing-gcp-deployment-manager
description: |
  Use when working with Gcp Deployment Manager — gCP Deployment Manager template
  and deployment management. Covers deployment creation, template validation,
  resource inspection, manifest review, deployment updates, and type provider
  management. Use when deploying GCP resources via Deployment Manager, reviewing
  deployment status, inspecting manifests, or troubleshooting failed
  deployments.
connection_type: gcp-deployment-manager
preload: false
---

# GCP Deployment Manager Management Skill

Manage GCP Deployment Manager deployments, templates, manifests, and type providers.

## MANDATORY: Discovery-First Pattern

**Always inspect existing deployments and project status before operations.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Current Project ==="
gcloud config get-value project 2>/dev/null

echo ""
echo "=== Deployments ==="
gcloud deployment-manager deployments list --format='table(name,operation.status,insertTime)' 2>/dev/null | head -15

echo ""
echo "=== Available Types ==="
gcloud deployment-manager types list --format='table(name)' 2>/dev/null | head -15

echo ""
echo "=== Composite Types ==="
gcloud deployment-manager type-providers list --format='table(name,insertTime)' 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
DEPLOYMENT="${1:?Deployment name required}"

echo "=== Deployment Resources ==="
gcloud deployment-manager deployments describe "$DEPLOYMENT" --format='table(resources[].name, resources[].type, resources[].update.state)' 2>/dev/null | head -20

echo ""
echo "=== Deployment Manifest ==="
MANIFEST=$(gcloud deployment-manager deployments describe "$DEPLOYMENT" --format='value(deployment.manifest)' 2>/dev/null | sed 's|.*/||')
gcloud deployment-manager manifests describe "$MANIFEST" --deployment "$DEPLOYMENT" --format='value(layout)' 2>/dev/null | head -25

echo ""
echo "=== Deployment Errors ==="
gcloud deployment-manager deployments describe "$DEPLOYMENT" --format='table(resources[].update.error.errors[].code, resources[].update.error.errors[].message)' 2>/dev/null | head -10

echo ""
echo "=== Preview (dry-run) ==="
TEMPLATE="${2:-}"
if [ -n "$TEMPLATE" ]; then
  gcloud deployment-manager deployments update "$DEPLOYMENT" --config "$TEMPLATE" --preview 2>&1 | tail -15
fi
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Show resource types and statuses, not full manifests
- Summarize deployment operations concisely
- Highlight errors and warnings

## Safety Rules
- **NEVER delete deployments without explicit confirmation**
- **Always use `--preview`** before applying updates
- **Review manifest changes** before confirming updates
- **Check resource dependencies** before deletion
- **Use `--delete-policy ABANDON`** to preserve resources when removing deployments

## Output Format

Present results as a structured report:
```
Managing Gcp Deployment Manager Report
══════════════════════════════════════
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

