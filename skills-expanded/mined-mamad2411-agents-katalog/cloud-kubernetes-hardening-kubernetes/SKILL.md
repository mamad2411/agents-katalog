---
name: cloud-kubernetes-hardening-kubernetes
description: "| | 1.1 | Control Plane - API Server | Anonymous auth, RBAC, audit logging | | 1."
domain: cybersecurity
---

|
| 1.1 | Control Plane - API Server | Anonymous auth, RBAC, audit logging |
| 1.2 | Control Plane - API Server | Admission controllers, encryption |
| 1.3 | Control Plane - Controller Manager | Service account tokens, bind address |
| 1.4 | Control Plane - Scheduler | Profiling, bind address |
| 2.1 | etcd | Client cert auth, peer encryption |
| 3.1 | Control Plane - Authentication | OIDC, client certs |
| 4.1 | Worker - kubelet | Anonymous auth, authorization |
| 4.2 | Worker - kubelet | TLS, read-only port |
| 5.1 | Policies - RBAC | Cluster-admin usage, service accounts |
| 5.2 | Policies - Pod Security | Privileged, host namespaces |
| 5.3 | Policies - Network | Network policies per namespace |
| 5.7 | Policies - General | Secrets, security context |

## Output Example

```
[INFO] 1 Control Plane Security Configuration
[INFO] 1.1 Control Plane Node Configuration Files
[PASS] 1.1.1 Ensure that the API server pod specification file permissions are set to 600
[PASS] 1.1.2 Ensure that the API server pod specification file ownership is set to root:root
[FAIL] 1.1.3 Ensure that the controller manager pod specification file permissions are set to 600
[WARN] 1.1.4 Ensure that the scheduler pod specification file permissions are set to 600

== Summary ==
45 checks PASS
12 checks FAIL
8 checks WARN
0 checks INFO
```

## CI/CD Integration

### GitHub Actions

```yaml
on:
  schedule:
    - cron: '0 6 * * 1'

jobs:
  kube-bench:
    runs-on: ubuntu-latest
    steps:
      - name: Configure kubectl
        uses: azure/setup-kubectl@v3

      - name: Run kube-bench
        run: |
          kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml
          kubectl wait --for=condition=complete job/kube-bench --timeout=120s
          kubectl logs job/kube-bench > kube-bench-report.txt

      - name: Check for failures
        run: |
          FAILS=$(grep -c "\[FAIL\]" kube-bench-report.txt || true)
          echo "Failed checks: $FAILS"
          if [ "$FAILS" -gt 0 ]; then
            echo "::warning::$FAILS CIS benchmark checks failed"
          fi

      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: kube-bench-report
          path: kube-bench-report.txt
```

## Remediation Examples

### 1.2.1 - Ensure --anonymous-auth is set to false
```yaml
# /etc/kubernetes/manifests/kube-apiserver.yaml
spec:
  containers:
  - command:
    - kube-apiserver
    - --anonymous-auth=false
```

### 4.2.1 - Ensure --anonymous-auth is set to false on kubelet
```yaml
# /var/libs/kubelet/config.yaml
authentication:
  anonymous:
    enabled: false
  webhook:
    enabled: true
```

### 5.2.1 - Minimize wildcard RBAC
```bash
# Find roles with wildcard permissions
kubectl get clusterroles -o json | jq '.items[] | select(.rules[].resources[] == "*") | .metadata.name'
```

## Best Practices

1. **Run kube-bench before and after** cluster provisioning
2. **Schedule weekly scans** via CronJob for drift detection
3. **Export JSON** for SIEM/compliance reporting
4. **Fix FAIL items first**, then address WARN items
5. **Use benchmark profiles** matching your Kubernetes distribution
6. **Track score over time** to measure security posture improvement
7. **Combine with admission controllers** to prevent drift
