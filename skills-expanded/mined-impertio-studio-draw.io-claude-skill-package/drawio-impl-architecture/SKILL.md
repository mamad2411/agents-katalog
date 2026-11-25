---
name: drawio-impl-architecture
description: >
  Use when creating C4 model diagrams, software architecture views, or cloud
  architecture diagrams in Draw.io. Prevents mixing cloud provider stencils
  in the same view or using wrong C4 color conventions. Covers C4 system context,
  container, and component diagrams, AWS/Azure/GCP stencil usage, and deployment views.
  Keywords: C4 model, architecture diagram, system context, container diagram,
  AWS, Azure, GCP, deployment, software architecture, cloud diagram,
  system design, infrastructure diagram.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io Architecture Diagram Implementation

## Purpose

This skill enables correct generation of software architecture diagrams in Draw.io mxGraph XML. It covers the C4 model (system context, container, component), cloud architecture with AWS/Azure/GCP stencils, and deployment diagrams. It enforces C4 color conventions, proper stencil namespaces, and correct nesting patterns.

## Critical Rules (Memorize These)

1. **ALWAYS use the C4 color conventions exactly** — Person=#08427b, System=#1168bd, External=#999999, Container=#438dd5, Component=#85bbf0. NEVER use arbitrary colors.
2. **ALWAYS include the three-line label format for C4 elements** — Name (bold), [Type], Description. NEVER omit the type tag or description.
3. **ALWAYS keep one C4 abstraction level per diagram page** — NEVER mix system context elements with container-level details on the same page.
4. **ALWAYS use `container=1;collapsible=0;` for deployment nodes** — Deployment environments and server nodes MUST be containers so child artifacts move with them.
5. **ALWAYS include `whiteSpace=wrap;html=1;`** in every shape style — Without it, labels overflow and do not wrap.
6. **NEVER mix cloud provider stencils in the same view** — AWS (`mxgraph.aws4.*`), Azure (`mxgraph.azure.*`), and GCP (`mxgraph.gcp2.*`) icons MUST be in separate zone containers when depicting multi-cloud.
7. **ALWAYS use `sketch=0;` on stencil shapes** — This prevents hand-drawn rendering mode that distorts stencil icons.
8. **ALWAYS use `endArrow=classic` for C4 relationships** — C4 relationships are directed. NEVER use `endArrow=none`.
9. **ALWAYS set `fontColor=#ffffff` on dark-filled C4 shapes** — Person, System, External, and Container shapes have dark backgrounds. Without white text, labels are unreadable.
10. **NEVER use generic rectangles for cloud resources** — ALWAYS use the appropriate stencil shape from the correct namespace.

## C4 Model Reference

### Color Conventions

| Element | fillColor | strokeColor | fontColor |
|---------|-----------|-------------|-----------|
| Person | `#08427b` | `#073763` | `#ffffff` |
| Software System (internal) | `#1168bd` | `#0b4884` | `#ffffff` |
| External System | `#999999` | `#8A8A8A` | `#ffffff` |
| Container | `#438dd5` | `#3C7FC0` | `#ffffff` |
| Component | `#85bbf0` | `#78A8D8` | `#000000` |

### C4 Shape Styles

#### Person

```
shape=mxgraph.c4.person2;whiteSpace=wrap;html=1;align=center;metaEdit=1;points=[[0.5,0,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0]];fillColor=#08427b;fontColor=#ffffff;strokeColor=#073763;fontSize=11;
```

Dimensions: 200 x 180.

#### Software System (Internal)

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#1168bd;fontColor=#ffffff;strokeColor=#0b4884;fontSize=11;align=center;
```

Dimensions: 300 x 150.

#### External System

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#999999;fontColor=#ffffff;strokeColor=#8A8A8A;fontSize=11;align=center;
```

Dimensions: 240 x 150.

#### Container

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#438dd5;fontColor=#ffffff;strokeColor=#3C7FC0;fontSize=11;align=center;
```

Dimensions: 240 x 150.

#### Component

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#85bbf0;fontColor=#000000;strokeColor=#78A8D8;fontSize=11;align=center;
```

Dimensions: 200 x 120.

### C4 Relationship Style

```
endArrow=classic;html=1;strokeColor=#707070;fontColor=#707070;fontSize=10;
```

ALWAYS include a `value` attribute describing the relationship (e.g., "Makes API calls to", "Reads from").

### C4 Label Format

Every C4 element MUST use this HTML label pattern:

```
<b>Element Name</b><br>[Type Tag]<br><br>Description of what this element does
```

The type tag MUST be one of: `[Person]`, `[Software System]`, `[External System]`, `[Container: Technology]`, `[Component: Technology]`.

## Cloud Architecture Stencils

### AWS (mxgraph.aws4.*)

