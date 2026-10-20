---
name: managing-external-secrets
description: |
  Use when working with External Secrets — external Secrets Operator management.
  Covers secret syncing from external providers, SecretStore configuration,
  ExternalSecret resource management, push secrets, ClusterSecretStore setup,
  and provider troubleshooting. Use when managing secret synchronization between
  external vaults and Kubernetes, debugging sync failures, or configuring secret
  providers.
connection_type: external-secrets
preload: false
---

# External Secrets Operator Management Skill

Manage and inspect External Secrets Operator resources, secret stores, and sync status.

## MANDATORY: Discovery-First Pattern

**Always check operator status and secret stores before managing external secrets.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== ESO Version ==="
kubectl get deployment external-secrets -n external-secrets \
    -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null
echo ""

echo ""
echo "=== ESO Pods ==="
kubectl get pods -n external-secrets 2>/dev/null

echo ""
echo "=== Cluster Secret Stores ==="
kubectl get clustersecretstores 2>/dev/null

echo ""
echo "=== Namespaced Secret Stores ==="
kubectl get secretstores --all-namespaces 2>/dev/null | head -10

echo ""
echo "=== External Secrets Summary ==="
kubectl get externalsecrets --all-namespaces --no-headers 2>/dev/null | wc -l | xargs -I{} echo "{} external secrets configured"
```

## Core Helper Functions

```bash
#!/bin/bash

# ESO resource status check
eso_status() {
    local kind="$1"
    local name="$2"
    local ns="${3:-}"
    if [ -n "$ns" ]; then
        kubectl get "$kind" "$name" -n "$ns" -o jsonpath='{range .status.conditions[*]}{.type}={.status} ({.reason}: {.message}){"\n"}{end}' 2>/dev/null
    else
        kubectl get "$kind" "$name" -o jsonpath='{range .status.conditions[*]}{.type}={.status} ({.reason}: {.message}){"\n"}{end}' 2>/dev/null
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `-o json` with jq for resource inspection
- Focus on sync status conditions for troubleshooting
- Never dump synced secret values -- show metadata and status only

## Common Operations

### Secret Store Health

```bash
#!/bin/bash
echo "=== Cluster Secret Store Status ==="
kubectl get clustersecretstores -o json 2>/dev/null | jq '.items[] | {
    name: .metadata.name,
    provider: (.spec.provider | keys[0]),
    ready: (.status.conditions[]? | select(.type == "Ready") | {status, reason, message})
}'

echo ""
echo "=== Namespaced Secret Stores ==="
kubectl get secretstores -A -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.namespace)/\(.metadata.name)\t\(.spec.provider | keys[0])\t\(.status.conditions[]? | select(.type == "Ready") | .status)"
' | column -t | head -15
```

### External Secret Sync Status

```bash
#!/bin/bash
NAMESPACE="${1:-}"

echo "=== External Secret Status ==="
if [ -n "$NAMESPACE" ]; then
    kubectl get externalsecrets -n "$NAMESPACE" -o json 2>/dev/null
else
    kubectl get externalsecrets -A -o json 2>/dev/null
fi | jq -r '
    .items[] | "\(.metadata.namespace)/\(.metadata.name)\t\(.status.conditions[]? | select(.type == "Ready") | .status)\t\(.status.refreshTime // "never")\t\(.spec.secretStoreRef.name)"
' | column -t | head -20

echo ""
echo "=== Failed Syncs ==="
kubectl get externalsecrets -A -o json 2>/dev/null | jq '
    [.items[] |
    select(.status.conditions[]? | select(.type == "Ready" and .status != "True")) |
    {
        namespace: .metadata.namespace,
        name: .metadata.name,
        store: .spec.secretStoreRef.name,
        error: (.status.conditions[] | select(.type == "Ready") | .message)
    }]
' | head -30
```

### Secret Data Mapping Inspection

```bash
#!/bin/bash
ES_NAME="${1:?ExternalSecret name required}"
NAMESPACE="${2:-default}"

echo "=== ExternalSecret: $ES_NAME ==="
kubectl get externalsecret "$ES_NAME" -n "$NAMESPACE" -o json 2>/dev/null | jq '{
    name: .metadata.name,
    store: .spec.secretStoreRef,
    target: {
        name: .spec.target.name,
        creation_policy: .spec.target.creationPolicy,
        deletion_policy: .spec.target.deletionPolicy
    },
    data_mappings: [.spec.data[]? | {
        secret_key: .secretKey,
        remote_ref: .remoteRef
    }],
    data_from: .spec.dataFrom,
    refresh_interval: .spec.refreshInterval,
    status: (.status.conditions[]? | select(.type == "Ready") | {status, reason, message})
}'
```

### Push Secret Management

```bash
#!/bin/bash
echo "=== Push Secrets ==="
kubectl get pushsecrets --all-namespaces 2>/dev/null | head -15

echo ""
echo "=== Push Secret Details ==="
kubectl get pushsecrets -A -o json 2>/dev/null | jq '.items[] | {
    namespace: .metadata.namespace,
    name: .metadata.name,
    store: .spec.secretStoreRefs,
    selector: .spec.selector,
    status: (.status.conditions[]? | select(.type == "Ready") | {status, reason})
}' | head -30
```

### Provider Troubleshooting

```bash
#!/bin/bash
STORE_NAME="${1:?SecretStore name required}"
STORE_KIND="${2:-ClusterSecretStore}"

echo "=== Store Details: $STORE_NAME ==="
kubectl get "$STORE_KIND" "$STORE_NAME" -o json 2>/dev/null | jq '{
    name: .metadata.name,
    provider: (.spec.provider | keys[0]),
    provider_config: (.spec.provider | to_entries[0].value | del(.auth)),
    conditions: .status.conditions
}'

echo ""
echo "=== ESO Controller Logs ==="
kubectl logs -n external-secrets deployment/external-secrets --tail=20 2>/dev/null | \
    grep -iE "(error|warn|$STORE_NAME)" | head -10

echo ""
echo "=== Events ==="
kubectl get events -n external-secrets --sort-by='.lastTimestamp' 2>/dev/null | tail -10
```

## Safety Rules

- **Never expose secret values in logs or output** -- only inspect metadata and sync status
- **Deletion policy defaults to `Retain`** -- changing to `Delete` removes K8s secrets when ExternalSecret is deleted
- **SecretStore credentials** need minimum required permissions in the external provider
- **Test new SecretStore configs** with a non-critical secret before migrating all secrets
- **Push secrets write to external stores** -- ensure permissions and naming are correct to avoid overwriting

## Output Format

Present results as a structured report:
```
Managing External Secrets Report
════════════════════════════════
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

- **Auth credential rotation**: If SecretStore auth credentials expire, all ExternalSecrets using it fail
- **Refresh interval**: Too-short intervals can hit provider API rate limits -- default 1h is usually fine
- **Provider-specific formats**: Secret paths/keys differ between providers (AWS SM, Vault, GCP SM, Azure KV)
- **Immutable secrets**: If target secret is immutable, ESO cannot update it -- delete and recreate
- **Namespace isolation**: SecretStore is namespace-scoped; ClusterSecretStore is cluster-wide -- choose carefully
- **Template rendering**: ESO templates use Go templating -- syntax errors cause silent failures
- **Ownership conflicts**: Multiple ExternalSecrets targeting the same K8s Secret cause conflicts
- **RBAC requirements**: ESO needs permissions to create/update Secrets in target namespaces
