---
name: rke2-operations
description: Day-2 RKE2 operations - cluster access/kubeconfig, bundled CLI tools (kubectl/crictl/ctr), logs and debugging, metrics endpoints, resource sizing, deploying add-ons via Helm/manifests, HelmChart and HelmChartConfig CRDs, GPU operators, and enduring known issues. Self-hosted RKE2 only.
---

# RKE2 Operations

Operational reference for self-hosted RKE2 clusters: accessing the cluster, using the bundled CLI tools, finding logs, scraping metrics, sizing nodes, deploying add-ons with the Helm controller, running the NVIDIA GPU operator, and avoiding well-known host-level pitfalls.

## Cluster Access

RKE2 writes an admin kubeconfig to `/etc/rancher/rke2/rke2.yaml` on server nodes. Any upstream tool (kubectl, helm, k9s, etc.) works against it — point the tool at the file:

```bash
export KUBECONFIG=/etc/rancher/rke2/rke2.yaml
kubectl get pods --all-namespaces
helm ls --all-namespaces

# or per-command
kubectl --kubeconfig /etc/rancher/rke2/rke2.yaml get pods -A
helm --kubeconfig /etc/rancher/rke2/rke2.yaml ls -A
```

The file is root-readable only by default. To relax permissions at install time, set in `/etc/rancher/rke2/config.yaml`:

```yaml
write-kubeconfig-mode: "0644"
```

### Access from outside the cluster

1. Copy `/etc/rancher/rke2/rke2.yaml` from a server node to your workstation as `~/.kube/config` (or merge it).
2. Edit the `server:` field, replacing `127.0.0.1` with the server's reachable IP or hostname:

```yaml
clusters:
- cluster:
    server: https://rke2-server.example.com:6443
```

3. If you connect via a hostname, load balancer, or IP that is not already in the server certificate, add it as a SAN in `/etc/rancher/rke2/config.yaml` on the servers (before or after install; restart `rke2-server` to apply):

```yaml
tls-san:
  - rke2-server.example.com
  - 203.0.113.10
```

Otherwise kubectl fails TLS verification (`x509: certificate is valid for ...`).

## Bundled CLI Tools

On startup RKE2 extracts its bundled binaries to `/var/lib/rancher/rke2/bin`: `kubectl`, `crictl`, `ctr` (plus others). This directory is not on `PATH` by default — call binaries by full path or add it:

```bash
export PATH=$PATH:/var/lib/rancher/rke2/bin
```

### kubectl

```bash
export KUBECONFIG=/etc/rancher/rke2/rke2.yaml
/var/lib/rancher/rke2/bin/kubectl get nodes
```

### containerd: crictl and ctr

RKE2's embedded containerd listens on the **k3s-style socket path**: `/run/k3s/containerd/containerd.sock` (not `/run/containerd/containerd.sock`). Stock crictl/ctr invocations fail without pointing at it.

crictl — use the generated config file (already contains the correct endpoint):

```bash
export CRI_CONFIG_FILE=/var/lib/rancher/rke2/agent/etc/crictl.yaml
/var/lib/rancher/rke2/bin/crictl ps
# or set the endpoint directly:
export CONTAINER_RUNTIME_ENDPOINT=unix:///run/k3s/containerd/containerd.sock
/var/lib/rancher/rke2/bin/crictl ps
/var/lib/rancher/rke2/bin/crictl logs <container_id>
```

ctr — must pass both the socket address and the `k8s.io` namespace (Kubernetes containers live there; the default namespace appears empty):

```bash
/var/lib/rancher/rke2/bin/ctr \
  --address /run/k3s/containerd/containerd.sock \
  --namespace k8s.io \
  container ls
```

## Logs and Debugging

| Component | Location / command |
|---|---|
| RKE2 server process | `journalctl -u rke2-server` |
| RKE2 agent process | `journalctl -u rke2-agent` |
| Syslog (some distros duplicate journald) | `/var/log/syslog` |
| containerd | `/var/lib/rancher/rke2/agent/containerd/containerd.log` |
| kubelet | `/var/lib/rancher/rke2/agent/logs/kubelet.log` |
| Pod/container logs | `/var/log/pods/` (also via `kubectl logs` or `crictl logs`) |

