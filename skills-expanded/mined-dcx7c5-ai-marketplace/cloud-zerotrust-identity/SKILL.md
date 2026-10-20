---
name: cloud-zerotrust-identity
description: "Cloud Zerotrust Identity."
domain: cybersecurity
---

|
| Identity-Aware Proxy | GCP service that intercepts web requests and TCP connections, authenticating users and evaluating access policies before proxying to backend services |
| Backend Service | GCP load balancer component that IAP protects; can serve Compute Engine instances, GKE pods, Cloud Run services, or App Engine |
| IAP Tunnel | Secure TCP tunnel through IAP allowing SSH, RDP, and other TCP access to VMs without public IPs or VPN |
| OAuth Consent Screen | GCP configuration specifying the application name and support email shown to users during IAP authentication |
| Access Level | Named condition in Access Context Manager evaluated during IAP authorization (device posture, IP, geography) |
| Re-authentication | IAP feature requiring users to prove their identity again after a configurable session duration |

## Tools & Systems

- **Google Cloud IAP**: Identity-aware reverse proxy for GCP applications and TCP services
- **Access Context Manager**: Defines access levels based on device, network, and geographic attributes
- **gcloud CLI**: Command-line tool for configuring IAP, access levels, and IAM bindings
- **IAP TCP Forwarding**: Tunnel-based access to VMs for SSH/RDP without public IPs
- **Cloud Audit Logs**: Immutable records of all IAP access decisions for compliance
- **Endpoint Verification**: Chrome extension collecting device attributes for access level evaluation

## Common Scenarios

### Scenario: Securing 15 Internal GCP Services with IAP

**Context**: An e-commerce company runs 15 internal services on GKE and Cloud Run (admin dashboards, internal APIs, monitoring tools). Currently, these services are protected only by VPN and firewall rules, creating excessive network-level access.

**Approach**:
1. Deploy all services behind an HTTPS Load Balancer with managed SSL certificates
2. Enable IAP on each backend service with per-service OAuth clients
3. Create IAM bindings mapping Google Groups to specific services (admin group -> admin dashboard, engineering -> monitoring)
4. Define access levels: managed-device (encryption + screen lock), corp-network (office IP ranges)
5. Apply managed-device access level to admin dashboard and financial tools
6. Configure IAP TCP tunneling for SSH access to GKE nodes (replacing SSH bastion host)
7. Set re-authentication to 4 hours for admin tools, 8 hours for monitoring
8. Configure Cloud Audit Logs and create alerting for repeated denials

**Pitfalls**: IAP adds 10-50ms latency per request; test application performance. WebSocket connections through IAP require specific backend service configuration. Service-to-service calls within GKE should bypass IAP using internal service mesh, not external IAP endpoints. Break-glass access should use a separate IAM binding without access level conditions.

## Output Format

```
Google Cloud IAP Configuration Report
==================================================
Project: ecommerce-internal
Report Date: 2026-02-23

IAP-PROTECTED SERVICES:
  Backend Services:     12
  App Engine:            1
  Cloud Run:             2
  IAP TCP Tunnels:       4 (SSH access)
  Total:                19

ACCESS CONTROL:
  IAM Bindings:         34
  With Access Levels:   18 (52.9%)
  Access Levels:         3 (managed-device, corp-network, high-trust)

SESSION POLICIES:
  Admin tools:          4h re-auth (SECURE_KEY)
  Sensitive apps:       4h re-auth (LOGIN)
  General tools:        8h re-auth (LOGIN)

ACCESS LOGS (last 24h):
  Total requests:       23,456
  Authenticated:        23,289 (99.3%)
  Denied by IAM:           112
  Denied by access level:   55
  Unique users:            134
```
