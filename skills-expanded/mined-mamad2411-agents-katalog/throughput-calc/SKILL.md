# Throughput Calculations — Skill Definition

## Purpose

Provide precise throughput calculation capabilities accounting for TCP behavior, latency effects, encryption overhead, MTU constraints, and multi-flow aggregation. This skill enables accurate prediction of achievable throughput for cloud networking paths.

## Core Knowledge

### TCP Throughput Formula

#### Basic Formula (BDP-Limited)
```
Max Throughput = TCP Window Size / Round-Trip Time (RTT)

Throughput (bits/sec) = (Window Size in bits) / (RTT in seconds)
Throughput (Mbps) = (Window Size in bytes × 8) / (RTT in ms × 1000)
```

#### Practical Examples
```
Default window 64 KB, RTT 10 ms:
  Throughput = (65,536 × 8) / (0.010) = 52.4 Mbps

Window scaling 1 MB, RTT 10 ms:
  Throughput = (1,048,576 × 8) / (0.010) = 838.9 Mbps

Window scaling 4 MB, RTT 50 ms:
  Throughput = (4,194,304 × 8) / (0.050) = 671.1 Mbps

Window scaling 4 MB, RTT 100 ms:
  Throughput = (4,194,304 × 8) / (0.100) = 335.5 Mbps
```

#### With Packet Loss (Mathis Formula)
```
Throughput ≈ (MSS / RTT) × (1 / √p)

Where:
- MSS = Maximum Segment Size (typically 1,460 bytes)
- RTT = Round-trip time in seconds
- p = packet loss probability

Example: MSS=1460, RTT=50ms, loss=0.1%:
  Throughput = (1460 × 8 / 0.050) × (1 / √0.001) = 7.4 Mbps per flow
```

### Bandwidth-Delay Product (BDP)

#### Definition
```
BDP (bytes) = Bandwidth (bytes/sec) × RTT (seconds)
BDP (bits) = Bandwidth (bits/sec) × RTT (seconds)
```

#### Significance
- BDP represents the amount of data "in flight" on the network path
- TCP window must be ≥ BDP to fully utilize the link
- If TCP window < BDP → Link is underutilized

#### BDP Reference Table

| Link Speed | RTT 5ms | RTT 20ms | RTT 50ms | RTT 100ms | RTT 200ms |
|-----------|---------|----------|----------|-----------|-----------|
| 100 Mbps | 62.5 KB | 250 KB | 625 KB | 1.25 MB | 2.5 MB |
| 1 Gbps | 625 KB | 2.5 MB | 6.25 MB | 12.5 MB | 25 MB |
| 10 Gbps | 6.25 MB | 25 MB | 62.5 MB | 125 MB | 250 MB |
| 100 Gbps | 62.5 MB | 250 MB | 625 MB | 1.25 GB | 2.5 GB |

#### TCP Window Size Requirements
```
Required Window = Target Throughput × RTT

For 1 Gbps at 100ms RTT:
  Window = 1,000,000,000 × 0.100 / 8 = 12.5 MB
  → Requires TCP window scaling (max 1 GB with scale factor 14)
```

### Impact of Latency on Throughput

#### Latency Sources in Cloud
| Component | Typical Latency |
|-----------|----------------|
| Same AZ/zone | 0.5 - 2 ms |
| Cross-AZ (same region) | 1 - 5 ms |
| Cross-region (same continent) | 10 - 50 ms |
| Cross-continent | 60 - 200 ms |
| VPN encryption/decryption | 1 - 5 ms added |
| Azure ExpressRoute (local peering) | 2 - 10 ms |
| Azure ExpressRoute (cross-region) | 10 - 50 ms |
| AWS Direct Connect (same metro) | 1 - 5 ms |
| GCP Interconnect | 1 - 10 ms |
| NAT Gateway processing | 0.1 - 0.5 ms |
| Firewall inspection | 0.5 - 5 ms |
| Load balancer | 0.1 - 1 ms |

