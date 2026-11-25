---
name: cloud-kubernetes-hardening-podsecurity
description: "Cloud Kubernetes Hardening Podsecurity."
domain: cybersecurity
---

-|
| HostProcess | Must not set | Pods cannot use Windows HostProcess |
| Host Namespaces | Must not set | No hostNetwork, hostPID, hostIPC |
| Privileged | Must not set | No privileged: true |
| Capabilities | Baseline list only | Only NET_BIND_SERVICE, drop ALL for restricted |
| HostPath Volumes | Must not use | No hostPath volume mounts |
| Host Ports | Must not use | No hostPort in container spec |
| AppArmor | Default/runtime | Cannot set to unconfined |
| SELinux | Limited types | Only container_t, container_init_t, container_kvm_t |
| /proc Mount Type | Default only | Must use Default proc mount |
| Seccomp | RuntimeDefault or Localhost | Must specify seccomp profile (restricted) |
| Sysctls | Safe set only | Limited to safe sysctls |

## Validation Commands

```bash
# Verify namespace labels
kubectl get ns --show-labels | grep pod-security

# Test pod creation against policy
kubectl run test-pod --image=nginx --namespace=production --dry-run=server

# Check for violations in audit logs
kubectl get events --field-selector reason=FailedCreate -A

# Scan with Kubescape for PSS compliance
kubescape scan framework nsa --namespace production
```

## References

- [Pod Security Standards - Kubernetes](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Pod Security Admission - Kubernetes](https://kubernetes.io/docs/concepts/security/pod-security-admission/)
- [Migrate from PodSecurityPolicy](https://kubernetes.io/docs/tasks/configure-pod-container/migrate-from-psp/)
- [Kubescape PSS Scanner](https://github.com/kubescape/kubescape)