| Resource | Style | Dimensions |
|----------|-------|-----------|
| EC2 Instance | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;` | 60 x 60 |
| RDS Database | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;` | 60 x 60 |
| S3 Bucket | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;` | 60 x 60 |
| Lambda | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;` | 60 x 60 |
| ALB | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_load_balancing;` | 60 x 60 |
| CloudFront | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudfront;` | 60 x 60 |
| SQS | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sqs;` | 60 x 60 |
| SNS | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sns;` | 60 x 60 |

AWS resource icons use a two-part style: `shape=mxgraph.aws4.resourceIcon` sets the frame, `resIcon=mxgraph.aws4.<service>` sets the icon.

#### AWS Group Containers

| Group | Style | strokeColor |
|-------|-------|-------------|
| Region | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_region;` | `#00A4A6` |
| VPC | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;` | `#8C4FFF` |
| Public Subnet | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_subnet;` | `#7AA116` |
| Private Subnet | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_subnet;` | `#147EBA` |
| Availability Zone | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_availability_zone;` | `#007CBC` |

All AWS group containers MUST include: `container=1;collapsible=0;recursiveResize=0;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontStyle=1;fontSize=12;html=1;whiteSpace=wrap;pointerEvents=0;`

### Azure (mxgraph.azure.*)

| Resource | Style | Dimensions |
|----------|-------|-----------|
| Virtual Machine | `shape=mxgraph.azure.virtual_machine;` | 60 x 60 |
| SQL Database | `shape=mxgraph.azure.sql_database;` | 50 x 60 |
| Virtual Network | `shape=mxgraph.azure.virtual_network;` | 60 x 60 |
| App Service | `shape=mxgraph.azure.app_service;` | 60 x 60 |
| Storage | `shape=mxgraph.azure.storage;` | 60 x 60 |
| Azure Functions | `shape=mxgraph.azure.azure_functions;` | 60 x 60 |
| Key Vault | `shape=mxgraph.azure.key_vaults;` | 60 x 60 |

Azure stencils use a flat namespace: `shape=mxgraph.azure.<service>;`.

### GCP (mxgraph.gcp2.*)

| Resource | Style | Dimensions |
|----------|-------|-----------|
| Compute Engine | `shape=mxgraph.gcp2.compute_engine;` | 60 x 60 |
| Cloud SQL | `shape=mxgraph.gcp2.cloud_sql;` | 60 x 60 |
| Cloud Storage | `shape=mxgraph.gcp2.cloud_storage;` | 60 x 60 |
| Cloud Functions | `shape=mxgraph.gcp2.cloud_functions;` | 60 x 60 |
| Pub/Sub | `shape=mxgraph.gcp2.cloud_pubsub;` | 60 x 60 |
| Cloud Run | `shape=mxgraph.gcp2.cloud_run;` | 60 x 60 |

GCP stencils use the `gcp2` namespace. NEVER use the legacy `gcp` namespace.

### Cloud Stencil Base Style

ALWAYS append these properties to every cloud stencil shape:

```
sketch=0;html=1;whiteSpace=wrap;verticalLabelPosition=bottom;verticalAlign=top;align=center;
```

## Deployment Diagram Pattern

Deployment diagrams use nested containers to represent environments, servers, and runtime artifacts.

### Deployment Node (Environment)

```
shape=cube;whiteSpace=wrap;html=1;size=10;container=1;fillColor=#f5f5f5;strokeColor=#666666;fontStyle=1;verticalAlign=top;
```

Dimensions: 300+ x 200+ (must be large enough to contain child nodes).

### Deployment Node (Server)

```
shape=cube;whiteSpace=wrap;html=1;size=10;container=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;verticalAlign=top;
```

Nested inside the environment node. Set `parent="<environment_id>"`.

### Artifact (Application)

```
shape=note;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;
```

Dimensions: 120 x 60. Set `parent="<server_id>"`.

### Artifact (Database)

```
shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;size=10;
```

Dimensions: 100 x 80. Set `parent="<server_id>"`.

### Nesting Hierarchy

```
Environment (cube, container=1)
  +-- Server (cube, container=1, parent=environment)
  |     +-- Application (note, parent=server)
  |     +-- Database (cylinder3, parent=server)
  +-- Server (cube, container=1, parent=environment)
        +-- Application (note, parent=server)
```

ALWAYS use relative coordinates for child elements within containers.

## Complete C4 System Context Example

