---
name: postgres-analyze-networking
description: Analyze Azure Database for PostgreSQL Flexible Server networking including private access/VNet integration, private endpoints where applicable, public access/firewall, DNS, routing, and application connectivity. Use for connection timeouts or network isolation reviews.
---

# Analyze Networking

1. Identify the server networking mode and application network.
2. Inspect VNet/subnet integration, private DNS, private endpoints where supported/configured, public access, and firewall rules.
3. Trace DNS and routing from the workload to the PostgreSQL endpoint.
4. Distinguish DNS, route, firewall, TLS, authentication, and database failures.
5. Do not enable broad public access as a troubleshooting shortcut.

## Output
- Network Architecture
- DNS/Route Findings
- Access Controls
- Failure Layer
- Recommended Action
