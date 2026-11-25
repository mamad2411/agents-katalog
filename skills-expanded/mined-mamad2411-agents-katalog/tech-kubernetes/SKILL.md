---
name: tech-kubernetes
description: Kubernetes cluster security review — identifies unauthenticated API server access, anonymous kubelet endpoints, etcd exposure, RBAC over-permissioning, pod security context weaknesses, service account token abuse, network policy gaps, secret management posture, admission controller misconfiguration, and container image supply-chain risks. All probes are read-only API inspection and configuration analysis. No pod creation, no container execution, no secret exfiltration, no privilege escalation attempts, no node compromise.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, blue-team, offensive, grey-hat]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft, k8s-security-audit, rbac-analysis-report]
---

# Kubernetes cluster security review

Use this skill to assess the security posture of Kubernetes clusters. The review covers external API server exposure, authentication and authorization configurations, anonymous access vectors, etcd datastore security, kubelet endpoint exposure, RBAC permission analysis, pod security standards, service account and secret management, network policy enforcement, admission controller configuration, and container image vulnerabilities. All probes are read-only API requests, configuration inspection, and permission evaluation. This skill never creates pods, executes commands in containers, reads secret data values, modifies RBAC rules, or performs privilege escalation that could compromise cluster nodes.

## Required inputs

- Kubernetes API server URL (e.g., `https://TARGET_IP:6443`, `http://TARGET_IP:8080`).
- If testing from inside a pod: service account token path (`/var/run/secrets/kubernetes.io/serviceaccount/token`), namespace, and CA certificate.
- If testing externally: optional bearer token, client certificate, or kubeconfig file for authenticated testing.
- Node IP addresses if kubelet assessment is in scope (default ports 10250 for authenticated, 10255 for read-only).
- Scope file confirming which cluster components, namespaces, and node addresses are in scope.
- Authorization cache valid for the cluster target.
- Optional: user-provided RBAC manifests, pod security policies, network policies, admission controller configurations, and CIS benchmark scan results (kube-bench output) for offline review. If provided, prefer offline review over live probing.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before any active probing.
2. `pentest_agent_parse_scope` and `pentest_agent_validate_target` for every host before requests.
3. `pentest_agent_check_authorization` before any HTTP request to cluster components.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for all live probing — rate-limit enforcement, approval for any risky requests.
6. `pentest_agent_append_evidence` with redacted output.

## Workflow

### Phase 1 — API server external enumeration

Determine cluster accessibility, authentication requirements, and version information.

1. **API server port discovery**:
   - Default Kubernetes API server ports: 6443 (TLS, standard), 8080 (insecure, deprecated since v1.20, disabled by default).
   - `curl -k -s https://TARGET_IP:6443/version | jq '{major, minor, gitVersion, platform}'`. If returns version JSON → the API server is reachable. If unauthenticated → CRITICAL.
   - `curl -s http://TARGET_IP:8080/api` — if this returns data, the insecure port is enabled. CRITICAL. No TLS, no authentication, full cluster admin access. This port has been disabled by default since Kubernetes 1.20 but misconfigurations persist.
2. **Anonymous access test** (standard check, read-only):
   - `curl -k -s https://TARGET_IP:6443/api | jq '{kind, apiVersion, serverAddressByClientCIDRs}'`.
   - `curl -k -s https://TARGET_IP:6443/api/v1 | jq '.resources[] | {name, namespaced, kind}'`.
   - `curl -k -s https://TARGET_IP:6443/apis | jq '.groups[] | {name, versions: [.versions[].version]}'`.
   - If any of these return data → anonymous access is enabled. CRITICAL.
   - Anonymous access is controlled by `--anonymous-auth=true` (default). Cluster administrators should bind the `system:anonymous` user to minimal or no permissions.
