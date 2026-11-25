---
name: azure-diagram
description: Create Azure cloud architecture diagrams in SVG format using official Microsoft Azure icons. Use when the user asks to create, generate, or draw an Azure architecture diagram, cloud diagram, infrastructure diagram, or any visual showing Azure services. Also trigger when user mentions creating diagrams for Azure Fabric, AKS, App Service, Functions, or any Azure service topology.
argument-hint: [description of the architecture] [output-file-path]
allowed-tools: Read, Write, WebFetch, Bash(mkdir *)
---

# Azure Architecture Diagram Generator

You are creating a professional Azure cloud architecture diagram in SVG format.

## User Request

$ARGUMENTS

## Instructions

### Step 1: Understand the Architecture

Parse the user's request to identify:
- Which Azure services are involved
- The data flow / connections between services
- Logical groupings (e.g., networking, compute, data, security)
- The output file path (default: `./azure-architecture.svg` if not specified)

### Step 2: Fetch Official Azure Icons

Fetch the official Microsoft Azure architecture icons from the `benc-uk/icon-collection` GitHub repository. These are the actual icons from the Azure Architecture Icon set.

**Base URL:** `https://raw.githubusercontent.com/benc-uk/icon-collection/master/azure-icons/`

For each Azure service in the diagram, fetch its SVG icon from:

| Service | Filename |
|---------|----------|
| Azure SQL Database | `SQL-Database.svg` |
| Azure Storage | `Storage-Accounts.svg` |
| Blob Storage | `Blob-Block.svg` |
| Cosmos DB | `Azure-Cosmos-DB.svg` |
| Event Hubs | `Event-Hubs.svg` |
| Service Bus | `Service-Bus.svg` |
| Data Factory | `Data-Factory.svg` |
| Azure Synapse Analytics | `Azure-Synapse-Analytics.svg` |
| Azure Functions | `Function-Apps.svg` |
| App Service | `App-Services.svg` |
| API Management | `API-Management-Services.svg` |
| Azure Kubernetes Service | `Kubernetes-Services.svg` |
| Container Instances | `Container-Instances.svg` |
| Container Registry | `Container-Registries.svg` |
| Virtual Machines | `Virtual-Machine.svg` |
| Virtual Networks | `Virtual-Networks.svg` |
| Load Balancer | `Load-Balancers.svg` |
| Application Gateway | `Application-Gateways.svg` |
| Azure Front Door | `Front-Doors.svg` |
| Azure CDN | `CDN-Profiles.svg` |
| Azure DNS | `DNS-Zones.svg` |
| Azure Firewall | `Firewalls.svg` |
| Azure Active Directory / Entra ID | `Azure-Active-Directory.svg` |
| Key Vault | `Key-Vaults.svg` |
| Azure Monitor | `Monitor.svg` |
| Log Analytics | `Log-Analytics-Workspaces.svg` |
| Application Insights | `Application-Insights.svg` |
| Azure Cache for Redis | `Cache-Redis.svg` |
| Azure Search / AI Search | `Search-Services.svg` |
| Cognitive Services / Azure AI | `Cognitive-Services.svg` |
| Azure Bot Service | `Bot-Services.svg` |
| Azure OpenAI | `Cognitive-Services.svg` |
| Notification Hubs | `Notification-Hubs.svg` |
| SignalR | `SignalR.svg` |
| Logic Apps | `Logic-Apps.svg` |
| Event Grid | `Event-Grid-Domains.svg` |
| Stream Analytics | `Stream-Analytics-Jobs.svg` |
| Azure DevOps | `Azure-DevOps.svg` |
| Azure Repos | `Azure-Repos.svg` |
| IoT Hub | `IoT-Hub.svg` |
| Data Lake Storage | `Data-Lake-Store-Gen1.svg` |
| Azure Databricks | `Azure-Databricks.svg` |
| HDInsight | `HDInsight-Clusters.svg` |
| Azure Batch | `Batch-Accounts.svg` |
| Azure Site Recovery | `Recovery-Services-Vaults.svg` |
| Azure Backup | `Recovery-Services-Vaults.svg` |
| Network Security Groups | `Network-Security-Groups.svg` |
| Private Endpoints | `Private-Link.svg` |
| Managed Identities | `Managed-Identities.svg` |
| Azure Policy | `Policy.svg` |

Additional icons for Power BI: `https://raw.githubusercontent.com/microsoft/PowerBI-Icons/main/SVG/Power-BI.svg`

If a specific icon filename returns 404, try variations:
- Add/remove "Azure-" prefix
- Try plural/singular forms
- Check the gallery at `https://code.benco.io/icon-collection/azure-icons/`

