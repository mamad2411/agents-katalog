# Skill: Multi-Cluster and Cross-Cluster Networking

## Purpose

Guide the design and implementation of networking between multiple Kubernetes clusters, enabling service discovery, traffic routing, and connectivity across cluster boundaries. Covers open-source solutions (Submariner, Cilium ClusterMesh, Istio multi-cluster) and cloud-managed options (Azure Fleet Manager, GKE Multi-Cluster Services).

## Core Knowledge

### Multi-Cluster Networking Patterns

#### Pattern 1: Flat Network (Shared Pod CIDR Routing)
All clusters share routable pod CIDRs — pods can communicate directly.
- **Pros:** Lowest latency, simplest service-to-service calls
- **Cons:** Requires non-overlapping CIDRs, complex routing, tight coupling
- **Use when:** Clusters in same VPC/VNet, tightly integrated services

#### Pattern 2: Gateway-Based (Ingress/Egress Gateways)
Traffic between clusters flows through dedicated gateways.
- **Pros:** Clusters can have overlapping CIDRs, security boundary at gateway, NAT possible
- **Cons:** Additional hop and latency, gateway becomes bottleneck
- **Use when:** Clusters in different networks, security isolation needed, heterogeneous environments

#### Pattern 3: VPN-Backed (Encrypted Tunnels)
IPsec/WireGuard tunnels connect cluster networks.
- **Pros:** Works across cloud providers, encrypted by default, handles NAT traversal
- **Cons:** Tunnel overhead, bandwidth limits, operational complexity
- **Use when:** Cross-cloud connectivity, compliance requires encryption, clusters in different regions

#### Pattern 4: Service Mesh Federation
Service mesh control planes coordinate across clusters.
- **Pros:** Unified policy, mTLS everywhere, advanced traffic management
- **Cons:** Mesh operational overhead, version coordination
- **Use when:** Already running service mesh, need L7 traffic control across clusters

### Submariner

Submariner connects Kubernetes clusters by establishing encrypted tunnels between them and enabling service discovery across cluster boundaries.

**Architecture:**
- **Broker:** Central coordination point (lightweight, runs in any cluster)
- **Gateway Engine:** Establishes IPsec or WireGuard tunnels (runs on designated gateway nodes)
- **Route Agent:** Programs routes on every node to send cross-cluster traffic to the gateway
- **Lighthouse:** DNS-based cross-cluster service discovery (ServiceImport/ServiceExport)
- **Globalnet:** Handles overlapping cluster CIDRs via global virtual IPs

**Requirements:**
- Non-overlapping pod and service CIDRs (unless using Globalnet)
- Direct connectivity or NAT traversal between gateway nodes
- Designated gateway nodes (labeled `submariner.io/gateway=true`)
- UDP ports 4500 (IPsec NAT-T), 4800 (VXLAN), 8080 (metrics)

**Installation:**
```bash
# Install subctl CLI
curl -Ls https://get.submariner.io | VERSION=0.17.0 bash

# Deploy broker (run once in broker cluster)
subctl deploy-broker --kubeconfig broker-kubeconfig

# Join clusters to the broker
subctl join --kubeconfig cluster-a-kubeconfig broker-info.subm \
  --clusterid cluster-a \
  --natt=false \
  --cable-driver wireguard

subctl join --kubeconfig cluster-b-kubeconfig broker-info.subm \
  --clusterid cluster-b \
  --cable-driver wireguard
```

**Service Discovery with Lighthouse:**
```yaml
# Export a service from cluster-a
apiVersion: multicluster.x-k8s.io/v1alpha1
kind: ServiceExport
metadata:
  name: api-service
  namespace: production
---
# In cluster-b, the service is automatically discoverable as:
# api-service.production.svc.clusterset.local
```

**Verify connectivity:**
```bash
# Status check
subctl show all

# Connectivity test between clusters
subctl diagnose all
subctl verify --context cluster-a --tocontext cluster-b --only connectivity
```

