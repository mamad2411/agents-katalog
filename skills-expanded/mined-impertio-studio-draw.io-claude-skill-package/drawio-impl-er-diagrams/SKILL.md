---
name: drawio-impl-er-diagrams
description: >
  Use when creating entity-relationship diagrams, database schemas, or data models
  in Draw.io. Prevents the common mistake of using generic arrows instead of
  crow's foot notation (ERone, ERmany, ERzeroToOne, etc.). Covers entity table
  shapes, PK/FK notation, all cardinality markers, and entityRelationEdgeStyle.
  Keywords: ER diagram, entity-relationship, crow's foot, ERone, ERmany,
  cardinality, database schema, table, database diagram, data model,
  table relationships, one-to-many, many-to-many.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io ER Diagram Implementation

## Purpose

This skill enables correct generation of entity-relationship diagrams, database schemas, and data models in Draw.io mxGraph XML. It enforces crow's foot notation for cardinality, proper entity table structures, and PK/FK visual conventions. The most common AI mistake is using generic arrows (`endArrow=classic`) instead of ER-specific markers (`ERone`, `ERmany`, etc.).

## Critical Rules (Memorize These)

1. **ALWAYS use `entityRelationEdgeStyle` for ER relationships** — NEVER use `orthogonalEdgeStyle` or default edge routing.
2. **ALWAYS use ER-specific arrow markers** (`ERone`, `ERmany`, `ERmandOne`, `ERzeroToOne`, `ERoneToMany`, `ERzeroToMany`) — NEVER use `endArrow=classic` or `endArrow=block` in ER diagrams.
3. **ALWAYS set `startFill=0` and `endFill=0`** on ER edges — crow's foot markers MUST use `Fill=0`. Setting `Fill=1` produces incorrect filled shapes.
4. **ALWAYS use `shape=table;childLayout=tableLayout;container=1;`** for entity shapes — this produces the standard database table appearance with a header row and stacked attribute rows.
5. **ALWAYS place attribute rows as children of the entity** — every attribute `mxCell` MUST have `parent="<entity_id>"`. NEVER use `parent="1"`.
6. **ALWAYS mark primary key fields with `fontStyle=4;`** (underline) — this is the standard ER convention for PKs.
7. **ALWAYS mark foreign key fields with `fontStyle=2;`** (italic) — this distinguishes FKs from regular attributes.
8. **ALWAYS include both structural cells** (`id="0"` and `id="1"` with `parent="0"`) in every diagram.

## Entity Table Shape

### Container Style (Header Row)

```
shape=table;startSize=30;container=1;collapsible=1;childLayout=tableLayout;fixedRows=1;rowLines=0;fontStyle=1;align=center;resizeLast=1;
```

Key properties:
- `shape=table` — renders as a table container with header band.
- `startSize=30` — header height in pixels. Controls the title band.
- `container=1` — REQUIRED. Without it, child cells will not attach.
- `childLayout=tableLayout` — auto-stacks attribute rows vertically.
- `collapsible=1` — allows collapsing the entity in the editor.
- `fontStyle=1` — bold entity name in header.
- `resizeLast=1` — last row stretches to fill remaining space.

### Attribute Row Style

```
text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;whiteSpace=wrap;html=1;
```

Every attribute row:
- MUST be a child of the entity container (`parent="<entity_id>"`).
- MUST have `y` offset calculated as: `startSize + (row_index * row_height)`.
- MUST have the same `width` as the parent entity.
- Uses a standard `height` of 30px per row.

### PK/FK Font Conventions

| Field Type | fontStyle | Visual | Example Value |
|-----------|-----------|--------|---------------|
| Primary Key | `fontStyle=4;` | Underlined | `customer_id  PK  INT` |
| Foreign Key | `fontStyle=2;` | Italic | `customer_id  FK  INT` |
| Regular field | (none) | Normal | `name  VARCHAR(100)` |
| PK + FK (composite) | `fontStyle=6;` | Underline + Italic | `order_id  PK FK  INT` |

## Entity Dimensions

| Component | Width | Height | Notes |
|-----------|-------|--------|-------|
| Entity container | 200 | startSize + (row_count * 30) | Minimum 200px wide |
| Header band | 200 | 30 (startSize) | Contains entity name |
| Attribute row | 200 | 30 | Each field gets one row |

### Height Calculation

Total entity height = `startSize` + (number_of_attributes * 30).

Example: Entity with 4 attributes = 30 + (4 * 30) = 150px.

## Crow's Foot Notation Reference

### Cardinality Markers

| Marker | Arrow Value | Symbol | Meaning |
|--------|------------|--------|---------|
| One (mandatory) | `ERone` | Single line | Exactly one |
| Many | `ERmany` | Crow's foot (fork) | One or more |
| Mandatory One | `ERmandOne` | Line + single line | Exactly one (mandatory) |
| Zero-or-One | `ERzeroToOne` | Circle + single line | Zero or one (optional) |
| One-or-Many | `ERoneToMany` | Line + crow's foot | At least one, possibly many |
| Zero-or-Many | `ERzeroToMany` | Circle + crow's foot | Zero, one, or many |

