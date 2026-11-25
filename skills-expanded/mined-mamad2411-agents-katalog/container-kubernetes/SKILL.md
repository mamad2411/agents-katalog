---
name: container-kubernetes
description: Kubernetes security review — validate API-server exposure, RBAC misconfiguration, pod security, network-policy gaps, secret hygiene, and etcd/data-store access with read-only checks and no pod execution or cluster modification.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Kubernetes security — cluster and workload review

Use this skill to review Kubernetes security posture on authorized in-scope clusters. Validate API-server exposure, RBAC misconfiguration, pod security standards, network-policy coverage, secret hygiene, and data-store protection. All tests must use read-only kubeconfig access (when authorized), user-provided manifest exports, or audit-tool output. Never execute commands in pods, create or modify resources, read Secret values, or access the etcd data store directly unless separately and explicitly approved.

## Required inputs

- Written scope naming the cluster, namespace(s), and allowed review methods (manifest review, read-only kubeconfig, audit-tool reports). Explicit confirmation that pod exec, resource creation/modification, Secret value retrieval, and etcd access are prohibited unless separately approved.
- User-provided artifacts: Kubernetes manifests (Deployments, Pods, Services, RBAC, NetworkPolicies), Helm charts, kustomize overlays, Kyverno/OPA policies, kube-bench reports, kube-hunter reports, Trivy image-scan output, and read-only kubeconfig when authorized.
- If a read-only kubeconfig is provided: confirm it is restricted to read-only operations on explicitly permitted namespaces. Test that create, update, delete, and exec are rejected before using the kubeconfig for review.
- Valid authorization cache for the Kubernetes cluster.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for read-only execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — API-server exposure and authentication review

Review the Kubernetes API-server's network exposure and authentication posture:

1. **External port exposure**: check whether the API server is reachable on the default port (6443) from outside the cluster network. Common exposure points: cloud load balancers, public IPs on control-plane nodes, or misconfigured firewall rules. Use a TCP connect probe (not an HTTP request) to avoid authentication attempts against unauthorized endpoints.
2. **Insecure port (8080)**: check whether the legacy insecure port (8080) is enabled. This port provides unauthenticated, unrestricted API access — critical finding if open. Most distributions disable it by default, but custom or old clusters may have it.
3. **Kubelet ports (10250, 10255)**: 
   - Port 10250: the kubelet API (authenticated, TLS). Check whether it is reachable and whether anonymous authentication is accepted. If anonymous auth is enabled, query `/pods`, `/stats/summary`, and `/metrics` to verify read-only access.
   - Port 10255: the legacy read-only kubelet port (no auth). If open, it exposes pod specifications, resource usage, and container metadata without authentication.
4. **Anonymous API access**: if read-only kubeconfig access is authorized, test anonymous API access: `kubectl auth can-i --list --as=system:anonymous`. If the anonymous user has any permissions beyond discovery, this is a finding.
5. **Authentication mechanism**: identify the configured authentication mode: client certificates, bearer tokens, OIDC, webhook, or static tokens. Check whether multiple auth mechanisms are configured (more attack surface) and whether static token files exist (tokens never expire).

### Phase 2 — RBAC and service-account review

Review role-based access control:

1. **Cluster-wide roles**: list all ClusterRoleBindings and ClusterRoles. Identify:
   - `cluster-admin` bindings: every subject with this role has full control over the entire cluster. Review whether each binding is justified.
   - Wildcard permissions: roles granting `*` on `*` resources in any scope.
   - `system:masters` group membership: any user or service account in this group has cluster-admin equivalent power.
2. **Namespace-scoped roles**: for each in-scope namespace, list RoleBindings and Roles. Identify over-privileged grants:
   - `pods/exec`, `pods/attach`, `pods/portforward` — allows command execution in pods.
   - `secrets` — allows reading all secrets in the namespace.
   - `pods create`, `deployments create`, `jobs create` — allows deploying workloads that may escape or escalate.
   - `clusterroles bind`, `roles bind` — allows escalating permissions by binding higher-privileged roles.
   - `serviceaccounts token` — allows creating long-lived service account tokens.
3. **Service account enumeration**: list all service accounts in each in-scope namespace. For each:
   - Check the attached roles and whether the service account has more permissions than its workload requires.
   - Check whether the service account is mounted in pods that don't need API access (`automountServiceAccountToken: false` is missing).
   - Check for default service accounts in namespaces — the `default` service account should have no permissions unless explicitly granted.
4. **RBAC privilege-escalation paths**: trace whether any non-admin principal can escalate:
   - Can the principal create a pod with a privileged service account?
   - Can the principal bind a ClusterRole to themselves?
   - Can the principal impersonate another user or group?
   - Can the principal create a ValidatingWebhookConfiguration or MutatingWebhookConfiguration?

### Phase 3 — pod security and workload configuration review

Review pod security configurations:

1. **Pod Security Standards (PSS)**: check the enforced level per namespace: `privileged`, `baseline`, or `restricted`. `restricted` is the recommended default. If a namespace allows `privileged`, any pod in that namespace can run as privileged.
2. **Privileged pods**: list all pods with `securityContext.privileged: true`. These pods have all Linux capabilities and access to all host devices.
3. **Host namespace sharing**: list pods with `hostPID: true`, `hostIPC: true`, or `hostNetwork: true`. Each weakens namespace isolation and may allow host compromise.
4. **Host mounts**: list pods with `hostPath` volumes. Check which host paths are mounted: `/`, `/var/run/docker.sock`, `/proc`, `/sys`, `/etc/kubernetes`, `/var/lib/kubelet`, or sensitive data directories. Docker socket and host-root mounts are container-escape vectors.
5. **Capability grants**: list pods with `capabilities.add`. Identify unnecessary or dangerous capabilities: `CAP_SYS_ADMIN`, `CAP_SYS_PTRACE`, `CAP_NET_RAW`, `CAP_SYS_MODULE`, `CAP_BPF`, `CAP_PERFMON`.
6. **Run-as-non-root**: check whether every pod explicitly sets `runAsNonRoot: true` in its security context. Containers running as root (UID 0) can exploit kernel vulnerabilities or misconfigured host mounts more easily.
7. **Read-only root filesystem**: check whether pods that don't need to write to the filesystem set `readOnlyRootFilesystem: true`.
8. **Seccomp, AppArmor, SELinux**: are these profiles configured? Seccomp profiles restrict system calls; AppArmor/SELinux restrict file and capability access. Pods without these run with the full kernel attack surface.

### Phase 4 — network-policy and service exposure review

Review network segmentation:

1. **NetworkPolicy coverage**: list all NetworkPolicies and check whether every namespace has a default-deny policy (deny all ingress and egress except explicitly allowed). Without a default-deny, all pods in the namespace can communicate freely.
2. **Egress restrictions**: are egress NetworkPolicies in place? Without egress restrictions, a compromised pod can connect to any external host for data exfiltration or C2.
3. **Ingress restrictions**: are pods that should only accept traffic from specific sources (frontend → backend, API gateway → services) restricted by ingress NetworkPolicies?
4. **Service exposure**: list all Services with `type: LoadBalancer` or `type: NodePort`. For each, check whether the exposed port is necessary and whether the service is reachable from the public internet. Use a TCP connect probe (not an application-layer request) to validate reachability when scope permits.
5. **Namespace isolation**: can pods in namespace-A communicate with pods in namespace-B? If namespace isolation relies on NetworkPolicy alone and no policies are defined, cross-namespace communication is unrestricted.

### Phase 5 — secret management and etcd protection review

Review how secrets are handled:

1. **Secret enumeration**: list all Secrets in each in-scope namespace (names and types only — never retrieve values). Identify which workloads mount or reference each Secret.
2. **Secret types**: categorize by type: `Opaque`, `kubernetes.io/tls`, `kubernetes.io/dockerconfigjson`, `kubernetes.io/service-account-token`, `kubernetes.io/basic-auth`, `kubernetes.io/ssh-auth`. TLS, dockerconfigjson, and basic-auth types may contain highly sensitive material.
3. **Secret exposure**: check whether Secrets are exposed via:
   - Environment variables (visible in `kubectl describe pod` and `/proc/<pid>/environ` in the container).
   - Volume mounts (check mount path permissions — world-readable mounts expose secrets to any process in the container).
   - ConfigMaps (ConfigMaps are not encrypted and should never contain secret data — check for ConfigMaps with secret-like keys).
4. **Encryption at rest**: is etcd encryption enabled? If not, anyone with etcd access can read all Secrets in plaintext. Check the encryption configuration for the list of encrypted resources (`secrets`, `configmaps`, etc.).
5. **etcd access**: is the etcd port (2379) reachable? If etcd is exposed without authentication, anyone can read all cluster data including Secrets. Check whether the etcd client certificate is required and whether peer-to-peer TLS is enabled.
6. **Secret rotation**: check whether service-account tokens have expiration (`automountServiceAccountToken` with projected tokens). Non-expiring tokens are long-lived credentials.

### Phase 6 — audit and compliance scan review

Review automated scan output:

1. **kube-bench**: run or review CIS Kubernetes Benchmark results. Focus on failures in the `master`, `etcd`, `control plane`, `worker`, and `policies` sections.
2. **kube-hunter**: review for active findings: exposed endpoints, vulnerable versions, anonymous access, and privileged access paths.
3. **Trivy/KubeClarity**: review image vulnerability scans for in-scope workloads. Critical and high CVEs in running containers are patch-now items.
4. **Kyverno/OPA Gatekeeper**: review policy reports for violations. If policy enforcement is in audit mode only (no `enforce`), violations exist but are not blocked.
5. **Falco/Tetragon**: review runtime security events for suspicious process execution, file access, or network connections that may indicate active compromise.

## Decision points