**Globalnet (Overlapping CIDRs):**
```bash
# Enable Globalnet during join
subctl join broker-info.subm \
  --clusterid cluster-a \
  --globalnet \
  --globalnet-cidr 242.0.0.0/16
```

### Cilium ClusterMesh

Cilium ClusterMesh connects multiple Cilium-managed clusters for cross-cluster service discovery and policy enforcement using a shared control plane approach.

**Architecture:**
- Each cluster runs a ClusterMesh API server (etcd-based)
- Cilium agents in each cluster connect to remote ClusterMesh APIs
- Pod identity and services are synchronized across clusters
- eBPF datapath handles cross-cluster routing directly
- No gateway bottleneck — direct pod-to-pod connectivity (with tunnel or native routing)

**Requirements:**
- Cilium installed in all clusters
- Non-overlapping pod CIDRs (mandatory)
- Unique cluster IDs (1-255)
- Network connectivity between clusters (direct, VPN, or peered VNets/VPCs)
- Shared CA for mTLS between clusters

**Enable ClusterMesh:**
```bash
# Cluster 1 - Enable ClusterMesh
cilium clustermesh enable --context cluster-1 --service-type LoadBalancer

# Cluster 2 - Enable ClusterMesh
cilium clustermesh enable --context cluster-2 --service-type LoadBalancer

# Connect clusters
cilium clustermesh connect --context cluster-1 --destination-context cluster-2

# Verify
cilium clustermesh status --context cluster-1
```

**Global Service (Load Balance Across Clusters):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
  namespace: production
  annotations:
    service.cilium.io/global: "true"
    # Share load across clusters
    service.cilium.io/shared: "true"
spec:
  selector:
    app: api
  ports:
    - port: 8080
      protocol: TCP
```

**Service Affinity (Prefer Local Cluster):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
  namespace: production
  annotations:
    service.cilium.io/global: "true"
    service.cilium.io/affinity: "local"
    # Only use remote if local backends are unavailable
spec:
  selector:
    app: api
  ports:
    - port: 8080
```

**Cross-Cluster Network Policy:**
```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-cross-cluster
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: database
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: api
            io.cilium.k8s.policy.cluster: cluster-1
      toPorts:
        - ports:
            - port: "5432"
              protocol: TCP
```

### Istio Multi-Cluster

Istio supports multiple deployment models for multi-cluster service mesh.

**Models:**
1. **Multi-primary:** Each cluster has its own istiod; shared trust domain
2. **Primary-remote:** One cluster runs istiod; remote clusters use it
3. **Multi-network:** Clusters on different networks; east-west gateways required

**Multi-Primary on Different Networks (Most Common):**

```bash
# Shared root CA for cross-cluster mTLS
# Generate intermediate CAs for each cluster from shared root

# Cluster 1 - Install Istio as primary
istioctl install -f cluster1-config.yaml

# Cluster 2 - Install Istio as primary
istioctl install -f cluster2-config.yaml

# Install east-west gateway in each cluster
# This gateway handles cross-cluster traffic
kubectl apply -f samples/multicluster/gen-eastwest-gateway.sh
```

**Cluster 1 IstioOperator:**
```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-cluster1
spec:
  values:
    global:
      meshID: production-mesh
      multiCluster:
        clusterName: cluster-1
      network: network-1
  meshConfig:
    defaultConfig:
      proxyMetadata:
        ISTIO_META_DNS_CAPTURE: "true"
        ISTIO_META_DNS_AUTO_ALLOCATE: "true"
```

**East-West Gateway:**
```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: cross-network-gateway
  namespace: istio-system
spec:
  selector:
    istio: eastwestgateway
  servers:
    - port:
        number: 15443
        name: tls
        protocol: TLS
      tls:
        mode: AUTO_PASSTHROUGH
      hosts:
        - "*.local"
```

