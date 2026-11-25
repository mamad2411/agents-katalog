---
name: drawio-aws-reference
description: Produce AWS architecture diagrams as editable .drawio files using the AWS 2026 shape set (mxgraph.aws4 stencils), with verified stencil names and a validator. Use this whenever an AWS architecture diagram is requested, revised, or reviewed, including when the user only says "draw the architecture", "diagram this", "make me a schema", "hazme un diagrama", or hands over a design document that needs a visual. Also use it when converting a Mermaid sketch into a real draw.io file. Do not use it for non-AWS diagrams.
---

# AWS architecture diagrams in draw.io

The goal is to hand over a `.drawio` file the user can open and adjust without
rebuilding nodes. Most rework comes from four mechanical mistakes, and all four
are avoidable by following this spec literally.

Mermaid is fine for iterating on the logic inside the conversation. The
deliverable is always `.drawio`.

## Source of truth

When the user supplies both a prose description and a Mermaid sketch, **the
prose wins.** Mermaid is a convenience for reading the shape of the system, and
it drops detail: a flow mentioned in the description but missing from the
diagram is still a flow.

Read both, then check for **orphans**: any resource with no edge in or out. A
bucket nothing writes to, a queue nothing reads, a database nobody queries. An
orphan is almost always a gap in the source description rather than a real dead
end. Ask before drawing it, and say which flow you think is missing.

## Required workflow

1. Settle the logic of the diagram in text or Mermaid, and confirm it with the
   user before writing any XML.
2. Look up every name: service icons in `reference/resicons.txt`, VPC
   sub-components and actors in `reference/shapes.txt`, containers in
   `reference/groups.md`. Never write a stencil name from memory.
3. Write the `.drawio` file.
4. Run `scripts/validate.py` against it and fix everything it reports as an
   error.
5. Deliver, and close with the handover note below.

Step 4 is not optional. A diagram that has not passed the validator is not
delivered.

## Handover note

The validator checks the mechanics. It cannot see the rendered result, so
spacing that is technically legal can still look wrong, and an edge label can
still land somewhere awkward. Say so when handing the file over, in the user's
language, in one or two sentences. Something along these lines:

> El diagrama puede necesitar retoques menores. Puedes resolverlos en draw.io,
> o exportarme el PNG en modo claro y sin fondo transparente y lo ajusto yo.

> The diagram may need minor touch-ups. You can fix them in draw.io, or export
> a PNG in light mode with a transparent background turned off and send it back
> so I can adjust it.

Two things make this note worth writing every time. It sets the expectation that
a first pass is a draft, not a finished artifact. And it asks for the one input
that actually lets the next iteration be better: a render, in light mode,
because draw.io inverts colors when exporting with the dark theme on and the
result is misleading.

Never claim the diagram is finished or correct because the validator passed.

## The four mistakes that cause rework

**Missing `points` array.** Without it draw.io only offers floating perimeter
connections, so the user cannot drag an arrow to a specific side of an icon.
They have to delete the node and pull a fresh one from the palette. This is the
most expensive of the four.

**Invented `resIcon` name.** If the stencil does not exist, no icon renders.
Names are verified against `reference/resicons.txt`, extracted from
`Sidebar-AWS4.js` in the draw.io repository.

**Unescaped `<br>` in a label.** A raw `<` inside an XML attribute makes the
whole file unparseable. It must be written `&lt;br&gt;`.

**Line breaks as `&#10;`.** With `html=1` these render as a space, not a break.
Two-line labels come out crammed onto one line.

## Language of labels

AWS service and resource names are always written in their original English
form. `Amazon CloudFront` is `Amazon CloudFront` in every language, and a
bucket named `media-delivery` keeps that name. Translating them breaks the
correspondence with the AWS console.

Everything else follows the language the user is writing in. Titles, edge
labels, notes and the legend go in that language: "cached responses" in
English, "respuestas en caché" in Spanish, "risposte memorizzate nella cache"
in Italian. If the user writes in Japanese, the descriptive text is in
Japanese.

When the diagram accompanies a document, the language of the document wins over
the language of the chat.

## Service nodes

Full pattern. The anchor array comes first and is never omitted:

```
sketch=0;points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],[0,0.25,0],[0,0.5,0],[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]];outlineConnect=0;fontColor=#232F3E;fillColor=FAMILY;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.NAME;
```

Size 78x78. `NAME` comes from `reference/resicons.txt`.

### Service tile or outline glyph

AWS draws a **service** as a glyph on a filled colored tile, and a **resource
inside a service** as an outline glyph with no background. The two are different
sections of the shape library and they carry different meaning: EC2, S3, Lambda
and RDS are services; Internet Gateway, NAT Gateway, Application Load Balancer,
VPC Endpoint and NACL are resources within a service. Users, clients and the
internet are not AWS at all and use the same outline form in dark navy.

