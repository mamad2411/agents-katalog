---
name: azure-topology-style
description: Create or review generic Azure architecture, hub-and-spoke network, resource hierarchy, and CI/CD diagrams using a self-contained semantic palette, containers, resource cards, connectors, tokens, and line-art sprite.
---

# Azure Topology Style

Use a restrained Microsoft Learn-like visual language to make Azure ownership, containment, traffic, and delivery flow legible. Load only the assets in this skill; do not assume another diagram package exists.

## Start from topology, not decoration

1. Inventory resources with ARM type, logical owner, scope, network placement, and dependencies.
2. Nest Subscription, Resource Group, VNet, and Subnet envelopes accurately.
3. Map every resource to one semantic family through `assets/tokens.json`.
4. Draw only relationships needed to answer the diagram's question.
5. Label connector intent and direction; do not rely on color alone.
6. Use generic placeholders unless the user supplies publishable names.

## Visual contract

- Use a white canvas, sharp container corners, and restrained shadows only on resource cards.
- Use dashed neutral boundaries for logical governance containers.
- Use solid Azure-blue borders for VNets and dashed Azure-blue borders for Subnets.
- Use Segoe UI or the system sans-serif stack for labels and a monospace stack for resource names.
- Use orthogonal connectors with round caps and visible arrow direction.
- Keep connector labels on the longest segment with a white halo or background.
- Do not use emoji or vendor service-logo artwork. Use the included line-art sprite or a labeled shape.

## Semantic families

Each resource belongs to one primary family:

| Family | Typical members |
| --- | --- |
| compute | App Service, Functions, Container Apps, AKS, virtual machines |
| data | SQL, Cosmos DB, Storage, Redis, analytics stores |
| identity | Key Vault, managed identity, application identity |
| integration | API Management, Front Door, gateways, messaging, events |
| network | VNet, Subnet, NSG, private endpoint, DNS, firewall |
| monitor | Application Insights, Log Analytics, alerts, dashboards |
| governance | Subscription, Resource Group, policy, locks |
| devops | repository, build, artifact, approval, deployment |

Use `resource_type_family` in `assets/tokens.json` for ARM-family mapping. When a type is missing, select the closest stable operational family and document the addition rather than inventing a one-off color.

## Containers and resource cards

Nest containers in this order when each level exists:

```text
Subscription
└── Resource Group
    └── VNet
        └── Subnet
            └── Resource card
```

Use hub and spoke modifiers on VNet containers to communicate network roles. A resource card contains one line-art icon, a concise name, the Azure service type, and optional status or private-endpoint badge. The badge communicates attachment; explain the actual connection with a connector or nearby note.

## Connector semantics

Use line pattern, arrow, label, and color together:

| Intent | Style |
| --- | --- |
| application dependency | solid blue, one-way arrow |
| network peering | solid dark blue, bidirectional arrows |
| data access | solid green, one-way arrow |
| secret or identity flow | dashed amber, open arrow |
| event or queue | dotted purple, one-way arrow |
| telemetry | dashed indigo, open arrow |
| delivery flow | solid magenta, one-way arrow |
| approval gate | dashed amber, one-way arrow |

Avoid crossing unrelated cards. Prefer left-to-right reading for application and delivery flows, and put shared hub services between spokes.

## Hub-and-spoke vocabulary

- Place shared connectivity, inspection, or DNS capabilities in the hub.
- Place application workloads in spokes.
- Show VNet peering as bidirectional network connectors.
- Show each Subnet inside its owning VNet; do not imply containment with proximity alone.
- Mark private endpoint attachment at the target resource and draw the data path from the source.
- Add Subscription and Resource Group boundaries only when ownership or scope matters.

See [hub-spoke.html](examples/hub-spoke.html) for a generic composition.

## CI/CD vocabulary

Represent delivery as composable stages rather than a mandated branching policy:

```text
source → validation/build → artifact → approval (when required) → deployment target
```

Use distinct cards for repository, build, artifact, approval, and deployment. Label automatic versus gated transitions explicitly. Environment and branch names remain user inputs; the style does not prescribe them.

See [cicd.html](examples/cicd.html) for a generic flow and [reference.html](examples/reference.html) for the palette and primitives.

## Assets and provenance

- `assets/tokens.css` provides the rendered components.
- `assets/tokens.json` is the machine-readable palette, mapping, and connector contract.
- `assets/azure-icons.svg` is the approved self-authored, Lucide-style line-art sprite.
- Individual Azure service icon files are intentionally not packaged.

See [PROVENANCE.md](PROVENANCE.md) for the asset boundary and digest.

## Review checklist

- Containment matches Azure scope and network ownership.
- Every resource has one semantic family and an accessible text label.
- Connectors expose direction and intent without depending on color alone.
- Hub/spoke and CI/CD composition reflects supplied facts without inventing policy.
- Examples and diagrams resolve only package-local tokens and sprite assets.
- Placeholder and published names contain no private identifiers.