**Expose services across clusters:**
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-cross-cluster
  namespace: production
spec:
  hosts:
    - api-service.production.svc.cluster.local
  http:
    - route:
        - destination:
            host: api-service.production.svc.cluster.local
          weight: 80
        # Failover to remote cluster
        - destination:
            host: api-service.production.svc.cluster.local
            subset: cluster-2
          weight: 20
```

### Azure Fleet Manager

Azure Fleet Manager provides centralized multi-cluster management for AKS clusters, including cross-cluster service placement and networking.

**Key Features:**
- Fleet-wide Kubernetes resource propagation
- Multi-cluster service export/import
- Hub-spoke fleet topology
- Consistent configuration across member clusters

```bash
# Create a fleet
az fleet create \
  --resource-group fleet-rg \
  --name my-fleet \
  --location eastus

# Join AKS clusters to fleet
az fleet member create \
  --resource-group fleet-rg \
  --fleet-name my-fleet \
  --name cluster-east \
  --member-cluster-id /subscriptions/.../managedClusters/aks-east

az fleet member create \
  --resource-group fleet-rg \
  --fleet-name my-fleet \
  --name cluster-west \
  --member-cluster-id /subscriptions/.../managedClusters/aks-west
```

**Multi-Cluster Service Export:**
```yaml
# Export service from member cluster
apiVersion: networking.fleet.azure.com/v1alpha1
kind: ServiceExport
metadata:
  name: api-service
  namespace: production
---
# On the fleet hub — define where traffic goes
apiVersion: networking.fleet.azure.com/v1alpha1
kind: MultiClusterService
metadata:
  name: api-service
  namespace: production
spec:
  serviceImport:
    name: api-service
```

### GKE Multi-Cluster Services (MCS)

GKE provides native multi-cluster service discovery and load balancing across GKE clusters in a fleet.

**Setup:**
```bash
# Register clusters to a fleet
gcloud container fleet memberships register cluster-us \
  --gke-cluster us-central1/cluster-us \
  --enable-workload-identity

gcloud container fleet memberships register cluster-eu \
  --gke-cluster europe-west1/cluster-eu \
  --enable-workload-identity

# Enable multi-cluster services
gcloud container fleet multi-cluster-services enable
```

**Export and Import Services:**
```yaml
# Export in source cluster
apiVersion: net.gke.io/v1
kind: ServiceExport
metadata:
  name: api-service
  namespace: production
---
# ServiceImport is auto-created in all fleet clusters
# Access via: api-service.production.svc.clusterset.local
```

**Multi-Cluster Ingress (GKE):**
```yaml
apiVersion: networking.gke.io/v1
kind: MultiClusterIngress
metadata:
  name: global-ingress
  namespace: production
