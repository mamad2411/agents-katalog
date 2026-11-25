---
name: drawio-impl-mindmaps
description: >
  Use when creating mind maps, concept maps, or radial hierarchy diagrams in Draw.io.
  Prevents the common mistake of using straight orthogonal connectors instead of
  curved organic lines for mind map branches. Covers central topic, branch shapes,
  curved connectors, color coding, and tree layout patterns.
  Keywords: mind map, concept map, central topic, branch, radial, tree layout,
  organic connector, brainstorm diagram, idea map, topic hierarchy,
  visual brainstorming.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io Implementation: Mind Maps

## Purpose

This skill teaches how to create mind maps, concept maps, and radial hierarchy diagrams in Draw.io mxGraph XML. It covers central topic design, branch shapes at multiple levels, curved organic connectors, color coding strategies, and the differences between mind maps and concept maps.

## Critical Rules (Memorize These)

1. **ALWAYS use curved connectors** — Set `curved=1` on every branch edge. NEVER use `edgeStyle=orthogonalEdgeStyle`.
2. **ALWAYS use `endArrow=none`** on mind map connectors. Mind map branches are NOT directional.
3. **ALWAYS center the root topic** and spread branches radially (top, bottom, left, right).
4. **ALWAYS color each branch family consistently** — All children of a branch share the parent branch's color family.
5. **NEVER use orthogonal (right-angle) connectors** in mind maps — they destroy the organic visual style.
6. **NEVER use directed arrows** (`endArrow=classic`) on mind map branches.
7. **ALWAYS include `whiteSpace=wrap;html=1;`** in every shape style.
8. **ALWAYS use `relative="1"`** on every edge `<mxGeometry>`.

## Mind Map Anatomy

A mind map has three levels of visual hierarchy:

```
Level 0: Central Topic  — large ellipse or rounded rectangle, bold text, dark fill
Level 1: Main Branches  — medium rounded rectangles, bold text, colored fill
Level 2: Sub-Branches   — small rounded rectangles, normal text, lighter fill
Level 3+: Leaf Nodes    — smallest rounded rectangles, normal text, lightest fill or white
```

### Decision Tree: Mind Map vs Concept Map

```
Does the diagram have ONE central topic radiating outward?
  YES --> Mind Map
    Are branches hierarchical (parent-child only)?
      YES --> Classic Mind Map (no cross-links)
      NO  --> Mind Map with cross-references
  NO  --> Does it show labeled relationships between concepts?
    YES --> Concept Map (uses labeled arrows between nodes)
    NO  --> Use a different diagram type (flowchart, org chart)
```

**Key difference:** Mind maps use `endArrow=none` (unlabeled branches). Concept maps use `endArrow=classic` with labeled edges describing the relationship.

## Central Topic (Level 0)

The central topic is the root node. It MUST be the largest and most prominent shape.

### Ellipse Style (Recommended)

```xml
<mxCell id="center" value="Central Topic"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#1168bd;fontColor=#ffffff;strokeColor=#0b4884;fontSize=16;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="300" y="250" width="180" height="90" as="geometry" />
</mxCell>
```

### Rounded Rectangle Style (Alternative)

```xml
<mxCell id="center" value="Central Topic"
        style="rounded=1;whiteSpace=wrap;html=1;arcSize=40;fillColor=#1168bd;fontColor=#ffffff;strokeColor=#0b4884;fontSize=16;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="300" y="250" width="180" height="80" as="geometry" />
</mxCell>
```

### Central Topic Properties

| Property | Value | Reason |
|----------|-------|--------|
| Width | 160–200 px | Largest shape in the diagram |
| Height | 70–100 px | Proportional to width |
| fontSize | 14–18 | Largest text in the diagram |
| fontStyle | 1 (bold) | Emphasis on the central topic |
| fillColor | Dark saturated color | Visual anchor point |
| fontColor | `#ffffff` | Contrast against dark fill |

## Main Branches (Level 1)

Main branches connect directly to the central topic. Each represents a major category.

```xml
<mxCell id="b1" value="Branch One"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=13;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="80" y="100" width="130" height="45" as="geometry" />
</mxCell>
```

### Main Branch Properties

| Property | Value | Reason |
|----------|-------|--------|
| Width | 110–140 px | Smaller than central topic |
| Height | 35–50 px | Compact but readable |
| fontSize | 12–14 | Smaller than central topic |
| fontStyle | 1 (bold) | Distinguishes from sub-branches |
| fillColor | Medium saturation | Each branch uses a distinct color |

## Sub-Branches (Level 2)

Sub-branches connect to main branches. They are smaller and use lighter fills.

```xml
<mxCell id="b1_1" value="Sub-topic A"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=11;"
        vertex="1" parent="1">
  <mxGeometry x="10" y="160" width="100" height="30" as="geometry" />
</mxCell>
```

### Sub-Branch Properties

| Property | Value | Reason |
|----------|-------|--------|
| Width | 80–110 px | Smaller than main branches |
| Height | 28–35 px | Compact |
| fontSize | 10–12 | Smaller than main branches |
| fontStyle | 0 (normal) | Less emphasis |
| fillColor | Light tint of parent branch color, or `#f5f5f5` | Visual hierarchy |

