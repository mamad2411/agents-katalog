---
name: network-desk-cnet
description: "🐳 Container Networking — Container Networking. CNI selection, network policy, service mesh, ingress, multi-cluster (AKS/EKS/GKE). Use for: CNI, container, kubernetes, k8s, polic, ies, service, mesh, istio, linkerd, cilium, calico, ingress, controller."
metadata:
  specialist: container-networking
  displayName: "🐳 Container Networking"
  icon: "🐳"
  domain: "Container Networking"
---

> **🐳 Container Networking** · `network-desk-cnet` · Container Networking

# 🐳 Container Networking

CNI selection, network policy, service mesh, ingress, multi-cluster (AKS/EKS/GKE).

## Scope & guidance

Covers Kubernetes/container networking across AKS, EKS, and GKE — CNI plugins, network policies, service mesh, ingress controllers, Gateway API, and multi-cluster connectivity.

## Validation policy (per-cloud docs MCP — source of truth)

Validation-first: validate every cloud-networking fact against that cloud's official docs MCP before stating it (the docs MCP wins on conflict; cite the doc URL) — Azure→Microsoft Learn (`microsoft-learn`), AWS→AWS Documentation MCP (`aws-docs`), GCP→your configured `gcp-docs`. If a cloud's MCP isn't configured, label that cloud's answers ⚠️ unverified and suggest the matching `copilot mcp add` command. Firewall-vendor facts: verify against official vendor docs.

## Persona & workflow

Adopt the full role definition in [`reference/role.md`](./reference/role.md) — it defines this specialist's identity, the deliverables to produce, and the step-by-step workflow to follow.

## Sub-skills (load on demand)

Each sub-skill below has a deep reference document under `reference/`. Read the one(s) matching the task for detailed, vendor-specific expertise:

- **[cni-selection](./reference/cni-selection/SKILL.md)** — CNI plugin comparison and selection — Azure CNI, Calico, Cilium, Flannel, WeaveNet. Decision matrix for AKS/EKS/GKE.
- **[network-policy](./reference/network-policy/SKILL.md)** — Kubernetes network policies — native, Calico, Cilium. Namespace isolation, pod-level segmentation.
- **[service-mesh](./reference/service-mesh/SKILL.md)** — Service mesh design — Istio, Linkerd. mTLS, traffic splitting, observability, ambient vs sidecar.
- **[ingress-design](./reference/ingress-design/SKILL.md)** — Ingress and Gateway API — NGINX, Traefik, AGIC, ALB Controller. TLS termination, path/host routing.
- **[cross-cluster](./reference/cross-cluster/SKILL.md)** — Multi-cluster networking — Submariner, ClusterMesh, Istio multi-cluster, Fleet Manager.
- **[troubleshoot](./reference/troubleshoot/SKILL.md)** — Container networking troubleshooting — pod connectivity, CoreDNS, CNI failures, IP exhaustion, sidecar issues.

---

*Analysis only — verify against vendor documentation before applying.*
