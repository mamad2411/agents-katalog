---
name: managing-k8s-sealed-secrets
description: |
  Use when working with K8S Sealed Secrets — sealed Secrets management for
  Kubernetes secret encryption. Covers SealedSecret resources, controller
  health, certificate rotation, key management, decryption status, and secret
  synchronization. Use when auditing encrypted secrets, debugging decryption
  failures, reviewing key rotation, or troubleshooting SealedSecret controller
  issues.
connection_type: k8s
preload: false
---

# Sealed Secrets Management Skill

Manage and analyze Bitnami Sealed Secrets controller, encryption keys, and sealed secret resources.

## MANDATORY: Discovery-First Pattern

**Always check controller health and active keys before inspecting sealed secrets.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Sealed Secrets Controller ==="
kubectl get deployment sealed-secrets-controller -n kube-system -o custom-columns='NAME:.metadata.name,READY:.status.readyReplicas,IMAGE:.spec.template.spec.containers[0].image' 2>/dev/null
# Try alternative namespace
kubectl get deployment -l app.kubernetes.io/name=sealed-secrets --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,READY:.status.readyReplicas,IMAGE:.spec.template.spec.containers[0].image' 2>/dev/null

echo ""
echo "=== Controller Pod ==="
kubectl get pods -l app.kubernetes.io/name=sealed-secrets --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,STATUS:.status.phase,RESTARTS:.status.containerStatuses[0].restartCount' 2>/dev/null

echo ""
echo "=== Sealing Keys ==="
kubectl get secrets -n kube-system -l sealedsecrets.bitnami.com/sealed-secrets-key=active -o custom-columns='NAME:.metadata.name,CREATED:.metadata.creationTimestamp' 2>/dev/null

echo ""
echo "=== SealedSecrets (all namespaces) ==="
kubectl get sealedsecrets --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,AGE:.metadata.creationTimestamp' 2>/dev/null | head -20
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== SealedSecret Status ==="
kubectl get sealedsecrets --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] |
  "\(.metadata.namespace)/\(.metadata.name)\tSynced:\(.status.conditions[]? | select(.type == "Synced") | .status // "unknown")"
' | head -20

echo ""
echo "=== Failed Decryptions ==="
kubectl get sealedsecrets --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] |
  select(.status.conditions[]? | select(.type == "Synced" and .status != "True")) |
  "\(.metadata.namespace)/\(.metadata.name)\t\(.status.conditions[] | select(.type == "Synced") | .message // "unknown error")"
' | head -10

echo ""
echo "=== Corresponding Secrets ==="
for ns_name in $(kubectl get sealedsecrets --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}/{.metadata.name}{"\n"}{end}' 2>/dev/null | head -15); do
  ns=$(echo "$ns_name" | cut -d/ -f1)
  name=$(echo "$ns_name" | cut -d/ -f2)
  exists=$(kubectl get secret "$name" -n "$ns" -o name 2>/dev/null)
  if [ -z "$exists" ]; then
    echo "MISSING: $ns/$name"
  else
    echo "OK: $ns/$name"
  fi
done

echo ""
echo "=== Key Rotation History ==="
kubectl get secrets -n kube-system -l sealedsecrets.bitnami.com/sealed-secrets-key -o custom-columns='NAME:.metadata.name,CREATED:.metadata.creationTimestamp,ACTIVE:.metadata.labels.sealedsecrets\.bitnami\.com/sealed-secrets-key' 2>/dev/null

echo ""
echo "=== Controller Logs (errors) ==="
NS=$(kubectl get pods -l app.kubernetes.io/name=sealed-secrets --all-namespaces -o jsonpath='{.items[0].metadata.namespace}' 2>/dev/null)
kubectl logs -l app.kubernetes.io/name=sealed-secrets -n "$NS" --tail=20 2>/dev/null | grep -i "error\|fail\|unseal" | head -10
```

## Output Format

- Target ≤50 lines per output
- Use `-o custom-columns` for resource listings
- Show sync status prominently for each SealedSecret
- Flag missing corresponding Secrets
- Never expose decrypted secret values -- show sync status only

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

- **Key rotation**: New keys are generated every 30 days by default -- old keys are kept for decryption
- **Scope**: SealedSecrets can be strict (namespace+name), namespace-wide, or cluster-wide -- scope mismatch causes decryption failure
- **Controller namespace**: Controller can be in kube-system or custom namespace -- check controller's --key-prefix flag
- **Re-encryption**: After key rotation, existing SealedSecrets still use old key -- re-seal for new key
- **Backup keys**: Sealing keys in Secrets are critical -- losing them means losing ability to decrypt
- **Cluster migration**: SealedSecrets are tied to the cluster's sealing key -- cannot move between clusters without key export
- **Template metadata**: SealedSecret `.spec.template` controls the generated Secret's metadata and type
- **Update conflicts**: Updating a SealedSecret replaces the entire Secret -- partial updates are not supported
