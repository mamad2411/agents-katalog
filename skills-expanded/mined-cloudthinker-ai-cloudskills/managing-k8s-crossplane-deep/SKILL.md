---
name: managing-k8s-crossplane-deep
description: |
  Use when working with K8S Crossplane Deep — crossplane deep-dive management
  for Kubernetes-native infrastructure provisioning. Covers provider health
  diagnostics, composition debugging, XRD schema validation, claim lifecycle
  analysis, managed resource drift detection, usage tracking, and
  EnvironmentConfig management. Use when debugging complex composition failures,
  analyzing cross-provider resource dependencies, or optimizing Crossplane
  performance.
connection_type: k8s
preload: false
---

# Crossplane Deep-Dive Skill

Advanced analysis of Crossplane compositions, provider internals, and infrastructure reconciliation.

## MANDATORY: Discovery-First Pattern

**Always check provider health and installed XRDs before deep-diving into resources.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Crossplane Core ==="
kubectl get deployment crossplane -n crossplane-system -o custom-columns='NAME:.metadata.name,READY:.status.readyReplicas,IMAGE:.spec.template.spec.containers[0].image' 2>/dev/null

echo ""
echo "=== RBAC Manager ==="
kubectl get deployment crossplane-rbac-manager -n crossplane-system -o custom-columns='NAME:.metadata.name,READY:.status.readyReplicas' 2>/dev/null

echo ""
echo "=== Provider Health ==="
kubectl get providers.pkg.crossplane.io -o custom-columns='NAME:.metadata.name,INSTALLED:.status.conditions[?(@.type=="Installed")].status,HEALTHY:.status.conditions[?(@.type=="Healthy")].status,PACKAGE:.spec.package,REVISION:.status.currentRevision' 2>/dev/null

echo ""
echo "=== Functions ==="
kubectl get functions.pkg.crossplane.io -o custom-columns='NAME:.metadata.name,INSTALLED:.status.conditions[?(@.type=="Installed")].status,HEALTHY:.status.conditions[?(@.type=="Healthy")].status,PACKAGE:.spec.package' 2>/dev/null

echo ""
echo "=== XRDs ==="
kubectl get xrd -o custom-columns='NAME:.metadata.name,ESTABLISHED:.status.conditions[?(@.type=="Established")].status,OFFERED:.status.conditions[?(@.type=="Offered")].status,GROUP:.spec.group' 2>/dev/null

echo ""
echo "=== Compositions ==="
kubectl get compositions -o custom-columns='NAME:.metadata.name,XR-KIND:.spec.compositeTypeRef.kind,RESOURCES:.spec.resources' 2>/dev/null | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Managed Resources Not Ready ==="
kubectl get managed -o json 2>/dev/null | jq -r '
  .items[] |
  select(.status.conditions[]? | select(.type == "Ready" and .status != "True")) |
  "\(.kind)/\(.metadata.name)\tReady:\(.status.conditions[] | select(.type == "Ready") | "\(.status) \(.reason)")\tSynced:\(.status.conditions[] | select(.type == "Synced") | .status)"
' | head -20

echo ""
echo "=== Stale Resources (Synced=False) ==="
kubectl get managed -o json 2>/dev/null | jq -r '
  .items[] |
  select(.status.conditions[]? | select(.type == "Synced" and .status != "True")) |
  "\(.kind)/\(.metadata.name)\t\(.status.conditions[] | select(.type == "Synced") | .reason): \(.message // "no message")[0:80]"
' | head -15

echo ""
echo "=== Composite Resources ==="
for xrd in $(kubectl get xrd -o jsonpath='{.items[*].metadata.name}' 2>/dev/null); do
  KIND=$(kubectl get xrd "$xrd" -o jsonpath='{.spec.names.kind}' 2>/dev/null)
  kubectl get "$KIND" -o custom-columns="KIND:.kind,NAME:.metadata.name,READY:.status.conditions[?(@.type==\"Ready\")].status,COMPOSITION:.spec.compositionRef.name" 2>/dev/null | tail -n +2
done | head -15

echo ""
echo "=== Claims (all namespaces) ==="
kubectl get claim --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,KIND:.kind,NAME:.metadata.name,READY:.status.conditions[?(@.type=="Ready")].status' 2>/dev/null | head -15

echo ""
echo "=== Provider Config Health ==="
for provider in $(kubectl get providers.pkg.crossplane.io -o jsonpath='{.items[*].metadata.name}' 2>/dev/null); do
  kubectl get providerconfigs -l pkg.crossplane.io/package="$provider" 2>/dev/null | head -5
done

echo ""
echo "=== EnvironmentConfigs ==="
kubectl get environmentconfigs -o custom-columns='NAME:.metadata.name,AGE:.metadata.creationTimestamp' 2>/dev/null

echo ""
echo "=== Usages (dependency tracking) ==="
kubectl get usages -o custom-columns='NAME:.metadata.name,OF:.spec.of.kind,BY:.spec.by.kind' 2>/dev/null | head -10

echo ""
echo "=== Provider Pod Errors ==="
for pod in $(kubectl get pods -n crossplane-system -l pkg.crossplane.io/revision -o name 2>/dev/null); do
  echo "--- $pod ---"
  kubectl logs "$pod" -n crossplane-system --tail=5 2>/dev/null | grep -i "error\|cannot\|fail" | head -3
done
```

## Output Format

- Target ≤50 lines per output
- Use `-o custom-columns` and jq for CRD field extraction
- Show Ready/Synced conditions prominently for all resources
- Group managed resources by provider/kind when many exist
- Never dump full composition YAML -- show compositeTypeRef and resource count

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

- **Provider vs ProviderConfig**: Provider is the package; ProviderConfig holds credentials -- both must be healthy
- **Composition selection**: Multiple compositions can match an XR -- use `compositionSelector` or `compositionRef` for determinism
- **Patch types**: FromCompositeFieldPath, ToCompositeFieldPath, CombineFromComposite -- wrong patch type causes silent failures
- **Finalizer blocking**: Deleting XRs deletes all composed resources -- stuck finalizers indicate provider issues
- **Management policies**: ObserveOnly, OrphanOnDelete -- understand lifecycle implications before changing
- **Functions pipeline**: Crossplane Functions (v1.14+) replace patch-and-transform -- check if compositions use pipeline mode
- **DeploymentRuntimeConfig**: Controls provider pod resources, replicas, and node selectors
- **Dependency ordering**: Use `readinessChecks` and Usages to handle resource dependencies