Keeping the distinction means a reader can tell at a glance what is a billable
service and what is a component inside one. Putting everything on a colored tile
throws that information away.

Technically `resIcon` accepts any stencil name, so a resource glyph can be
forced onto a tile and it will render. Do not: use `resIcon` for the names in
`reference/resicons.txt`, and the plain shape style for the names in
`reference/shapes.txt`.

`fillColor` by service family:

| Family | Color |
|---|---|
| Storage | `#7AA116` |
| Compute, containers, Lambda | `#ED7100` |
| Networking and content delivery | `#8C4FFF` |
| Database | `#C925D1` |
| Security, identity, compliance | `#DD344C` |
| Management and governance | `#E7157B` |
| Application integration | `#E7157B` |
| Analytics | `#8C4FFF` |

## VPC sub-components and external actors

Internet Gateway, NAT Gateway, VPC Endpoint, NACL, router, Elastic IP, users,
traditional server and similar are **not** `resourceIcon` entries. They are
plain shapes, listed in `reference/shapes.txt`, and they use a different style
prefix:

```
sketch=0;ANCHORS;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#8C4FFF;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.NAME;
```

VPC networking components are `#8C4FFF`. External actors (users, internet,
on-premise servers) are `#7D8998` or `#232F3D`.

The palette version of these shapes ships **without** the `points` array, so it
has to be added by hand exactly as with `resourceIcon` nodes. Same failure mode:
arrows that cannot be moved.

## Group containers

Only 15 `grIcon` values exist. They are listed in `reference/groups.md` with
their exact styles. **There is no `group_subnet`.** Subnets are built from
`group_security_group` with different colors.

Containers use the paired anchor array:

```
points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]]
```

## Labels

Line breaks are `&lt;br&gt;` inside the XML attribute. Never a raw `<br>`,
never `&#10;`, never a literal newline.

## Edges

Use `edgeStyle=orthogonalEdgeStyle`. Set the exit and entry anchors and let the
router solve the path:

```
edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;fontSize=11;strokeColor=#232F3E;endArrow=blockThin;endFill=1;labelBackgroundColor=#ffffff;exitX=1;exitY=0.5;exitPerimeter=0;entryX=0;entryY=0.5;entryPerimeter=0;
```

Labeled edges carry `labelBackgroundColor=#ffffff` so the text stays readable
where lines cross.

### Routing: side exit, then a dogleg through a free channel

The default router picks its own path and usually drags the line across an icon
or a label. The reliable pattern is:

1. Leave the source through its **side** (`exitX=1` or `exitX=0`), pointing
   toward the target.
2. Run horizontally only as far as a **free vertical channel**, meaning the
   empty column between two icon columns.
3. Turn there with an explicit waypoint pair and travel vertically.
4. Enter the target through a side or a corner-adjacent anchor.

Waypoints are not forbidden, they are the tool for step 3. What is forbidden is
placing them without computing them: every waypoint x must fall inside a gap
between icon columns, never inside an icon's bounding box.

Concretely, with icons at x=355 and x=640, both 78 wide, the free channel runs
from 433 to 640. Any turn between roughly 460 and 620 is safe.

When several edges share a region, give each one a **different channel**, spaced
at least 40px apart. Below that, two parallel lines read as one thick line and
the reader cannot tell which arrowhead belongs to which. The same applies to
horizontal bands running under a group of containers. Give them
different entry anchors on a shared target too (`entryY=0.75` for one,
`entryX=0.5;entryY=1` for another), so the arrowheads do not stack.

A vertical leg crossing a container border is fine and normal. A horizontal leg
running along a row that contains another icon is not.

### Label position on the path

By default the label sits at the midpoint, which on a dogleg is the corner: the
worst place. The `x` attribute of an edge's `mxGeometry` moves it along the
path, and the range is **-1 to 1**, where -1 is the source end, 0 the middle and
1 the target end. To pull a label back toward the source, the value must be
**negative**: -0.8 sits close to the source, -0.4 partway along. Positive values
push it toward the target, which is usually where the crowding already is.

```xml
<mxGeometry x="0.09" relative="1" as="geometry">
  <Array as="points"><mxPoint x="624" y="524" /><mxPoint x="624" y="228" /></Array>
  <mxPoint as="offset" />
</mxGeometry>
```

Line style convention: solid for data flow, dashed (`dashed=1`) for control,
encryption, auditing and lifecycle transitions.

## Canvas layout

