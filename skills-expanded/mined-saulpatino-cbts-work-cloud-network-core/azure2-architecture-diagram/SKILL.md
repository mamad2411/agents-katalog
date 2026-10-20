---
name: azure2-architecture-diagram
description: Generate validated Microsoft Azure architecture diagrams as uncompressed draw.io XML using the built-in Azure2 SVG icon library. Use for Azure cloud, landing-zone, network, application, data, integration, AI, hybrid, migration, resiliency, and CI/CD architecture visuals, including diagrams inferred from Bicep, ARM JSON, Terraform, Azure Developer CLI, Kubernetes, or application repositories. Supports codebase analysis and interactive design, with optional PNG, SVG, or PDF export.
---

# Azure2 Architecture Diagram

Generate professional draw.io diagrams with official Azure2 icons, explicit Azure boundaries, readable data flow, and reusable project-scoped output.

## Workflow

### 1. Determine the mode

Use codebase analysis when the request says analyze, scan, existing project, or from code.

1. Scan Bicep (`*.bicep`, `bicepconfig.json`), ARM JSON (`Microsoft.*` resource types), Terraform (`azurerm_*`, `azapi_*`), `azure.yaml`, Kubernetes manifests, and deployment workflows.
2. Extract subscriptions, resource groups, regions, VNets, subnets, zones, services, identities, private endpoints, dependencies, and data-flow direction.
3. Scan application and platform files for Docker, databases, APIs, messaging, ML, and non-Azure dependencies. Map non-Azure technology with `references/general-icons.md`.
4. Separate discovered facts from inferred recommendations. Confirm material uncertainty before generation.
5. Select the diagram type that best communicates the architecture.

Use brainstorming when the request describes a new system or says design, brainstorm, or from scratch.

1. Ask only questions that materially affect the diagram: purpose, users, data sensitivity, scale, availability target, connectivity, identity, and preferred Azure services.
2. Propose a minimal architecture and data flow.
3. Identify optional reliability, security, and observability additions separately.
4. Generate after the design is accepted, or proceed with clearly stated assumptions when the user asks for an immediate draft.

### 2. Apply presentation choices

- Enable sketch mode only when explicitly requested.
- Add a numbered step legend for seven or more primary services or branching flows unless disabled.
- Produce `.drawio` by default. Export PNG, SVG, or PDF only when requested.
- Use Azure naming current in the source or prompt. Do not silently rename a deployed resource.

### 3. Load generation references

Read these files before writing XML:

1. `references/xml-rules.md`
2. `references/style-guide.md`
3. `references/xml-templates-structure.md`
4. `references/layout-guidelines.md`
5. `references/azure2-icons-services.md`

Read `references/azure2-icons-resources.md` for boundary, resource, and generic component patterns. Read `references/general-icons.md` for mixed-cloud or third-party systems. Use the example table conceptually; do not read the `.drawio` examples unless the user asks to match or modify one.

| Diagram type | Primary example | Secondary example |
| --- | --- | --- |
| Serverless or API | `example-saas-backend.drawio` | `example-event-driven.drawio` |
| Event-driven | `example-event-driven.drawio` | `example-microservices.drawio` |
| Microservices or AKS | `example-microservices.drawio` | `example-complex-platform.drawio` |
| Multi-region | `example-multi-region-active-active.drawio` | - |
| Complex platform | `example-complex-platform.drawio` | `example-saas-backend.drawio` |
| AI agent | `example-foundry-agent-service.drawio` | `example-event-driven.drawio` |
| Sketch | `example-sketch.drawio` | one architecture example |

### 4. Generate XML

