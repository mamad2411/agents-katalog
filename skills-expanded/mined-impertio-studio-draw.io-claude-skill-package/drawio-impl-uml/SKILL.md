---
name: drawio-impl-uml
description: >
  Use when creating UML diagrams (class, sequence, use case, state machine, activity)
  in Draw.io. Prevents the common mistake of using generic arrows instead of UML-specific
  connector styles (aggregation=open diamond, composition=filled diamond, generalization=open
  triangle). Covers class diagram compartments, sequence diagram lifelines, and all 6 UML
  relationship types with correct arrow styles.
  Keywords: UML, class diagram, sequence diagram, use case, state machine,
  aggregation, composition, generalization, software design, object model,
  interaction diagram, class relationships.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io UML Diagram Implementation

## Purpose

This skill enables correct generation of UML diagrams in Draw.io mxGraph XML. It covers the five most common UML diagram types: class, sequence, use case, state machine, and activity. The most common AI mistake is using generic arrows (`endArrow=classic`) instead of UML-specific connector styles (open diamond for aggregation, filled diamond for composition, hollow triangle for generalization).

## Critical Rules (Memorize These)

1. **ALWAYS use `endArrow=block;endFill=0` for generalization/inheritance** — the hollow triangle. NEVER use `endFill=1` which produces a filled triangle (wrong UML semantics).
2. **ALWAYS use `startArrow=diamond;startFill=0` for aggregation** — the open diamond. NEVER use `startFill=1` which produces composition instead.
3. **ALWAYS use `startArrow=diamond;startFill=1` for composition** — the filled diamond. The fill distinguishes composition from aggregation.
4. **ALWAYS use `dashed=1` for dependency and realization edges** — solid lines are WRONG for these relationship types.
5. **ALWAYS use `shape=umlLifeline;perimeter=lifelinePerimeter` for sequence diagram participants** — NEVER use plain rectangles with manual dashed lines.
6. **ALWAYS use `shape=umlActor` for UML actors** — NEVER use `shape=ellipse` or stick-figure images.
7. **ALWAYS use the 3-compartment swimlane pattern for UML classes** — class name header, attributes compartment, operations compartment, separated by `line` cells.
8. **ALWAYS include both structural cells** (`id="0"` and `id="1"` with `parent="0"`) in every diagram.
9. **ALWAYS use `endArrow=open;endFill=0;dashed=1` for return messages** in sequence diagrams — NEVER use solid lines for returns.
10. **ALWAYS place use cases inside the system boundary container** — NEVER place them at `parent="1"` when a system boundary exists.

## UML Relationship Arrow Styles

### The 6 Core Relationship Types

| Relationship | startArrow | endArrow | dashed | startFill | endFill | Visual |
|-------------|-----------|----------|--------|-----------|---------|--------|
| Association | none | none | 0 | — | — | Plain line |
| Directed Association | none | open | 0 | — | 1 | Line + open arrow |
| Generalization | none | block | 0 | — | 0 | Line + hollow triangle |
| Realization | none | block | 1 | — | 0 | Dashed + hollow triangle |
| Aggregation | diamond | none | 0 | 0 | — | Open diamond + line |
| Composition | diamond | none | 0 | 1 | — | Filled diamond + line |
| Dependency | none | open | 1 | — | 1 | Dashed + open arrow |

### Edge Style Strings

**Association (plain):**
```
endArrow=none;html=1;edgeStyle=orthogonalEdgeStyle;
```

**Directed Association:**
```
endArrow=open;endFill=1;html=1;edgeStyle=orthogonalEdgeStyle;
```

**Generalization (inheritance):**
```
endArrow=block;endFill=0;html=1;edgeStyle=orthogonalEdgeStyle;
```

**Realization (interface implementation):**
```
endArrow=block;endFill=0;dashed=1;html=1;edgeStyle=orthogonalEdgeStyle;
```

**Aggregation (has-a, shared):**
```
startArrow=diamond;startFill=0;endArrow=none;html=1;edgeStyle=orthogonalEdgeStyle;
```

**Composition (has-a, owned):**
```
startArrow=diamond;startFill=1;endArrow=none;html=1;edgeStyle=orthogonalEdgeStyle;
```

**Dependency (uses):**
```
endArrow=open;endFill=1;dashed=1;html=1;edgeStyle=orthogonalEdgeStyle;
```

## Class Diagram

### 3-Compartment Class Structure

A UML class uses `swimlane` with `childLayout=stackLayout` containing three child zones separated by `line` cells.

**Container style (class header):**
```
swimlane;fontStyle=1;align=center;startSize=26;container=1;collapsible=0;childLayout=stackLayout;
```

**Attributes compartment:**
```
text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;whiteSpace=wrap;html=0;
```

**Separator line:**
```
line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=10;rotatable=0;labelPosition=left;points=[];portConstraint=eastwest;
```

**Operations compartment:**
```
text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;whiteSpace=wrap;html=0;
```

