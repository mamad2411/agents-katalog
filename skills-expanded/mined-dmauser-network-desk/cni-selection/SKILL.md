# Skill: CNI Plugin Selection

## Purpose

Guide users in selecting, configuring, and migrating between Container Network Interface (CNI) plugins for Kubernetes clusters. This skill covers the major CNI options across AKS, EKS, and GKE, providing decision frameworks based on performance requirements, policy needs, IPAM strategy, and operational complexity.

## Core Knowledge

### CNI Fundamentals

The Container Network Interface (CNI) specification defines how network plugins configure networking for containers. Every pod in Kubernetes requires a network identity (IP address) and connectivity to other pods, services, and external endpoints. The CNI plugin is responsible for:

- Assigning IP addresses to pods (IPAM)
- Configuring the pod's network namespace (veth pairs, routes)
- Implementing network policies (traffic filtering)
- Managing overlay or underlay networking
- Handling IP address lifecycle (allocation and release)

### Azure CNI — Traditional (VNet Integration)

Azure CNI in traditional mode assigns VNet IP addresses directly to pods. Each pod receives a routable IP from the node's subnet.

**Characteristics:**
- Pods get IPs from the Azure VNet subnet (pre-allocated on node)
- Full VNet integration — pods are directly reachable from VNet, on-premises via VPN/ExpressRoute
- IP consumption: each node reserves a configurable number of IPs (default 30)
- Subnet sizing must account for max pods × max nodes
- No overlay — flat networking with native Azure routing
- Supports Windows nodes

**When to use:**
- Pods must be directly addressable from outside the cluster (on-premises, other VNets)
- Compliance requires no overlay/encapsulation
- Integration with Azure services that need direct pod IP connectivity (e.g., Azure Firewall rules per pod)

**IP Planning Example:**
```
Subnet size needed = (max_nodes × max_pods_per_node) + max_nodes + reserved
Example: 50 nodes × 30 pods = 1500 pod IPs + 50 node IPs + 5 reserved = /21 minimum
```

### Azure CNI — Overlay Mode

Azure CNI Overlay assigns pod IPs from a private CIDR that is independent of the VNet address space. Node IPs come from the VNet; pod IPs come from a separate overlay network.

**Characteristics:**
- Pod CIDR (default 10.244.0.0/16) is not routable from VNet by default
- Dramatically reduces VNet IP consumption (only node IPs from subnet)
- Supports up to 250 pods per node
- AKS creates a separate pod routing domain without VXLAN encapsulation or tunneling; do not assume overlay MTU overhead
- Compatible with Network Policies (Calico or Cilium)
- Supported from AKS Kubernetes 1.25+

**When to use:**
- Large clusters where VNet IP space is scarce
- Pods do not need direct VNet-routable IPs
- Standard east-west traffic patterns within cluster
- Cost-effective scaling without massive subnet allocation

**Configuration:**
```bash
az aks create \
  --name myCluster \
  --resource-group myRG \
  --network-plugin azure \
  --network-plugin-mode overlay \
  --pod-cidr 10.244.0.0/16 \
  --network-policy calico
```

### Azure CNI Powered by Cilium

AKS supports Cilium as the dataplane for Azure CNI, combining Azure IPAM with Cilium's eBPF-based networking.

**Characteristics:**
- eBPF dataplane replaces iptables for service routing and policy
- Supports Cilium Network Policies (L3/L4/L7)
- Hubble observability built-in
- Compatible with both overlay and VNet-allocated pod IPs
- Replaces kube-proxy with eBPF

**Configuration:**
```bash
az aks create \
  --name myCluster \
  --resource-group myRG \
  --network-plugin azure \
  --network-plugin-mode overlay \
  --network-dataplane cilium \
  --pod-cidr 10.244.0.0/16
```

### Calico

Calico is a widely deployed CNI providing both networking and network policy enforcement. It operates in multiple modes.

**Networking Modes:**
- **VXLAN (overlay):** Encapsulates pod traffic; works anywhere without BGP
- **IP-in-IP (overlay):** Lighter encapsulation; Linux only
- **Native routing (BGP):** No encapsulation; requires BGP peering with network infrastructure
- **Policy-only mode:** Uses another CNI for networking; Calico provides only policy enforcement (common on AKS, EKS)

