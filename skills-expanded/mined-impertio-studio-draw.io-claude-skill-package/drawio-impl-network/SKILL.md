---
name: drawio-impl-network
description: >
  Use when creating network topology diagrams, infrastructure layouts, or cloud
  architecture diagrams in Draw.io. Prevents using wrong stencil namespaces
  (e.g., mxgraph.cisco vs mxgraph.cisco19). Covers Cisco/AWS/Azure/GCP stencils,
  network topology patterns, zone boundaries, and rack diagrams.
  Keywords: network diagram, topology, Cisco, AWS, Azure, GCP, stencil, router,
  switch, server, cloud, infrastructure diagram, network layout, server rack,
  IT architecture, network map.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io Network Diagram Implementation

## Purpose

This skill enables correct generation of network topology diagrams, infrastructure layouts, and cloud architecture diagrams in Draw.io mxGraph XML. It enforces the use of proper stencil namespaces for vendor-specific icons and prevents the most common AI mistakes: wrong shape namespaces, directed arrows for physical links, and missing zone boundaries.

## Critical Rules (Memorize These)

1. **ALWAYS use `mxgraph.cisco19.*` for modern Cisco icons** — NEVER use the legacy `mxgraph.cisco.*` namespace. The `cisco19` stencils are the current set with updated iconography.
2. **ALWAYS use `endArrow=none` for physical network links** — Physical connectivity is bidirectional. NEVER use directed arrows (`endArrow=classic`) for cables, fibers, or wireless links.
3. **ALWAYS use containers for network zones** — Zones (DMZ, LAN, WAN, subnets) MUST use `container=1;collapsible=0;` so child devices move with the zone boundary.
4. **ALWAYS include `whiteSpace=wrap;html=1;`** in every shape style — Without it, labels overflow and do not wrap.
5. **ALWAYS include `sketch=0;`** on stencil shapes — This prevents the hand-drawn rendering mode that distorts stencil icons.
6. **ALWAYS add `verticalLabelPosition=bottom;verticalAlign=top;align=center;`** on icon-style shapes — Without it, the label overlaps the icon graphic.
7. **NEVER mix cloud provider stencils** in the same zone — AWS, Azure, and GCP icons MUST be separated into distinct zone containers when depicting multi-cloud.
8. **NEVER use generic rectangles for network devices** — ALWAYS use the appropriate stencil shape from the correct namespace.

## Stencil Namespace Reference

### Cisco (Modern: cisco19)

| Device | Style | Dimensions |
|--------|-------|-----------|
| Router | `shape=mxgraph.cisco19.rect;prIcon=mxgraph.cisco19.router;` | 78 x 53 |
| Switch L2 | `shape=mxgraph.cisco19.rect;prIcon=mxgraph.cisco19.switch;` | 78 x 53 |
| Switch L3 | `shape=mxgraph.cisco19.rect;prIcon=mxgraph.cisco19.layer_3_switch;` | 78 x 53 |
| Firewall | `shape=mxgraph.cisco19.rect;prIcon=mxgraph.cisco19.firewall;` | 78 x 53 |
| Server | `shape=mxgraph.cisco19.rect;prIcon=mxgraph.cisco19.server;` | 50 x 65 |
| Wireless AP | `shape=mxgraph.cisco19.rect;prIcon=mxgraph.cisco19.access_point;` | 50 x 50 |
| Laptop | `shape=mxgraph.cisco19.rect;prIcon=mxgraph.cisco19.laptop;` | 50 x 40 |
| IP Phone | `shape=mxgraph.cisco19.rect;prIcon=mxgraph.cisco19.ip_phone;` | 50 x 50 |
| Load Balancer | `shape=mxgraph.cisco19.rect;prIcon=mxgraph.cisco19.load_balancer;` | 78 x 53 |

### Cisco (Legacy: for reference ONLY)

