---
name: cloud-containers-runtime
description: "Cloud Containers Runtime."
domain: cybersecurity
---

--|
| `tetragon_events_total` | Total security events observed | Spike > 3x baseline |
| `tetragon_policy_events_total` | Events matching TracingPolicies | Any Sigkill action |
| `tetragon_process_exec_total` | Process executions tracked | Anomalous new binaries |
| `tetragon_missed_events_total` | Dropped events due to buffer overflow | > 0 sustained |

## References

- [Tetragon Official Documentation](https://tetragon.io/docs/)
- [Cilium Tetragon GitHub Repository](https://github.com/cilium/tetragon)
- [CNCF Tetragon Project Page](https://www.cncf.io/projects/tetragon/)
- [eBPF Security Observability with Tetragon - CoreWeave](https://docs.coreweave.com/security/tutorials/ebpf-observability)
- [Kubernetes Security: eBPF & Tetragon for Runtime Monitoring](https://medium.com/@noah_h/kubernetes-security-ebpf-tetragon-for-runtime-monitoring-policy-enforcement-819b6ed97953)