## Curved Connectors (Branch Lines)

Mind map connectors MUST use curved lines without arrowheads.

### Central-to-Branch Connector (Level 0 to Level 1)

```xml
<mxCell id="e_center_b1"
        style="endArrow=none;html=1;curved=1;strokeWidth=2;strokeColor=#6c8ebf;"
        edge="1" source="center" target="b1" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Branch-to-Sub-Branch Connector (Level 1 to Level 2)

```xml
<mxCell id="e_b1_b1_1"
        style="endArrow=none;html=1;curved=1;strokeWidth=1;strokeColor=#999999;"
        edge="1" source="b1" target="b1_1" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Connector Style Rules

| Level | strokeWidth | strokeColor | Reason |
|-------|-------------|-------------|--------|
| 0 to 1 | 2–3 | Match branch fillColor or strokeColor | Thick main branches |
| 1 to 2 | 1–2 | `#999999` or lighter branch color | Thinner sub-branches |
| 2 to 3+ | 1 | `#BBBBBB` or `#CCCCCC` | Thinnest leaf connections |

### Required Connector Properties

| Property | Value | NEVER Use |
|----------|-------|-----------|
| `endArrow` | `none` | `classic`, `block`, `open` |
| `startArrow` | *(omit)* | Any arrow type |
| `curved` | `1` | `0` or omitting it |
| `edge` | `"1"` | *(NEVER omit)* |
| `relative` | `"1"` | *(NEVER omit on geometry)* |

## Color Coding Strategy

### Recommended Branch Color Families

| Branch | fillColor | strokeColor | Hex Family |
|--------|-----------|-------------|------------|
| Branch 1 (Blue) | `#dae8fc` | `#6c8ebf` | Blue |
| Branch 2 (Green) | `#d5e8d4` | `#82b366` | Green |
| Branch 3 (Yellow) | `#fff2cc` | `#d6b656` | Yellow |
| Branch 4 (Purple) | `#e1d5e7` | `#9673a6` | Purple |
| Branch 5 (Orange) | `#f8cecc` | `#b85450` | Red/Orange |
| Branch 6 (Teal) | `#d4e1f5` | `#4a86c8` | Teal |

### Color Hierarchy Rule

```
Central Topic:  DARKEST color      (fillColor=#1168bd, fontColor=#ffffff)
Main Branch:    MEDIUM saturation   (fillColor=#dae8fc, strokeColor=#6c8ebf)
Sub-Branch:     LIGHT tint          (fillColor=#f5f5f5, strokeColor=#666666)
Leaf Node:      LIGHTEST or white   (fillColor=#ffffff, strokeColor=#999999)
```

## Radial Layout Pattern

### Branch Positioning Strategy

Position main branches around the central topic. ALWAYS distribute branches to avoid overlap.

```
                    [Branch Top-Left]     [Branch Top-Right]
                           \                /
                            \              /
           [Branch Left] --- [CENTRAL] --- [Branch Right]
                            /              \
                           /                \
                 [Branch Bottom-Left]  [Branch Bottom-Right]
```

### Position Reference (Central Topic at 380,250, size 180x90)

| Branch Position | X | Y | Direction from Center |
|----------------|-----|-----|----------------------|
| Top-left | 80 | 60 | Upper-left quadrant |
| Top-right | 600 | 60 | Upper-right quadrant |
| Left | 30 | 240 | Directly left |
| Right | 650 | 240 | Directly right |
| Bottom-left | 80 | 440 | Lower-left quadrant |
| Bottom-right | 600 | 440 | Lower-right quadrant |

### Sub-Branch Positioning

Place sub-branches further out from the center, clustered near their parent branch:

- Sub-branches of a top-left branch go ABOVE and to the LEFT of the parent.
- Sub-branches of a bottom-right branch go BELOW and to the RIGHT of the parent.
- ALWAYS maintain at least 20px vertical spacing between sibling sub-branches.

## Complete Mind Map XML Example

A 3-level mind map with central topic, 3 main branches, and sub-branches.

