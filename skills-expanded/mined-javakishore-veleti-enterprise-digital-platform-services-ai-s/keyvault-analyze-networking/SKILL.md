---
name: keyvault-analyze-networking
description: Analyze Azure Key Vault networking including firewall rules, public network access, private endpoints, private DNS, VNet integration, routing, and connectivity from applications or AKS. Use for connection timeouts, DNS issues, or private-access failures.
---

# Analyze Networking

1. Resolve caller network location and vault network configuration.
2. Inspect public network access, firewall rules, private endpoints, subnet/VNet connectivity, and private DNS resolution.
3. Confirm the vault hostname resolves to the intended endpoint from the workload network.
4. Distinguish DNS, routing, firewall, private endpoint, authentication, and authorization failures.
5. For AKS, correlate with pod/node DNS and network path.
6. Do not enable public access as a troubleshooting shortcut unless explicitly authorized.

## Output
- Network Path
- DNS/Endpoint Findings
- Firewall/VNet Findings
- Failure Layer
- Recommended Action
