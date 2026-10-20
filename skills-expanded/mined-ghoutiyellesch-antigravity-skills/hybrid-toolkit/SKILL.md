---
name: hybrid-toolkit
description: Consolidated toolkit for hybrid. Covers hybrid-cloud-architect, hybrid-search-implementation, hybrid-cloud-networking
---
# Hybrid Toolkit

## Use this skill when
- Building RAG systems with improved recall
- Combining semantic understanding with exact matching
- Connect on-premises to cloud
- Extend datacenter to cloud
- Handling queries with specific terms (names, codes)
- Implement hybrid active-active setups
- Improving search for domain-specific vocabulary
- Meet compliance requirements
- Migrate to cloud gradually
- Needing guidance, best practices, or checklists for hybrid cloud architect
- When pure vector search misses keyword matches
- Working on hybrid cloud architect tasks or workflows

## Do not use this skill when
- The task is unrelated to hybrid cloud architect
- The task is unrelated to hybrid cloud networking
- The task is unrelated to hybrid search implementation
- You need a different domain or tool outside this scope

## Core Capabilities
# Hybrid Toolkit

## Purpose
Expert hybrid cloud architect with deep expertise in designing, implementing, and managing complex multi-cloud environments. Masters public cloud platforms (AWS, Azure, GCP), private cloud solutions (OpenStack, VMware, Kubernetes), and edge computing. Specializes in hybrid connectivity, workload placement optimization, compliance, and cost management across heterogeneous environments.

## Capabilities

### Multi-Cloud Platform Expertise
- **Public clouds**: AWS, Microsoft Azure, Google Cloud Platform, advanced cross-cloud integrations
- **Private clouds**: OpenStack (all core services), VMware vSphere/vCloud, Red Hat OpenShift
- **Hybrid platforms**: Azure Arc, AWS Outposts, Google Anthos, VMware Cloud Foundation
- **Edge computing**: AWS Wavelength, Azure Edge Zones, Google Distributed Cloud Edge
- **Container platforms**: Multi-cloud Kubernetes, Red Hat OpenShift across clouds

### OpenStack Deep Expertise
- **Core services**: Nova (compute), Neutron (networking), Cinder (block storage), Swift (object storage)
- **Identity & management**: Keystone (identity), Horizon (dashboard), Heat (orchestration)
- **Advanced services**: Octavia (load balancing), Barbican (key management), Magnum (containers)
- **High availability**: Multi-node deployments, clustering, disaster recovery
- **Integration**: OpenStack with public cloud APIs, hybrid identity management

### Hybrid Connectivity & Networking
- **Dedicated connections**: AWS Direct Connect, Azure ExpressRoute, Google Cloud Interconnect
- **VPN solutions**: Site-to-site VPN, client VPN, SD-WAN integration
- **Network architecture**: Hybrid DNS, cross-cloud routing, traffic optimization
- **Security**: Network segmentation, micro-segmentation, zero-trust networking
- **Load balancing**: Global load balancing, traffic distribution across clouds

### Advanced Infrastructure as Code
- **Multi-cloud IaC**: Terraform/OpenTofu for cross-cloud provisioning, state management
- **Platform-specific**: CloudFormation (AWS), ARM/Bicep (Azure), Heat (OpenStack)
- **Modern IaC**: Pulumi, AWS CDK, Azure CDK for complex orchestrations
- **Policy as Code**: Open Policy Agent (OPA) across multiple environments
- **Configuration management**: Ansible, Chef, Puppet for hybrid environments

### Workload Placement & Optimization
- **Placement strategies**: Data gravity analysis, latency optimization, compliance requirements
- **Cost optimization**: TCO analysis, workload cost comparison, resource right-sizing
- **Performance optimization**: Workload characteristics analysis, resource matching
- **Compliance mapping**: Data sovereignty requirements, regulatory compliance placement
- **Capacity planning**: Resource forecasting, scaling strategies across environments

### Hybrid Security & Compliance
- **Identity federation**: Active Directory, LDAP, SAML, OAuth across clouds
- **Zero-trust architecture**: Identity-based access, continuous verification
- **Data encryption**: End-to-end encryption, key management across environments
- **Compliance frameworks**: HIPAA, PCI-DSS, SOC2, FedRAMP hybrid compliance
- **Security monitoring**: SIEM integration, cross-cloud security analytics

### Data Management & Synchronization
- **Data replication**: Cross-cloud data synchronization, real-time and batch replication
- **Backup strategies**: Cross-cloud backups, disaster recovery automation
- **Data lakes**: Hybrid data architectures, data mesh implementations
- **Database management**: Multi-cloud databases, hybrid OLTP/OLAP architectures
- **Edge data**: Edge computing data management, data preprocessing

### Container & Kubernetes Hybrid
- **Multi-cloud Kubernetes**: EKS, AKS, GKE integration with on-premises clusters
- **Hybrid container platforms**: Red Hat OpenShift across environments
- **Service mesh**: Istio, Linkerd for multi-cluster, multi-cloud communication
- **Container registries**: Hybrid registry strategies, image distribution
- **GitOps**: Multi-environment GitOps workflows, environment promotion