spec:
  template:
    spec:
      backend:
        serviceName: api-service
        servicePort: 8080
      rules:
        - host: api.example.com
          http:
            paths:
              - path: /*
                backend:
                  serviceName: api-service
                  servicePort: 8080
```

### Cross-Cluster DNS

#### Kubernetes MCS DNS Convention
The Multi-Cluster Services API defines a standard DNS format:
```
<service>.<namespace>.svc.clusterset.local
```

#### CoreDNS Configuration for Cross-Cluster
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-custom
  namespace: kube-system
data:
  clusterset.server: |
    clusterset.local:53 {
        forward . 10.96.0.100  # Lighthouse or MCS DNS endpoint
        cache 30
    }
```

#### External DNS for Multi-Cluster
```yaml
# ExternalDNS with weighted records for active-active
apiVersion: externaldns.k8s.io/v1alpha1
kind: DNSEndpoint
metadata:
  name: api-global
  namespace: production
spec:
  endpoints:
    - dnsName: api.example.com
      recordTTL: 60
      recordType: A
      targets:
        - 20.50.100.1    # Cluster 1 ingress IP
        - 34.120.200.1   # Cluster 2 ingress IP
      providerSpecific:
        - name: weight
          value: "50"
```

## Network Connectivity Patterns

### Pattern: VNet/VPC Peering (Same Cloud)

```bash
# Azure VNet peering between AKS clusters
az network vnet peering create \
  --name cluster1-to-cluster2 \
  --resource-group rg-cluster1 \
  --vnet-name vnet-cluster1 \
  --remote-vnet /subscriptions/.../vnets/vnet-cluster2 \
  --allow-vnet-access

# Ensure pod CIDRs don't overlap and are routable
# Azure CNI traditional: pod CIDRs are VNet-routable by default
# Azure CNI overlay: need UDR for cross-cluster pod routing
```

### Pattern: Transit Gateway (AWS Cross-VPC)

```bash
# AWS Transit Gateway for EKS clusters
aws ec2 create-transit-gateway \
  --description "EKS multi-cluster transit"

# Attach VPCs
aws ec2 create-transit-gateway-vpc-attachment \
  --transit-gateway-id tgw-xxx \
  --vpc-id vpc-cluster1 \
  --subnet-ids subnet-xxx

# Add routes for pod CIDRs
aws ec2 create-transit-gateway-route \
  --destination-cidr-block 10.1.0.0/16 \
  --transit-gateway-route-table-id tgw-rtb-xxx \
  --transit-gateway-attachment-id tgw-attach-xxx
```

### Pattern: Cross-Cloud (Azure ↔ AWS)

For connecting clusters across cloud providers:
1. **VPN (IPsec):** Site-to-site VPN between Azure VPN Gateway and AWS VPN
2. **Submariner:** Handles tunneling and service discovery
3. **Cilium ClusterMesh:** With WireGuard tunnels over public endpoints
4. **Istio Multi-Network:** East-west gateways exposed publicly with mTLS

## Decision Matrix: Multi-Cluster Solutions

| Criteria | Submariner | Cilium ClusterMesh | Istio Multi-Cluster | Azure Fleet | GKE MCS |
|----------|------------|-------------------|---------------------|-------------|---------|
| **Cross-cloud** | Yes | Yes | Yes | Azure only | GKE only |
| **Overlapping CIDRs** | Globalnet | No | Via gateways | No | No |
| **L7 Traffic Mgmt** | No | No | Yes (VirtualService) | No | Limited |
| **Service Discovery** | Lighthouse | Built-in | Built-in | ServiceExport | ServiceExport |
| **Encryption** | IPsec/WireGuard | WireGuard | mTLS | VNet-level | VPC-level |
| **Policy Across Clusters** | No | Yes (CiliumNP) | Yes (AuthzPolicy) | Limited | Limited |
| **Prerequisite** | Any K8s | Cilium CNI | Istio mesh | AKS + Fleet | GKE + Fleet |
| **Complexity** | Medium | Medium | High | Low (managed) | Low (managed) |
| **Best For** | Cross-cloud, any CNI | Cilium users, eBPF | Full mesh features | AKS fleet ops | GKE fleet ops |

## Troubleshooting Tips

- **Cross-cluster DNS not resolving:** Check CoreDNS config for `clusterset.local` zone, verify Lighthouse/MCS controller is running, test with `nslookup svc.ns.svc.clusterset.local`
- **Submariner tunnel down:** `subctl diagnose all`, check gateway node firewall rules (UDP 4500, 4800), verify `kubectl get clusters -n submariner-operator`
- **ClusterMesh not syncing:** `cilium clustermesh status`, check etcd connectivity, verify cluster IDs are unique, check CA trust
- **Istio cross-cluster 503:** Verify east-west gateway is reachable, check endpoint discovery (`istioctl proxy-config endpoints`), confirm shared root CA
- **IP conflicts:** Run `subctl diagnose` or verify CIDRs with `kubectl cluster-info dump | grep -i cidr`

---

**Analysis only — verify against vendor documentation before applying.**