etcd and the control-plane components (kube-apiserver, kube-controller-manager, kube-scheduler, kube-proxy, cloud-controller-manager) run as **static pods** in `kube-system`, so their logs are available through kubectl even though they are not deployments:

```bash
/var/lib/rancher/rke2/bin/kubectl --kubeconfig /etc/rancher/rke2/rke2.yaml \
  logs -n kube-system -l component=kube-apiserver
```

If the apiserver itself is down, fall back to crictl or read the files under `/var/log/pods/kube-system_kube-apiserver-*/`.

Debug verbosity: add `debug: true` to `/etc/rancher/rke2/config.yaml` (or `--debug`) for verbose supervisor logging, and restart the service. Component log levels can be raised via config, e.g.:

```yaml
kube-apiserver-arg:
  - "v=4"
kubelet-arg:
  - "v=4"
```

## Metrics

Most metrics come from the standard components; scrape them as you would on any Kubernetes cluster:

- etcd metrics — see https://etcd.io/docs/v3.5/metrics/
- CoreDNS metrics — see https://coredns.io/plugins/metrics/
- Kubernetes node metrics (kubelet, cAdvisor) and component metrics (apiserver, scheduler, controller-manager) — standard upstream endpoints

### Supervisor metrics

The RKE2 supervisor process exposes its own metrics only when enabled in `/etc/rancher/rke2/config.yaml`:

```yaml
supervisor-metrics: true
```

They are then served at `/metrics` on the supervisor port **9345** of each node (authenticated — use the admin kubeconfig):

```bash
kubectl get --server https://NODENAME:9345 --raw /metrics
```

Exposed metric families include:

- **RKE2 cluster management metrics:**
  - `rke2_certificate_expiration_seconds` (gauge; labels `subject`, `usage`) — remaining lifetime of internal certificates. Alert on this to catch cert expiry.
  - `rke2_loadbalancer_server_connections` (gauge; `name`, `server`) — current connections through the client loadbalancer.
  - `rke2_loadbalancer_server_health` (gauge; `name`, `server`) — backend health enum: 0=INVALID, 1=FAILED, 2=STANDBY, 3=UNCHECKED, 4=RECOVERING, 5=HEALTHY, 6=PREFERRED, 7=ACTIVE.
  - `rke2_loadbalancer_dial_duration_seconds` (histogram; `name`, `status`).
  - `rke2_etcd_snapshot_save_duration_seconds`, `..._save_local_duration_seconds`, `..._save_s3_duration_seconds` (histograms; `status`) — etcd snapshot timing.
  - `rke2_etcd_snapshot_reconcile_duration_seconds`, `..._reconcile_local_...`, `..._reconcile_s3_...` (histograms; `status`) — snapshot list sync timing.
- Lasso controller metrics, Kubernetes client-go/workqueue metrics, Go runtime metrics.
- If the embedded registry mirror is enabled: Spegel and libp2p metrics.

## Resource Sizing (baseline profiling)

Upstream profiling (RKE2 v1.27, all packaged components enabled, Canal CNI, Ubuntu 22.04 on a 4-core Xeon 8375C / 8 GB node; 95th-percentile steady-state via `systemd-cgtop`):

| Role | Scenario | CPU | Memory |
|---|---|---|---|
| Server (single node) | server + simple nginx workload | ~17% of a core | ~5.0 GB |
| Server | server + one agent joined, no workload | ~18% of a core | ~4.8 GB |
| Agent | joined to server, no workload | ~5% of a core | ~3.6 GB |

Practical guidance:

- Server nodes: plan for roughly **5 GB RAM** consumed by the RKE2 stack (supervisor, etcd, control plane, containerd, packaged add-ons) before workload; 4 GB total RAM is the floor, 8 GB+ recommended.
- Agent nodes: reserve roughly **3.5 GB RAM** and a fraction of a core for kubelet + agent + containerd overhead.
- `system.slice/rke2-server.service` and `system.slice/rke2-agent.service` cgroups are where this overhead accrues — use `systemd-cgtop` to measure on your own hardware.

