---
name: architecture
description: "Generate professional .drawio architecture diagrams with Azure and AWS icons via the drawio MCP server and save them to the customer repo's architecture/ folder. Triggers include: 'architecture diagram', 'draw architecture', 'create diagram', 'architecture for customer', 'network topology', 'diagram this architecture', 'draw this in drawio', or any request to produce a visual architecture diagram for a customer engagement."
---

# /architecture — Architecture Diagram Generator

Create professional architecture diagrams using the Draw.io MCP server
(`drawio/create_diagram`) with verified Azure and AWS icons, and save them to
the customer engagement repo's `architecture/` folder.

## Platform Compatibility

This skill runs on **macOS, Linux, and Windows**. Detect the OS first and pick the right syntax. See `_shared/PLATFORM.md` (skills repo root) for the full reference.

| Action | macOS / Linux (bash) | Windows (PowerShell) |
|--------|----------------------|----------------------|
| Make dir | `mkdir -p X` | `New-Item -ItemType Directory -Force -Path X \| Out-Null` |
| Search file content | `grep -i "pattern" file` | `Select-String -Pattern "pattern" -Path file` |
| Home dir | `~` or `$HOME` | `$HOME` |

Note: the icon-catalog grep examples in this skill use bash. On Windows PowerShell, substitute `Select-String -Pattern "<pattern>" -Path "$HOME/.copilot/skills/drawio-mcp-diagramming/references/<catalog>.txt"`.

## Core Principles

- **Customer-scoped output.** All diagrams are saved to `~/customer-engagements/{slug}/architecture/` with a descriptive filename and committed to git.
- **Azure-first defaults.** Default to Azure icons and patterns unless the user specifies AWS or multi-cloud. Azure2 image-based icons are the primary style.
- **Preserve bilingual labels.** Section headings are always English. Service labels and annotations stay in their original language — do not translate content.
- **Verified icons only.** Never use an icon path or shape name in a diagram unless it has been confirmed by grepping the static catalogs. Unverified icons will not render.
- **Clean before dense.** Start with a clean, readable layout (3-4 lanes, left-to-right flow). Add detail only when the user explicitly asks.

## Prerequisite Auto-Install

Before running, verify all dependencies are present. **Install anything missing automatically.**

### Required Sibling Skills

This skill requires the following sibling skill from the same repository
(`https://github.com/roie9876/clawpilot-skills`):

| Skill | Purpose | Required? |
|-------|---------|-----------|
| `/customer-repo` | Customer engagement folder structure (`~/customer-engagements/`) | ✅ For storing diagrams |

Check if it is installed:

```bash
# macOS / Linux
[ -f "$HOME/.copilot/skills/customer-repo/SKILL.md" ] && echo "✅ customer-repo" || echo "❌ customer-repo MISSING"
```

```powershell
# Windows
if (Test-Path "$HOME\.copilot\skills\customer-repo\SKILL.md") { "✅ customer-repo" } else { "❌ customer-repo MISSING" }
```

**If missing**, install all skills from the repository:

1. Clone the repo (skip if already cloned):
   ```bash
   # macOS / Linux
   [ -d "$HOME/customer-skills/.git" ] || git clone https://github.com/roie9876/clawpilot-skills.git "$HOME/customer-skills"
   ```
   ```powershell
   # Windows
   if (-not (Test-Path "$HOME\customer-skills\.git")) {
       git clone https://github.com/roie9876/clawpilot-skills.git "$HOME\customer-skills"
   }
   ```

2. Run the installer (idempotent — safe to re-run):
   ```bash
   # macOS / Linux
   bash "$HOME/customer-skills/scripts/install.sh"
   ```
   ```powershell
   # Windows
   pwsh "$HOME\customer-skills\scripts\install.ps1"
   ```

3. Verify installed. If still missing, stop and report the error.

### Required Tools

| Tool | Check (POSIX) | Check (Windows) | Install (macOS) | Install (Windows) |
|------|---------------|-----------------|-----------------|-------------------|
| git | `git --version` | `Get-Command git` | Pre-installed | `winget install Git.Git` |

### Draw.io MCP Server