```xml
<mxGraphModel>
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />

    <!-- Central Topic -->
    <mxCell id="center" value="Project Plan"
            style="ellipse;whiteSpace=wrap;html=1;fillColor=#1168bd;fontColor=#ffffff;strokeColor=#0b4884;fontSize=16;fontStyle=1;"
            vertex="1" parent="1">
      <mxGeometry x="300" y="200" width="160" height="80" as="geometry" />
    </mxCell>

    <!-- Branch 1: Design (Blue, top-left) -->
    <mxCell id="b1" value="Design"
            style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=13;fontStyle=1;"
            vertex="1" parent="1">
      <mxGeometry x="80" y="60" width="120" height="40" as="geometry" />
    </mxCell>
    <mxCell id="b1_1" value="Wireframes"
            style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;"
            vertex="1" parent="1">
      <mxGeometry x="10" y="120" width="100" height="30" as="geometry" />
    </mxCell>
    <mxCell id="b1_2" value="Mockups"
            style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;"
            vertex="1" parent="1">
      <mxGeometry x="130" y="120" width="100" height="30" as="geometry" />
    </mxCell>

    <!-- Branch 2: Development (Green, top-right) -->
    <mxCell id="b2" value="Development"
            style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=13;fontStyle=1;"
            vertex="1" parent="1">
      <mxGeometry x="540" y="60" width="120" height="40" as="geometry" />
    </mxCell>
    <mxCell id="b2_1" value="Frontend"
            style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;"
            vertex="1" parent="1">
      <mxGeometry x="510" y="120" width="100" height="30" as="geometry" />
    </mxCell>
    <mxCell id="b2_2" value="Backend"
            style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;"
            vertex="1" parent="1">
      <mxGeometry x="630" y="120" width="100" height="30" as="geometry" />
    </mxCell>

    <!-- Branch 3: Testing (Yellow, bottom-center) -->
    <mxCell id="b3" value="Testing"
            style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=13;fontStyle=1;"
            vertex="1" parent="1">
      <mxGeometry x="320" y="360" width="120" height="40" as="geometry" />
    </mxCell>
    <mxCell id="b3_1" value="Unit Tests"
            style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;"
            vertex="1" parent="1">
      <mxGeometry x="240" y="420" width="100" height="30" as="geometry" />
    </mxCell>
    <mxCell id="b3_2" value="Integration"
            style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;"
            vertex="1" parent="1">
      <mxGeometry x="360" y="420" width="100" height="30" as="geometry" />
    </mxCell>
    <mxCell id="b3_3" value="E2E Tests"
            style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;"
            vertex="1" parent="1">
      <mxGeometry x="480" y="420" width="100" height="30" as="geometry" />
    </mxCell>

    <!-- Connectors: Center to Main Branches (thick, colored, curved) -->
    <mxCell id="ec1" style="endArrow=none;html=1;curved=1;strokeWidth=2;strokeColor=#6c8ebf;"
            edge="1" source="center" target="b1" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="ec2" style="endArrow=none;html=1;curved=1;strokeWidth=2;strokeColor=#82b366;"
            edge="1" source="center" target="b2" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="ec3" style="endArrow=none;html=1;curved=1;strokeWidth=2;strokeColor=#d6b656;"
            edge="1" source="center" target="b3" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>

    <!-- Connectors: Main Branches to Sub-Branches (thin, gray, curved) -->
    <mxCell id="ec1a" style="endArrow=none;html=1;curved=1;strokeColor=#999999;"
            edge="1" source="b1" target="b1_1" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="ec1b" style="endArrow=none;html=1;curved=1;strokeColor=#999999;"
            edge="1" source="b1" target="b1_2" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="ec2a" style="endArrow=none;html=1;curved=1;strokeColor=#999999;"
            edge="1" source="b2" target="b2_1" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="ec2b" style="endArrow=none;html=1;curved=1;strokeColor=#999999;"
            edge="1" source="b2" target="b2_2" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="ec3a" style="endArrow=none;html=1;curved=1;strokeColor=#999999;"
            edge="1" source="b3" target="b3_1" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="ec3b" style="endArrow=none;html=1;curved=1;strokeColor=#999999;"
            edge="1" source="b3" target="b3_2" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="ec3c" style="endArrow=none;html=1;curved=1;strokeColor=#999999;"
            edge="1" source="b3" target="b3_3" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
  </root>
</mxGraphModel>
```

## Concept Map Variant

Concept maps differ from mind maps: they use **labeled, directed edges** and allow **cross-links** between any nodes.

### Concept Map Connector Style

```xml
<mxCell id="cm_e1" value="requires"
        style="endArrow=classic;html=1;curved=1;strokeColor=#666666;fontSize=10;fontColor=#666666;"
        edge="1" source="concept_a" target="concept_b" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Mind Map vs Concept Map Summary

| Property | Mind Map | Concept Map |
|----------|----------|-------------|
| `endArrow` | `none` | `classic` |
| Edge labels | NEVER | ALWAYS (relationship name) |
| Cross-links | Rare | Common |
| Structure | Strict hierarchy | Network/graph |
| Central topic | ALWAYS one | Optional |

## Draw.io Tree Layout Integration

Draw.io provides automatic mind map layout. After placing nodes and edges manually, apply the layout:

**Menu path:** Edit > Layout > Tree > Mindmap

This auto-arranges nodes radially. The XML remains unchanged; Draw.io recalculates `<mxGeometry>` positions.

### Tree Layout Plugin Properties

When using the `mxCompactTreeLayout` programmatically:

| Property | Mind Map Value | Description |
|----------|---------------|-------------|
| `horizontal` | `false` | Radial spread (not left-to-right) |
| `levelDistance` | `60` | Gap between hierarchy levels |
| `nodeDistance` | `20` | Gap between sibling nodes |
| `edgeRouting` | `curved` | ALWAYS use curved for mind maps |

## Reference Links

- [Complete Reference](references/methods.md)
- [Working Examples](references/examples.md)
- [Anti-Patterns](references/anti-patterns.md)