```xml
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />

    <!-- Person: Customer -->
    <mxCell id="person1" value="&lt;b&gt;Customer&lt;/b&gt;&lt;br&gt;[Person]&lt;br&gt;&lt;br&gt;Uses the web app to browse products and place orders" style="shape=mxgraph.c4.person2;whiteSpace=wrap;html=1;align=center;metaEdit=1;points=[[0.5,0,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0]];fillColor=#08427b;fontColor=#ffffff;strokeColor=#073763;fontSize=11;" vertex="1" parent="1">
      <mxGeometry x="350" y="20" width="200" height="180" as="geometry" />
    </mxCell>

    <!-- Internal System: E-Commerce Platform -->
    <mxCell id="sys1" value="&lt;b&gt;E-Commerce Platform&lt;/b&gt;&lt;br&gt;[Software System]&lt;br&gt;&lt;br&gt;Handles product catalog, shopping cart, and order processing" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1168bd;fontColor=#ffffff;strokeColor=#0b4884;fontSize=11;align=center;" vertex="1" parent="1">
      <mxGeometry x="300" y="300" width="300" height="150" as="geometry" />
    </mxCell>

    <!-- External System: Payment Gateway -->
    <mxCell id="ext1" value="&lt;b&gt;Payment Gateway&lt;/b&gt;&lt;br&gt;[External System]&lt;br&gt;&lt;br&gt;Processes credit card and bank payments via Stripe API" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#999999;fontColor=#ffffff;strokeColor=#8A8A8A;fontSize=11;align=center;" vertex="1" parent="1">
      <mxGeometry x="680" y="300" width="240" height="150" as="geometry" />
    </mxCell>

    <!-- External System: Email Service -->
    <mxCell id="ext2" value="&lt;b&gt;Email Service&lt;/b&gt;&lt;br&gt;[External System]&lt;br&gt;&lt;br&gt;Sends order confirmations and shipping notifications via SendGrid" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#999999;fontColor=#ffffff;strokeColor=#8A8A8A;fontSize=11;align=center;" vertex="1" parent="1">
      <mxGeometry x="680" y="520" width="240" height="150" as="geometry" />
    </mxCell>

    <!-- Internal System: Inventory System -->
    <mxCell id="sys2" value="&lt;b&gt;Inventory System&lt;/b&gt;&lt;br&gt;[Software System]&lt;br&gt;&lt;br&gt;Tracks stock levels, warehouses, and restocking" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1168bd;fontColor=#ffffff;strokeColor=#0b4884;fontSize=11;align=center;" vertex="1" parent="1">
      <mxGeometry x="300" y="520" width="300" height="150" as="geometry" />
    </mxCell>

    <!-- Relationship: Customer -> E-Commerce -->
    <mxCell id="r1" value="Browses products and places orders using" style="endArrow=classic;html=1;strokeColor=#707070;fontColor=#707070;fontSize=10;" edge="1" parent="1" source="person1" target="sys1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>

    <!-- Relationship: E-Commerce -> Payment Gateway -->
    <mxCell id="r2" value="Sends payment requests to" style="endArrow=classic;html=1;strokeColor=#707070;fontColor=#707070;fontSize=10;" edge="1" parent="1" source="sys1" target="ext1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>

    <!-- Relationship: E-Commerce -> Email Service -->
    <mxCell id="r3" value="Sends emails using" style="endArrow=classic;html=1;strokeColor=#707070;fontColor=#707070;fontSize=10;" edge="1" parent="1" source="sys1" target="ext2">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>

    <!-- Relationship: E-Commerce -> Inventory -->
    <mxCell id="r4" value="Checks stock levels via" style="endArrow=classic;html=1;strokeColor=#707070;fontColor=#707070;fontSize=10;" edge="1" parent="1" source="sys1" target="sys2">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
  </root>
</mxGraphModel>
```

## Checklist: Before Outputting an Architecture Diagram

1. Every C4 element uses the correct fillColor from the color conventions table.
2. Every C4 element label follows the three-line format: Name, [Type], Description.
3. Only one C4 abstraction level per diagram page.
4. C4 relationships use `endArrow=classic` (NEVER `endArrow=none`).
5. Cloud stencils use the correct namespace (`aws4`, `azure`, `gcp2`).
6. Cloud provider stencils from different vendors are in separate zone containers.
7. Deployment nodes use `container=1` and child artifacts set the correct `parent`.
8. All shapes include `whiteSpace=wrap;html=1;`.
9. Stencil shapes include `sketch=0;`.
10. Both structural cells (`id="0"` and `id="1"`) are present.
11. Cell IDs are unique across the entire diagram.
12. All edges have `source` and `target` pointing to valid cell IDs.

## Cross-References

- **XML fundamentals:** See `drawio-core-xml-format` for file structure and structural cells.
- **Style syntax:** See `drawio-syntax-styles` for the complete style property reference.
- **Connection details:** See `drawio-syntax-connections` for edge routing and waypoints.
- **Cloud network stencils:** See `drawio-impl-network` for Cisco stencils, zone boundaries, and network topology patterns.
- **Geometry:** See `drawio-core-geometry` for coordinate system and positioning.

## Reference Links

- [Complete Reference](references/methods.md)
- [Working Examples](references/examples.md)
- [Anti-Patterns](references/anti-patterns.md)