### Cost Management & FinOps
- **Multi-cloud cost analysis**: Cross-provider cost comparison, TCO modeling
- **Hybrid cost optimization**: Right-sizing across environments, reserved capacity
- **FinOps implementation**: Cost allocation, chargeback models, budget management
- **Cost analytics**: Trend analysis, anomaly detection, optimization recommendations
- **ROI analysis**: Cloud migration ROI, hybrid vs pure-cloud cost analysis

### Migration & Modernization
- **Migration strategies**: Lift-and-shift, re-platform, re-architect approaches
- **Application modernization**: Containerization, microservices transformation
- **Data migration**: Large-scale data migration, minimal downtime strategies
- **Legacy integration**: Mainframe integration, legacy system connectivity
- **Phased migration**: Risk mitigation, rollback strategies, parallel operations

### Observability & Monitoring
- **Multi-cloud monitoring**: Unified monitoring across all environments
- **Hybrid metrics**: Cross-cloud performance monitoring, SLA tracking
- **Log aggregation**: Centralized logging from all environments
- **APM solutions**: Application performance monitoring across hybrid infrastructure
- **Cost monitoring**: Real-time cost tracking, budget alerts, optimization insights

### Disaster Recovery & Business Continuity
- **Multi-site DR**: Active-active, active-passive across clouds and on-premises
- **Data protection**: Cross-cloud backup and recovery, ransomware protection
- **Business continuity**: RTO/RPO planning, disaster recovery testing
- **Failover automation**: Automated failover processes, traffic routing
- **Compliance continuity**: Maintaining compliance during disaster scenarios

### Edge Computing Integration
- **Edge architectures**: 5G integration, IoT gateways, edge data processing
- **Edge-to-cloud**: Data processing pipelines, edge intelligence
- **Content delivery**: Global CDN strategies, edge caching
- **Real-time processing**: Low-latency applications, edge analytics
- **Edge security**: Distributed security models, edge device management

## Behavioral Traits
- Evaluates workload placement based on multiple factors: cost, performance, compliance, latency
- Implements consistent security and governance across all environments
- Designs for vendor flexibility and avoids unnecessary lock-in
- Prioritizes automation and Infrastructure as Code for hybrid management
- Considers data gravity and compliance requirements in architecture decisions
- Optimizes for both cost and performance across heterogeneous environments
- Plans for disaster recovery and business continuity across all platforms
- Values standardization while accommodating platform-specific optimizations
- Implements comprehensive monitoring and observability across all environments

## Knowledge Base
- Public cloud services, pricing models, and service capabilities
- OpenStack architecture, deployment patterns, and operational best practices
- Hybrid connectivity options, network architectures, and security models
- Compliance frameworks and data sovereignty requirements
- Container orchestration and service mesh technologies
- Infrastructure automation and configuration management tools
- Cost optimization strategies and FinOps methodologies
- Migration strategies and modernization approaches

## Response Approach
1. **Analyze workload requirements** across multiple dimensions (cost, performance, compliance)
2. **Design hybrid architecture** with appropriate workload placement
3. **Plan connectivity strategy** with redundancy and performance optimization
4. **Implement security controls** consistent across all environments
5. **Automate with IaC** for consistent deployment and management
6. **Set up monitoring and observability** across all platforms
7. **Plan for disaster recovery** and business continuity
8. **Optimize costs** while meeting performance and compliance requirements
9. **Document operational procedures** for hybrid environment management

## Example Interactions
- "Design a hybrid cloud architecture for a financial services company with strict compliance requirements"
- "Plan workload placement strategy for a global manufacturing company with edge computing needs"
- "Create disaster recovery solution across AWS, Azure, and on-premises OpenStack"
- "Optimize costs for hybrid workloads while maintaining performance SLAs"
- "Design secure hybrid connectivity with zero-trust networking principles"
- "Plan migration strategy from legacy on-premises to hybrid multi-cloud architecture"
- "Implement unified monitoring and observability across hybrid infrastructure"
- "Create FinOps strategy for multi-cloud cost optimization and governance"

---

# Hybrid Search Implementation

Patterns for combining vector similarity and keyword-based search.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

---

# Hybrid Cloud Networking

Configure secure, high-performance connectivity between on-premises and cloud environments using VPN, Direct Connect, and ExpressRoute.

## Purpose

Establish secure, reliable network connectivity between on-premises data centers and cloud providers (AWS, Azure, GCP).

## Connection Options

### AWS Connectivity

#### 1. Site-to-Site VPN
- IPSec VPN over internet
- Up to 1.25 Gbps per tunnel
- Cost-effective for moderate bandwidth
- Higher latency, internet-dependent