### Step 3: Process Fetched Icons

When embedding icons into the diagram SVG:

1. **Namespace all gradient/filter/clipPath IDs** to avoid conflicts. Each icon's internal `id="a"`, `id="b"` etc. MUST be renamed to unique IDs like `sql_a`, `cosmos_a`, `storage_a` etc. Update all `url(#...)` and `fill="url(#...)"` references accordingly.

2. **Place all `<defs>` (gradients, filters, clipPaths)** in a single top-level `<defs>` block in the output SVG.

3. **Scale icons** using `transform="translate(x, y) scale(s)"` on a `<g>` element wrapping each icon's paths. Icons from benc-uk have an 18x18 viewBox, so scale(2) gives ~36px, scale(2.5) gives ~45px icons.

### Step 4: Build the SVG Diagram

Create a complete SVG with:

**Design system (Azure-style):**
- Font: `Segoe UI, Arial, sans-serif`
- Primary blue: `#0078D4`
- Background: `#FAFAFA` or `#F9F9F9`
- Card background: `#fff` with `stroke="#E1DFDD"` and subtle drop shadow
- Section header colors per domain:
  - Networking: `#0078D4` (blue)
  - Compute: `#5C2D91` (purple)
  - Data: `#0078D4` (blue)
  - AI/ML: `#5C2D91` (purple)
  - Security: `#D83B01` (dark orange)
  - Integration: `#F7630C` (orange)
  - DevOps: `#107C10` (green)
  - Monitoring: `#0078D4` (blue)

**Layout structure:**
```
┌─────────────────────────────────────────┐
│ Title Banner (gradient blue header)     │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────┐    ┌──────┐    ┌──────┐      │
│  │ Icon │───>│ Icon │───>│ Icon │      │
│  │ Label│    │ Label│    │ Label│      │
│  └──────┘    └──────┘    └──────┘      │
│       │           │           │         │
│  Grouping boxes with headers            │
│  Flow arrows between components         │
│                                         │
├─────────────────────────────────────────┤
│ Foundation / Infrastructure layer       │
├─────────────────────────────────────────┤
│ Legend                                  │
└─────────────────────────────────────────┘
```

**Each service card pattern:**
```svg
<g transform="translate(x, y)" filter="url(#shadowSm)">
  <rect width="W" height="H" rx="6" fill="#fff" stroke="#E1DFDD"/>
  <!-- Official Azure icon, scaled -->
  <g transform="translate(8, 8) scale(2.2)">
    <!-- icon paths here -->
  </g>
  <text x="52" y="26" fill="#323130" font-size="11" font-weight="600">Service Name</text>
</g>
```

**Standard defs to always include:**
```svg
<filter id="shadow" x="-5%" y="-5%" width="115%" height="115%">
  <feDropShadow dx="1" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.12"/>
</filter>
<filter id="shadowSm" x="-5%" y="-5%" width="115%" height="115%">
  <feDropShadow dx="0" dy="1" stdDeviation="2" flood-color="#000" flood-opacity="0.08"/>
</filter>
<marker id="arrowR" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
  <polygon points="0 0, 8 3, 0 6" fill="#0078D4"/>
</marker>
```

**Flow arrows:** Use `<line>` or `<path>` elements with `marker-end="url(#arrowR)"`, stroke `#0078D4`, stroke-width `1.5`.

**Grouping boxes:** Use rounded `<rect>` with colored header bar + white body, similar to Azure portal resource group visualization.

### Step 5: Write Output

Save the SVG file to the path specified by the user (or default `./azure-architecture.svg`).

### Important Rules

1. **Always fetch real icons** — never use placeholder shapes or hand-drawn approximations.
2. **Always namespace gradient IDs** — icon SVGs reuse generic IDs like `a`, `b` which WILL conflict. Prefix them (e.g., `sql_a`, `cosmos_b`).
3. **Keep the layout clean** — use consistent spacing (16px grid), aligned elements, and clear visual hierarchy.
4. **Include a legend** explaining color coding.
5. **Use proper Azure naming** — "Entra ID" (not just "Azure AD"), "Azure Cosmos DB" (not just "Cosmos"), etc.
6. **Responsive viewBox** — use `viewBox` on the root SVG, no fixed `width`/`height` attributes so it scales.
7. **Show data flow** — use directional arrows to indicate how data/requests move between services.
8. For fetching icons, fetch multiple icons **in parallel** using concurrent WebFetch calls to be efficient.
9. When processing fetched SVG content, extract only the inner elements (paths, rects, circles, etc.) and their defs — strip the outer `<svg>` wrapper.
10. **Handle complex icons carefully** — some icons (like Power BI) have masks and filters that also need ID namespacing.