### Common Relationship Patterns

| Relationship | startArrow | endArrow | Description |
|-------------|-----------|----------|-------------|
| One-to-One (mandatory) | `ERone` | `ERone` | Exactly one on each side |
| One-to-Many | `ERone` | `ERmany` | Source has one, target has many |
| One-to-Many (mandatory) | `ERmandOne` | `ERoneToMany` | Must have at least one on each side |
| One-to-Many (optional) | `ERzeroToOne` | `ERzeroToMany` | Zero or more on each side |
| Many-to-Many | `ERmany` | `ERmany` | Many on both sides |
| Zero-or-One to Many | `ERzeroToOne` | `ERmany` | Optional source, many targets |

## Relationship Edge Style

### Standard ER Edge

```
edgeStyle=entityRelationEdgeStyle;html=1;endArrow=ERmany;endFill=0;startArrow=ERone;startFill=0;strokeColor=#666666;
```

Key properties:
- `edgeStyle=entityRelationEdgeStyle` — REQUIRED. Produces the classic ER curved connector.
- `startArrow=ERone` / `endArrow=ERmany` — crow's foot markers at each end.
- `startFill=0` / `endFill=0` — REQUIRED. ER markers MUST be unfilled.
- `strokeColor=#666666` — neutral gray for relationship lines.

### Relationship Labels

Add a `value` attribute to the edge to label the relationship:

```xml
<mxCell id="rel1" value="places" style="edgeStyle=entityRelationEdgeStyle;html=1;endArrow=ERmany;endFill=0;startArrow=ERone;startFill=0;" edge="1" parent="1" source="ent_customer" target="ent_order">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

## Entity Color Conventions

Use distinct colors per entity to visually separate tables:

| Entity Role | Fill Color | Stroke Color |
|------------|-----------|-------------|
| Primary entity | `#dae8fc` (light blue) | `#6c8ebf` |
| Secondary entity | `#d5e8d4` (light green) | `#82b366` |
| Junction/bridge table | `#fff2cc` (light yellow) | `#d6b656` |
| Lookup/reference table | `#e1d5e7` (light purple) | `#9673a6` |
| Audit/log table | `#f5f5f5` (light gray) | `#666666` |

## Layout Strategy

### Entity Spacing

- **Horizontal spacing:** 120-180px between entities placed side by side.
- **Vertical spacing:** 80-120px between entities placed above/below.
- **Relationship lines:** `entityRelationEdgeStyle` auto-routes curves; no manual waypoints needed.

### Positioning Guidelines

- Place primary entities (Customer, Product) on the left or top.
- Place dependent entities (Order, OrderLine) to the right or below.
- Place junction tables between the entities they bridge.
- Align entity tops when placed in a row for visual consistency.

## Complete Example: E-Commerce Database (3 Entities)