### UML Visibility Prefixes

| Prefix | Meaning |
|--------|---------|
| `+` | Public |
| `-` | Private |
| `#` | Protected |
| `~` | Package |

### Attribute Format

```
visibility name: Type
```

Example: `- id: int` or `+ getName(): String`

### Class Dimensions

| Component | Width | Height | Notes |
|-----------|-------|--------|-------|
| Class container | 200 | Calculated | startSize + attr_height + sep + ops_height |
| Header band | 200 | 26 (startSize) | Bold class name |
| Attributes cell | 200 | attr_count * 18 | ~18px per attribute line |
| Separator | 200 | 8 | Fixed thin line |
| Operations cell | 200 | ops_count * 18 | ~18px per operation line |

Use `&#xa;` for newlines within attribute/operation text values (`html=0` mode).

### Abstract and Interface Classes

**Abstract class** — add `fontStyle=3;` (bold + italic) to the container and prefix name with `<<abstract>>`:
```
swimlane;fontStyle=3;align=center;startSize=26;container=1;collapsible=0;childLayout=stackLayout;
```

**Interface** — prefix name with `<<interface>>` and use `fontStyle=3;`:
```
swimlane;fontStyle=3;align=center;startSize=26;container=1;collapsible=0;childLayout=stackLayout;
```

## Sequence Diagram

### Lifeline Shape

```
shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;container=1;collapsible=0;recursiveResize=0;outlineConnect=0;size=40;
```

Key properties:
- `shape=umlLifeline` — REQUIRED. Renders the rectangle header + dashed vertical line.
- `perimeter=lifelinePerimeter` — REQUIRED. Enables correct connection points along the lifeline.
- `size=40` — height of the participant header box in pixels.
- `container=1` — allows activation bars as children.
- Total `height` of the mxGeometry determines how far the dashed line extends.

### Lifeline Dimensions

| Property | Value | Notes |
|----------|-------|-------|
| Width | 100 | Standard lifeline width |
| Height | 300-500 | Total lifeline length (adjust per diagram complexity) |
| size | 40 | Header box height |
| Horizontal spacing | 200 | Between lifeline centers |

### Message Types

| Message Type | endArrow | endFill | dashed | Visual |
|-------------|----------|---------|--------|--------|
| Synchronous | block | 1 | 0 | Solid + filled arrow |
| Asynchronous | open | 1 | 0 | Solid + open arrow |
| Return | open | 0 | 1 | Dashed + open arrow |
| Create | open | 1 | 0 | Solid + open arrow (to new lifeline) |
| Destroy | none | — | 0 | Solid line + X at target |

**Synchronous message style:**
```
html=1;verticalAlign=bottom;endArrow=block;endFill=1;
```

**Asynchronous message style:**
```
html=1;verticalAlign=bottom;endArrow=open;endFill=1;
```

**Return message style:**
```
html=1;verticalAlign=bottom;endArrow=open;endFill=0;dashed=1;
```

### Message Positioning

Messages use absolute `sourcePoint` and `targetPoint` coordinates (NOT `source`/`target` cell references):

```xml
<mxCell id="msg1" value="request()" style="html=1;verticalAlign=bottom;endArrow=block;endFill=1;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="130" y="120" as="sourcePoint" />
    <mxPoint x="330" y="120" as="targetPoint" />
  </mxGeometry>
</mxCell>
```

- `sourcePoint.x` = source lifeline center (lifeline x + width/2).
- `targetPoint.x` = target lifeline center.
- Both points share the same `y` value for horizontal messages.
- Increment `y` by 40-50px between consecutive messages.

### Activation Bars

Activation bars are child cells of their lifeline:

```xml
<mxCell id="act1" value="" style="html=1;points=[];perimeter=orthogonalPerimeter;outlineConnect=0;targetShapes=umlLifeline;portConstraint=eastwest;newEdgeStyle={&quot;curved&quot;:0,&quot;rounded&quot;:0};" vertex="1" parent="ll1">
  <mxGeometry x="45" y="80" width="10" height="80" as="geometry" />
</mxCell>
```

- `x=45` centers the 10px-wide bar on a 100px-wide lifeline ((100-10)/2 = 45).
- `y` is relative to the lifeline top (NOT absolute).
- `height` spans from first incoming message to last outgoing message.

## Use Case Diagram

### Actor Shape

```
shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;
```

Dimensions: width=30, height=55. ALWAYS place actors outside the system boundary.

### Use Case (Ellipse)

```
ellipse;whiteSpace=wrap;html=1;
```

Dimensions: width=180, height=60. ALWAYS place inside the system boundary container.

### System Boundary

```
rounded=1;whiteSpace=wrap;html=1;container=1;collapsible=0;fillColor=none;strokeColor=#666666;strokeWidth=2;dashed=1;verticalAlign=top;fontStyle=1;fontSize=14;
```

The system boundary is a `container=1` cell. Use cases MUST be children of this container (`parent="<system_id>"`).