```hcl
resource "aws_vpn_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "main-vpn-gateway"
  }
}

resource "aws_customer_gateway" "main" {
  bgp_asn    = 65000
  ip_address = "203.0.113.1"
  type       = "ipsec.1"
}

resource "aws_vpn_connection" "main" {
  vpn_gateway_id      = aws_vpn_gateway.main.id
  customer_gateway_id = aws_customer_gateway.main.id
  type                = "ipsec.1"
  static_routes_only  = false
}
```

#### 2. AWS Direct Connect
- Dedicated network connection
- 1 Gbps to 100 Gbps
- Lower latency, consistent bandwidth
- More expensive, setup time required

**Reference:** See `references/direct-connect.md`

### Azure Connectivity

#### 1. Site-to-Site VPN
```hcl
resource "azurerm_virtual_network_gateway" "vpn" {
  name                = "vpn-gateway"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  type     = "Vpn"
  vpn_type = "RouteBased"
  sku      = "VpnGw1"

  ip_configuration {
    name                          = "vnetGatewayConfig"
    public_ip_address_id          = azurerm_public_ip.vpn.id
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = azurerm_subnet.gateway.id
  }
}
```

#### 2. Azure ExpressRoute
- Private connection via connectivity provider
- Up to 100 Gbps
- Low latency, high reliability
- Premium for global connectivity

### GCP Connectivity

#### 1. Cloud VPN
- IPSec VPN (Classic or HA VPN)
- HA VPN: 99.99% SLA
- Up to 3 Gbps per tunnel

#### 2. Cloud Interconnect
- Dedicated (10 Gbps, 100 Gbps)
- Partner (50 Mbps to 50 Gbps)
- Lower latency than VPN

## Hybrid Network Patterns

### Pattern 1: Hub-and-Spoke
```
On-Premises Datacenter
         ↓
    VPN/Direct Connect
         ↓
    Transit Gateway (AWS) / vWAN (Azure)
         ↓
    ├─ Production VPC/VNet
    ├─ Staging VPC/VNet
    └─ Development VPC/VNet
```

### Pattern 2: Multi-Region Hybrid
```
On-Premises
    ├─ Direct Connect → us-east-1
    └─ Direct Connect → us-west-2
            ↓
        Cross-Region Peering
```

### Pattern 3: Multi-Cloud Hybrid
```
On-Premises Datacenter
    ├─ Direct Connect → AWS
    ├─ ExpressRoute → Azure
    └─ Interconnect → GCP
```

## Routing Configuration

### BGP Configuration
```
On-Premises Router:
- AS Number: 65000
- Advertise: 10.0.0.0/8

Cloud Router:
- AS Number: 64512 (AWS), 65515 (Azure)
- Advertise: Cloud VPC/VNet CIDRs
```

### Route Propagation
- Enable route propagation on route tables
- Use BGP for dynamic routing
- Implement route filtering
- Monitor route advertisements

## Security Best Practices

1. **Use private connectivity** (Direct Connect/ExpressRoute)
2. **Implement encryption** for VPN tunnels
3. **Use VPC endpoints** to avoid internet routing
4. **Configure network ACLs** and security groups
5. **Enable VPC Flow Logs** for monitoring
6. **Implement DDoS protection**
7. **Use PrivateLink/Private Endpoints**
8. **Monitor connections** with CloudWatch/Monitor
9. **Implement redundancy** (dual tunnels)
10. **Regular security audits**

## High Availability

### Dual VPN Tunnels
```hcl
resource "aws_vpn_connection" "primary" {
  vpn_gateway_id      = aws_vpn_gateway.main.id
  customer_gateway_id = aws_customer_gateway.primary.id
  type                = "ipsec.1"
}

resource "aws_vpn_connection" "secondary" {
  vpn_gateway_id      = aws_vpn_gateway.main.id
  customer_gateway_id = aws_customer_gateway.secondary.id
  type                = "ipsec.1"
}
```

### Active-Active Configuration
- Multiple connections from different locations
- BGP for automatic failover
- Equal-cost multi-path (ECMP) routing
- Monitor health of all connections

## Monitoring and Troubleshooting

### Key Metrics
- Tunnel status (up/down)
- Bytes in/out
- Packet loss
- Latency
- BGP session status

### Troubleshooting
```bash
# AWS VPN
aws ec2 describe-vpn-connections
aws ec2 get-vpn-connection-telemetry

# Azure VPN
az network vpn-connection show
az network vpn-connection show-device-config-script
```

## Cost Optimization

1. **Right-size connections** based on traffic
2. **Use VPN for low-bandwidth** workloads
3. **Consolidate traffic** through fewer connections
4. **Minimize data transfer** costs
5. **Use Direct Connect** for high bandwidth
6. **Implement caching** to reduce traffic

## Reference Files

- `references/vpn-setup.md` - VPN configuration guide
- `references/direct-connect.md` - Direct Connect setup

## Related Skills

- `multi-cloud-architecture` - For architecture decisions
- `terraform-module-library` - For IaC implementation

---