The `mxgraph.cisco.*` namespace (without `19`) is the legacy stencil set. It still renders in Draw.io but uses outdated iconography. ALWAYS prefer `mxgraph.cisco19.*`.

Legacy format: `shape=mxgraph.cisco.routers.router;` — note the nested category path.

### AWS (v4)

| Resource | Style | Dimensions |
|----------|-------|-----------|
| EC2 Instance | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;` | 60 x 60 |
| RDS Database | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;` | 60 x 60 |
| S3 Bucket | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;` | 60 x 60 |
| Lambda | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;` | 60 x 60 |
| VPC (group) | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;` | container |
| Region (group) | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_region;` | container |
| Subnet (group) | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_subnet;` | container |
| ALB | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_load_balancing;` | 60 x 60 |

AWS resource icons use a two-part style: `shape=mxgraph.aws4.resourceIcon` sets the frame, `resIcon=mxgraph.aws4.<service>` sets the specific icon inside the frame.

### Azure

| Resource | Style | Dimensions |
|----------|-------|-----------|
| Virtual Machine | `shape=mxgraph.azure.virtual_machine;` | 60 x 60 |
| SQL Database | `shape=mxgraph.azure.sql_database;` | 50 x 60 |
| Virtual Network | `shape=mxgraph.azure.virtual_network;` | 60 x 60 |
| App Service | `shape=mxgraph.azure.app_service;` | 60 x 60 |
| Storage | `shape=mxgraph.azure.storage;` | 60 x 60 |

### GCP (v2)

| Resource | Style | Dimensions |
|----------|-------|-----------|
| Compute Engine | `shape=mxgraph.gcp2.compute_engine;` | 60 x 60 |
| Cloud SQL | `shape=mxgraph.gcp2.cloud_sql;` | 60 x 60 |
| Cloud Storage | `shape=mxgraph.gcp2.cloud_storage;` | 60 x 60 |
| Cloud Functions | `shape=mxgraph.gcp2.cloud_functions;` | 60 x 60 |

### Generic Network Shapes (No Stencil Required)

| Shape | Style | Purpose |
|-------|-------|---------|
| Cloud | `shape=cloud;whiteSpace=wrap;html=1;` | Internet / external network |
| Cylinder | `shape=cylinder3;whiteSpace=wrap;html=1;` | Database or storage |
| Rectangle | `rounded=1;whiteSpace=wrap;html=1;` | Generic device or service |

## Network Connection Styles

### Physical Links (ALWAYS Bidirectional)

```
endArrow=none;html=1;strokeWidth=2;
```

Physical network cables, fibers, and wireless links are ALWAYS bidirectional. NEVER use `endArrow=classic`.

### Backbone / Trunk Links

```
endArrow=none;html=1;strokeWidth=3;strokeColor=#0066CC;
```

Use thicker lines (`strokeWidth=3`) and a distinct color for backbone or trunk connections.

### Redundant Links

```
endArrow=none;html=1;strokeWidth=2;strokeColor=#CC0000;dashed=1;
```

Use `dashed=1` for redundant or standby links to distinguish them from primary paths.

### Logical / Data Flow (Directed)

```
endArrow=classic;html=1;strokeWidth=1;dashed=1;
```

Use directed arrows ONLY for logical data flow overlays, NEVER for physical topology.

### Labeled Links (IP / VLAN)

Use the `value` attribute on edge cells to label connections with IP addresses or VLAN IDs:

```xml
<mxCell id="link1" value="VLAN 10" style="endArrow=none;html=1;strokeWidth=2;"
        edge="1" parent="1" source="sw1" target="srv1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

## Zone / Segment Boundaries

ALWAYS use container cells for network zones. The pattern:

```
rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#<color>;strokeWidth=2;dashed=1;verticalAlign=top;fontStyle=1;fontSize=12;fontColor=#<color>;container=1;collapsible=0;
```

### Zone Color Conventions

| Zone | Stroke/Font Color | Purpose |
|------|-------------------|---------|
| DMZ | `#FF0000` (red) | Demilitarized zone |
| LAN / Internal | `#009900` (green) | Internal trusted network |
| WAN / External | `#0066CC` (blue) | Wide area / external network |
| Management | `#FF9900` (orange) | Management plane |
| Guest / IoT | `#9933CC` (purple) | Untrusted internal segments |