3. **Unauthenticated endpoint enumeration**:
   - Common endpoints accessible without authentication (even on secured clusters): `/healthz`, `/livez`, `/readyz`, `/version`, `/metrics`, `/openapi/v2`, `/openapi/v3`.
   - `curl -k -s https://TARGET_IP:6443/metrics | head -30` — if accessible, reveals: etcd request latencies, API request counts, scheduler metrics, controller manager health, node status counts. MEDIUM finding.
   - `curl -k -s https://TARGET_IP:6443/openapi/v2 | jq '.definitions | keys | length'` — reveals full API schema. LOW informational.
   - These are expected to be unauthenticated on most clusters and are not findings on their own, but their presence confirms the API server is reachable.
4. **API server version and build info**:
   - `curl -k -s https://TARGET_IP:6443/version | jq .`.
   - Document: major, minor, gitVersion, gitCommit, buildDate, platform, goVersion.
   - Cross-reference against known CVEs for that version. Kubernetes follows a ~14-month patch support window.
   - Version ≤ 1.26 (as of 2025) → EOL, no security patches. HIGH if internet-facing.

### Phase 2 — Authenticated RBAC and permission analysis

If valid credentials (token, cert, kubeconfig) are available, evaluate what the credential can access.

1. **Self-subject access review** (safe, read-only introspection):
   - `kubectl auth can-i --list` (or via API: `/apis/authorization.k8s.io/v1/selfsubjectrulesreviews`).
   - This shows all permissions the current credential has. It does not require any specific RBAC permission — every authenticated user can check their own permissions.
   - Key dangerous permissions to flag:
     - `pods/exec` on `*` → can exec into any pod. CRITICAL if combined with a sensitive namespace.
     - `secrets` with `get`, `list`, or `watch` → can read all secrets in the namespace. HIGH.
     - `pods` with `create` → can create a pod. If also has `pods/exec` or can specify `privileged: true`, this enables container escape to the node. HIGH.
     - `clusterroles` / `clusterrolebindings` with `create`, `update`, `bind`, or `escalate` → can grant self cluster-admin. CRITICAL.
     - `nodes` with `get`, `list` → can enumerate all cluster nodes, their addresses, OS, and labels. MEDIUM.
     - `namespaces` with `create` → can create namespaces, bypassing namespace-scoped policies. MEDIUM.
     - `persistentvolumes` with `get`, `list` → can read cluster-wide storage configuration. LOW-MEDIUM.
2. **Service account enumeration**:
   - `kubectl get serviceaccounts -A`. Lists every service account in every namespace. LOW informational.
   - Cross-reference: which deployments use which service accounts. A web app deployment using a service account with `cluster-admin` → CRITICAL.
3. **Secret enumeration** (metadata only, never read data):
   - `kubectl get secrets -A` — lists all secret names. MEDIUM if more than expected number of secrets exist (leftover credentials, old service account tokens).
   - `kubectl get secret SECRET_NAME -o json | jq '.metadata.annotations, .metadata.labels, .type'` — metadata only. Do not decode `.data`.
   - **PROHIBITED**: do not decode or read secret data values. Document only secret names, types, and annotations.

### Phase 3 — kubelet endpoint security

The kubelet runs on every node and exposes two ports: 10250 (authenticated) and 10255 (read-only, unauthenticated).

1. **Read-only kubelet port** (10255, unauthenticated):
   - `curl -s http://NODE_IP:10255/pods | jq '.items[] | {name: .metadata.name, namespace: .metadata.namespace, node: .spec.nodeName}'`.
   - If this returns pod data → HIGH. Full pod enumeration is available without any authentication.
   - `curl -s http://NODE_IP:10255/stats/summary | jq '{node: .node.nodeName, cpu: .node.cpu, memory: .node.memory}'` — reveals node resource usage. MEDIUM.
   - This port has been deprecated and should be disabled (`--read-only-port=0` on the kubelet).
