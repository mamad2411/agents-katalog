---
name: drawio-impl-bpmn
description: >
  Use when creating BPMN 2.0 process diagrams, workflow models, or business process
  maps in Draw.io. Prevents using wrong shapes for BPMN elements (e.g., rectangles
  for gateways) or mixing sequence and message flow styles. Covers events, activities,
  gateways, pools/lanes, and sequence vs message flows per BPMN 2.0 specification.
  Keywords: BPMN, business process, workflow, gateway, event, pool, lane,
  sequence flow, message flow, process diagram, model business process,
  workflow diagram, decision gateway.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io BPMN 2.0 Implementation

## Purpose

This skill enables correct generation of BPMN 2.0 (Business Process Model and Notation) process diagrams in Draw.io mxGraph XML. It enforces BPMN 2.0 shape semantics and prevents the most common AI mistakes: using generic shapes instead of BPMN-specific shapes, mixing sequence flows with message flows, and omitting mandatory pool containers for inter-organizational processes.

## Critical Rules (Memorize These)

1. **ALWAYS use `shape=mxgraph.bpmn.shape` for events and gateways** -- NEVER use generic `ellipse` for events or `rhombus` for gateways. BPMN shapes carry semantic meaning through `outline` and `symbol` properties.
2. **ALWAYS use dashed lines for message flows** -- Message flows between pools MUST have `dashed=1;endArrow=open;endFill=0;startArrow=oval;startFill=0;`. NEVER use solid arrows for message flows.
3. **ALWAYS use solid arrows for sequence flows** -- Sequence flows within a pool MUST have `endArrow=classic;html=1;`. NEVER use dashed arrows for sequence flows.
4. **NEVER connect elements in different pools with sequence flows** -- Cross-pool communication ALWAYS uses message flows. Sequence flows are ONLY valid within a single pool.
5. **ALWAYS wrap activities in a pool or lane** -- Every BPMN diagram with more than one participant MUST use pool containers. NEVER place BPMN elements directly on the canvas without a pool when modelling inter-organizational processes.
6. **ALWAYS use the correct gateway symbol** -- Exclusive (X) uses `symbol=exclusiveGw`, Parallel (+) uses `symbol=parallelGw`, Inclusive (O) uses `symbol=inclusiveGw`, Event-based uses `symbol=eventGw`. NEVER use a blank diamond.
7. **ALWAYS label gateway outgoing edges** -- Every edge leaving a gateway MUST have a `value` attribute describing the condition (except for parallel gateways where all paths execute).
8. **ALWAYS set `perimeter=ellipsePerimeter` on events and `perimeter=rhombusPerimeter` on gateways** -- This ensures edges connect correctly to the shape boundary.

## BPMN Element Categories

### Events

Events are circles that represent something that happens during a process. They differ by position (start/intermediate/end) and type (none, message, timer, error, signal, terminate).

| Event | outline | symbol | Visual | strokeWidth |
|-------|---------|--------|--------|-------------|
| Start (None) | `standard` | `general` | Thin circle, empty | 1 (default) |
| Start (Message) | `standard` | `message` | Thin circle, envelope icon | 1 |
| Start (Timer) | `standard` | `timer` | Thin circle, clock icon | 1 |
| Start (Signal) | `standard` | `signal` | Thin circle, triangle icon | 1 |
| Intermediate Catch (Message) | `catching` | `message` | Double thin circle, envelope | 1 |
| Intermediate Catch (Timer) | `catching` | `timer` | Double thin circle, clock | 1 |
| Intermediate Catch (Signal) | `catching` | `signal` | Double thin circle, triangle | 1 |
| Intermediate Throw (Message) | `throwing` | `message` | Double thin circle, filled envelope | 1 |
| Intermediate Throw (Signal) | `throwing` | `signal` | Double thin circle, filled triangle | 1 |
| End (None) | `end` | `terminate` | Thick circle, filled | 3 |
| End (Message) | `end` | `message` | Thick circle, envelope | 3 |
| End (Error) | `end` | `error` | Thick circle, lightning bolt | 3 |
| End (Terminate) | `end` | `terminate` | Thick circle, filled circle | 3 |

**Event style template:**

```
shape=mxgraph.bpmn.shape;perimeter=ellipsePerimeter;outline={OUTLINE};symbol={SYMBOL};
```

**Event dimensions:** ALWAYS use 40 x 40 for events. This is the BPMN standard circle size.

### Activities

Activities represent work performed in the process. BPMN uses rounded rectangles for tasks and double-bordered rounded rectangles for subprocesses.

| Activity | Style | Dimensions |
|----------|-------|-----------|
| Task | `rounded=1;whiteSpace=wrap;html=1;arcSize=20;` | 120 x 70 |
| Subprocess (collapsed) | `rounded=1;whiteSpace=wrap;html=1;arcSize=20;strokeWidth=2;` | 120 x 70 |
| Subprocess (expanded) | `rounded=1;whiteSpace=wrap;html=1;arcSize=10;container=1;collapsible=0;startSize=25;strokeWidth=2;` | 300 x 200 |