**A labeled icon is as wide as its label, not 78px.** This is the single most
common cause of an ugly diagram. A two-line label like
`NAT Gateway dataconnect-nat` is roughly 170px wide and sits centered under a
78px icon, so it spills 45px past each side. Budget columns from the label
width, not the icon width.

Keep node labels to two lines: the resource name, then at most one line of
detail. Anything longer goes in the surrounding prose, not on the canvas. Three
lines of configuration under every icon is how a diagram turns into a wall.

- Minimum horizontal gap between icon columns: 180px when edges carry labels,
  120px when they do not. More when labels are long.
- Minimum vertical gap between rows: 120px, and more when labels wrap.
- The top-left corner of every group container belongs to that container's own
  label. Nothing goes there. An icon placed on a container border, which is the
  correct convention for an Internet Gateway or a NAT Gateway, must sit well
  clear of that corner.
- Do not straddle container borders with icons. An Internet Gateway drawn on
  the VPC edge looks right in AWS marketing diagrams and reads badly in a dense
  one: its label lands inside the container and collides with whatever sits
  below. Place it fully outside the border instead, with its label in the
  default position underneath.
- Grouping boxes never sit on a channel that edges must cross. If a group is in
  the way, move the group.
- External actors (users, internet, on-premise datacenter) go outside the AWS
  Cloud container.
- The AWS Cloud container must fully enclose everything inside it, and should
  not leave more than about 150px of dead space on any side.

## Edges must not cross other nodes

An orthogonal edge leaves through its exit anchor and travels along that axis
first. If the exit anchor is on a side (`exitY=0.5`), the first leg runs along
the source's row and will plough straight through anything sitting in that row
between source and target. The same applies to the arriving leg.

Before choosing anchors, check what sits between the two nodes. Leaving through
the top or bottom (`exitY=0` or `exitY=1`) sidesteps a same-row obstacle
entirely. When two edges leave the same node, give them different anchors
(`exitX=0.25` and `exitX=0.75`) so they do not stack on top of each other.

## Edge labels

Edge labels default to the midpoint of the path, which on a bend often lands on
top of a node label or another edge. Keep them to three or four words. If an
edge needs a sentence to explain it, the explanation belongs in the document,
not on the arrow.

**Pad every edge label with `&#160;` on both sides.** draw.io fits the white
label background tightly around the text, so without padding the line touches
the letters and the label reads as part of the stroke. Write
`value="&#160;via Elastic IP&#160;"`, not `value="via Elastic IP"`.

An edge label needs a channel to live in. Where a labeled edge runs horizontally
between two stacked containers, leave at least 60px between them. At 30px the
label sits across both borders and the diagram looks crowded even though nothing
technically overlaps.

An edge that does not represent a flow is usually not an edge. A NACL filtering
its subnet, for instance, reads better as an icon placed inside that subnet with
the relationship stated in its label than as an arrow pointing at a container
border.

## Legend box

Only in complex diagrams, where the line or color convention is not obvious. If
the diagram explains itself, the legend is noise and gets cut.

## Validation

```
python3 scripts/validate.py path/to/file.drawio
```

Checks: well-formed XML, existing `resIcon`, `shape` and `grIcon` names, the
`points` array on every node, escaping of line breaks, hand-written waypoints,
overlapping nodes and labels, icons colliding with container labels, edges
routed through a third node, column spacing and dead space inside containers.

Errors are fixed before delivering, no exceptions. Warnings are judgment calls
that need a look at the rendered diagram: resolve them, or report them to the
user with the reason they were left as they are.

The 180px and 120px figures above are design guidance. The validator only warns
below 110px, which is the floor where the diagram looks cramped regardless.
Between those two numbers lies judgment.

## Updating the stencil list

AWS ships new services and draw.io ships new stencils. When a name that should
exist is missing from `reference/resicons.txt`, regenerate it:

```
python3 scripts/update_icons.py
```

## Worked example

`examples/serverless-api.drawio` is a six-node serverless architecture built to
this spec. Good starting point for structure, spacing and edge anchors.

`examples/vpc-dataconnect.drawio` and its English twin `vpc-dataconnect-en`: a
two-AZ VPC with public and private subnets, NAT Gateway, Internet Gateway, a
Gateway VPC Endpoint and a NACL. The reference for container nesting, for VPC
sub-components, and for the side-exit dogleg routing pattern.

`examples/ticket-platform.drawio` is the dense case: 19 nodes and 20 flows
across regional services, a two-AZ VPC and three external actors. Read its
generator header in `examples/_generate.py` for how the free channels were
picked before any edge was written.

Each has a `comparison-*-without-skill` counterpart showing the same
architecture as a generic diagram.