1. Create an uncompressed `<mxfile><diagram><mxGraphModel>` document.
2. Use `image=img/lib/azure2/<category>/<File_Name>.svg` for Azure2 icons. Do not use the legacy `mxgraph.azure.*` stencil namespace for current Azure service icons.
3. Put each 48x48 icon inside a 120x120 category container.
4. Connect edges to icon cells, not category containers.
5. Model real boundaries with plain adaptive containers: tenant, management group, subscription, resource group, region, VNet, availability zone, subnet, and AKS cluster.
6. Keep decorative region boundaries non-container (`container=0`) and use absolute coordinates to avoid broken edge routing.
7. Add title and subtitle to every page. Add numbered badges and a right-side legend for complex flows.
8. Write a descriptive kebab-case filename under `./docs/`. Create a new file unless the user explicitly asks to update one.

### 5. Validate and export

Perform deterministic validation before reporting success:

- Parse XML and require one `mxfile`, `diagram`, `mxGraphModel`, `root`, cell `0`, and cell `1`.
- Require unique cell IDs.
- Require every edge source, target, and parent to reference an existing cell.
- Reject compressed diagram bodies and illegal double hyphens inside XML comments.
- Require every `img/lib/azure2/...svg` icon path to be listed in `references/azure2-icons-services.md` or `references/azure2-icons-resources.md`.
- Check that all style attributes include `fontFamily=Helvetica` where text is rendered.
- Check for icon, label, badge, and connector overlap as a visual/manual step; structural XML validation alone is insufficient.

Use `references/cli-export.md` when an export is requested. If draw.io desktop is unavailable, keep the `.drawio` source and state that export was not verified.

## Defaults

- Font: Helvetica
- Grid: off
- Icon: 48x48 inside 120x120 category container
- Gap: 180px horizontal and 120px vertical; use 220px and 160px for 13+ services
- Azure accent: `#0078D4`
- Connector: orthogonal, dark gray, directional
- Dark mode: adaptive `light-dark()` fills on structural elements
- Output: `./docs/<descriptive-name>.drawio`

## Azure boundary model

Use this hierarchy only where it reflects the design:

`Microsoft Entra tenant -> management group -> subscription -> resource group -> region -> VNet -> availability zone -> subnet -> workload`

Do not imply that resource groups or subscriptions are network boundaries. Use VNets/subnets for network isolation and management groups/subscriptions/resource groups for governance scope.

## Diagram types

- Landing zone: management groups, subscriptions, hub-spoke or Virtual WAN, policy, identity, logging
- VNet/network: subnets, NSGs, route tables, NAT Gateway, Firewall, Application Gateway, Load Balancer, private endpoints
- Serverless: Front Door, API Management, Functions, Logic Apps, Event Grid, Service Bus, Cosmos DB, Storage
- Containers: AKS or Container Apps, ACR, ingress, Key Vault, managed identity, monitoring
- Data/analytics: Event Hubs, Data Factory, ADLS, Databricks, Synapse, Fabric or Power BI
- Multi-region: Front Door or Traffic Manager, paired/regional workloads, database replication, failover
- Hybrid: ExpressRoute or VPN, Azure Arc, hub connectivity, private DNS
- AI: Microsoft Foundry, Foundry Agent Service, Azure OpenAI, AI Search, Storage, Cosmos DB, API Management
- CI/CD: GitHub or Azure Repos, Azure Pipelines/GitHub Actions, workload identity federation, ACR, deployment targets

## Critical rules

- Use Azure2 image paths exactly as cataloged; never invent icon paths.
- Prefer current icons and services; mark legacy/classic icons only when the deployed system actually uses them.
- Treat managed identity and private endpoints as relationships/configuration unless their explicit icon materially improves the diagram.
- Do not add Defender for Cloud, Monitor, Key Vault, Log Analytics, or backup solely as decoration. Include them when requested, discovered, or essential to the stated design.
- Do not show a public path to a private endpoint.
- Do not place Azure Firewall as an application-layer WAF; use Application Gateway WAF or Front Door WAF for HTTP(S) inspection.
- Distinguish control-plane flow, deployment flow, user traffic, and data replication with labels or line styles.
- Escape XML attribute characters and keep all IDs unique and descriptive.

## Output report

Report the file path, diagram type, included services, assumptions, structural validation result, visual/export verification status, and concise alt text under 100 characters. Provide a preview URL only when one was actually generated.