**Key Features:**
- Full Kubernetes NetworkPolicy support
- Extended Calico NetworkPolicy with namespaceSelector, serviceAccountSelector, HTTP match
- GlobalNetworkPolicy for cluster-wide rules
- eBPF dataplane option (Calico 3.13+)
- WireGuard encryption for pod traffic
- Supports IPv4, IPv6, and dual-stack

**When to use:**
- Need advanced network policies beyond native K8s spec
- Policy-only mode alongside cloud-managed CNI
- On-premises clusters with BGP routing infrastructure
- WireGuard-encrypted pod traffic without service mesh overhead

### Cilium

Cilium is an eBPF-native CNI providing networking, observability, and security.

**Key Features:**
- eBPF dataplane — no iptables, kube-proxy replacement
- L7 network policies (HTTP, gRPC, Kafka, DNS)
- Transparent encryption (WireGuard or IPsec)
- Hubble — built-in observability with flow logs, service map
- ClusterMesh — multi-cluster connectivity
- Host-level firewall policies
- Bandwidth Manager (EDT-based rate limiting)
- Big TCP support for high-throughput workloads

**Networking Modes:**
- **VXLAN/Geneve overlay:** Default; works anywhere
- **Native routing:** Direct routing via cloud provider routes or BGP
- **AWS ENI mode:** Direct integration with AWS VPC ENIs
- **Azure IPAM:** Integration with Azure CNI for IP allocation

**When to use:**
- High-performance networking (eBPF avoids iptables overhead)
- L7 policy enforcement without service mesh
- Built-in observability requirements
- Multi-cluster connectivity (ClusterMesh)
- Large clusters where iptables scale limits apply (>10K services)

### Flannel

Flannel is a simple overlay network focused on basic connectivity.

**Characteristics:**
- VXLAN overlay (default backend)
- Minimal features — networking only, no network policies
- Simple to deploy and operate
- Low resource overhead
- Often paired with Calico for policy (Canal)

**When to use:**
- Development/testing environments
- Simple clusters without network policy requirements
- When operational simplicity is paramount
- Canal (Flannel + Calico) for basic policy needs

### WeaveNet

WeaveNet provides mesh networking with built-in encryption.

**Characteristics:**
- Mesh overlay using VXLAN or sleeve (userspace fallback)
- Built-in encryption (NaCl) — all pod traffic encrypted by default
- Multicast support
- Automatic topology discovery
- Network policy support
- Higher CPU overhead due to encryption

**When to use:**
- Encryption required without service mesh or WireGuard
- Multicast workloads
- Small to medium clusters
- Note: Less actively developed than Calico/Cilium

### AWS VPC CNI

The default CNI for EKS, assigning VPC IPs directly to pods via Elastic Network Interfaces (ENIs).

**Characteristics:**
- Each pod gets a VPC IP from the node's ENI secondary IPs
- Instance type determines max pods (ENI count × IPs per ENI - 1)
- VPC-routable pod IPs — full integration with Security Groups, NACLs, VPC Flow Logs
- Prefix delegation mode: assigns /28 prefixes for higher pod density
- Custom networking: pods use different subnets than nodes
- Security Groups for Pods (SGP): per-pod AWS security groups

**Prefix Delegation:**
```bash
kubectl set env daemonset aws-node -n kube-system ENABLE_PREFIX_DELEGATION=true
kubectl set env daemonset aws-node -n kube-system WARM_PREFIX_TARGET=1
```

### GKE Dataplane V2 (Cilium-based)

GKE's default dataplane for new clusters, built on Cilium.

**Characteristics:**
- eBPF-based dataplane (Cilium under the hood)
- Built-in network policy enforcement and logging
- Network policy logging (shows allowed/denied connections)
- FQDN-based network policies
- Multi-cluster services integration
- No separate CNI installation needed — managed by GKE

**When to use:**
- GKE clusters (enabled by default on new clusters)
- Need policy logging for compliance
- FQDN-based egress policies