### Zone XML Pattern

```xml
<mxCell id="dmz_zone" value="DMZ" style="rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#FF0000;strokeWidth=2;dashed=1;verticalAlign=top;fontStyle=1;fontSize=12;fontColor=#FF0000;container=1;collapsible=0;" vertex="1" parent="1">
  <mxGeometry x="30" y="200" width="300" height="200" as="geometry" />
</mxCell>
```

Devices inside a zone MUST set `parent="<zone_id>"` and use coordinates relative to the zone container.

## Topology Patterns

### Star Topology

One central device (switch/hub) connects to all peripheral devices. Place the central device at the center and distribute endpoints in a circular or grid pattern around it.

### Ring Topology

Devices connect in a closed loop. Place devices in a circle and connect each to its neighbor, with the last connecting back to the first.

### Mesh Topology

Every device connects to every other device (full mesh) or a subset (partial mesh). Use for core router interconnections.

### Three-Tier Architecture

Standard enterprise layout (top-to-bottom):

```
Internet Cloud (y=20)
    |
Firewall (y=140)
    |
Core Router (y=260)
    |-------------|
Distribution SW   Distribution SW (y=380)
    |                |
Access SW  Access SW  Access SW (y=500)
    |         |         |
Endpoints (y=620)
```

Vertical spacing: 120px between tiers. Horizontal spacing: 180px between parallel devices.

## Rack Diagram Pattern

For server rack representations, use a tall container with stacked elements:

```xml
<!-- Rack frame -->
<mxCell id="rack1" value="Rack A" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#333333;strokeWidth=2;verticalAlign=top;fontStyle=1;fontSize=12;container=1;collapsible=0;" vertex="1" parent="1">
  <mxGeometry x="100" y="40" width="200" height="400" as="geometry" />
</mxCell>

<!-- Rack units (1U = ~20px height, stacked from top) -->
<mxCell id="ru1" value="Patch Panel" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=10;" vertex="1" parent="rack1">
  <mxGeometry x="10" y="30" width="180" height="20" as="geometry" />
</mxCell>
<mxCell id="ru2" value="Core Switch" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=10;" vertex="1" parent="rack1">
  <mxGeometry x="10" y="55" width="180" height="40" as="geometry" />
</mxCell>
```

Each rack unit (1U) is approximately 20px in height. Common sizes: 1U = 20px, 2U = 40px, 4U = 80px.

## AWS Architecture Diagram Pattern

AWS diagrams use nested group containers for Region > VPC > Subnet hierarchy:

```xml
<!-- Region -->
<mxCell id="region" value="eu-west-1" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=1;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_region;strokeColor=#00A4A6;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#147EBA;dashed=1;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="600" height="400" as="geometry" />
</mxCell>

<!-- VPC inside region -->
<mxCell id="vpc" value="VPC 10.0.0.0/16" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=1;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;strokeColor=#8C4FFF;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#AAB7B8;dashed=0;" vertex="1" parent="region">
  <mxGeometry x="20" y="40" width="560" height="340" as="geometry" />
</mxCell>

<!-- Subnet inside VPC -->
<mxCell id="subnet_pub" value="Public Subnet 10.0.1.0/24" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=1;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_subnet;strokeColor=#7AA116;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#248814;dashed=0;" vertex="1" parent="vpc">
  <mxGeometry x="20" y="40" width="240" height="270" as="geometry" />
</mxCell>
```

## Complete Example: LAN Topology

