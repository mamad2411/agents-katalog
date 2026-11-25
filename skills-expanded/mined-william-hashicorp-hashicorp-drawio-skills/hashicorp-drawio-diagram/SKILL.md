---
name: hashicorp-drawio-diagram
description: Use when creating, editing, or analyzing HashiCorp architecture diagrams in draw.io/diagrams.net, especially for Vault, Boundary, Terraform Enterprise, Consul, Nomad, HCP, and HashiCorp platform diagrams. Supports Chrome-based draw.io workflows and native .drawio XML generation using HashiCorp visual conventions.
---

# HashiCorp Draw.io Diagram Skill

Create HashiCorp architecture diagrams as native `.drawio` files, or work in an existing draw.io/diagrams.net Chrome session when the user has opened sample diagrams or a target file.

## Core Workflow

1. Clarify the target product and diagram type:
   - Executive/product architecture
   - Enterprise deployment/placement
   - HCP regional/DR layout
   - Kubernetes integration flow
   - Multi-datacenter replication or failover
   - Logical access, tenancy, and operations flow
2. Load only the needed reference:
   - Product deployment patterns: `references/hashicorp-architecture-patterns.md`
   - Visual conventions from sample draw.io files: `references/hashicorp-drawio-visual-patterns.md`
   - Exact icon/style catalog: `references/hashicorp-icons.md` when it exists
   - For Kubernetes auth teaching diagrams, read the `Vault Kubernetes Auth Concept Style` section in `references/hashicorp-drawio-visual-patterns.md`.
3. Prefer the user's existing draw.io visual grammar when editing an existing file.
4. For new diagrams, generate native `.drawio` XML with stable layout, clean labels, unique cell IDs, and no XML comments.
5. After creating or materially updating any diagram file, open it in draw.io/diagrams.net in Chrome, inspect the rendered canvas visually, identify layout or semantic-flow issues that the XML validator cannot catch, apply any needed XML fixes, then validate again.
6. If Chrome/draw.io is open and the user asks for browser work, inspect the visible file/pages first, then preserve the current library, page structure, and styling.
7. When reopening an edited file in draw.io, confirm the canvas reflects the on-disk XML by checking for a newly added label or structural change. If draw.io shows stale content, open a fresh `https://app.diagrams.net/?src=about` tab, choose Device storage, then open the file from disk again.

## Drawing Principles

- Use left-to-right flow for request, access, provisioning, and integration paths.
- For Vault cluster architecture diagrams, prefer north/south flow: clients at the top, Layer 4 load balancer below, Vault cluster below the load balancer, and storage/snapshots or supporting systems below or adjacent to the cluster.
- Use top-to-bottom or side-by-side regions for DR, replication, and multi-datacenter layouts.
- Use large dashed containers for environments such as HCP, AWS Cloud, VPC, on-prem datacenter, Kubernetes cluster, or HVN.
- Use nested containers for subnets, fault zones, namespaces, clusters, and network boundaries.
- Keep edge labels short: `Access`, `Auth`, `VCS`, `Writes`, `DR Replication`, `Service Mesh`.
- Use orthogonal connectors with connection arrows enabled.
- Keep product names visible under icons; do not rely on icons alone.
- Show HA roles explicitly when important: `Leader/Voting`, `Follower/Voter`, `Active`, `Perf Replica`, `DR`.
- For detailed placement diagrams, draw load-balanced client/API traffic separately from direct server-to-server or replication traffic.
- For L4 load balancers, draw a clean vertical trunk down into the cluster, then branch above the target nodes. Avoid east/west NLB-to-node flows when matching HashiCorp Vault validated design diagrams.
- For backups, audit, and log shipping, make the arrow direction match the data movement: Vault/Raft flows to object storage or SIEM/audit sinks. Auto-unseal and external identity checks may point from Vault toward the dependency.

## Vault on Kubernetes Diagrams

For Vault Enterprise on Kubernetes, prefer a two-page `.drawio` file when the scenario includes both deployment and application consumption:

1. **Physical Kubernetes Deployment**
   - Use north/south flow: clients and apps -> ingress/internal load balancer -> Kubernetes Services -> Vault StatefulSet -> Vault pods -> Raft PVCs -> snapshots/backup.
   - Place a large dashed `Kubernetes cluster` boundary around an `Application namespaces` box and a nested `Namespace: vault` box.
   - Split Kubernetes Services into distinct boxes: `vault` for general API, `vault-active` for active endpoint routing, and `vault-internal`/headless for pod DNS and Raft `:8201`.
   - Show the Vault pods as three or more repeated nodes with explicit roles: active/Raft leader and standby/Raft followers. Put PVC/Raft data directly below each pod and a shared `Integrated Storage / Raft` callout underneath.
   - Keep external dependencies in a separate column, not inside the Vault cluster: KMS/HSM auto-unseal, Kubernetes API TokenReview, and IdP/JWKS.
   - Put audit, SIEM/log collector, Prometheus/Grafana/Alertmanager, snapshot CronJob, and object storage in a bottom `Operations plane` band.
2. **Logical Access and Operations**
   - Use readable lanes from left to right: `Consumers`, `Auth methods`, `Authorization`, `Secret engines`, and `Delivery and targets`.
   - Consumers commonly include Kubernetes workloads, human administrators, CI/CD systems, and external machines.
   - Auth methods commonly include Kubernetes auth, OIDC/SAML, JWT/OIDC, and AppRole/cloud IAM.
   - Keep `Vault roles`, `Vault policies`, and `Authorized Vault token` in the authorization lane. Put `Enterprise namespaces` in a separate horizontal tenancy band below this flow so it does not collide with auth/policy arrows.
   - Show secret engines as separate boxes: KV v2, Database, PKI, Transit, and Cloud/SSH/KMIP.
   - Distinguish secret delivery methods that avoid Kubernetes Secret storage (`Agent Injector`, `CSI`, `direct API`) from methods that sync into Kubernetes Secret (`Vault Secrets Operator`, `External Secrets Operator`).
   - Keep audit logging, telemetry/health, Raft snapshots, and optional performance/DR replication in a bottom operations/resilience band. Do not visually confuse replication with backup.

For conceptual Kubernetes auth diagrams, do not use the full production topology. Use a two-domain teaching layout instead: Kubernetes namespace/workloads on the left, Vault secrets/role/policy/capabilities on the right, with explicit `NS` and `SA` bindings into `Vault Role` and green/red outcomes for authorized vs denied workloads.

## Product Pattern Selection

- **Vault**: Use HA cluster, integrated storage, load balancer, auto-unseal/KMS or HSM, snapshots, audit devices, performance replication, and DR secondary patterns.
- **Boundary**: Use controllers, workers, PostgreSQL, KMS/Vault Transit, API/UI load balancer, and individually addressable workers.
- **Terraform Enterprise**: Use application nodes, optional agents, PostgreSQL, Redis, object storage, VCS, identity provider, and active-active or external-services topologies.
- **Consul**: Use VM server control plane, redundancy zones, service discovery, service mesh, catalog sync, Kubernetes dataplane, and direct Consul server connectivity.
- **Nomad**: Use server cluster, client pools, workload groups, L4 API load balancer, Autopilot redundancy zones, snapshots, audit, and Vault/Consul integrations.
- **HCP**: Use dashed HCP region/HVN boundaries, product cluster boxes, peering/network connectivity, and DR replication between regions.

## Validation Checklist

Before finishing a `.drawio` output:

- All product icons have readable labels.
- The file has been opened in draw.io/diagrams.net in Chrome for human visual review whenever a browser session is available.
- A vision pass has been completed after opening the file; any visual or semantic-flow issues found in Chrome/draw.io have been fixed and the validator has been rerun.
- Containers make ownership and network boundaries obvious.
- HA/failover roles are labeled when shown.
- Client/API traffic, write traffic, backup/audit traffic, replication traffic, and management traffic are visually distinct by label, route, color, and arrow direction.
- No connector crosses through a major icon when an orthogonal route could avoid it.
- For Vault on Kubernetes, API `:8200`, Raft `:8201`, KMS/TokenReview/IdP dependencies, audit, monitoring, and backup are visually separated into obvious lanes or bands.
- All cell IDs are unique.
- Every edge has an `mxGeometry` child.
- XML is well formed and contains no XML comments.
- If using HashiCorp custom icons, verify styles against `references/hashicorp-icons.md` once available.
