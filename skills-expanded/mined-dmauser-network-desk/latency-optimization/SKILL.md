# Latency Optimization — Cross-Cloud Performance Engineering

## Overview

Cross-cloud latency is a primary concern for applications with components distributed across Azure, AWS, and GCP. This skill covers peering locations, backbone vs. internet transit, CDN strategies, expected latencies, measurement methodology, and optimization techniques.

## Peering Locations — Major Exchange Points

Cross-cloud private connectivity is established at colocation facilities where multiple cloud providers maintain points of presence (PoPs). Selecting the right peering location is critical for minimizing latency:

| Metro | Facility | Azure ER | AWS DX | GCP Interconnect | Notes |
|---|---|---|---|---|---|
| **Ashburn, VA** | Equinix DC1-DC15 | ✓ | ✓ | ✓ | Largest peering hub globally; Northern Virginia metro |
| **Dallas, TX** | Equinix DA1-DA7 | ✓ | ✓ | ✓ | Central US coverage |
| **Silicon Valley, CA** | Equinix SV1-SV5, CoreSite SV1 | ✓ | ✓ | ✓ | West Coast primary |
| **Amsterdam** | Equinix AM1-AM7 | ✓ | ✓ | ✓ | Europe primary |
| **London** | Equinix LD4-LD8 | ✓ | ✓ | ✓ | UK and Europe |
| **Singapore** | Equinix SG1-SG4 | ✓ | ✓ | ✓ | Southeast Asia primary |
| **Tokyo** | Equinix TY1-TY11 | ✓ | ✓ | ✓ | Japan and East Asia |
| **Sydney** | Equinix SY1-SY5 | ✓ | ✓ | ✓ | Australia/Oceania |
| **Global (Megaport)** | Megaport MCR (30+ metros) | ✓ | ✓ | ✓ | Virtual router, no physical cross-connect needed |
| **Hong Kong** | PCCW, Equinix HK1-HK5 | ✓ | ✓ | ✓ | Greater China access |

When selecting a peering location, ensure all target cloud providers have on-ramps at that facility. Co-locating cross-connects in a single metro eliminates inter-metro latency from the cross-cloud path.

## Backbone Routing vs. Internet Transit

**Private Backbone (Interconnect):** Traffic traverses the cloud provider's private backbone and the colocation fabric. Path is deterministic, latency is consistent, and jitter is minimal. The route does not cross the public internet at any point. This is the preferred path for latency-sensitive workloads.

**Internet Transit (VPN):** Traffic exits one cloud via a public IP, traverses multiple ISP networks and internet exchange points, and enters the other cloud via a public IP. Path is non-deterministic — latency varies with internet congestion, routing changes, and peering policies. Jitter can be significant (±5–20ms).

**Performance Impact:** For the same source-destination metro (e.g., Ashburn), private backbone latency is typically 0.5–2ms while internet transit latency ranges from 3–15ms with higher variance. For cross-continent paths, the difference can exceed 50ms.

## CDN and Edge Caching

For application traffic that tolerates caching, CDN services reduce effective latency by serving content from edge PoPs close to end users:

- **Azure Front Door** — Global L7 load balancer with integrated CDN, WAF, and SSL offload. Anycast-based routing to nearest PoP. Supports dynamic site acceleration (DSA) for non-cacheable content.
- **AWS CloudFront** — Global CDN with 450+ PoPs. Supports Lambda@Edge for compute at the edge. Origin can be ALB, S3, or custom origin.
- **GCP Cloud CDN** — Integrated with Google's global HTTP(S) load balancer. Uses Google's edge network (140+ PoPs). Supports cache keys, signed URLs, and origin shields.

For cross-cloud architectures, place CDN at the edge tier of whichever cloud serves end users, with origins pointing to backend services in other clouds via private interconnects.

## Expected Latencies for Common Cross-Cloud Paths

These are approximate round-trip times (RTT) based on typical production measurements:

| Path | Connection Type | Expected RTT |
|---|---|---|
| Azure East US ↔ AWS us-east-1 (same metro: N. Virginia) | Private Interconnect | 1–2ms |
| Azure East US ↔ AWS us-east-1 | VPN (internet) | 3–10ms |
| Azure West US 2 ↔ GCP us-west1 | Private Interconnect | 2–4ms |
| Azure West Europe ↔ AWS eu-west-1 | Private Interconnect | 4–8ms |
| AWS us-east-1 ↔ GCP us-east1 (same metro) | Private Interconnect | 1–3ms |
| Azure East US ↔ GCP europe-west1 | Private Interconnect | 70–85ms |
| AWS us-east-1 ↔ AWS ap-southeast-1 | AWS backbone | 200–230ms |
| Any cross-cloud, cross-continent | VPN (internet) | 80–300ms (variable) |

**Note:** Same-metro cross-cloud latency via private interconnect is comparable to intra-cloud cross-AZ latency (typically 1–2ms). This makes region co-location the single most impactful optimization.

## Measurement Methodology

### traceroute / mtr

Use `traceroute` or `mtr` (My Traceroute) to identify the path and per-hop latency between cloud instances:

```bash
# Linux MTR (combined traceroute + ping)
mtr --report --report-cycles=100 --tcp --port=443 <target-ip>

# Windows traceroute
tracert -d <target-ip>

# TCP-based traceroute (avoids ICMP filtering)
tcptraceroute <target-ip> 443
```

### Cloud-Native Tools

```bash
# Azure: Network Watcher connectivity check
az network watcher test-connectivity \
  --source-resource <vm-resource-id> \
  --dest-address <target-ip> \
  --dest-port 443

# AWS: Reachability Analyzer
aws ec2 create-network-insights-path \
  --source <eni-source> \
  --destination <eni-dest> \
  --protocol TCP \
  --destination-port 443

# GCP: Connectivity Tests
gcloud network-management connectivity-tests create cross-cloud-test \
  --source-instance=projects/<project>/zones/<zone>/instances/<vm> \
  --destination-ip-address=<target-ip> \
  --destination-port=443 \
  --protocol=TCP
```

### Continuous Monitoring

Deploy lightweight probes (e.g., Prometheus blackbox exporter, ThousandEyes, Catchpoint) in each cloud to continuously measure cross-cloud RTT, jitter, and packet loss. Set alerts on latency thresholds (e.g., >5ms for same-metro interconnect, >100ms for cross-continent).

## Optimization Techniques

**Region Co-Location:** Deploy workloads that communicate frequently in the same metro across clouds (e.g., Azure East US + AWS us-east-1 + GCP us-east4, all in Northern Virginia). This is the single most effective optimization, reducing cross-cloud RTT to 1–3ms.

**Backbone Preference:** Use private interconnects instead of VPN for production traffic. Configure BGP route preferences to prefer interconnect paths over VPN fallback paths (lower MED or higher local preference for interconnect-learned routes).

**TCP Optimization:** For high-latency cross-cloud paths, tune TCP parameters to improve throughput:

```bash
# Increase TCP window size for high-bandwidth-delay paths
sysctl -w net.core.rmem_max=16777216
sysctl -w net.core.wmem_max=16777216
sysctl -w net.ipv4.tcp_rmem="4096 87380 16777216"
sysctl -w net.ipv4.tcp_wmem="4096 65536 16777216"

# Enable TCP BBR congestion control (better for long-distance)
sysctl -w net.core.default_qdisc=fq
sysctl -w net.ipv4.tcp_congestion_control=bbr
```

**Application-Level Optimization:** Use gRPC with connection pooling instead of REST for high-frequency cross-cloud calls. Implement read replicas and caches close to consumers to reduce cross-cloud data fetches. Batch API calls to reduce round-trip overhead.

**DNS Optimization:** Use low-TTL DNS records and health-checked routing to steer traffic to the lowest-latency path. Configure DNS resolvers in each cloud to forward to local endpoints rather than crossing cloud boundaries for name resolution.

**Analysis only — verify against vendor documentation before applying.**
