---
name: network-desk-capabilities
description: "🧭 Network Desk Capabilities — overview and index of all 20 cloud-networking specialists (with emoji icons) plus example prompts. Load this whenever the user asks what Network Desk can do, its capabilities, the list of specialists/skills, or for examples of how to use the plugin."
metadata:
  displayName: "🧭 Network Desk Capabilities"
  icon: "🧭"
---

# 🧭 Network Desk — Capabilities

When the user asks what Network Desk can do, its capabilities, or for examples, **reproduce the table and example prompts below verbatim, keeping every emoji icon.** Do not drop the icons or collapse specialists down to bare `network-desk-*` ids.

**20 cloud-networking specialists** spanning Azure, AWS, GCP and 14 firewall vendors — analysis-only (no changes are applied).

| Specialist | Domain | What it does |
| --- | --- | --- |
| 🏗️ VNet/Subnet Architect | VNet/Subnet Architecture | CIDR/IP planning, hub-spoke, peering, subnet math, topology diagrams (ASCII console default; Mermaid/Excalidraw/draw.io on request) |
| 🔥 Firewall Engineer | Firewall Engineering | Rule audits, policy design/test, vendor migration, config gen, HA, log analysis (14 vendors) |
| ⚖️ Load Balancer | Load Balancing | L4/L7 selection, health probes, TLS offload/certs, WAF rules, routing, troubleshooting |
| 🌐 DNS Specialist | DNS | Zone/resolver design, DNSSEC, record audits, migrations, resolution debugging |
| 🔒 Private Link Engineer | Private Link / Endpoints | Endpoint design, private DNS integration, service exposure, security review |
| 🔗 Hybrid Connectivity | Hybrid Connectivity | VPN, ExpressRoute/Direct Connect, BGP, bandwidth, failover/redundancy |
| 🛡️ Network Security | Network Security | NSG/SG audits, segmentation, Zero Trust, WAF, DDoS, compliance (CIS/NIST/PCI) |
| 🔧 Network Troubleshooter | Network Troubleshooting | Connectivity tests, packet capture, PCAP analysis, latency, routing, NAT, MTU, TLS |
| 🌍 Virtual WAN / SD-WAN | Virtual WAN / SD-WAN | vWAN/secured-hub design, routing intent, NVA, branch connectivity |
| 📊 Network Monitor | Network Monitoring | Flow logs, traffic analytics, connection/synthetic monitors, alerts, dashboards |
| ☁️ Multi-Cloud Networking | Multi-Cloud Networking | Transit design, cross-cloud addressing, service mapping, latency/cost comparison |
| 💰 Pricing Analyst | Network Pricing | Egress/VPN/circuit/LB/firewall pricing, cross-cloud cost compare & optimization |
| 📐 IaC Generator | IaC Generator | Bicep, Terraform, Ansible, ARM for networking resources |
| 🐳 Container Networking | Container Networking | CNI selection, network policy, service mesh, ingress, multi-cluster (AKS/EKS/GKE) |
| 🌐 CDN & Edge Networking | CDN & Edge Networking | Front Door/CloudFront/Cloud CDN, edge routing, caching, edge WAF |
| 🔄 Network Automation & GitOps | Network Automation & GitOps | CI/CD pipelines, drift detection, policy-as-code, testing, rollback |
| 🛡️ SASE / SSE | SASE / SSE | SASE architecture, ZTNA, SWG/CASB, SD-WAN integration, vendor comparison |
| 📏 Network Capacity Planning | Network Capacity Planning | Bandwidth forecasting, gateway sizing, throughput, scalability, growth |
| 🔢 IPv6 Migration | IPv6 Migration | Dual-stack design, transition planning, addressing, NAT64/DNS64, troubleshooting |
| 📄 Report Builder | Documentation & Reporting | Polished MD/HTML/PDF/DOCX reports & XLSX models from any specialist's findings |

## Example prompts

- 🏗️ "Plan a /16 hub-and-spoke address space for 3 spokes with no overlap."
- 🔥 "Audit my Azure Firewall policy and migrate the rules to FortiGate."
- ⚖️ "Compare Application Gateway vs Front Door for L7 with WAF."
- 🌐 "Design a private DNS resolver setup for hybrid name resolution."
- 🔗 "Set up a Private Endpoint for Azure Storage with private DNS."
- 🔐 "Run a Zero Trust segmentation review of my NSGs against NIST."
- 🛠️ "Troubleshoot intermittent TCP resets between two VNets."
- 💰 "Estimate monthly egress + VPN cost for 5 TB cross-region traffic."
- 📄 "Turn the analysis above into a polished PDF report."

Just describe your goal in plain language — the **Network Desk** coordinator routes to the right specialist automatically. For a polished deliverable, do the analysis with a specialist first, then ask the 📄 Report Builder to package it.

_Analysis only — verify against vendor documentation before applying._