This skill requires the Draw.io MCP server. Check if the `drawio/create_diagram` tool is available.
If not: add the MCP server in Clawpilot settings → MCP Servers → URL: `https://mcp.draw.io/mcp`.

---

## Step 1: Understand the Architecture

Ask the user to describe the architecture they want to diagram, or accept it directly from the prompt (e.g., "/architecture hub-spoke network for Contoso").

Gather:
- What services and components are involved?
- What is the primary flow (data pipeline, request path, network topology)?
- Which cloud provider? (Default: Azure. Support AWS and multi-cloud.)
- Any specific requirements? (VNet isolation, traffic labels, compliance zones)

If the user provides a text description or whiteboard sketch, extract the components and flows from it.

## Step 2: Identify Cloud Provider and Icon Library

Determine which icon library to use:

| Provider | Icon Library | Catalog File | Style Pattern |
|----------|-------------|-------------|---------------|
| **Azure** (default) | Azure2 SVG images | `~/.copilot/skills/drawio-mcp-diagramming/references/azure2-complete-catalog.txt` | `image;aspect=fixed;html=1;points=[];align=center;image=img/lib/azure2/<category>/<Icon>.svg;` |
| **AWS** | AWS4 stencil shapes | `~/.copilot/skills/drawio-mcp-diagramming/references/aws4-complete-catalog.txt` | `shape=mxgraph.aws4.<shape_name>;fillColor=<color>;fontColor=#ffffff;strokeColor=none;` |
| **Multi-cloud** | Both catalogs | Grep both as needed | Mix styles per provider |

**Important style differences:**
- Azure icons are **SVG images** — use `image=img/lib/azure2/...` style.
- AWS icons are **stencils** — use `shape=mxgraph.aws4.<name>` style. Do NOT use `image=img/lib/aws4/...`.

## Step 3: Look Up and Verify Icon Paths

For every service in the diagram, grep the appropriate static catalog to find the correct icon path. **This is a hard gate — never guess icon paths.**

### Azure Icon Lookup

```bash
grep -i "gateway" ~/.copilot/skills/drawio-mcp-diagramming/references/azure2-complete-catalog.txt
grep -i "virtual_machine\|load_balancer\|key_vault" ~/.copilot/skills/drawio-mcp-diagramming/references/azure2-complete-catalog.txt
```

Azure icon style template:
```
image;aspect=fixed;html=1;points=[];align=center;image=img/lib/azure2/<category>/<Icon_Name>.svg;
```

If local rendering fails, use absolute URL fallback:
```
image;aspect=fixed;html=1;points=[];align=center;image=https://raw.githubusercontent.com/jgraph/drawio/dev/src/main/webapp/img/lib/azure2/<category>/<Icon_Name>.svg;
```

### AWS Icon Lookup

```bash
grep -i "lambda" ~/.copilot/skills/drawio-mcp-diagramming/references/aws4-complete-catalog.txt
grep -i "load_balancing\|cloudfront\|route_53" ~/.copilot/skills/drawio-mcp-diagramming/references/aws4-complete-catalog.txt
```

AWS icon style template with service color conventions:
```
shape=mxgraph.aws4.<shape_name>;fillColor=<color>;fontColor=#ffffff;strokeColor=none;
```

AWS fill color conventions:
| Category | Fill Color |
|----------|-----------|
| Compute (orange) | `#ED7100` |
| Storage (green) | `#3F8624` |
| Database (red) | `#C7131F` |
| Networking (purple) | `#8C4FFF` |
| Security (red) | `#DD344C` |
| Management (pink) | `#E7157B` |
| General/generic (dark) | `#232F3E` |

### Validation Rule

If an icon path or shape name **cannot** be confirmed in the catalog:
1. Do NOT use it in the diagram.
2. Grep for alternatives (try partial names, synonyms).
3. If no match exists, use a generic rectangle with a text label instead.

## Step 4: Build the mxGraphModel XML

Construct a valid `mxGraphModel` XML payload using the verified icons.

### XML Wrapper Format

Every .drawio file uses this outer structure:

```xml
<mxfile host="app.diagrams.net" modified="2026-01-01T00:00:00.000Z" agent="architecture-skill" version="24.0.0" type="device">
  <diagram id="architecture" name="Architecture">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1200" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- Diagram content here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### General Layout Rules

- **Canvas sizing:** Use `pageWidth="1600" pageHeight="1200"` for standard diagrams. Use `pageWidth="1900" pageHeight="1500"` for complex infrastructure/network topologies.
- **Icon sizing:** Use `width="64" height="64"` for service icons (or `width="48" height="48"` for compact layouts).
- **Labels:** Keep concise — service name + role (e.g., "App Gateway\n(WAF v2)"). Use `whiteSpace=wrap;html=1;` for multi-line.
- **Edges:** Use `edgeStyle=orthogonalEdgeStyle` for clean routing. Label with flow semantics (protocols, ports, data types).
- **Cell IDs:** Use descriptive IDs (e.g., `id="app-gateway"`, `id="subnet-app"`) for readability.

## Step 5: Apply Network Topology Patterns (if applicable)

For infrastructure and network diagrams, apply these professional patterns.

### Azure Network Topology

**VNet styling:**
- VNets: Thick borders (`strokeWidth=4`), large containers
  - DMZ VNet: Yellow (`fillColor=#fff2cc`, `strokeColor=#d6b656`)
  - Internal VNet: Green (`fillColor=#d5e8d4`, `strokeColor=#82b366`)
  - Management Zone: Blue (`fillColor=#dae8fc`, `strokeColor=#6c8ebf`)

**Subnet styling:**
- Dashed borders (`strokeWidth=2`, `dashed=1`, `dashPattern=8 8`)
- Position inside VNet containers
- Lighter shades of parent VNet color
- Label with subnet name and CIDR (e.g., "Application Subnet - 10.x.2.0/24")
- Delegated subnets: add delegation info (e.g., "PostgreSQL Subnet - 10.x.4.0/24 (Delegated)")

**Resource positioning:**
- All resources **inside their respective subnet containers**
- VMs, databases, load balancers visually contained within subnets
- This clearly shows network isolation boundaries

**Traffic flow labeling:**
- HTTPS:443 → red thick arrows for internet ingress
- HTTP:8080/8090 → gold arrows for backend pools
- PostgreSQL:5432 → blue dashed arrows for database connections
- NFS/Gluster → green arrows for shared storage
- RBAC/Identity → orange dashed arrows for management

**Required boxes:**
1. **Traffic Legend** (bottom-left): All traffic types with color-coded arrows and protocol/port info. Use thick bordered white box (`strokeWidth=3`).
2. **Network Isolation Explanation** (top-left): Visual conventions — VNets thick borders, subnets dashed borders, NSGs, private DNS. Use yellow background (`fillColor=#fff9cc`).
3. **Zone Separation**: VNet Peering Zone (grey `#f5f5f5`), External Services Zone (orange `#ffe6cc`).

**Azure topology example:**
```xml
<mxGraphModel pageWidth="1900" pageHeight="1500">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <!-- VNet Container -->
    <mxCell id="vnet-internal" value="Internal VNet - 10.x.0.0/16"
      style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;verticalAlign=top;fontSize=16;fontStyle=1;align=center;strokeWidth=4;"
      vertex="1" parent="1">
      <mxGeometry x="220" y="580" width="1340" height="820" as="geometry"/>
    </mxCell>
    <!-- Subnet inside VNet -->
    <mxCell id="subnet-app" value="Application Subnet - 10.x.2.0/24"
      style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e6f4ea;strokeColor=#82b366;verticalAlign=top;fontSize=13;fontStyle=1;align=center;strokeWidth=2;dashed=1;dashPattern=8 8;"
      vertex="1" parent="vnet-internal">
      <mxGeometry x="40" y="70" width="480" height="340" as="geometry"/>
    </mxCell>
    <!-- Resource inside subnet -->
    <mxCell id="vm-app" value="App VM"
      style="image;aspect=fixed;html=1;points=[];align=center;image=img/lib/azure2/compute/Virtual_Machine.svg;"
      vertex="1" parent="subnet-app">
      <mxGeometry x="40" y="70" width="64" height="59" as="geometry"/>
    </mxCell>
    <!-- Labeled traffic edge -->
    <mxCell id="edge-db" value="PostgreSQL:5432"
      style="edgeStyle=orthogonalEdgeStyle;strokeWidth=2;strokeColor=#6c8ebf;dashed=1;"
      edge="1" source="vm-app" target="postgres" parent="1"/>
  </root>
</mxGraphModel>
```

