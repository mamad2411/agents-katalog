---
name: cloud-zerotrust-prisma
description: "Cloud Zerotrust Prisma."
domain: cybersecurity
---

|
| Prisma Access | Palo Alto's cloud-delivered SASE platform providing FWaaS, SWG, CASB, DLP, and ZTNA from a single architecture |
| ZTNA Connector | VM-based connector establishing IPSec tunnels from internal networks to Prisma Access for private application access |
| GlobalProtect | Endpoint agent providing secure connectivity to Prisma Access with HIP checks and always-on VPN |
| Host Information Profile (HIP) | Device posture checks evaluating endpoint security state (EDR, encryption, patches) before granting access |
| Strata Cloud Manager | Unified management console for Prisma Access, NGFW, and Prisma Cloud security policy |
| Cortex Data Lake | Cloud-based log storage and analytics platform for Palo Alto security telemetry |

## Tools & Systems

- **Prisma Access**: Cloud-delivered SASE with integrated ZTNA, SWG, CASB, DLP, FWaaS
- **Strata Cloud Manager (SCM)**: Unified policy management across Palo Alto security products
- **GlobalProtect Agent**: Endpoint connectivity agent with HIP data collection
- **ZTNA Connector**: Outbound-only tunnel connector for internal application access
- **Cortex Data Lake**: Centralized log storage with analytics and threat detection
- **WildFire**: Cloud-based malware analysis and prevention integrated with Prisma Access

## Common Scenarios

### Scenario: Enterprise SASE Migration for 5,000-User Organization

**Context**: A manufacturing company with 5,000 users across 15 offices is consolidating VPN, SWG, and branch firewalls into Prisma Access SASE. Users access 50+ internal applications and need consistent security regardless of location.

**Approach**:
1. Deploy ZTNA Connectors at 3 data centers (2 per DC for HA) for internal application access
2. Configure GlobalProtect with pre-logon connection for always-on security
3. Define 50+ application definitions in SCM with FQDN and port mappings
4. Create HIP profiles: Standard (encryption + AV), Enhanced (+ CrowdStrike + patches)
5. Build security policies mapping user groups to applications with HIP requirements
6. Enable threat prevention profiles (Anti-Spyware, Anti-Virus, WildFire, URL Filtering)
7. Deploy GlobalProtect agent via SCCM to all 5,000 endpoints in phases
8. Configure Cortex Data Lake forwarding to Splunk for SOC monitoring
9. Decommission VPN concentrators and branch firewall appliances

**Pitfalls**: ZTNA Connector requires minimum 4 vCPU and 8GB RAM; under-provisioning causes latency. GlobalProtect pre-logon requires machine certificates for authentication before user login. HIP check intervals should be 60 seconds minimum to avoid performance impact. Plan for a 4-6 week pilot before full deployment.

## Output Format

```
Prisma Access ZTNA Deployment Report
==================================================
Organization: ManufactureCorp
Deployment Date: 2026-02-23

INFRASTRUCTURE:
  ZTNA Connectors: 6 (2x DC-East, 2x DC-West, 2x DC-EU)
  Prisma Access Locations: 8 (auto-selected)
  GlobalProtect Portal: portal.manufacturecorp.com

APPLICATION ACCESS:
  Defined Applications: 52
  Active ZTNA Connections: 3,247
  Average Latency: 12ms

ENDPOINT DEPLOYMENT:
  GlobalProtect Deployed: 4,812 / 5,000 (96.2%)
  HIP Compliant: 4,567 / 4,812 (94.9%)
  HIP Failures: 245 (top: missing patches 120, encryption 85)

SECURITY (last 30 days):
  Threats Blocked: 1,234
  DLP Violations: 89
  URL Blocked: 45,678
  WildFire Submissions: 2,345
```