2. **Authenticated kubelet port** (10250, TLS, requires client cert or token):
   - `curl -k https://NODE_IP:10250/pods` — if this returns data without a certificate, the kubelet is misconfigured. CRITICAL. The kubelet API allows executing commands in containers and reading container logs.
   - `curl -k https://NODE_IP:10250/runningpods/` — another endpoint that may reveal running pods. MEDIUM.
3. **Kubelet healthz and metrics**:
   - `curl -s http://NODE_IP:10255/healthz`, `curl -s http://NODE_IP:10255/metrics` — informational but confirms the kubelet is running.

### Phase 4 — etcd security

etcd stores all cluster state including secrets, service account tokens, and configuration.

1. **etcd port discovery** (2379 client, 2380 peer):
   - `curl -k -s https://ETCD_IP:2379/version` — if the etcd API responds, etcd is network-accessible. CRITICAL if no client certificate is required.
   - `curl -k -s https://ETCD_IP:2379/v3/kv/range -X POST -H "Content-Type: application/json" -d '{"key":"Lw=="}'` — an empty range request (`/` base64 encoded). If this returns data, etcd allows unauthenticated reads. CRITICAL.
   - **PROHIBITED**: do not attempt to read or decode any etcd data. Confirm accessibility only. If the endpoint returns base64-encoded data, stop immediately.
2. **etcd peer port** (2380):
   - If accessible, may allow cluster membership manipulation. Document exposure without probing further.
3. **etcd client certificate requirement**:
   - etcd should require client certificates (`--client-cert-auth=true`). If `curl -k` without a certificate returns data, this setting is disabled. CRITICAL.

### Phase 5 — Pod security and container runtime assessment

If pod/namespace listing is available, evaluate pod security configurations.

1. **Privileged pods**:
   - `kubectl get pods -A -o json | jq '.items[] | select(.spec.containers[].securityContext.privileged == true) | {name: .metadata.name, namespace: .metadata.namespace}'`.
   - Privileged containers have all capabilities and access to all host devices. CRITICAL unless a well-documented and reviewed exception.
2. **Host namespace sharing**:
   - `hostPID: true` → container sees and can interact with all host processes. CRITICAL.
   - `hostNetwork: true` → container uses host network namespace, can sniff host traffic. HIGH.
   - `hostIPC: true` → container shares host IPC namespace. MEDIUM.
3. **Capability grants**:
   - `kubectl get pods -A -o json | jq '.items[] | select(.spec.containers[].securityContext.capabilities.add != null) | {name: .metadata.name, ns: .metadata.namespace, caps: .spec.containers[].securityContext.capabilities.add}'`.
   - `SYS_ADMIN` → nearly equivalent to privileged. CRITICAL.
   - `NET_ADMIN` → can modify network configuration. MEDIUM.
   - `SYS_PTRACE` → can trace processes, potential container escape. HIGH.
4. **Docker socket or container runtime socket mount**:
   - `kubectl get pods -A -o json | jq '.items[] | select(.spec.volumes[].hostPath.path == "/var/run/docker.sock" or .spec.volumes[].hostPath.path == "/run/containerd/containerd.sock") | {name: .metadata.name, namespace: .metadata.namespace}'`.
   - Mounting the container runtime socket → CRITICAL. The container can create/start/stop other containers, effectively root on the node.
5. **Root filesystem mounts**:
   - `hostPath` volumes mounting `/`, `/etc`, `/var`, `/proc`, `/sys` → HIGH to CRITICAL depending on path and mount flags.
6. **Read-only root filesystem**:
   - Check: `readOnlyRootFilesystem: true` is set. Absent → container filesystem is writable. MEDIUM.
7. **RunAsNonRoot / RunAsUser**:
   - Check if `runAsNonRoot: true` is set. If absent, the container may run as root (UID 0). HIGH if the image default is root.

### Phase 6 — Network policy and service exposure

Assess network segmentation and service accessibility.