#### Throughput vs Latency Table (Single TCP Flow, 4 MB Window)
| RTT | Max Single-Flow Throughput |
|-----|---------------------------|
| 1 ms | 32 Gbps (limited by NIC/path) |
| 5 ms | 6.7 Gbps |
| 10 ms | 3.4 Gbps |
| 20 ms | 1.7 Gbps |
| 50 ms | 671 Mbps |
| 100 ms | 336 Mbps |
| 200 ms | 168 Mbps |

### MTU and Fragmentation Impact

#### Standard MTU Values
| Path Type | MTU | MSS (TCP) |
|-----------|-----|-----------|
| Ethernet (default) | 1,500 bytes | 1,460 bytes |
| VPN/IPsec tunnel | 1,400 bytes (typical) | 1,360 bytes |
| GRE tunnel | 1,476 bytes | 1,436 bytes |
| VXLAN encapsulation | 1,450 bytes | 1,410 bytes |
| Azure VNet (default) | 1,500 bytes | 1,460 bytes |
| Azure VNet (jumbo) | 9,000 bytes (within VNet) | 8,960 bytes |
| AWS VPC | 9,001 bytes (within VPC) | 8,961 bytes |
| GCP VPC | 1,460 bytes (default) | 1,420 bytes |

#### Fragmentation Performance Impact
```
Overhead per fragment:
- IP header: 20 bytes
- Per-packet processing at each hop
- Reassembly buffer at destination
- Retransmission of entire datagram on any fragment loss

Performance degradation from fragmentation:
- ~15-25% throughput loss with moderate fragmentation
- 2× latency for fragments requiring reassembly
- Fragment loss requires retransmission of entire original packet
```

#### Path MTU Discovery (PMTUD)
```
Best Practice:
- Enable PMTUD (DF bit set)
- Ensure ICMP "Fragmentation Needed" (Type 3, Code 4) is not blocked
- If PMTUD fails: manually set MSS clamping at tunnel interfaces
- Azure VPN gateway: MSS clamped to 1350 bytes by default
- GCP default MTU: 1460 bytes (not 1500!) — account for this
```

### Encryption Overhead

#### IPsec Overhead (ESP Tunnel Mode)
```
Per-packet overhead:
- New IP header: 20 bytes
- ESP header: 8 bytes
- ESP trailer: 2-14 bytes (padding to block size)
- ESP auth (ICV): 12-16 bytes (SHA-256 = 16 bytes)
- IV: 8-16 bytes (AES-CBC = 16, AES-GCM = 8)

Total overhead: 50-74 bytes per packet

Effective payload with 1500 MTU:
- Original: 1,460 bytes payload per packet
- IPsec tunnel: ~1,390-1,406 bytes payload per packet
- Efficiency: ~95-96% for large packets
- Efficiency for small packets (100 bytes): ~57-63%
```

#### IPsec CPU Impact
| Algorithm | Throughput (per core, modern CPU) |
|-----------|----------------------------------|
| AES-128-GCM | 10-20 Gbps (hardware AES-NI) |
| AES-256-GCM | 8-15 Gbps (hardware AES-NI) |
| AES-256-CBC + SHA-256 | 3-6 Gbps |
| ChaCha20-Poly1305 | 5-8 Gbps (no AES-NI needed) |

#### TLS Overhead
```
Per-record overhead:
- TLS record header: 5 bytes
- IV (TLS 1.2): 8-16 bytes; (TLS 1.3): 0 bytes (implicit)
- MAC/AEAD tag: 16 bytes
- Padding: 0-255 bytes (TLS 1.2 CBC); 0-255 (TLS 1.3)

Effective overhead: 21-37 bytes per record (TLS 1.2), 21 bytes (TLS 1.3)
Maximum record size: 16,384 bytes

Handshake overhead:
- TLS 1.2: 2 RTT (4 messages before data)
- TLS 1.3: 1 RTT (2 messages before data)
- TLS 1.3 0-RTT: 0 RTT (resumption)
```

#### WireGuard Overhead
```
Per-packet overhead:
- Outer UDP header: 8 bytes
- WireGuard header: 16 bytes
- Poly1305 auth tag: 16 bytes
- Total: 60 bytes (including outer IP header)

Effective MTU: 1,420 bytes (from 1,500 Ethernet MTU)
Performance: 1-4 Gbps per core (varies by implementation)
```

### Azure Accelerated Networking