## Deploying Add-ons: Manifests Directory and Helm Controller

### Auto-deploy manifests directory

Any Kubernetes manifest placed in `/var/lib/rancher/rke2/server/manifests` (server nodes) is applied automatically — like `kubectl apply` — at startup and again whenever the file changes on disk.

Key behaviors:

- Each file becomes an `AddOn` custom resource: `kubectl get addon -A`. Packaged components (CoreDNS, Traefik, Metrics Server, etc.) appear here too.
- The AddOn name derives from the file basename, which must be a valid RFC 1123 subdomain (lowercase alphanumerics, `-`, `.`); underscores cause `Failed to process config ... metadata.name: Invalid value` errors. Names must be unique and must not collide with packaged component names.
- **Deleting a file does NOT delete the resources from the cluster.** Delete the resources with kubectl, or use the disable mechanism below.
- Disable packaged components (or your own AddOns) in `/etc/rancher/rke2/config.yaml`; disabled AddOns are actively uninstalled and their manifest files removed:

```yaml
disable:
  - rke2-coredns
  - rke2-metrics-server
```

### HelmChart CRD

RKE2 embeds the k3s helm-controller. A `HelmChart` resource (`helm.cattle.io/v1`) is equivalent to running `helm install/upgrade`, executed by a job pod. Typical pattern: drop a HelmChart manifest in the manifests directory.

```yaml
apiVersion: helm.cattle.io/v1
kind: HelmChart
metadata:
  name: grafana
  namespace: kube-system   # the CR lives here; the release goes to targetNamespace
spec:
  repo: https://grafana.github.io/helm-charts
  chart: grafana
  version: 8.5.1
  targetNamespace: monitoring
  createNamespace: true
  set:
    adminPassword: "NotVerySafePassword"
  valuesContent: |-
    env:
      GF_EXPLORE_ENABLED: true
    sidecar:
      datasources:
        enabled: true
```

Important spec fields (mapping to helm CLI flags):

| Field | Meaning / helm equivalent |
|---|---|
| `spec.chart` | Chart name in repo, or full HTTPS URL to a .tgz |
| `spec.chartContent` | Base64-encoded .tgz (overrides `chart`) |
| `spec.repo` | Repo URL (`--repo`) |
| `spec.version` | Chart version (`--version`) |
| `spec.targetNamespace` / `spec.createNamespace` | `--namespace` / `--create-namespace` |
| `spec.set` | `--set` / `--set-string` — **overrides valuesContent** |
| `spec.valuesContent` | Inline YAML values (`--values`) |
| `spec.valuesSecrets` | Values from external Secrets |
| `spec.repoCA` / `spec.repoCAConfigMap` | PEM CA bundle for HTTPS repo (`--ca-file`) |
| `spec.authSecret` | `kubernetes.io/basic-auth` Secret for the repo |
| `spec.dockerRegistrySecret` | `kubernetes.io/dockerconfigjson` Secret for OCI repos |
| `spec.plainHTTP` / `spec.insecureSkipTLSVerify` | Insecure download options |
| `spec.timeout` | Helm timeout, duration string (default `300s`) |
| `spec.backOffLimit` | Job retries before failure (default 1000) |
| `spec.failurePolicy` | `reinstall` (default) or `abort` |
| `spec.bootstrap` | `true` for charts needed to bootstrap the cluster (CCM, CNI) |
| `spec.jobImage`, `spec.podSecurityContext`, `spec.securityContext` | Helm job pod customization |

**failurePolicy caution:** the default `reinstall` will uninstall-and-reinstall a release stuck in pending after an interrupted upgrade. For critical infrastructure (CNIs, Rancher, anything with CRDs whose deletion is destructive) set `failurePolicy: abort` so a failed release is left in place for manual troubleshooting.

Private repo with auth + custom CA example:

```yaml
apiVersion: helm.cattle.io/v1
kind: HelmChart
metadata:
  name: example-app
  namespace: kube-system
spec:
  targetNamespace: example-space
  createNamespace: true
  chart: example-app
  version: v1.2.3
  repo: https://secure-repo.example.com
  authSecret:
    name: example-repo-auth
  repoCAConfigMap:
    name: example-repo-ca
---
apiVersion: v1
kind: Secret
metadata:
  name: example-repo-auth
  namespace: kube-system
type: kubernetes.io/basic-auth
stringData:
  username: user
  password: pass
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: example-repo-ca
  namespace: kube-system
data:
  ca.crt: |-
    -----BEGIN CERTIFICATE-----
    ...
    -----END CERTIFICATE-----
```

### HelmChartConfig: customizing packaged components

To override values on RKE2's packaged charts (rke2-canal, rke2-coredns, rke2-traefik, rke2-metrics-server, ...) without editing the packaged HelmChart, create a `HelmChartConfig` with the **same name and namespace** as the target HelmChart. Its `valuesContent` is passed to helm as an extra values file. Note `spec.set` on the HelmChart still wins over any `valuesContent`.

Example — `/var/lib/rancher/rke2/server/manifests/rke2-coredns-config.yaml`:

```yaml
apiVersion: helm.cattle.io/v1
kind: HelmChartConfig
metadata:
  name: rke2-coredns
  namespace: kube-system
spec:
  valuesContent: |-
    image:
      tag: v1.14.3-build20260506
```

Packaged chart defaults/docs: https://github.com/rancher/rke2-charts/tree/main/charts

## NVIDIA GPU Operator on RKE2

Prerequisites on the host OS (unless letting the operator install drivers — supported on NVIDIA-listed OSes, and on any OS from operator v26.3.x if a compatible driver container image is available):

```bash
lsmod | grep nvidia                 # kernel modules loaded
cat /proc/driver/nvidia/version     # NVRM version
find /usr/ -iname libnvidia-ml.so   # library present (used by k8s components)
```

Deploy via HelmChart (drop in the manifests directory). The RKE2-specific detail is the **containerd socket path** — the toolkit must be pointed at `/run/k3s/containerd/containerd.sock`:

Operator v25.x (pre-CDI/NRI):

```yaml
apiVersion: helm.cattle.io/v1
kind: HelmChart
metadata:
  name: gpu-operator
  namespace: kube-system
spec:
  repo: https://helm.ngc.nvidia.com/nvidia
  chart: gpu-operator
  version: v25.3.4
  targetNamespace: gpu-operator
  createNamespace: true
  valuesContent: |-
    toolkit:
      env:
      - name: CONTAINERD_SOCKET
        value: /run/k3s/containerd/containerd.sock
      - name: ACCEPT_NVIDIA_VISIBLE_DEVICES_ENVVAR_WHEN_UNPRIVILEGED
        value: "false"
      - name: ACCEPT_NVIDIA_VISIBLE_DEVICES_AS_VOLUME_MOUNTS
        value: "true"
    devicePlugin:
      env:
      - name: DEVICE_LIST_STRATEGY
        value: volume-mounts
```

The three extra env vars enforce proper GPU isolation; workloads then need `runtimeClassName: nvidia`. With v25.10.x (CDI, requires containerd 2.0) only `CONTAINERD_SOCKET` is needed and `runtimeClassName` is no longer required. With v26.3.x (NRI, requires containerd 2.1 — shipped in RKE2 v1.31.13+rke2r1 / v1.32.9 / v1.33.5 / v1.34.1 and later) no containerd config change at all is needed:

```yaml
spec:
  version: v26.3.1
  valuesContent: |-
    cdi:
      nriPluginEnabled: true
```

**Warning:** the operator restarts containerd with a hangup call, which restarts RKE2.

Verification:

```bash
kubectl get node $NODE -o jsonpath='{.metadata.labels}' | grep nvidia.com   # driver/GPU labels
kubectl get node $NODE -o jsonpath='{.status.allocatable}'                 # "nvidia.com/gpu": N
ls /usr/local/nvidia/toolkit/nvidia-container-runtime                       # toolkit installed
grep nvidia /var/lib/rancher/rke2/agent/etc/containerd/config.toml          # runtime registered (non-NRI only)
```