## Decision Matrix

| Criteria | Azure CNI Overlay | Calico | Cilium | Flannel | AWS VPC CNI |
|----------|-------------------|--------|--------|---------|-------------|
| **Performance** | High | High | Very High (eBPF) | Medium | High |
| **Network Policy** | Via Calico/Cilium | Full + extended | Full + L7 | None | Via Calico |
| **eBPF Dataplane** | Via Cilium | Optional | Native | No | No |
| **IPAM Flexibility** | Azure-managed | Multiple modes | Multiple modes | Host-local | VPC ENI |
| **Encryption** | Via Cilium | WireGuard | WireGuard/IPsec | No | No |
| **Observability** | Basic | Basic | Hubble (rich) | None | VPC Flow Logs |
| **Multi-cluster** | No | Federation | ClusterMesh | No | No |
| **Operational Complexity** | Low (managed) | Medium | Medium-High | Low | Low (managed) |
| **Max Scale** | 65K pods | 50K+ pods | 50K+ pods | ~5K pods | Instance-limited |

## Cloud-Specific Defaults

### AKS
- **Default CNI:** Azure CNI (traditional) — can choose overlay at creation
- **Default policy engine:** None (must enable Calico or Cilium)
- **Managed option:** Azure CNI powered by Cilium (fully managed eBPF)
- **kubenet:** Legacy option, overlay with limited features (no Windows, no policies)

### EKS
- **Default CNI:** AWS VPC CNI
- **Default policy engine:** None (install Calico or Cilium separately)
- **Alternative:** Can replace VPC CNI entirely with Calico or Cilium (lose VPC integration)
- **Managed add-on:** VPC CNI available as EKS managed add-on

### GKE
- **Default CNI:** GKE Dataplane V2 (Cilium-based) for new clusters
- **Default policy engine:** Built into Dataplane V2
- **Legacy:** kube-proxy + Calico (older clusters)
- **Managed option:** Fully managed — no user CNI installation

## Migration Guidance

### Azure CNI Traditional → Overlay
- AKS supports a forward-only in-place migration from Azure CNI traditional to overlay with `az aks update` when prerequisites in the AKS migration documentation are met.
- Validate the target pod CIDR does not overlap any VNet, peered VNet, on-premises, or service CIDR ranges.
- Treat the change as irreversible for the cluster; plan a maintenance window because node pools may need to be reimaged/recreated and pods drained.

```bash
az aks update \
  --resource-group myRG \
  --name myCluster \
  --network-plugin-mode overlay \
  --pod-cidr 10.244.0.0/16
```

- Use a rebuild/blue-green cluster only when the cluster does not meet the supported in-place migration prerequisites.

### Adding Cilium to Existing Cluster (AKS)
```bash
# Only at cluster creation — cannot retrofit
az aks create \
  --network-dataplane cilium \
  --network-plugin azure \
  --network-plugin-mode overlay
```

### EKS — Adding Calico for Network Policy
```bash
# Install Calico operator
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.0/manifests/tigera-operator.yaml

# Apply Calico installation CR (policy-only mode)
kubectl apply -f - <<EOF
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  kubernetesProvider: EKS
  cni:
    type: AmazonVPC
  calicoNetwork:
    bgp: Disabled
EOF
```

## Troubleshooting Tips

- **IP exhaustion (Azure CNI traditional):** Monitor with `kubectl get nodes -o custom-columns=NAME:.metadata.name,PODS:.status.allocatable.pods`; resize subnet or switch to overlay
- **IP exhaustion (AWS VPC CNI):** Check `WARM_IP_TARGET` and `MINIMUM_IP_TARGET` env vars; enable prefix delegation for higher density
- **CNI binary missing:** Check `/opt/cni/bin/` on node; verify DaemonSet pods running in `kube-system`
- **Pod stuck in ContainerCreating:** Check `kubectl describe pod` for CNI errors; inspect `/var/log/containers/` for CNI plugin logs
- **eBPF verification:** `cilium status` or check eBPF maps with `bpftool`

---

**Analysis only — verify against vendor documentation before applying.**
