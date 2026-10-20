---
name: managing-k8s-flux-deep
description: |
  Use when working with K8S Flux Deep — flux CD deep-dive management for
  Kubernetes GitOps delivery. Covers GitRepository sources, Kustomization
  reconciliation, HelmRelease status, HelmRepository health, ImagePolicy
  automation, notification providers, and multi-tenancy configurations. Use when
  debugging reconciliation failures, analyzing Flux source health, reviewing
  Helm release drift, or auditing image automation pipelines.
connection_type: k8s
preload: false
---

# Flux CD Deep-Dive Skill

Advanced analysis of Flux CD GitOps sources, reconciliation, and deployment pipelines.

## MANDATORY: Discovery-First Pattern

**Always check Flux installation and source health before inspecting reconciliation.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Flux Components ==="
kubectl get deployment -n flux-system -o custom-columns='NAME:.metadata.name,READY:.status.readyReplicas,IMAGE:.spec.template.spec.containers[0].image' 2>/dev/null

echo ""
echo "=== Flux Version ==="
kubectl get deployment source-controller -n flux-system -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null
echo ""

echo ""
echo "=== GitRepositories ==="
kubectl get gitrepositories --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,READY:.status.conditions[?(@.type=="Ready")].status,REVISION:.status.artifact.revision,AGE:.metadata.creationTimestamp' 2>/dev/null | head -15

echo ""
echo "=== HelmRepositories ==="
kubectl get helmrepositories --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,READY:.status.conditions[?(@.type=="Ready")].status,URL:.spec.url' 2>/dev/null | head -15

echo ""
echo "=== OCIRepositories ==="
kubectl get ocirepositories --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,READY:.status.conditions[?(@.type=="Ready")].status' 2>/dev/null | head -10

echo ""
echo "=== Kustomizations ==="
kubectl get kustomizations --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,READY:.status.conditions[?(@.type=="Ready")].status,REVISION:.status.lastAppliedRevision' 2>/dev/null | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== HelmReleases ==="
kubectl get helmreleases --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,READY:.status.conditions[?(@.type=="Ready")].status,CHART:.spec.chart.spec.chart,VERSION:.spec.chart.spec.version' 2>/dev/null | head -15

echo ""
echo "=== Failed Reconciliations ==="
kubectl get kustomizations,helmreleases --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] |
  select(.status.conditions[]? | select(.type == "Ready" and .status != "True")) |
  "\(.kind)/\(.metadata.name)\t\(.status.conditions[] | select(.type == "Ready") | .reason): \(.message // "")[0:80]"
' | head -15

echo ""
echo "=== Source Errors ==="
kubectl get gitrepositories,helmrepositories --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] |
  select(.status.conditions[]? | select(.type == "Ready" and .status != "True")) |
  "\(.kind)/\(.metadata.name)\t\(.status.conditions[] | select(.type == "Ready") | .message // "unknown")[0:80]"
' | head -10

echo ""
echo "=== Image Policies ==="
kubectl get imagepolicies --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,LATEST:.status.latestImage' 2>/dev/null | head -10

echo ""
echo "=== Image Update Automations ==="
kubectl get imageupdateautomations --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,LAST_RUN:.status.lastAutomationRunTime' 2>/dev/null | head -10

echo ""
echo "=== Notification Providers ==="
kubectl get providers --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,TYPE:.spec.type' 2>/dev/null | head -10

echo ""
echo "=== Alerts ==="
kubectl get alerts --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,SEVERITY:.spec.summary' 2>/dev/null | head -10

echo ""
echo "=== Suspended Resources ==="
kubectl get kustomizations,helmreleases --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] | select(.spec.suspend == true) |
  "\(.kind)/\(.metadata.namespace)/\(.metadata.name)\tSUSPENDED"
'

echo ""
echo "=== Source Controller Logs (errors) ==="
kubectl logs deployment/source-controller -n flux-system --tail=15 2>/dev/null | grep -i "error\|fail" | head -5
```

## Output Format

- Target ≤50 lines per output
- Use `-o custom-columns` for CRD resource listings
- Show Ready status and last applied revision for quick health check
- Group HelmReleases by namespace for organized view
- Never dump full Kustomization patches -- show source ref and status only

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

- **Dependency ordering**: Kustomizations support `dependsOn` -- circular dependencies cause deadlocks
- **Suspend flag**: `spec.suspend: true` stops reconciliation -- check before assuming failures
- **Source interval**: `spec.interval` controls how often sources are checked -- too frequent causes rate limits
- **HelmRelease remediation**: `spec.install.remediation` and `spec.upgrade.remediation` control retry behavior
- **Drift detection**: Enable `spec.force` on Kustomizations to correct drift -- but may cause disruption
- **Multi-tenancy**: Use `spec.serviceAccountName` on Kustomizations for RBAC scoping per tenant
- **Image automation**: Requires image-reflector and image-automation controllers -- not installed by default
- **Prune**: `spec.prune: true` on Kustomizations deletes resources removed from Git -- use with caution
- **Health checks**: Custom health checks in Kustomizations can delay Ready status -- check `spec.healthChecks`