#### Impact on Throughput
```
Without accelerated networking:
- Virtual switch in hypervisor processes all packets
- CPU overhead limits to ~8-12 Gbps depending on VM size
- Higher latency (100-500 μs added)

With accelerated networking (SR-IOV):
- NIC hardware directly connected to VM
- Up to 100 Gbps (VM size dependent)
- Latency reduced by 50-80% (50-100 μs)
- CPU freed from network processing
```

#### VM Size Network Limits
| VM Size | Max NICs | Max Bandwidth | Accelerated Networking |
|---------|----------|---------------|----------------------|
| Standard_D2s_v5 | 2 | 12.5 Gbps | Yes |
| Standard_D4s_v5 | 2 | 12.5 Gbps | Yes |
| Standard_D8s_v5 | 4 | 12.5 Gbps | Yes |
| Standard_D16s_v5 | 8 | 12.5 Gbps | Yes |
| Standard_D32s_v5 | 8 | 16 Gbps | Yes |
| Standard_D48s_v5 | 8 | 24 Gbps | Yes |
| Standard_D64s_v5 | 8 | 30 Gbps | Yes |
| Standard_D96s_v5 | 8 | 35 Gbps | Yes |

**Note:** Bandwidth is per-VM, shared across all NICs. Bursting above limit possible for short periods.

### Multi-Flow vs Single-Flow Limits

#### Single-Flow Constraints
```
Azure:
- Single TCP flow: up to 10 Gbps (within region, accelerated networking)
- Single flow across VNet peering: up to 10 Gbps
- Single flow through VPN gateway: limited by tunnel crypto processing
- Single flow through Azure Firewall: follows overall SKU limits

AWS:
- Single flow within placement group: up to 10 Gbps (Enhanced Networking)
- Single flow across AZs: 5 Gbps
- Single flow through Transit Gateway: depends on attachment/AZ path and flow hashing; verify current quotas
- Single flow through NAT Gateway: no separate hardcoded per-flow planning value here; size against per-gateway bandwidth, packets-per-second, and per-destination connection quotas

GCP:
- Single flow between VMs (same zone): up to 32 Gbps (with gVNIC, T2D/C3)
- Single flow between zones: 7 Gbps per flow (Tier_1 networking: up to 50 Gbps)
- Per-VM maximum (aggregate): 32-200 Gbps (machine-type dependent)
```

#### Multi-Flow Aggregation
```
Aggregate throughput = N_flows × per_flow_throughput
(up to path/device maximum)

Example: Azure VM Standard_D32s_v5 (16 Gbps limit)
- Single flow at 50ms RTT, 4MB window: 671 Mbps
- Flows needed for line rate: 16,000 / 671 ≈ 24 flows
- With 32 parallel flows: saturates 16 Gbps link
```

### ECMP and Flow Hashing

#### ECMP Throughput Calculation
```
Theoretical aggregate = N_paths × per_path_capacity
Effective aggregate = N_paths × per_path_capacity × utilization_factor

Where utilization_factor accounts for uneven hash distribution:
- 2 paths: ~90-95% efficiency
- 4 paths: ~85-92% efficiency
- 8 paths: ~80-90% efficiency
- 16 paths: ~75-85% efficiency
```

#### Hash Distribution
```
Standard 5-tuple hash (src IP, dst IP, src port, dst port, protocol):
- Elephant flows can create imbalance
- Single src→dst pair on same port always takes same path
- More diverse source/destination pairs = better distribution

Mitigation for imbalance:
- Increase flow diversity (more source ports)
- Use flowlet-based load balancing where available
- Monitor per-path utilization for skew detection
```

### NAT Gateway Throughput

#### Azure NAT Gateway
```
Bandwidth: per NAT gateway resource, not multiplied by public IP count.
- Standard NAT Gateway: up to 50 Gbps per resource.
- StandardV2 NAT Gateway: up to 100 Gbps per resource where available.
SNAT inventory: 64,512 SNAT ports per public IP address; public IP count scales ports, not bandwidth.

SNAT port calculation:
- Use 64,512 ports per public IP for inventory planning.
- Each unique outbound flow consumes source-port capacity against destination IP, destination port, and protocol uniqueness.
- Avoid brittle reuse-timer assumptions in sizing; validate with Azure Monitor metrics and current Azure limits/quotas.
```