Test pod (add `runtimeClassName: nvidia` only for v25.3.x):

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nbody-gpu-benchmark
spec:
  restartPolicy: OnFailure
  containers:
  - name: cuda-container
    image: nvcr.io/nvidia/k8s/cuda-sample:nbody
    args: ["nbody", "-gpu", "-benchmark"]
    resources:
      limits:
        nvidia.com/gpu: 1
```

RKE2 also searches the service's `PATH` for alternative container runtimes. To use runtimes installed in nonstandard locations, extend `PATH` in `/etc/default/rke2-server` (or `/etc/sysconfig/rke2-server`, or the `-agent` equivalents) — carefully, since the service runs as root.

## Known Issues (enduring/structural)

- **firewalld conflicts with Canal.** Disable firewalld on RKE2 nodes; the kernel firewall (iptables/nftables) remains and Canal manages its own rules. Implement custom rules via Calico resources instead.
- **NetworkManager interferes with CNI interfaces.** Tell NetworkManager to ignore CNI veth/tunnel devices — create `/etc/NetworkManager/conf.d/rke2-canal.conf`:

  ```ini
  [keyfile]
  unmanaged-devices=interface-name:flannel*;interface-name:cali*;interface-name:tunl*;interface-name:vxlan.calico;interface-name:vxlan-v6.calico;interface-name:wireguard.cali;interface-name:wg-v6.cali
  ```

  `systemctl reload NetworkManager` before install; reboot if RKE2 is already installed. On RHEL 8.4+, also disable `nm-cloud-setup.service` and `nm-cloud-setup.timer` — they add a routing table that breaks the CNI and cannot be worked around by config.
- **Wicked (SUSE) reverts sysctls.** Wicked can undo RKE2's runtime sysctl changes when it reapplies network config. Persist forwarding in `/etc/sysctl.d/90-rke2.conf`:

  ```
  net.ipv4.conf.all.forwarding=1
  net.ipv6.conf.all.forwarding=1   # dual-stack only
  ```
- **Istio on SELinux-enforcing hosts fails by default** (just-in-time kernel module loading is disallowed for unprivileged containers). Install Istio with its CNI enabled (`cniBinDir=/opt/cni/bin`, `cniConfDir=/etc/cni/net.d`) and patch the `istio-cni-node` DaemonSet's `install-cni` container to `securityContext.privileged: true` (an IstioOperator overlay works).
- **Calico VXLAN checksum-offload kernel bug.** RKE2's packaged Calico chart sets `ChecksumOffloadBroken=true` to disable checksum offload on the vxlan interface; keep that setting if using custom Calico with VXLAN (seen on Ubuntu 18.04/20.04, openSUSE Leap 15.3).
- **Canal IP exhaustion.** Two causes: (1) missing `iptables` binary on the host with a hostPort pod — pod creation fails in a retry loop, leaking one IP per attempt (`plugin type="portmap" failed ... "iptables": executable file not found`); install iptables/xtables-nft. (2) Leaked IP lock files in `/var/lib/cni/networks/k8s-pod-network` after containerd loses track of pods (`failed to allocate for range 0: no IP addresses available`); remove stale files manually, or drain the node, run `rke2-killall.sh`, restart the rke2 service, and uncordon.
- **Ingress unreachable in CIS mode.** With a `profile:` (CIS) set, restrictive default NetworkPolicies can block traffic from the ingress controller to app namespaces; add a NetworkPolicy per app namespace allowing ingress from the ingress controller's `kube-system` pods (match on the controller's `app.kubernetes.io/name` label).
- **Hardened-cluster upgrades across the PSP removal (v1.24 -> v1.25).** Set `profile: cis-1.23` on all nodes before upgrading, and label automation namespaces (e.g. `system-upgrade`) with `pod-security.kubernetes.io/enforce: privileged` so upgrade controllers can run under Pod Security Admission.

Upstream docs: https://docs.rke2.io/ — file new issues at https://github.com/rancher/rke2/issues.