### AWS Network Topology

**VPC styling:**
- VPCs: Thick borders (`strokeWidth=4`)
  - Production: Green (`fillColor=#d5e8d4`, `strokeColor=#82b366`)
  - Development: Blue (`fillColor=#dae8fc`, `strokeColor=#6c8ebf`)
  - Shared Services: Yellow (`fillColor=#fff2cc`, `strokeColor=#d6b656`)

**Subnet styling:**
- Dashed borders (`strokeWidth=2`, `dashed=1`, `dashPattern=8 8`)
  - Public Subnets: Light green (`fillColor=#e6f4ea`, `strokeColor=#82b366`)
  - Private Subnets: Light blue (`fillColor=#EFF7FF`, `strokeColor=#6c8ebf`)
  - Isolated Subnets (databases): Light orange (`fillColor=#fff3e0`, `strokeColor=#e6821e`)
- Label with subnet name, AZ, and CIDR (e.g., "Public Subnet A - us-east-1a - 10.x.1.0/24")
- Use Availability Zone containers (light grey) inside VPCs

**Traffic flow labeling:**
- HTTPS:443 → red thick arrows for internet ingress via ALB/CloudFront
- Port 5432/3306 → blue dashed arrows for DB connections
- HTTPS:443 → green arrows for VPC Endpoints / AWS service calls
- SSH:22 / SSM → orange dashed for management / Bastion access

**Required boxes:**
1. **Traffic Legend** (bottom-left): Traffic types with color-coded arrows
2. **Network Isolation Explanation** (top-left): VPCs, subnets, Security Groups, NACLs, VPC Endpoints
3. **Zone Separation**: Internet/Edge Zone (orange), VPC Peering / Transit Gateway Zone (grey), AWS Managed Services Zone (purple)

**AWS topology example:**
```xml
<mxGraphModel pageWidth="1900" pageHeight="1500">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <!-- VPC Container -->
    <mxCell id="vpc-prod" value="Production VPC - 10.x.0.0/16"
      style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;verticalAlign=top;fontSize=16;fontStyle=1;align=center;strokeWidth=4;"
      vertex="1" parent="1">
      <mxGeometry x="220" y="200" width="1340" height="1100" as="geometry"/>
    </mxCell>
    <!-- Public Subnet -->
    <mxCell id="subnet-pub-a" value="Public Subnet A - us-east-1a - 10.x.1.0/24"
      style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e6f4ea;strokeColor=#82b366;verticalAlign=top;fontSize=12;fontStyle=1;align=center;strokeWidth=2;dashed=1;dashPattern=8 8;"
      vertex="1" parent="vpc-prod">
      <mxGeometry x="40" y="80" width="550" height="200" as="geometry"/>
    </mxCell>
    <!-- ALB stencil -->
    <mxCell id="alb" value="ALB"
      style="shape=mxgraph.aws4.application_load_balancer;fillColor=#8C4FFF;fontColor=#ffffff;strokeColor=none;align=center;html=1;"
      vertex="1" parent="subnet-pub-a">
      <mxGeometry x="40" y="50" width="64" height="64" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>
```

## Step 6: Create the Diagram via MCP

Call the drawio MCP server to generate the diagram:

```
drawio/create_diagram
```

Pass the complete `mxGraphModel` XML as the input. The MCP server validates the XML and produces the diagram.

**Before calling the tool, verify:**
- [ ] All icon paths confirmed against the appropriate catalog
- [ ] XML is well-formed (no unclosed tags, proper escaping)
- [ ] Cell IDs are unique across the diagram
- [ ] Parent-child relationships are correct (resources inside subnets inside VNets/VPCs)

## Step 7: Save to Customer Repo

1. **Detect the customer** from the conversation context or ask.
2. **Compute the output path:**
   ```
   ~/customer-engagements/{slug}/architecture/{descriptive-name}.drawio
   ```
   Where `{descriptive-name}` is a lowercase, hyphenated description of the diagram content.

   **File naming examples:**
   - `network-topology.drawio`
   - `data-pipeline.drawio`
   - `hub-spoke-network.drawio`
   - `microservices-architecture.drawio`
   - `event-driven-pipeline.drawio`

