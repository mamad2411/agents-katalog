---
name: cloud-kubernetes-etcd-kubernetes
description: "-| | 2.1 | etcd cert-file set | TLS certificate configured | | 2."
domain: cybersecurity
---

-|
| 2.1 | etcd cert-file set | TLS certificate configured |
| 2.2 | etcd client-cert-auth | Client certificate authentication enabled |
| 2.3 | etcd auto-tls disabled | auto-tls=false |
| 2.4 | etcd peer cert-file set | Peer TLS configured |
| 2.5 | etcd peer client-cert-auth | Peer authentication enabled |
| 2.6 | etcd peer auto-tls disabled | peer-auto-tls=false |
| 2.7 | etcd unique CA | Separate CA for etcd (not shared with cluster) |

## Key Rotation Procedure

```bash
# 1. Generate new encryption key
NEW_KEY=$(head -c 32 /dev/urandom | base64)

# 2. Update EncryptionConfiguration with new key first
cat > /etc/kubernetes/enc/encryption-config.yaml <<EOF
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key2
              secret: ${NEW_KEY}
            - name: key1
              secret: <old-key>
      - identity: {}
EOF

# 3. Restart API server to pick up new config
# 4. Re-encrypt all secrets with new key
kubectl get secrets --all-namespaces -o json | \
  kubectl replace -f -

# 5. Remove old key from EncryptionConfiguration
# 6. Restart API server again
```

## References

- [Kubernetes etcd Encryption Documentation](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/)
- [CIS Kubernetes Benchmark - etcd Controls](https://www.cisecurity.org/benchmark/kubernetes)
- [Securing etcd - K8s Security Guide](https://k8s-security.geek-kb.com/docs/best_practices/cluster_setup_and_hardening/control_plane_security/etcd_security_mitigation/)
- [Infosec: Encryption and etcd](https://www.infosecinstitute.com/resources/cryptography/encryption-and-etcd-the-key-to-securing-kubernetes/)
