---
name: cloud-kubernetes-hardening-kubesecmanifest
description: "Cloud Kubernetes Hardening Kubesecmanifest."
domain: cybersecurity
---

-|
| ReadOnlyRootFilesystem | +1 | Prevents filesystem writes |
| RunAsNonRoot | +1 | Non-root process execution |
| RunAsUser > 10000 | +1 | High UID reduces collision risk |
| LimitsCPU | +1 | Prevents CPU resource exhaustion |
| LimitsMemory | +1 | Prevents memory resource exhaustion |
| RequestsCPU | +1 | Ensures scheduler resource awareness |
| ServiceAccountName | +3 | Explicit service account |
| AppArmor annotation | +3 | Kernel-level MAC enforcement |
| Seccomp profile | +4 | Syscall filtering |

## References

- [Kubesec GitHub Repository](https://github.com/controlplaneio/kubesec)
- [Kubesec Online Scanner](https://kubesec.io/)
- [ControlPlane Security Tools](https://controlplane.io/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