### Use Case Relationships

| Relationship | Style | Notes |
|-------------|-------|-------|
| Actor-to-UseCase | `endArrow=none;html=1;` | Plain line, no arrows |
| Include | `endArrow=open;endFill=1;dashed=1;html=1;` | Dashed + label `<<include>>` |
| Extend | `endArrow=open;endFill=1;dashed=1;html=1;` | Dashed + label `<<extend>>` |
| Generalization | `endArrow=block;endFill=0;html=1;` | Hollow triangle |

## State Machine Diagram

### State Shapes

**Initial state (filled circle):**
```
ellipse;fillColor=#000000;strokeColor=#000000;
```
Dimensions: width=30, height=30.

**Regular state (with actions):**
```
rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=top;arcSize=15;
```

Use HTML in the value for state compartments:
```
<b>StateName</b><hr>entry / action()<br>exit / action()
```

**Final state (bullseye):**
```
ellipse;html=1;shape=doubleCircle;fillColor=#000000;strokeColor=#000000;
```
Dimensions: width=30, height=30.

### Transition Edge

```
endArrow=open;endFill=1;html=1;
```

Label format: `event [guard] / action`

## Activity Diagram

### Activity Shapes

**Initial node:** Same as state machine initial state.

**Action node:**
```
rounded=1;whiteSpace=wrap;html=1;
```

**Decision node (diamond):**
```
rhombus;whiteSpace=wrap;html=1;
```
Dimensions: width=40, height=40. Label outgoing edges with `[guard]`.

**Fork/Join bar (horizontal):**
```
shape=line;html=1;strokeWidth=6;strokeColor=#000000;fillColor=#000000;
```
Dimensions: width=200, height=10.

**Fork/Join bar (vertical):**
```
shape=line;html=1;strokeWidth=6;strokeColor=#000000;fillColor=#000000;direction=south;
```
Dimensions: width=10, height=200.

**Final node:** Same as state machine final state.

### Activity Edge

```
endArrow=open;endFill=1;html=1;edgeStyle=orthogonalEdgeStyle;
```

## Color Conventions

| Element | Fill Color | Stroke Color |
|---------|-----------|-------------|
| Primary class/lifeline | `#dae8fc` (light blue) | `#6c8ebf` |
| Secondary class/lifeline | `#d5e8d4` (light green) | `#82b366` |
| Tertiary class/lifeline | `#fff2cc` (light yellow) | `#d6b656` |
| Abstract/interface | `#e1d5e7` (light purple) | `#9673a6` |
| System boundary | `none` | `#666666` |
| Initial/final state | `#000000` | `#000000` |

## Layout Strategy

### Class Diagrams
- Horizontal spacing: 120-160px between classes.
- Vertical spacing: 100-140px for inheritance hierarchies.
- Place parent classes ABOVE child classes for generalization.
- Place associated classes side by side.

### Sequence Diagrams
- Lifeline horizontal spacing: 200px center-to-center.
- Message vertical spacing: 40-50px between messages.
- Total lifeline height: 40 (header) + (message_count * 50) + 60 (margin).

### Use Case Diagrams
- Actors 80-120px outside the system boundary.
- Use cases spaced 80px vertically within the boundary.
- System boundary sized to fit all use cases with 40px padding.

## Checklist: Before Outputting a UML Diagram

1. Every class uses `swimlane;container=1;childLayout=stackLayout;` with 3 compartments.
2. Every class has a `line` separator between attributes and operations.
3. Every generalization edge uses `endArrow=block;endFill=0` (hollow triangle).
4. Every aggregation edge uses `startArrow=diamond;startFill=0` (open diamond).
5. Every composition edge uses `startArrow=diamond;startFill=1` (filled diamond).
6. Every dependency/realization edge uses `dashed=1`.
7. Every sequence lifeline uses `shape=umlLifeline;perimeter=lifelinePerimeter`.
8. Every return message uses `dashed=1;endArrow=open;endFill=0`.
9. Every actor uses `shape=umlActor` — NEVER `shape=ellipse`.
10. Every use case is a child of the system boundary container.
11. Both structural cells (`id="0"` and `id="1"`) are present.
12. All cell IDs are unique across the entire diagram.
13. All edge `source`/`target` attributes (or sourcePoint/targetPoint) are valid.

## Cross-References

- **XML fundamentals:** See `drawio-core-xml-format` for file structure and structural cells.
- **Style syntax:** See `drawio-syntax-styles` for the complete style property reference.
- **Connection details:** See `drawio-syntax-connections` for edge routing and waypoints.
- **Geometry:** See `drawio-core-geometry` for coordinate system and positioning.
- **Swimlanes:** See `drawio-impl-swimlanes` for container and lane patterns.

## Reference Links

- [Complete Reference](references/methods.md)
- [Working Examples](references/examples.md)
- [Anti-Patterns](references/anti-patterns.md)
