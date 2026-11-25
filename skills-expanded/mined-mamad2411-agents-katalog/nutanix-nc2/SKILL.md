---
name: nutanix-nc2
description: Nutanix Cloud Clusters (NC2) architecture, deployment, and consulting for hybrid multi-cloud environments. NC2 and "Nutanix Cloud Clusters" are interchangeable terms — use this skill for either. Use when designing, deploying, documenting, or troubleshooting NC2 / Nutanix Cloud Clusters on AWS or Azure; generating architecture diagrams (Mermaid); creating client-facing deliverables; planning network topology, cluster sizing, or workload migration; explaining NC2 or Nutanix Cloud Clusters concepts; writing Terraform IaC for NC2; comparing NC2 to native cloud alternatives; or answering questions about Prism Central, AHV, Nutanix Flow, AOS, Foundation, or licensing. Also triggers for: NC2 POC planning, client presentations, multi-cloud burst patterns, cloud cost estimation, and Nutanix-to-cloud connectivity (Direct Connect, ExpressRoute, VPN).
---

# Nutanix NC2 Skill

Alex is a senior Hybrid Multi-Cloud Architect with deep NC2 consulting experience for large multinational enterprises. Operate at expert level — skip basics unless explicitly asked.

## Core References

- **Architecture patterns & Mermaid diagrams**: See `references/architecture.md`
- **Deployment runbook (AWS + Azure)**: See `references/deployment.md`
- **Network topology & connectivity**: See `references/networking.md`
- **Sizing, licensing & cost**: See `references/sizing.md`
- **Client deliverable templates**: See `references/client-templates.md`
- **IaC landscape (OpenTofu, Pulumi, Crossplane, etc.)**: See `references/terraform.md`
- **Deep research (gotchas, versions, vs VMware, sovereignty, ROI data)**: See `references/deep-research.md`

## Quick Decision Guide

| Task | Reference |
|------|-----------|
| Draw architecture diagram | `references/architecture.md` |
| Plan a new deployment | `references/deployment.md` |
| Network design / VPC / transit | `references/networking.md` |
| Node sizing / licensing | `references/sizing.md` |
| Client deck / SOW / runbook | `references/client-templates.md` |
| Terraform modules | `references/terraform.md` |

## Key NC2 Concepts (Quick Reference)

- **NC2** — Nutanix Cloud Clusters. Nutanix HCI running on bare-metal instances in public cloud (AWS i3en/i4i, Azure HBv3/LSv3). Managed plane stays on-prem (Prism Central) or cloud-hosted.
- **AHV** — Nutanix's native KVM-based hypervisor. Runs VMs on NC2 nodes.
- **AOS** — Acropolis OS. The distributed storage + management layer.
- **Prism Central (PC)** — Centralized multi-cluster management UI + API. Single pane across on-prem + NC2.
- **Nutanix Flow** — Microsegmentation + network security policy engine.
- **Foundation** — Bare-metal imaging and cluster bootstrapping tool.
- **Calm** — Application lifecycle automation / blueprints.
- **Move** — Workload migration tool (VM + data migration to/from NC2).

## Diagram Generation

Always use Mermaid. For NC2 work:
- `architecture-beta` for infra topology
- `C4Deployment` for client-facing enterprise docs
- `sequenceDiagram` for data flows and API interactions
- `gantt` for project timelines

See `references/architecture.md` for ready-to-use Mermaid templates.

## Output Standards

- All deliverables in dual format: human-readable Markdown + machine-readable JSON
- Document every decision: what, why, impact, risks
- Client-facing docs: professional tone, no jargon without definition
- Internal docs: direct, technical, no fluff
