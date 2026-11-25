---
name: rke2-networking
description: Load for questions about RKE2 networking on self-hosted clusters - CNI selection/configuration (Canal, Cilium, Calico, Flannel), Traefik ingress and Gateway API, CoreDNS/NodeLocal DNSCache, dual-stack and IPv6, Multus/SR-IOV, external load balancers for the supervisor/API, ServiceLB, and kube-proxy options.
---

# RKE2 Networking

Guidance for configuring networking on self-hosted RKE2 clusters: CNI plugins, DNS, ingress, dual-stack, Multus, and control-plane load balancing.

## Core concepts

- RKE2 bundles four primary CNI plugins: **Canal** (default), **Cilium**, **Calico**, and **Flannel**. Only Calico and Flannel support Windows nodes. **Multus** is bundled as a secondary CNI multiplexer that must run alongside a primary CNI.
- Bundled CNIs (and other packaged components like CoreDNS and the ingress controller) are installed as Helm charts named `rke2-<component>` in the `kube-system` namespace.
- To customize any packaged component, create a **HelmChartConfig** resource whose `metadata.name` and `metadata.namespace` match the corresponding HelmChart, and drop it into `/var/lib/rancher/rke2/server/manifests/` on a server node. The helm controller merges `spec.valuesContent` into the chart values and redeploys.
- Main RKE2 config file: `/etc/rancher/rke2/config.yaml`.
- Default chart values per RKE2 version: browse https://github.com/rancher/rke2-charts/tree/main/charts.

## Selecting a CNI

Set the `cni` key in `/etc/rancher/rke2/config.yaml`:

```yaml
# /etc/rancher/rke2/config.yaml
cni: canal        # canal | cilium | calico | flannel | none
```

- `cni: none` means you bring your own CNI; nodes stay NotReady and tainted unschedulable until one is installed.
- CNI charts appear as `rke2-canal`, `rke2-cilium`, `rke2-calico`, `rke2-flannel` in `kube-system`.

### CNI tradeoffs at a glance

| CNI | Notes |
|---|---|
| Canal (default) | Flannel for inter-node traffic (vxlan overlay by default) + Calico for network policy. Requires iptables/xtables-nft on the node. **Not supported with Windows nodes.** |
| Cilium | eBPF dataplane; requires kernel >= 4.9.17. Supports kube-proxy replacement (kernel >= 5.8 recommended), WireGuard encryption, Hubble observability. **Not supported on Windows.** |
| Calico | Full-featured; supports BGP, eBPF dataplane (Jan 2026+ releases), nftables dataplane. Requires iptables/xtables-nft. Works with Windows nodes. SELinux needs extra care. |
| Flannel | Simple; vxlan backend only (available since Feb 2024 releases: v1.29.2, v1.28.7, v1.27.11, v1.26.14). **No network policy support** - not recommended for hardened installs. Works with Windows. |

### Canal customization

Override the flannel interface:

```yaml
# /var/lib/rancher/rke2/server/manifests/rke2-canal-config.yaml
apiVersion: helm.cattle.io/v1
kind: HelmChartConfig
metadata:
  name: rke2-canal
  namespace: kube-system
spec:
  valuesContent: |-
    flannel:
      iface: "eth1"
```

WireGuard backend (kernels < 5.6 need the wireguard module installed):

```yaml
spec:
  valuesContent: |-
    flannel:
      backend: "wireguard"
```

After changing Canal config, restart the daemonset: `kubectl rollout restart ds rke2-canal -n kube-system`.

### Cilium customization

Enable WireGuard encryption:

```yaml
# /var/lib/rancher/rke2/server/manifests/rke2-cilium-config.yaml
apiVersion: helm.cattle.io/v1
kind: HelmChartConfig
metadata:
  name: rke2-cilium
  namespace: kube-system
spec:
  valuesContent: |-
    encryption:
      enabled: true
      type: wireguard
```

**Kube-proxy replacement** (kernel >= 5.8 strongly recommended). Set `disable-kube-proxy: true` in `/etc/rancher/rke2/config.yaml` plus:

```yaml
spec:
  valuesContent: |-
    kubeProxyReplacement: true
    k8sServiceHost: "localhost"
    k8sServicePort: "6443"
```

**Hubble observability:**

```yaml
spec:
  valuesContent: |-
    hubble:
      enabled: true
      relay:
        enabled: true
      ui:
        enabled: true
```