#### AWS NAT Gateway
```
Per-NAT Gateway bandwidth: starts at 5 Gbps and scales up to 100 Gbps.
Packet rate: scales from 1 million to 10 million packets per second.
Connections per unique destination: 55,000 simultaneous connections per IPv4 address for each destination IP, destination port, and protocol.
Scaling pattern: deploy one NAT gateway per AZ for resilience and capacity locality; add secondary private IPv4 addresses or additional NAT gateways when per-destination connection capacity is the bottleneck.
Sizing note: verify current AWS Service Quotas and CloudWatch metrics before committing capacity.
```

#### GCP Cloud NAT
```
Per-VM: 7 Gbps (with minimum 1,024 ports per VM)
Minimum ports per VM: 64 (default) to 65,536
Total ports per NAT IP: 64,512
Auto-scaling: adds IPs as port demand grows
Manual allocation: pre-assign IP ranges for predictable SNAT
```

### Load Balancer Throughput and SNAT

#### Azure Load Balancer (Standard)
```
Throughput: Millions of flows, 100 Gbps+ aggregate
Per-flow: Same as VM NIC speed
SNAT ports (outbound rules): 64,000 per frontend IP per backend instance
Default allocation: 1,024 ports per instance (configurable)
Maximum frontend IPs: 600

SNAT port formula:
Required ports = peak_concurrent_connections × 4 (for TIME_WAIT)
Available ports = frontend_IPs × 64,000 / backend_instances
```

#### AWS Network Load Balancer
```
Throughput: Millions of requests/sec, scales automatically
Per-AZ: single static IP, auto-scales backends
Connection idle timeout: 350 seconds (TCP)
No SNAT (preserves client IP by default)
Cross-zone: distributes across all registered targets
```

#### AWS Application Load Balancer
```
Throughput: scales automatically (no fixed limit published)
New connections: 50,000/second (soft limit)
Active connections: 2,000,000 (soft limit)
Rules evaluated: 100 per request (default)
```

#### GCP Load Balancer
```
External TCP/UDP (Network LB): 1M+ requests/sec
Internal TCP/UDP: region-scoped, auto-scales
HTTP(S) LB: Global, auto-scales, no published throughput cap
Per-backend: limited by instance/group capacity
Connection draining timeout: configurable (0-3600 sec)
```

## Practical Calculations

### End-to-End Throughput Estimation
```
Given: 
- Azure VM (D32s_v5, 16 Gbps) in East US
- Connected via ExpressRoute (1 Gbps) to on-premises
- RTT: 15 ms
- TCP window: 2 MB
- Single flow required

Step 1: TCP limit = (2 MB × 8) / 15 ms = 1,068 Mbps
Step 2: ExpressRoute limit = 1,000 Mbps
Step 3: VM limit = 16,000 Mbps

Bottleneck: ExpressRoute circuit (1 Gbps)
Achievable single-flow: MIN(1068, 1000, 16000) = 1,000 Mbps

For multi-flow (10 parallel):
- TCP per flow: 1,068 Mbps (each fills the pipe alone)
- ExpressRoute aggregate: 1,000 Mbps (circuit is the bottleneck regardless)
- Achievable: 1,000 Mbps (circuit-limited)
```

### VPN Throughput with Overhead
```
Given:
- VPN tunnel over internet (50 ms RTT)
- AES-256-GCM encryption
- MTU: 1,400 bytes (after IPsec encapsulation)
- TCP window: 4 MB

Effective MSS: 1,400 - 40 (TCP/IP) = 1,360 bytes
IPsec overhead per packet: ~62 bytes
Efficiency: 1,360 / (1,360 + 62) = 95.6%

TCP throughput (per flow): (4 MB × 8) / 50 ms = 671 Mbps
After encryption efficiency: 671 × 0.956 = 641 Mbps per flow

Gateway limit (VpnGw3): 1,250 Mbps
Flows for line rate: 1,250 / 641 = 2 flows minimum
```

---

**Analysis only — verify against vendor documentation before applying.**
