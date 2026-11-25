---
name: managing-crossplane
description: |
  Use when working with Crossplane — crossplane Kubernetes-native infrastructure
  management. Covers managed resources, compositions, provider configurations,
  composite resource definitions (XRDs), claims, and provider health. Use when
  managing Crossplane resources, debugging provisioning failures, inspecting
  compositions, or auditing cloud resource status.
connection_type: crossplane
preload: false
---

# Crossplane Management Skill

Manage and inspect Crossplane managed resources, compositions, and provider configurations.

## MANDATORY: Discovery-First Pattern

**Always check provider health and installed CRDs before managing resources.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Crossplane Version ==="
kubectl get deployment crossplane -n crossplane-system -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null
echo ""

echo ""
echo "=== Installed Providers ==="
kubectl get providers.pkg.crossplane.io 2>/dev/null || \
kubectl get providers 2>/dev/null

echo ""
echo "=== Provider Health ==="
kubectl get providers.pkg.crossplane.io -o custom-columns='NAME:.metadata.name,INSTALLED:.status.conditions[?(@.type=="Installed")].status,HEALTHY:.status.conditions[?(@.type=="Healthy")].status,PACKAGE:.spec.package' 2>/dev/null

echo ""
echo "=== Composite Resource Definitions ==="
kubectl get xrd 2>/dev/null | head -15

echo ""
echo "=== Compositions ==="
kubectl get compositions 2>/dev/null | head -15
```

## Core Helper Functions

```bash
#!/bin/bash

# Crossplane resource status helper
xp_status() {
    local kind="$1"
    local name="$2"
    kubectl get "$kind" "$name" -o jsonpath='{range .status.conditions[*]}{.type}={.status} ({.reason}: {.message}){"\n"}{end}' 2>/dev/null
}

# List all managed resources
xp_managed() {
    kubectl get managed 2>/dev/null | head -30
}

# Get composite resource details
xp_composite() {
    local kind="$1"
    local name="$2"
    kubectl get "$kind" "$name" -o yaml 2>/dev/null | head -50
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `-o custom-columns` for targeted field extraction
- Use `kubectl get managed` for cross-provider resource listing
- Never dump full YAML manifests -- extract status and key fields

## Common Operations

### Managed Resource Status

```bash
#!/bin/bash
echo "=== All Managed Resources ==="
kubectl get managed -o custom-columns='KIND:.kind,NAME:.metadata.name,READY:.status.conditions[?(@.type=="Ready")].status,SYNCED:.status.conditions[?(@.type=="Synced")].status,AGE:.metadata.creationTimestamp' 2>/dev/null | head -30

echo ""
echo "=== Not Ready Resources ==="
kubectl get managed -o json 2>/dev/null | jq -r '
    .items[] |
    select(.status.conditions[]? | select(.type == "Ready" and .status != "True")) |
    "\(.kind)/\(.metadata.name)\t\(.status.conditions[] | select(.type == "Ready") | .reason): \(.message // "no message")"
' | column -t | head -20
```

### Composition Debugging

```bash
#!/bin/bash
COMPOSITION="${1:?Composition name required}"

echo "=== Composition Details ==="
kubectl get composition "$COMPOSITION" -o json 2>/dev/null | jq '{
    name: .metadata.name,
    compositeTypeRef: .spec.compositeTypeRef,
    resourceCount: (.spec.resources | length),
    resources: [.spec.resources[] | {name: .name, base_kind: .base.kind, base_apiVersion: .base.apiVersion}]
}'

echo ""
echo "=== Composite Resources Using This Composition ==="
XR_KIND=$(kubectl get composition "$COMPOSITION" -o jsonpath='{.spec.compositeTypeRef.kind}' 2>/dev/null)
kubectl get "$XR_KIND" 2>/dev/null | head -15
```

### Provider Configuration

```bash
#!/bin/bash
echo "=== Provider Configs ==="
kubectl get providerconfigs --all-namespaces 2>/dev/null || \
kubectl get providerconfig.aws.crossplane.io,providerconfig.gcp.crossplane.io,providerconfig.azure.crossplane.io 2>/dev/null

echo ""
echo "=== Provider Revisions ==="
kubectl get providerrevisions.pkg.crossplane.io -o custom-columns='NAME:.metadata.name,HEALTHY:.status.conditions[?(@.type=="Healthy")].status,REVISION:.spec.revision,IMAGE:.spec.image' 2>/dev/null | head -15

echo ""
echo "=== Provider Logs (errors) ==="
for pod in $(kubectl get pods -n crossplane-system -l pkg.crossplane.io/revision -o name 2>/dev/null); do
    echo "--- $pod ---"
    kubectl logs "$pod" -n crossplane-system --tail=10 2>/dev/null | grep -i error | head -5
done
```

### Claims and XR Inspection

```bash
#!/bin/bash
echo "=== Claims (all namespaces) ==="
kubectl get claim --all-namespaces 2>/dev/null | head -20

echo ""
echo "=== Composite Resources ==="
for xrd in $(kubectl get xrd -o jsonpath='{.items[*].metadata.name}' 2>/dev/null); do
    KIND=$(kubectl get xrd "$xrd" -o jsonpath='{.spec.names.kind}' 2>/dev/null)
    echo "--- $KIND ---"
    kubectl get "$KIND" 2>/dev/null | head -5
done
```

### Resource Events and Troubleshooting

```bash
#!/bin/bash
RESOURCE_KIND="${1:?Resource kind required}"
RESOURCE_NAME="${2:?Resource name required}"

echo "=== Resource Status ==="
kubectl get "$RESOURCE_KIND" "$RESOURCE_NAME" -o json 2>/dev/null | jq '{
    ready: (.status.conditions[] | select(.type == "Ready") | {status, reason, message}),
    synced: (.status.conditions[] | select(.type == "Synced") | {status, reason, message}),
    externalName: .metadata.annotations["crossplane.io/external-name"]
}'

echo ""
echo "=== Events ==="
kubectl describe "$RESOURCE_KIND" "$RESOURCE_NAME" 2>/dev/null | grep -A 20 "^Events:" | head -20
```

## Safety Rules

- **NEVER delete managed resources without understanding cascading effects** -- deleting XRs deletes all composed resources
- **Check provider credentials** before assuming resource provisioning failures are config issues
- **Use `deletionPolicy: Orphan`** on managed resources you want to keep when removing from Crossplane
- **Review compositions carefully** -- patches can silently override user-provided values
- **Test compositions in dev** before applying to production claims

## Output Format

Present results as a structured report:
```
Managing Crossplane Report
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

## Common Pitfalls

- **Provider not healthy**: Most common issue -- check provider pod logs in crossplane-system namespace
- **Credential rotation**: Expired cloud credentials cause all managed resources to show Synced=False
- **XRD version changes**: Updating XRD served versions can break existing claims -- use conversion webhooks
- **Composition selection**: Multiple compositions matching same XRD -- use `compositionSelector` labels
- **External name conflicts**: Two managed resources with same external name cause cloud-side conflicts
- **Finalizer stuck**: Deleting resources with failing providers hangs -- may need to remove finalizers manually
- **Rate limiting**: Cloud provider API rate limits can cause intermittent Synced=False across many resources
- **Observe-only resources**: Use `managementPolicies: ["Observe"]` to import existing resources without managing them