```xml
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />

    <!-- Internet Cloud -->
    <mxCell id="cloud" value="Internet" style="shape=cloud;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=14;" vertex="1" parent="1">
      <mxGeometry x="300" y="20" width="200" height="100" as="geometry" />
    </mxCell>

    <!-- Firewall -->
    <mxCell id="fw" value="Firewall" style="shape=mxgraph.cisco19.rect;prIcon=mxgraph.cisco19.firewall;fillColor=#FAFAFA;strokeColor=#005073;sketch=0;html=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;whiteSpace=wrap;" vertex="1" parent="1">
      <mxGeometry x="361" y="170" width="78" height="53" as="geometry" />
    </mxCell>

    <!-- Core Router -->
    <mxCell id="router" value="Core Router" style="shape=mxgraph.cisco19.rect;prIcon=mxgraph.cisco19.router;fillColor=#FAFAFA;strokeColor=#005073;sketch=0;html=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;whiteSpace=wrap;" vertex="1" parent="1">
      <mxGeometry x="361" y="300" width="78" height="53" as="geometry" />
    </mxCell>

    <!-- Distribution Switch 1 -->
    <mxCell id="dsw1" value="Dist SW 1" style="shape=mxgraph.cisco19.rect;prIcon=mxgraph.cisco19.layer_3_switch;fillColor=#FAFAFA;strokeColor=#005073;sketch=0;html=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;whiteSpace=wrap;" vertex="1" parent="1">
      <mxGeometry x="180" y="430" width="78" height="53" as="geometry" />
    </mxCell>

    <!-- Distribution Switch 2 -->
    <mxCell id="dsw2" value="Dist SW 2" style="shape=mxgraph.cisco19.rect;prIcon=mxgraph.cisco19.layer_3_switch;fillColor=#FAFAFA;strokeColor=#005073;sketch=0;html=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;whiteSpace=wrap;" vertex="1" parent="1">
      <mxGeometry x="540" y="430" width="78" height="53" as="geometry" />
    </mxCell>

    <!-- DMZ Zone -->
    <mxCell id="dmz_zone" value="DMZ" style="rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#FF0000;strokeWidth=2;dashed=1;verticalAlign=top;fontStyle=1;fontSize=12;fontColor=#FF0000;container=1;collapsible=0;" vertex="1" parent="1">
      <mxGeometry x="100" y="570" width="250" height="180" as="geometry" />
    </mxCell>

    <!-- Web Server in DMZ -->
    <mxCell id="web1" value="Web Server" style="shape=mxgraph.cisco19.rect;prIcon=mxgraph.cisco19.server;fillColor=#FAFAFA;strokeColor=#005073;sketch=0;html=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;whiteSpace=wrap;" vertex="1" parent="dmz_zone">
      <mxGeometry x="20" y="40" width="50" height="65" as="geometry" />
    </mxCell>

    <!-- Mail Server in DMZ -->
    <mxCell id="mail1" value="Mail Server" style="shape=mxgraph.cisco19.rect;prIcon=mxgraph.cisco19.server;fillColor=#FAFAFA;strokeColor=#005073;sketch=0;html=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;whiteSpace=wrap;" vertex="1" parent="dmz_zone">
      <mxGeometry x="140" y="40" width="50" height="65" as="geometry" />
    </mxCell>

    <!-- LAN Zone -->
    <mxCell id="lan_zone" value="Internal LAN" style="rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#009900;strokeWidth=2;dashed=1;verticalAlign=top;fontStyle=1;fontSize=12;fontColor=#009900;container=1;collapsible=0;" vertex="1" parent="1">
      <mxGeometry x="430" y="570" width="250" height="180" as="geometry" />
    </mxCell>

    <!-- DB Server in LAN -->
    <mxCell id="db1" value="DB Server" style="shape=mxgraph.cisco19.rect;prIcon=mxgraph.cisco19.server;fillColor=#FAFAFA;strokeColor=#005073;sketch=0;html=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;whiteSpace=wrap;" vertex="1" parent="lan_zone">
      <mxGeometry x="20" y="40" width="50" height="65" as="geometry" />
    </mxCell>

    <!-- App Server in LAN -->
    <mxCell id="app1" value="App Server" style="shape=mxgraph.cisco19.rect;prIcon=mxgraph.cisco19.server;fillColor=#FAFAFA;strokeColor=#005073;sketch=0;html=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;whiteSpace=wrap;" vertex="1" parent="lan_zone">
      <mxGeometry x="140" y="40" width="50" height="65" as="geometry" />
    </mxCell>

    <!-- Connections (all bidirectional) -->
    <mxCell id="c1" style="endArrow=none;html=1;strokeWidth=2;" edge="1" parent="1" source="cloud" target="fw">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="c2" style="endArrow=none;html=1;strokeWidth=2;" edge="1" parent="1" source="fw" target="router">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="c3" style="endArrow=none;html=1;strokeWidth=2;" edge="1" parent="1" source="router" target="dsw1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="c4" style="endArrow=none;html=1;strokeWidth=2;" edge="1" parent="1" source="router" target="dsw2">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="c5" style="endArrow=none;html=1;strokeWidth=2;" edge="1" parent="1" source="dsw1" target="dmz_zone">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="c6" style="endArrow=none;html=1;strokeWidth=2;" edge="1" parent="1" source="dsw2" target="lan_zone">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <!-- Redundant cross-link between distribution switches -->
    <mxCell id="c7" style="endArrow=none;html=1;strokeWidth=2;strokeColor=#CC0000;dashed=1;" edge="1" parent="1" source="dsw1" target="dsw2">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
  </root>
</mxGraphModel>
```

