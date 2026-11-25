---
name: cloud-kubernetes-net-k8snetpol
description: "- [Network Policy Editor](https://editor.networkpolicy."
domain: cybersecurity
---

# Allow backend to reach database only
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: database
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: backend
      ports:
        - protocol: TCP
          port: 5432
```

### Step 4: Cross-Namespace Policies

```yaml
# Allow monitoring namespace to scrape metrics
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              purpose: monitoring
      ports:
        - protocol: TCP
          port: 9090  # Prometheus metrics port
```

### Step 5: Egress Restrictions

```yaml
# Restrict egress to specific external services
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Egress
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: database
      ports:
        - protocol: TCP
          port: 5432
    - to:  # Allow external API
        - ipBlock:
            cidr: 203.0.113.0/24
      ports:
        - protocol: TCP
          port: 443
    - to:  # DNS
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
      ports:
        - protocol: UDP
          port: 53
```

### Step 6: Block Cloud Metadata Access

```yaml
# Prevent SSRF to cloud metadata service
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Egress
  egress:
    - to:
        - ipBlock:
            cidr: 0.0.0.0/0
            except:
              - 169.254.169.254/32  # AWS/GCP metadata
              - 100.100.100.200/32  # Azure metadata
```

## Validation Commands

```bash
# Verify policies are applied
kubectl get networkpolicies -n production

# Test connectivity (should be blocked)
kubectl run test-pod --image=busybox --restart=Never -n production -- wget -qO- --timeout=2 http://database-service:5432
# Expected: timeout (blocked by policy)

# Test allowed traffic
kubectl run frontend-test --image=busybox --labels=app=frontend --restart=Never -n production -- wget -qO- --timeout=2 http://backend-service:8080
# Expected: connection succeeds
```

## References

- [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Calico Network Policies](https://docs.tigera.io/calico/latest/network-policy/)
- [Cilium Network Policies](https://docs.cilium.io/en/stable/security/policy/)
- [Network Policy Editor](https://editor.networkpolicy.io/)