- **Escalate on exposed etcd without authentication**: critical — all cluster data including Secrets is readable.
- **Escalate on insecure kubelet port (10255) open**: medium/high — pod and resource metadata exposed without authentication.
- **Escalate on cluster-admin bound to non-admin principal**: critical.
- **Escalate on RBAC privilege-escalation path** (create pod + bind role): high/critical.
- **Escalate on privileged pod in a non-system namespace**: high.
- **Escalate on host-root or Docker socket mount in pod**: container escape possible — high/critical.
- **Escalate on missing default-deny NetworkPolicy**: medium. Unrestricted pod-to-pod communication increases blast radius.
- **Downgrade on advisory-only scan findings**: CIS benchmark failures at the "manual" or "scored-but-not-automatable" level are informational unless independently validated.

## Prohibited behavior

- Executing commands in pods (`kubectl exec`, `kubectl attach`, or interactive shells).
- Creating, modifying, or deleting any Kubernetes resource (pods, deployments, services, RBAC, secrets, configmaps, network policies).
- Reading Secret values from the API server or etcd.
- Accessing etcd directly (port 2379) with any client.
- Deploying privileged pods, host-mount volumes, or any test workload to the cluster.
- Tainting or cordoning nodes.
- Accessing the kubelet API (10250) with authentication credentials unless the kubeconfig is explicitly authorized for kubelet access.

## Stop conditions

- Exposed etcd or anonymous API access discovered → critical finding, stop active probing of the control plane.
- Read-only kubeconfig can perform create/update/delete operations → stop, report the misconfigured kubeconfig as a finding.
- Secrets visible in environment variables or world-readable mounts → record finding metadata, do not retrieve or store secret values.
- Cluster or namespace not confirmed in scope → stop.
- Active compromise indicators discovered (unexpected processes, connections, cryptomining) → stop, notify escalation contact.

## Evidence — Kubernetes security posture matrix

For each cluster, record:

```text
Cluster: <name or endpoint prefix>
API server version: <major.minor>
Namespaces in scope: <list>

API-server findings:
  External access: <yes (port 6443 open) | no>
  Insecure port (8080): <open | closed>
  Anonymous auth: <enabled | disabled>
  Kubelet 10255: <open | closed>
  Kubelet 10250 anonymous: <accepted | rejected>

RBAC findings:
  ClusterRoleBindings: <total count>
  Cluster-admin bindings: <count, list subjects>
  Wildcard-role subjects: <count, list subjects>
  Privilege-escalation paths: <count, list paths>
  Service accounts with excessive roles: <count>

Workload findings:
  Total pods: <count>
  Privileged pods: <count>
  Host-network pods: <count>
  HostPID/HostIPC pods: <count>
  Docker socket mounts: <count>
  Host-root mounts: <count>
  runAsNonRoot missing: <count>
  readOnlyRootFilesystem missing: <count>

Network findings:
  Namespaces with default-deny: <count> / <total>
  Services exposed externally: <count, list>
  Egress restrictions: <present on N namespaces | absent>

Secret and etcd findings:
  Secret count: <count>
  ConfigMaps with secret-like keys: <count>
  Encryption at rest: <enabled | disabled>
  etcd port exposed: <yes (2379) | no>
  Non-expiring service-account tokens: <count>

Overall risk: <critical | high | medium | low | none>
```

Never store: kubeconfig files, service-account tokens, Secret values, etcd client certificates, TLS private keys, cluster CA certificates, or unredacted pod environment variables containing credentials.

## Report handoff

When review is complete:
1. `pentest_agent_record_finding` for each category: exposed etcd/API, anonymous access, cluster-admin proliferation, RBAC escalation paths, privileged pods, host namespace sharing, socket/host mounts, missing NetworkPolicy, unencrypted secrets, and compliance-scan failures.
2. Reference the Kubernetes security posture matrix.
3. Recommend:
   - **API server**: never expose the API server on the public internet without IP restrictions and strong authentication. Disable anonymous access and the insecure port (8080).
   - **RBAC**: audit ClusterRoleBindings quarterly. Apply least-privilege roles per namespace per workload. Remove wildcard grants. Block privilege-escalation paths with Pod Security Admission or OPA/Kyverno policies.
   - **Workloads**: enforce the `restricted` Pod Security Standard on all non-system namespaces. Run every container as non-root with a read-only root filesystem. Drop all capabilities; add only those required. Never mount host paths or the Docker socket.
   - **Network**: apply a default-deny NetworkPolicy to every namespace. Define explicit ingress and egress rules for every workload. Restrict cross-namespace traffic.
   - **Secrets**: enable etcd encryption at rest. Use a secrets-management solution (External Secrets Operator, Vault, Sealed Secrets) instead of native Kubernetes Secrets for high-sensitivity data. Use projected service-account tokens with expiration. Never store secrets in ConfigMaps.
   - **Auditing**: enable Kubernetes audit logging to a secure external sink. Run `kube-bench` and `kube-hunter` quarterly. Scan all images for CVEs in CI before deployment. Deploy runtime security monitoring (Falco/Tetragon) for production clusters.