**Task type markers:** Add task type icons using additional style properties:

| Task Type | Additional Style |
|-----------|-----------------|
| User Task | `shape=mxgraph.bpmn.task;taskMarker=user;` |
| Service Task | `shape=mxgraph.bpmn.task;taskMarker=service;` |
| Script Task | `shape=mxgraph.bpmn.task;taskMarker=script;` |
| Send Task | `shape=mxgraph.bpmn.task;taskMarker=send;` |
| Receive Task | `shape=mxgraph.bpmn.task;taskMarker=receive;` |
| Manual Task | `shape=mxgraph.bpmn.task;taskMarker=manual;` |
| Business Rule Task | `shape=mxgraph.bpmn.task;taskMarker=businessRule;` |

### Gateways

Gateways are diamond shapes that control the flow branching and merging. ALWAYS use 50 x 50 dimensions.

| Gateway | symbol | Marker | Purpose |
|---------|--------|--------|---------|
| Exclusive (XOR) | `exclusiveGw` | X inside diamond | Exactly one outgoing path based on condition |
| Parallel (AND) | `parallelGw` | + inside diamond | ALL outgoing paths execute simultaneously |
| Inclusive (OR) | `inclusiveGw` | O inside diamond | One or more outgoing paths based on conditions |
| Event-based | `eventGw` | Pentagon inside diamond | Path determined by which event occurs first |

**Gateway style template:**

```
shape=mxgraph.bpmn.shape;perimeter=rhombusPerimeter;outline=standard;symbol={SYMBOL};
```

### Pools and Lanes

Pools represent participants (organizations, departments, systems). Lanes subdivide a pool into roles or responsibilities.

**Pool style:**

```
shape=pool;startSize=30;horizontal=1;container=1;collapsible=0;swimlaneLine=1;fillColor=#f5f5f5;strokeColor=#666666;fontStyle=1;
```

**Lane style:**

```
swimlane;startSize=30;container=1;collapsible=0;horizontal=1;fillColor=#f5f5f5;strokeColor=#666666;fontStyle=1;
```

Pool and lane rules follow the same container hierarchy as `drawio-impl-swimlanes`. ALWAYS set `container=1` and `collapsible=0`. ALWAYS use container-relative coordinates for children.

### Sequence Flows vs Message Flows

| Flow Type | Usage | Style |
|-----------|-------|-------|
| Sequence Flow | Between elements in the SAME pool | `endArrow=classic;html=1;` |
| Conditional Sequence Flow | Sequence flow with condition | `endArrow=classic;html=1;startArrow=diamond;startFill=0;startSize=14;` |
| Default Sequence Flow | Default path from gateway | `endArrow=classic;html=1;` + tick marker on source end |
| Message Flow | Between elements in DIFFERENT pools | `endArrow=open;endFill=0;startArrow=oval;startFill=0;dashed=1;strokeColor=#666666;` |
| Association | Link to data objects/annotations | `endArrow=none;dashed=1;strokeColor=#999999;` |

### Data Objects and Data Stores

| Element | Style | Dimensions |
|---------|-------|-----------|
| Data Object | `shape=mxgraph.bpmn.data;labelPosition=center;verticalLabelPosition=bottom;verticalAlign=top;` | 35 x 50 |
| Data Store | `shape=datastore;whiteSpace=wrap;html=1;` | 60 x 60 |

Data objects and data stores connect to activities using association flows (dashed, no arrowhead).

## Layout Guidelines

| Element | Spacing | Notes |
|---------|---------|-------|
| Events | 40 x 40 | Standard BPMN circle size |
| Activities | 120 x 70 | Rounded rectangles with arcSize=20 |
| Gateways | 50 x 50 | Diamond shapes |
| Horizontal gap | 40-60 px | Between consecutive elements |
| Vertical gap | 60-80 px | Between parallel branches |
| Pool width | 700-900 px | Wide enough for all elements |
| Pool height | 200-400 px | Tall enough for branches |

## Complete Example: Invoice Processing with BPMN 2.0

