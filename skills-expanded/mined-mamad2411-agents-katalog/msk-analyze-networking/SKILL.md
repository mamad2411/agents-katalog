---
name: msk-analyze-networking
description: Analyze Amazon MSK VPC networking, subnets, security groups, DNS, PrivateLink or multi-VPC private connectivity, bootstrap brokers, routes, and client connectivity. Use for connection failures, cross-VPC access, or network isolation reviews.
---

# Analyze Networking

1. Resolve cluster VPC/subnets, client network, security groups, DNS, and bootstrap endpoints.
2. Inspect routing and security-group paths between clients and MSK.
3. Evaluate private connectivity or multi-VPC connectivity where configured.
4. Distinguish DNS, routing, TLS, authentication, and broker failures.
5. Check cross-account/cross-VPC assumptions explicitly.
6. Do not open broad network access as a troubleshooting shortcut.

## Output
- Network Path
- Endpoint/DNS Findings
- Security Group/Route Findings
- Failure Layer
- Recommended Action