```xml
<mxGraphModel>
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />

    <!-- Entity: Customer -->
    <mxCell id="ent_cust" value="Customer" style="shape=table;startSize=30;container=1;collapsible=1;childLayout=tableLayout;fixedRows=1;rowLines=0;fontStyle=1;align=center;resizeLast=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="60" y="80" width="200" height="120" as="geometry" />
    </mxCell>
    <mxCell id="cust_pk" value="customer_id  PK  INT" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;whiteSpace=wrap;html=1;fontStyle=4;" vertex="1" parent="ent_cust">
      <mxGeometry y="30" width="200" height="30" as="geometry" />
    </mxCell>
    <mxCell id="cust_f1" value="name  VARCHAR(100)" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;whiteSpace=wrap;html=1;" vertex="1" parent="ent_cust">
      <mxGeometry y="60" width="200" height="30" as="geometry" />
    </mxCell>
    <mxCell id="cust_f2" value="email  VARCHAR(255)" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;whiteSpace=wrap;html=1;" vertex="1" parent="ent_cust">
      <mxGeometry y="90" width="200" height="30" as="geometry" />
    </mxCell>

    <!-- Entity: Order -->
    <mxCell id="ent_ord" value="Order" style="shape=table;startSize=30;container=1;collapsible=1;childLayout=tableLayout;fixedRows=1;rowLines=0;fontStyle=1;align=center;resizeLast=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
      <mxGeometry x="380" y="60" width="200" height="150" as="geometry" />
    </mxCell>
    <mxCell id="ord_pk" value="order_id  PK  INT" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;whiteSpace=wrap;html=1;fontStyle=4;" vertex="1" parent="ent_ord">
      <mxGeometry y="30" width="200" height="30" as="geometry" />
    </mxCell>
    <mxCell id="ord_fk" value="customer_id  FK  INT" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;whiteSpace=wrap;html=1;fontStyle=2;" vertex="1" parent="ent_ord">
      <mxGeometry y="60" width="200" height="30" as="geometry" />
    </mxCell>
    <mxCell id="ord_f1" value="order_date  DATE" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;whiteSpace=wrap;html=1;" vertex="1" parent="ent_ord">
      <mxGeometry y="90" width="200" height="30" as="geometry" />
    </mxCell>
    <mxCell id="ord_f2" value="total  DECIMAL(10,2)" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;whiteSpace=wrap;html=1;" vertex="1" parent="ent_ord">
      <mxGeometry y="120" width="200" height="30" as="geometry" />
    </mxCell>

    <!-- Entity: OrderLine -->
    <mxCell id="ent_line" value="OrderLine" style="shape=table;startSize=30;container=1;collapsible=1;childLayout=tableLayout;fixedRows=1;rowLines=0;fontStyle=1;align=center;resizeLast=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
      <mxGeometry x="700" y="60" width="200" height="150" as="geometry" />
    </mxCell>
    <mxCell id="line_pk" value="line_id  PK  INT" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;whiteSpace=wrap;html=1;fontStyle=4;" vertex="1" parent="ent_line">
      <mxGeometry y="30" width="200" height="30" as="geometry" />
    </mxCell>
    <mxCell id="line_fk1" value="order_id  FK  INT" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;whiteSpace=wrap;html=1;fontStyle=2;" vertex="1" parent="ent_line">
      <mxGeometry y="60" width="200" height="30" as="geometry" />
    </mxCell>
    <mxCell id="line_fk2" value="product_id  FK  INT" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;whiteSpace=wrap;html=1;fontStyle=2;" vertex="1" parent="ent_line">
      <mxGeometry y="90" width="200" height="30" as="geometry" />
    </mxCell>
    <mxCell id="line_f1" value="quantity  INT" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;whiteSpace=wrap;html=1;" vertex="1" parent="ent_line">
      <mxGeometry y="120" width="200" height="30" as="geometry" />
    </mxCell>

    <!-- Relationship: Customer 1:N Order -->
    <mxCell id="rel1" value="places" style="edgeStyle=entityRelationEdgeStyle;html=1;endArrow=ERmany;endFill=0;startArrow=ERone;startFill=0;strokeColor=#666666;" edge="1" parent="1" source="ent_cust" target="ent_ord">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>

    <!-- Relationship: Order 1:N OrderLine -->
    <mxCell id="rel2" value="contains" style="edgeStyle=entityRelationEdgeStyle;html=1;endArrow=ERmany;endFill=0;startArrow=ERone;startFill=0;strokeColor=#666666;" edge="1" parent="1" source="ent_ord" target="ent_line">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
  </root>
</mxGraphModel>
```

This example demonstrates:
- 3 entities with proper table containers and stacked attribute rows.
- PK fields with `fontStyle=4` (underline) and FK fields with `fontStyle=2` (italic).
- Crow's foot notation (`ERone` to `ERmany`) on both relationships.
- `entityRelationEdgeStyle` for ER-specific edge routing.
- Distinct colors per entity role (primary blue, secondary green, junction yellow).
- Relationship labels (`places`, `contains`) on edges.

## Alternative: Swimlane Entity Pattern

An alternative entity representation uses `swimlane` with `childLayout=stackLayout`:

```
swimlane;fontStyle=1;align=center;startSize=26;container=1;collapsible=0;childLayout=stackLayout;fillColor=#dae8fc;strokeColor=#6c8ebf;
```

This pattern is used in UML class diagrams and works for ER entities. The `shape=table;childLayout=tableLayout` pattern is PREFERRED for ER diagrams because it provides better table-like rendering with row separators.

## Checklist: Before Outputting an ER Diagram

1. Every entity uses `shape=table;container=1;childLayout=tableLayout;`.
2. Every attribute row is a child of its entity (`parent="<entity_id>"`).
3. Every PK field has `fontStyle=4;` (underline).
4. Every FK field has `fontStyle=2;` (italic).
5. Every relationship edge uses `edgeStyle=entityRelationEdgeStyle;`.
6. Every relationship edge uses `ER*` arrow types — NEVER `classic` or `block`.
7. Every ER arrow has `startFill=0;endFill=0;`.
8. Both structural cells (`id="0"` and `id="1"`) are present.
9. All edge `source` and `target` attributes point to valid entity cell IDs.
10. Entity heights match: `startSize + (attribute_count * 30)`.
11. Attribute row widths match the parent entity width.
12. Cell IDs are unique across the entire diagram.

## Cross-References

- **XML fundamentals:** See `drawio-core-xml-format` for file structure and structural cells.
- **Style syntax:** See `drawio-syntax-styles` for the complete style property reference.
- **Connection details:** See `drawio-syntax-connections` for edge routing and waypoints.
- **Geometry:** See `drawio-core-geometry` for coordinate system and positioning.

## Reference Links

- [Complete Reference](references/methods.md)
- [Working Examples](references/examples.md)
- [Anti-Patterns](references/anti-patterns.md)