```xml
<mxGraphModel>
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />

    <!-- Pool: Finance Department -->
    <mxCell id="pool1" value="Finance Department" style="shape=pool;startSize=30;horizontal=1;container=1;collapsible=0;swimlaneLine=1;fillColor=#f5f5f5;strokeColor=#666666;fontStyle=1;" vertex="1" parent="1">
      <mxGeometry x="40" y="40" width="820" height="250" as="geometry" />
    </mxCell>

    <!-- Start Event -->
    <mxCell id="start" value="" style="shape=mxgraph.bpmn.shape;perimeter=ellipsePerimeter;outline=standard;symbol=general;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="pool1">
      <mxGeometry x="30" y="105" width="40" height="40" as="geometry" />
    </mxCell>

    <!-- Task: Receive Invoice -->
    <mxCell id="task1" value="Receive&#xa;Invoice" style="rounded=1;whiteSpace=wrap;html=1;arcSize=20;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="pool1">
      <mxGeometry x="110" y="90" width="120" height="70" as="geometry" />
    </mxCell>

    <!-- Exclusive Gateway: Amount Check -->
    <mxCell id="gw1" value="" style="shape=mxgraph.bpmn.shape;perimeter=rhombusPerimeter;outline=standard;symbol=exclusiveGw;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="pool1">
      <mxGeometry x="275" y="100" width="50" height="50" as="geometry" />
    </mxCell>

    <!-- Task: Auto-Approve -->
    <mxCell id="task2" value="Auto-Approve" style="rounded=1;whiteSpace=wrap;html=1;arcSize=20;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="pool1">
      <mxGeometry x="380" y="30" width="120" height="50" as="geometry" />
    </mxCell>

    <!-- Task: Manual Review -->
    <mxCell id="task3" value="Manual Review" style="rounded=1;whiteSpace=wrap;html=1;arcSize=20;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="pool1">
      <mxGeometry x="380" y="160" width="120" height="50" as="geometry" />
    </mxCell>

    <!-- Parallel Gateway: Merge -->
    <mxCell id="gw2" value="" style="shape=mxgraph.bpmn.shape;perimeter=rhombusPerimeter;outline=standard;symbol=parallelGw;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="pool1">
      <mxGeometry x="545" y="100" width="50" height="50" as="geometry" />
    </mxCell>

    <!-- Task: Process Payment -->
    <mxCell id="task4" value="Process&#xa;Payment" style="rounded=1;whiteSpace=wrap;html=1;arcSize=20;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="pool1">
      <mxGeometry x="640" y="90" width="120" height="70" as="geometry" />
    </mxCell>

    <!-- End Event -->
    <mxCell id="end" value="" style="shape=mxgraph.bpmn.shape;perimeter=ellipsePerimeter;outline=end;symbol=terminate;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="pool1">
      <mxGeometry x="770" y="105" width="40" height="40" as="geometry" />
    </mxCell>

    <!-- Sequence Flows -->
    <mxCell id="f1" style="endArrow=classic;html=1;" edge="1" parent="pool1" source="start" target="task1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="f2" style="endArrow=classic;html=1;" edge="1" parent="pool1" source="task1" target="gw1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="f3" value="&lt;= $1000" style="endArrow=classic;html=1;" edge="1" parent="pool1" source="gw1" target="task2">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="f4" value="&gt; $1000" style="endArrow=classic;html=1;" edge="1" parent="pool1" source="gw1" target="task3">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="f5" style="endArrow=classic;html=1;" edge="1" parent="pool1" source="task2" target="gw2">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="f6" style="endArrow=classic;html=1;" edge="1" parent="pool1" source="task3" target="gw2">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="f7" style="endArrow=classic;html=1;" edge="1" parent="pool1" source="gw2" target="task4">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="f8" style="endArrow=classic;html=1;" edge="1" parent="pool1" source="task4" target="end">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
  </root>
</mxGraphModel>
```

## Checklist: Before Outputting a BPMN Diagram

1. Every event uses `shape=mxgraph.bpmn.shape` with correct `outline` and `symbol` -- NOT generic `ellipse`.
2. Every gateway uses `shape=mxgraph.bpmn.shape` with correct `symbol` -- NOT generic `rhombus`.
3. Every event has `perimeter=ellipsePerimeter` and every gateway has `perimeter=rhombusPerimeter`.
4. Events are 40 x 40. Gateways are 50 x 50. Activities are 120 x 70.
5. Sequence flows use solid arrows (`endArrow=classic`). Message flows use dashed open arrows (`dashed=1;endArrow=open;endFill=0;startArrow=oval;startFill=0;`).
6. Cross-pool communication uses message flows ONLY -- NEVER sequence flows.
7. Every exclusive/inclusive gateway outgoing edge has a condition label.
8. All elements within a pool use container-relative coordinates.
9. Every pool and lane has `container=1` and `collapsible=0`.
10. Both structural cells (`id="0"` and `id="1"`) are present.
11. All cell IDs are unique and all edges have valid `source` and `target`.

## Cross-References

- **Swimlane containers:** See `drawio-impl-swimlanes` for pool/lane container hierarchy and coordinate rules.
- **XML fundamentals:** See `drawio-core-xml-format` for file structure and structural cells.
- **Style syntax:** See `drawio-syntax-styles` for the complete style property reference.
- **Connection details:** See `drawio-syntax-connections` for edge routing and waypoints.
- **Geometry:** See `drawio-core-geometry` for coordinate system and positioning.

## Reference Links

- [Complete Reference](references/methods.md)
- [Working Examples](references/examples.md)
- [Anti-Patterns](references/anti-patterns.md)