1. **Services with external exposure**:
   - `kubectl get svc -A -o json | jq '.items[] | select(.spec.type == "LoadBalancer" or .spec.type == "NodePort") | {name: .metadata.name, namespace: .metadata.namespace, type: .spec.type, ports: [.spec.ports[].port]}'`.
   - Each LoadBalancer service exposes ports to the internet. Check for: database services (5432, 3306, 27017, 6379, 9200), admin panels, unauthenticated web services.
2. **Network policy audit**:
   - `kubectl get networkpolicies -A`. If no network policies exist → all pods can communicate with all other pods. MEDIUM (no micro-segmentation).
   - Check for: default-deny policies, namespace isolation policies, ingress/egress rules.

### Phase 7 — Admission controller and policy enforcement

Review dynamic admission controllers that enforce security policy.

1. **Pod Security Admission (PSA) / Pod Security Policies (PSP)**:
   - `kubectl get psp` (PodSecurityPolicy, deprecated in v1.21, removed in v1.25). If a PSP exists, it may be overly permissive.
   - PSA labels on namespaces: `kubectl get ns -o json | jq '.items[] | {name: .metadata.name, labels: .metadata.labels | with_entries(select(.key | startswith("pod-security.kubernetes.io/")))}'`.
   - `enforce: privileged` → no pod security restrictions. MEDIUM.
2. **Validating/Mutating Webhook configurations**:
   - `kubectl get validatingwebhookconfigurations` and `kubectl get mutatingwebhookconfigurations`.
   - Check for security-enforcing webhooks (OPA/Gatekeeper, Kyverno, custom policy engines). Their presence is a positive control.

### Phase 8 — CIS benchmark and automated scanning

If the user provides automated scan results or runs them within scope.

1. **kube-bench review** (CIS Kubernetes Benchmark):
   - `kube-bench` checks control plane, etcd, controller manager, scheduler, worker node configurations against CIS benchmarks.
   - Review the output for: FAIL statuses. Prioritize: anonymous auth enabled, insecure port enabled, etcd auto-tls enabled, kubelet read-only port enabled, always-allow authorization mode.
2. **kube-hunter results** (if user ran it and provides output):
   - `kube-hunter` is an active scanner that probes for vulnerabilities. Review its findings but do not run it (active probing tool).
3. **trivy / image scanning results** (if user provides):
   - Review container image CVE reports for CRITICAL/HIGH CVEs in running containers.

## Decision points

- **Anonymous access to `/api` and `/api/v1` returns data**: CRITICAL. The cluster's `system:anonymous` user has been granted permissions. This is a deliberate RBAC binding, not a default. Stop and document.
- **Insecure port (8080) is reachable**: CRITICAL. This port bypasses all authentication and authorization. It has been disabled by default since v1.20.
- **kubelet read-only port returns pod data**: HIGH. Common on older or default installations. Remediation: `--read-only-port=0`.
- **etcd returns data without client certificate**: CRITICAL. All cluster secrets are accessible. Etcd should always require client certs and be firewalled from general network access.
- **Service account in the `kube-system` namespace has `cluster-admin`**: many system components need cluster-admin. This is expected for `kube-system` SAs. Flag only if a non-system namespace SA has cluster-admin.

## Prohibited behavior

- Creating pods, deployments, or any Kubernetes resources.
- Executing commands inside containers (`pods/exec`).
- Reading secret data values (`.data` fields).
- Modifying RBAC roles, role bindings, or cluster role bindings.
- Deleting or modifying any Kubernetes resource.
- Attempting privilege escalation from a pod to the node (container escape).
- Accessing cloud metadata services from within pods (`169.254.169.254`).
- Port-forwarding to services or pods.
- Running `kube-hunter` or other active vulnerability scanners against the cluster.
- Dumping etcd data.

## Stop conditions