## IP Address Labeling

Use the `<object>` wrapper to attach metadata (IP, VLAN, hostname) to network devices:

```xml
<object label="Web Server&lt;br&gt;&lt;font style=&quot;font-size:10px&quot;&gt;192.168.1.10&lt;/font&gt;" id="web_srv" ip="192.168.1.10" hostname="web01.local">
  <mxCell style="shape=mxgraph.cisco19.rect;prIcon=mxgraph.cisco19.server;fillColor=#FAFAFA;strokeColor=#005073;sketch=0;html=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;whiteSpace=wrap;" vertex="1" parent="1">
    <mxGeometry x="100" y="100" width="50" height="65" as="geometry" />
  </mxCell>
</object>
```

The `<object>` element supports custom attributes (`ip`, `hostname`, `vlan`) that appear as tooltip metadata in Draw.io. The `label` attribute overrides `value` and supports HTML.

## Checklist: Before Outputting a Network Diagram

1. Every network device uses an appropriate stencil shape (NEVER generic rectangles).
2. Cisco shapes use `mxgraph.cisco19.*` namespace (NEVER legacy `mxgraph.cisco.*`).
3. Physical links use `endArrow=none` (NEVER directed arrows).
4. Network zones use `container=1;collapsible=0;dashed=1;fillColor=none;`.
5. Devices inside zones have `parent="<zone_id>"`.
6. All shapes include `whiteSpace=wrap;html=1;sketch=0;`.
7. Icon-style shapes include `verticalLabelPosition=bottom;verticalAlign=top;align=center;`.
8. Both structural cells (`id="0"` and `id="1"`) are present.
9. Cell IDs are unique across the entire diagram.
10. All edges have `source` and `target` pointing to valid cell IDs.
11. Cloud provider shapes from different vendors are in separate zone containers.

## Cross-References

- **XML fundamentals:** See `drawio-core-xml-format` for file structure and structural cells.
- **Style syntax:** See `drawio-syntax-styles` for the complete style property reference.
- **Connection details:** See `drawio-syntax-connections` for edge routing and waypoints.
- **Geometry:** See `drawio-core-geometry` for coordinate system and positioning.

## Reference Links

- [Complete Reference](references/methods.md)
- [Working Examples](references/examples.md)
- [Anti-Patterns](references/anti-patterns.md)