### Calico customization

Change MTU:

```yaml
# /var/lib/rancher/rke2/server/manifests/rke2-calico-config.yaml
apiVersion: helm.cattle.io/v1
kind: HelmChartConfig
metadata:
  name: rke2-calico
  namespace: kube-system
spec:
  valuesContent: |-
    installation:
      calicoNetwork:
        mtu: 9000
```

Calico disables hardware checksum offload to work around a kernel bug (< 5.7), capping TCP throughput around 2.5 Gbps. On kernels > 5.7, re-enable offload:

```yaml
spec:
  valuesContent: |-
    felixConfiguration:
      featureDetectOverride: "ChecksumOffloadBroken=false"
```

**Calico eBPF dataplane** (Jan 2026 releases: v1.33.8+rke2r1, v1.34.4+rke2r1, v1.35.1+rke2r1). Replaces iptables and can replace kube-proxy. Set `disable-kube-proxy: true` in config.yaml plus:

```yaml
spec:
  valuesContent: |-
    installation:
      calicoNetwork:
        kubeProxyManagement: Enabled
        linuxDataplane: BPF
    kubernetesServiceEndpoint:
      host: "<control_node_ip>"      # with HA, use the external LB VIP
      port: "6443"
```

### Flannel customization

```yaml
# /var/lib/rancher/rke2/server/manifests/rke2-flannel-config.yaml
apiVersion: helm.cattle.io/v1
kind: HelmChartConfig
metadata:
  name: rke2-flannel
  namespace: kube-system
spec:
  valuesContent: |-
    flannel:
      mtu: 9000
```

## Dual-stack (IPv4/IPv6)

Set dual-stack CIDRs on control-plane nodes at **cluster creation time** - dual-stack cannot be enabled on an existing IPv4-only cluster:

```yaml
# /etc/rancher/rke2/config.yaml
cluster-cidr: "10.42.0.0/16,2001:cafe:42::/56"
service-cidr: "10.43.0.0/16,2001:cafe:43::/112"
```

Per-CNI notes: Canal, Cilium, Calico, and Flannel all auto-detect dual-stack; no extra chart config needed. Calico in dual-stack mode creates two ippool resources and uses **BGP instead of VXLAN** encapsulation. Dual-stack (and Calico BGP) is not supported on Windows nodes.

## IPv6-only

- RKE2 uses `localhost` to reach the etcd liveness URL; ensure `/etc/hosts` contains `::1 localhost`.
- If the IPv6 default route comes from a router advertisement, set `net.ipv6.conf.all.accept_ra=2` or the node drops the default route when it expires (note: accepting RAs increases MITM risk).
- Cilium in IPv6-only mode does not encapsulate inter-node IPv6 traffic; the host network must route pod IPs. Cilium can manage static routes between nodes:

```yaml
# /var/lib/rancher/rke2/server/manifests/rke2-cilium-config.yaml
apiVersion: helm.cattle.io/v1
kind: HelmChartConfig
metadata:
  name: rke2-cilium
  namespace: kube-system
spec:
  valuesContent: |-
    autoDirectNodeRoutes: true
```

## kube-proxy notes

- Disable with `disable-kube-proxy: true` when using Cilium kube-proxy replacement or Calico eBPF with `kubeProxyManagement: Enabled`.
- **nftables proxy mode** (experimental; July 2026 releases v1.36.3+rke2r1, v1.35.7+rke2r1, v1.34.10+rke2r1): `kube-proxy-arg: ["proxy-mode=nftables"]` in config.yaml. CNIs need matching HelmChartConfig: Canal `flannel.enableNFTables: true` + `calico.felixIptablesBackend: nft`; Calico `installation.calicoNetwork.linuxDataplane: Nftables`; Flannel `flannel.enableNFTables: true`; Cilium uses eBPF, nothing to configure.
- IPVS mode is deprecated starting Kubernetes v1.35 and scheduled for removal.
- Nodes without a hostname (some clouds set "localhost" or none): set `node-name` in config.yaml to avoid DNS resolution issues.

## CoreDNS and NodeLocal DNSCache

- CoreDNS deploys by default with a cluster-proportional autoscaler. Disable entirely with `disable: rke2-coredns` in config.yaml (then you must supply your own cluster DNS).
- Customize via a HelmChartConfig for `rke2-coredns` in `kube-system`.