- API server insecure port (8080) returns data → CRITICAL. Document immediately; do not enumerate further.
- Anonymous access to `/api/v1/secrets` returns data → CRITICAL. All secrets are exposed. Stop; do not read secret data.
- etcd responds without authentication → CRITICAL. Document access; do not query data.
- Kubelet port 10250 returns pod data without authentication → CRITICAL. Do not enumerate further or attempt command execution.
- Pod security context reveals `privileged: true` plus `hostPID: true` in a non-system namespace → CRITICAL. Flag for immediate architectural review.

## Evidence

For each finding, record: cluster component, finding type, endpoint/resource, access level, severity, and remediation. Evidence template:

```text
Kubernetes cluster security review for: [API_SERVER:PORT]
Kubernetes version: [major.minor.patch]
Review date: [DATE]

API server access:
  Insecure port (8080): [reachable (CRITICAL) / not reachable]
  TLS port (6443): [reachable / not reachable]
  Anonymous access: [enabled with permissions (CRITICAL) / enabled no permissions (OK) / disabled]
  `/metrics` accessible: [yes / no]
  `/version`: [VERSION]

RBAC analysis (authenticated):
  Current credential permissions: [N] rules, [N] cluster-scoped rules
  Dangerous permissions: [pods/exec (CRITICAL) / secrets (HIGH) / cluster-admin (CRITICAL) / nodes / namespaces]
  Service accounts: [N] total across [N] namespaces
  Service accounts with cluster-admin: [N] in non-system namespaces

Kubelet security:
  Read-only port (10255): [enabled — pod listing (HIGH) / enabled — metrics only (MEDIUM) / disabled]
  Authenticated port (10250): [TLS enforced / unauthenticated (CRITICAL)]

etcd security:
  2379 accessible: [no (OK) / with auth (OK) / without auth (CRITICAL)]
  Client certificate required: [yes / no (CRITICAL)]

Pod security:
  Privileged pods: [N] — [namespaces redacted]
  Host PID sharing: [N] pods
  Host Network sharing: [N] pods
  Docker/CRI socket mounts: [N] pods (CRITICAL)
  SYS_ADMIN capability: [N] pods (CRITICAL)
  Containers running as root: [N] / [total] pods
  Read-only root FS: [N] / [total] pods

Network policy:
  NetworkPolicies: [N] in [N] namespaces
  Default-deny: [present / absent]

Admission control:
  PSA enforce level: [privileged (MEDIUM) / baseline / restricted]
  Policy engine: [OPA/Gatekeeper / Kyverno / none]

Redaction notes:
  - No pods were created, deleted, or modified.
  - No commands were executed inside containers.
  - No secret data values were read.
  - No etcd data was queried.
  - Node IPs and hostnames are redacted to NODE_N.
  - Namespace names containing organizational info are redacted.
```

## Report handoff

1. `pentest_agent_record_finding` for each finding with: cluster component, finding type, severity, evidence reference, remediation (specific kubelet flag, API server flag, RBAC change, pod security context change), and CIS benchmark reference.
2. Priority matrix: CRITICAL (insecure port enabled, anonymous access with dangerous permissions, etcd unauthenticated, kubelet unauthenticated on 10250, Docker socket mounted in pod, SYS_ADMIN capability, service account with cluster-admin in non-system namespace). HIGH (anonymous pod listing via kubelet 10255, secrets readable, privileged pods, hostPID/hostNetwork, missing network policies). MEDIUM (read-only root FS missing, running as root, PSA enforce: privileged, LoadBalancer exposing internal services). LOW (metrics endpoint accessible, version info exposed).
3. Provide a Kubernetes hardening checklist: disable insecure port (`--anonymous-auth=false` if not needed, `--insecure-port=0`), bind `system:anonymous` to no permissions, require client certificates for etcd, set `--read-only-port=0` on kubelets, enforce PSA restricted, implement network policies, use OPA/Gatekeeper for policy enforcement, run kube-bench regularly, and scan container images for CVEs in CI.
4. Explicitly note: no pods were created or executed in, no secrets were read, no etcd data was accessed, no privilege escalation was attempted, and no cluster configuration was modified.
