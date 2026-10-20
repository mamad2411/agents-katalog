---
name: trust-manager
description: trust-manager Kubernetes operator for distributing X.509 CA trust bundles. Use when installing trust-manager via Helm, writing Bundle CRDs (sources/targets), syncing CA bundles to namespaces, integrating with cert-manager root CAs, configuring JKS/PKCS12 additional formats, secretTargets RBAC, or troubleshooting bundle sync.
---

# trust-manager

Kubernetes operator that distributes X.509 CA certificate bundles cluster-wide via the `Bundle` CRD. Maintained by Jetstack alongside cert-manager.

## When to Use

- Distributing private/internal root CA certificates to many namespaces
- Bundling system trust roots (Debian/Mozilla) with custom CAs into one ConfigMap
- Generating JKS or PKCS#12 trust stores for Java/.NET workloads
- Syncing the cert-manager root CA Secret out to consumer namespaces

## Architecture

```
Sources (trust namespace) ──► Bundle controller ──► Targets (selected namespaces)
  configMap | secret                                  ConfigMap | Secret
  inLine    | useDefaultCAs                           + JKS / PKCS12 formats
```

Bundle is **cluster-scoped**. Sources live in the trust namespace (default `cert-manager`). Targets fan out via `namespaceSelector`.

## Helm Install (Quick)

```bash
# Prerequisite: cert-manager (provides webhook cert)
helm upgrade cert-manager oci://quay.io/jetstack/charts/cert-manager \
  --install --namespace cert-manager --create-namespace \
  --set crds.enabled=true

# trust-manager (must share namespace with cert-manager by default)
helm upgrade trust-manager oci://quay.io/jetstack/charts/trust-manager \
  --install --namespace cert-manager --wait
```

For production values, secretTargets RBAC, and approver-policy integration, see `references/helm-installation.md`.

## Minimal Bundle

```yaml
apiVersion: trust.cert-manager.io/v1alpha1
kind: Bundle
metadata:
  name: public-trust
spec:
  sources:
    - useDefaultCAs: true
  target:
    configMap:
      key: ca-bundle.crt
```

This creates a `public-trust` ConfigMap in **every** namespace containing Mozilla/Debian default CAs.

## Common Patterns

### Internal CA + Public roots, fanned out by label

```yaml
apiVersion: trust.cert-manager.io/v1alpha1
kind: Bundle
metadata:
  name: org-trust
spec:
  sources:
    - useDefaultCAs: true
    - configMap:
        name: internal-root-ca
        key: ca.crt
  target:
    configMap:
      key: ca-bundle.crt
    namespaceSelector:
      matchLabels:
        trust: enabled
```

Label namespaces with `kubectl label ns my-app trust=enabled` to opt in.

### Java/JKS keystore output

```yaml
target:
  configMap:
    key: ca-bundle.crt
  additionalFormats:
    jks:
      key: truststore.jks
      password: changeit
    pkcs12:
      key: truststore.p12
```

For source field options (configMap, secret, inLine, useDefaultCAs, selectors), see `references/bundle-sources.md`. For targets, namespaceSelector, additionalFormats, and pod mounting, see `references/bundle-targets.md`.

## cert-manager Integration

**Critical rule:** never reference `tls.crt` from a cert-manager-issued Secret as a trust source — it contains intermediates that change on rotation. Use the issuer's root CA via `ca.crt` (only populated when issuer is `ca:` type with a root in the source Secret), or copy the root into a dedicated ConfigMap.

For root rotation patterns and `ca.crt` vs `tls.crt` details, see `references/cert-manager-integration.md`.

## Verification

```bash
# Bundle status (look for Synced=True)
kubectl get bundle
kubectl describe bundle <name>

# Confirm sync to a target namespace
kubectl get configmap <bundle-name> -n <namespace> -o yaml

# trust-manager controller logs
kubectl logs -n cert-manager deploy/trust-manager
```

## Common Issues

| Symptom | Cause | Reference |
|---------|-------|-----------|
| Bundle stuck `Synced=False` | Source ConfigMap/Secret not in trust namespace | troubleshooting.md |
| `secret target requires --secret-targets-enabled` | Secret targets disabled by default | helm-installation.md |
| Target ConfigMap missing in namespace | `namespaceSelector` does not match labels | troubleshooting.md |
| Webhook cert errors on install | cert-manager not installed/ready | helm-installation.md |
| Intermediates appearing in bundle | Sourcing `tls.crt` instead of root | cert-manager-integration.md |
| Bundle works for new ns but not existing | Namespace lacks selector label | troubleshooting.md |

## References

- `references/helm-installation.md` — Helm values, namespace, secretTargets RBAC, approver-policy, default CA package
- `references/bundle-spec.md` — Bundle CRD overview, status conditions, full reference example
- `references/bundle-sources.md` — Source types: configMap, secret, inLine, useDefaultCAs, selectors
- `references/bundle-targets.md` — Target types, namespaceSelector, JKS/PKCS12, pod mounting
- `references/cert-manager-integration.md` — Sourcing CAs from cert-manager Issuers, rotation, ca.crt vs tls.crt
- `references/troubleshooting.md` — Sync failures, RBAC, webhook, namespace selector pitfalls
