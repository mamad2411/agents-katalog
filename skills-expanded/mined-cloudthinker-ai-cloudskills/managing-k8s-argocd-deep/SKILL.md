---
name: managing-k8s-argocd-deep
description: |
  Use when working with K8S Argocd Deep — argoCD deep-dive management for
  advanced GitOps operations. Covers ApplicationSet controllers, multi-cluster
  sync strategies, notification configurations, resource hook analysis, sync
  wave ordering, application health aggregation, image updater integration, and
  RBAC policy auditing. Use when debugging complex sync failures, analyzing
  multi-cluster deployments, or optimizing ArgoCD performance at scale.
connection_type: k8s
preload: false
---

# ArgoCD Deep-Dive Skill

Advanced analysis of ArgoCD GitOps deployments, ApplicationSets, and multi-cluster management.

## MANDATORY: Discovery-First Pattern

**Always check ArgoCD component health and application inventory before deep-diving.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== ArgoCD Components ==="
kubectl get deployment -n argocd -o custom-columns='NAME:.metadata.name,READY:.status.readyReplicas,IMAGE:.spec.template.spec.containers[0].image' 2>/dev/null

echo ""
echo "=== ArgoCD Server Version ==="
kubectl get configmap argocd-cm -n argocd -o jsonpath='{.metadata.labels.app\.kubernetes\.io/version}' 2>/dev/null
echo ""

echo ""
echo "=== Applications Summary ==="
kubectl get applications -n argocd -o custom-columns='NAME:.metadata.name,SYNC:.status.sync.status,HEALTH:.status.health.status,DEST-NS:.spec.destination.namespace,PROJECT:.spec.project' 2>/dev/null | head -20

echo ""
echo "=== ApplicationSets ==="
kubectl get applicationsets -n argocd -o custom-columns='NAME:.metadata.name,GENERATORS:.spec.generators[*]' 2>/dev/null | head -15

echo ""
echo "=== AppProjects ==="
kubectl get appprojects -n argocd -o custom-columns='NAME:.metadata.name,SOURCE-REPOS:.spec.sourceRepos[0],DESTINATIONS:.spec.destinations[*].namespace' 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Unhealthy Applications ==="
kubectl get applications -n argocd -o json 2>/dev/null | jq -r '
  .items[] |
  select(.status.health.status != "Healthy" or .status.sync.status != "Synced") |
  "\(.metadata.name)\tSync:\(.status.sync.status)\tHealth:\(.status.health.status)"
' | head -15

echo ""
echo "=== Sync Errors ==="
kubectl get applications -n argocd -o json 2>/dev/null | jq -r '
  .items[] |
  select(.status.conditions != null) |
  .status.conditions[] |
  "\(.type)\t\(.message[0:100])"
' | head -15

echo ""
echo "=== Resource Hooks ==="
kubectl get applications -n argocd -o json 2>/dev/null | jq -r '
  .items[] |
  select(.status.operationState.syncResult.resources != null) |
  .status.operationState.syncResult.resources[] |
  select(.hook == true) |
  "\(.kind)/\(.name)\tPhase:\(.hookPhase)\tStatus:\(.status)"
' | head -10

echo ""
echo "=== ApplicationSet Generator Status ==="
kubectl get applicationsets -n argocd -o json 2>/dev/null | jq -r '
  .items[] |
  "\(.metadata.name)\tGenerators:\([.spec.generators[].type // keys[0]] | join(","))\tApps:\(.status.conditions[0].message // "unknown")"
' | head -10

echo ""
echo "=== Image Updater (if installed) ==="
kubectl get deployment argocd-image-updater -n argocd -o custom-columns='NAME:.metadata.name,READY:.status.readyReplicas' 2>/dev/null
kubectl get applications -n argocd -o json 2>/dev/null | jq -r '
  .items[] |
  select(.metadata.annotations["argocd-image-updater.argoproj.io/image-list"] // "" != "") |
  "\(.metadata.name)\tImages:\(.metadata.annotations["argocd-image-updater.argoproj.io/image-list"])"
' | head -10

echo ""
echo "=== Notifications Config ==="
kubectl get configmap argocd-notifications-cm -n argocd -o jsonpath='{.data}' 2>/dev/null | jq -r 'keys[]' | head -10

echo ""
echo "=== RBAC Policies ==="
kubectl get configmap argocd-rbac-cm -n argocd -o jsonpath='{.data.policy\.csv}' 2>/dev/null | head -10

echo ""
echo "=== Controller Logs (errors) ==="
kubectl logs deployment/argocd-application-controller -n argocd --tail=20 2>/dev/null | grep -i "error\|fail" | head -10
```

## Output Format

- Target ≤50 lines per output
- Use `-o custom-columns` for Application listings
- Show sync/health status matrix for quick overview
- Aggregate ApplicationSet-generated apps by set name
- Never dump full Application manifests -- show status and source references only

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

- **Sync waves**: Resources with `argocd.argoproj.io/sync-wave` are applied in order -- failed early waves block later ones
- **ApplicationSet generators**: Git, List, Cluster, Matrix, Merge generators have different refresh behaviors
- **Resource tracking**: `argocd.argoproj.io/tracking-method` annotation controls label vs annotation tracking
- **Diff customization**: `ignoreDifferences` in Application spec prevents false OutOfSync on dynamic fields
- **Server-side apply**: Enable for large resources or CRDs that exceed client-side apply limits
- **Sharding**: Large installations need controller sharding -- check `--application-controller-shard` settings
- **Notification templates**: Template errors silently fail -- test with `argocd admin notifications` CLI
- **Image updater**: Writes back to Git or uses parameter overrides -- check write-back method configuration
- **Orphaned resources**: Enabled via AppProject `orphanedResources` -- can cause unexpected warnings