3. **Create the directory if needed:**

   ```bash
   # macOS / Linux / WSL / Git Bash
   mkdir -p "$HOME/customer-engagements/{slug}/architecture"
   ```

   ```powershell
   # Windows PowerShell
   New-Item -ItemType Directory -Force -Path "$HOME/customer-engagements/{slug}/architecture" | Out-Null
   ```

4. **Check if the file exists** — If it does, read it and ask the user whether to overwrite, create a versioned copy (e.g., `network-topology-v2.drawio`), or skip.

5. **Write the .drawio file** using the full `<mxfile>` wrapper (see Step 4 XML wrapper format).

6. **Commit to git:**
   ```bash
   cd ~/customer-engagements/{slug}
   git add architecture/{descriptive-name}.drawio
   git commit -m "architecture: add {descriptive-name} diagram"
   ```

   If the repo is not a git repo or the commit fails, inform the user but do not fail — the diagram file is still written.

## Visual Quality Guardrails

Apply these defaults unless the user explicitly asks for a dense or technical view:

- **3-4 major lanes/zones max** (e.g., Source, Pipeline, Cloud target).
- **Left-to-right primary flow** with a single main path.
- **Stage numbering** (`1`, `2`, `3`, `4`) instead of many edge labels.
- **One icon per major service** — avoid icon-per-step layouts.
- **Limit cross-lane lines** to one security/auth line and one optional telemetry line.
- **Concise text** — single purpose per box, no multiline overload.
- **Clean variant first** — add detail only if requested.

## Error Handling

| Failure Mode | Behavior |
|-------------|----------|
| `drawio/create_diagram` returns XML parse error | Check XML for malformed tags, unclosed elements, or invalid characters. Fix and retry. |
| `drawio/create_diagram` MCP server unavailable | Check MCP server connectivity: verify `drawio` server appears in MCP server list. If offline, inform user and suggest trying again later or saving the XML manually. |
| Icon not found in catalog | Do NOT guess. Grep catalog for alternatives (partial names, synonyms). If no match, use a generic rectangle with text label. |
| Icon renders as blank/broken in diagram | Grep catalog for alternative icon paths. For Azure, try absolute GitHub URL fallback. For AWS, verify using `shape=mxgraph.aws4.*` not `image=img/lib/aws4/...`. Regenerate diagram. |
| Customer folder not found | Offer to run `/customer-repo` to scaffold the engagement folder first. |
| `git commit` fails | Inform the user the diagram was saved but not committed. Do not fail the skill. |
| Diagram too complex for canvas | Increase canvas size (`pageWidth`/`pageHeight`) or suggest splitting into multiple diagrams. |

## Troubleshooting

### MCP Server Connectivity
- Confirm drawio MCP server appears in MCP server list.
- If tool list is stale, reset cached tools and retry.
- The drawio server URL is `https://mcp.draw.io/mcp` (HTTP transport).

### Icon Rendering Issues
- **Azure icons not showing:** Verify style uses `image=img/lib/azure2/...` (not `shape=mxgraph.azure2.*`). Try absolute GitHub URL fallback.
- **AWS icons not showing:** Verify style uses `shape=mxgraph.aws4.<name>` (not `image=img/lib/aws4/...`). AWS4 icons are stencils, not SVG files.
- **Icons work in app.diagrams.net but not in VS Code:** This is a known limitation of the VS Code draw.io extension. Recommend opening in the web app for full rendering.

### XML Validation
- Ensure all tags are properly closed.
- Escape special characters in labels (`&` → `&amp;`, `<` → `&lt;`).
- Verify cell IDs are unique.
- Check parent-child relationships match the container hierarchy.

### Catalog Staleness
If icons that should exist are not in the catalog, the catalog may need refreshing (human-run, not per diagram):
```bash
cd ~/.copilot/skills/drawio-mcp-diagramming/scripts
python3 search_azure2_icons_github.py --max-results 9999 > ../references/azure2-complete-catalog.txt
python3 search_aws4_icons_github.py --max-results 9999 > ../references/aws4-complete-catalog.txt
```