Enable NodeLocal DNSCache (per-node DNS caching agent):

```yaml
# /var/lib/rancher/rke2/server/manifests/rke2-coredns-config.yaml
apiVersion: helm.cattle.io/v1
kind: HelmChartConfig
metadata:
  name: rke2-coredns
  namespace: kube-system
spec:
  valuesContent: |-
    nodelocal:
      enabled: true
```

Caveats:
- NodeLocal modifies node iptables to intercept DNS traffic; toggling it off without redeploying breaks DNS.
- With kube-proxy in IPVS mode, add `ipvs: true` under `nodelocal`, and point kubelets at the node-local address (`kubelet-arg: ["cluster-dns=169.254.20.10"]`); requires restarting RKE2 and all pods.
- **Cilium kube-proxy replacement + NodeLocal** (v1.28.13+rke2r1, v1.29.8+rke2r1, v1.30.4+rke2r1+): Cilium eBPF bypasses iptables, so use a Cilium Local Redirect Policy. Set `localRedirectPolicy: true` (with `kubeProxyReplacement: true`, `k8sServiceHost`, `k8sServicePort`) in the rke2-cilium HelmChartConfig, and in the rke2-coredns HelmChartConfig set `nodelocal: {enabled: true, use_cilium_lrp: true}`.

## Ingress controller: Traefik

Use **Traefik** as the ingress controller. Set it on every server node in config.yaml:

```yaml
# /etc/rancher/rke2/config.yaml
ingress-controller: traefik
```

To run without any bundled ingress controller (e.g. when deploying your own), set `ingress-controller: none` instead.

- The ingress controller binds host ports **80 and 443** on nodes in its default configuration, making those ports unusable for other HostPort/NodePort services.
- Customize via HelmChartConfig for `rke2-traefik`, e.g. log level:

```yaml
# /var/lib/rancher/rke2/server/manifests/rke2-traefik-config.yaml
apiVersion: helm.cattle.io/v1
kind: HelmChartConfig
metadata:
  name: rke2-traefik
  namespace: kube-system
spec:
  valuesContent: |-
    logs:
      general:
        level: "DEBUG"
```

Operational notes:
- Traefik's health-check endpoint is `/ping` - use it for external load balancer health checks against the ingress nodes.
- Airgap: Traefik images ship in a separate `rke2-images-traefik.linux-amd64.tar.zst` tarball - include it alongside the core images tarball.
- Full chart options: see values.yaml of the `rke2-traefik` chart at https://github.com/rancher/rke2-charts.

### Gateway API

Gateway API in RKE2 requires Traefik. Enable it via the rke2-traefik HelmChartConfig:

```yaml
# /var/lib/rancher/rke2/server/manifests/rke2-traefik-config.yaml
apiVersion: helm.cattle.io/v1
kind: HelmChartConfig
metadata:
  name: rke2-traefik
  namespace: kube-system
spec:
  valuesContent: |-
    providers:
      kubernetesGateway:
        enabled: true
```

Experimental Gateway API resources must be installed separately (official gateway-api experimental-install.yaml) together with `providers.kubernetesGateway.experimentalChannel: true`. Caution: before the April 2026 releases (v1.33.11+rke2r1, v1.34.7+rke2r1, v1.35.4+rke2r1), disabling Traefik after enabling it removes the Gateway API CRDs and their resources.

## Service LoadBalancer (ServiceLB)

Services of type LoadBalancer need a controller. RKE2 can optionally deploy **ServiceLB** (klipper-lb), which uses available host ports: enable with `--enable-servicelb`. Labels use the `svccontroller.rke2.cattle.io` prefix (vs `svccontroller.k3s.cattle.io` in K3s docs). For most production cases, MetalLB or Kube-VIP are better LoadBalancer-service controllers.

## Load-balancing the supervisor / API server (HA control plane)

An external L4 load balancer provides a **fixed registration address** for node joins (port 9345, the supervisor) and optionally external access to the API server (port 6443). Typical pattern: HAProxy on two LB nodes with Keepalived managing a VIP.

- HAProxy: TCP frontends on 9345 and 6443, round-robin backends to each server node's 9345/6443 with tcp-check health checks.
- Keepalived: VRRP instance holding the VIP (MASTER/higher priority on lb-1, BACKUP on lb-2), with a `killall -0 haproxy` track script.
- Server nodes: share a `token` and add the VIP to `tls-san`:

```yaml
# /etc/rancher/rke2/config.yaml (servers)
token: "lb-cluster-gd"
tls-san:
  - "10.10.10.100"      # the VIP
```

Servers beyond the first also set `server: https://<VIP>:9345`. Agents join with:

```yaml
server: "https://10.10.10.100:9345"
token: "lb-cluster-gd"
```

With Calico eBPF + HA, point `kubernetesServiceEndpoint.host` at the VIP (port 6443) in the rke2-calico HelmChartConfig. Kube-VIP or MetalLB can replace the external LB pair for LoadBalancer Services, and Kube-VIP can also serve as a control-plane VIP alternative.

## Multus and SR-IOV

Multus attaches extra network interfaces to pods (CNI multiplexer). It always needs a primary CNI; list `multus` **first** in the `cni` key:

```yaml
# /etc/rancher/rke2/config.yaml
cni:
- multus
- canal        # or cilium/calico, or "none" to bring your own default plugin
```

- **With Cilium**, older releases require disabling Cilium's exclusive CNI ownership (not needed from Nov 2025 releases: v1.31.14+rke2r1, v1.32.10+rke2r1, v1.33.6+rke2r1, v1.34.2+rke2r1): set `cni: {exclusive: false}` in the rke2-cilium HelmChartConfig.
- Secondary networks are defined via **NetworkAttachmentDefinition** objects referenced by pod annotations; the standard containernetworking plugins (bridge, host-device, macvlan, ...) ship automatically with Multus.

IPAM options for secondary interfaces (configure via `rke2-multus` HelmChartConfig, written **before** starting RKE2):

- **host-local**: per-host state; not recommended for multi-node clusters.
- **DHCP daemon** (2024-01 releases+): `valuesContent: manifests: {dhcpDaemonSet: true}`.
- **Whereabouts** (cluster-wide IPAM):

```yaml
# /var/lib/rancher/rke2/server/manifests/rke2-multus-config.yaml
apiVersion: helm.cattle.io/v1
kind: HelmChartConfig
metadata:
  name: rke2-multus
  namespace: kube-system
spec:
  valuesContent: |-
    rke2-whereabouts:
      enabled: true
```

**Thick plugin mode** (experimental; v1.31.11+rke2r1, v1.32.7+rke2r1, v1.33.3+rke2r1+): `thickPlugin: {enabled: true}`; required for the Multus Dynamic Networks Controller (`dynamicNetworksController: {enabled: true}`).

**SR-IOV**: use the SR-IOV CNI with Multus for dataplane acceleration / very high throughput pod interfaces. Deploy via the SR-IOV Network Operator - see the quickstart at https://github.com/k8snetworkplumbingwg/sriov-network-operator/blob/master/doc/quickstart.md (hardware compatibility and prerequisites there); SUSE Telco Cloud documents validated configurations.

## Windows nodes and BGP (brief)

- Only **Calico** and **Flannel** support Windows nodes; dual-stack and Calico BGP are not supported on Windows installs of RKE2.
- For BGP routing across Linux + Windows nodes: set `cni: calico`, then enable BGP with encapsulation off:

```yaml
# /var/lib/rancher/rke2/server/manifests/rke2-calico-config.yaml
apiVersion: helm.cattle.io/v1
kind: HelmChartConfig
metadata:
  name: rke2-calico
  namespace: kube-system
spec:
  valuesContent: |-
    installation:
      calicoNetwork:
        bgp: Enabled
      backend: "None"
```

- On the Windows agent, before starting RKE2: install `RemoteAccess`, `RSAT-RemoteAccess-PowerShell`, and `Routing` Windows features (reboot required), then `Install-RemoteAccess -VpnType RoutingOnly` and `Start-Service RemoteAccess`.

## Quick reference

- CNI choice: `cni:` in `/etc/rancher/rke2/config.yaml` (canal default; none = BYO).
- Component tuning: HelmChartConfig in `/var/lib/rancher/rke2/server/manifests/`, name/namespace matching the `rke2-*` HelmChart in `kube-system`.
- Dual-stack: comma-separated `cluster-cidr`/`service-cidr` at cluster creation only.
- Disable built-ins: `disable: rke2-coredns`, `ingress-controller: none`, `disable-kube-proxy: true`.
- HA joins: external LB/VIP on 9345 (+6443), VIP in `tls-san`.
