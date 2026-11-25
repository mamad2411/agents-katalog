---
name: architecture-diagrams
description: Turn a system description or a codebase into an explorable standalone HTML diagram — architecture, workflow, data flow, request sequence, or lifecycle state machine. Write a small JSON document, render it with a zero-dependency Python script, and get one self-contained file with inline SVG, dark and light themes, pan and zoom, click-to-isolate, and node search. Use when asked to visualise or document system architecture, cloud or network topology, trust boundaries, a technical workflow, an API call sequence, a request lifecycle, a data or ETL pipeline, or a state machine, or to replace a Mermaid diagram that has outgrown what Mermaid renders well.
---

# Architecture diagrams

Produce diagrams that survive. One HTML file, no dependencies, no network, no
build step. It opens from a `file://` path, from a CI artifact, or from a wiki
attachment, on a machine with no toolchain, years later.

## When to reach for this

Use it when the diagram is an artifact someone will come back to: an ADR, a
design doc, a runbook, a handover, a security review, a client deliverable.

Do not use it for a throwaway sketch inside a chat reply. A fenced Mermaid block
is faster and good enough when nobody needs to open it twice.

## Why not just Mermaid

Mermaid is excellent until you need trust boundaries that do not overlap, notes
per node, a legend, technology labels, a readable state machine with retry loops,
or a diagram a reader can interrogate rather than squint at. This produces a file
where clicking a node isolates it and everything one hop away, which is the
question a reader actually has: *what talks to this thing?*

## Workflow

**1. Decide the kind.** One diagram answers one question. If you cannot state the
question in a sentence, you are about to draw two diagrams on top of each other.

| Kind | Answers | Shape |
| --- | --- | --- |
| `architecture` | What are the pieces and what talks to what? | nodes, edges, boundaries |
| `workflow` | What are the steps and where does it branch? | nodes, edges, decisions |
| `dataflow` | Where does data come from and go? | nodes, edges, stores |
| `lifecycle` | What states exist and how are they left? | nodes, edges, cycles |
| `sequence` | In what order, between whom, over time? | participants, messages |

**2. Gather evidence before drawing.** If the diagram claims to describe real
code, read the code. Config, route definitions, IaC, CI workflows and queue
consumers tell you the truth; a README tells you the intent. When they disagree,
draw what the code does and note the difference. A diagram that quietly documents
the intended system rather than the running one is worse than no diagram, because
it is trusted.

**3. Write the document.** A single JSON file. Full contract in
[references/authoring-contract.md](references/authoring-contract.md); schema in
[schemas/diagram.schema.json](schemas/diagram.schema.json).

```json
{
  "kind": "architecture",
  "title": "Lead capture path",
  "subtitle": "Boundaries are trust boundaries, not team boundaries.",
  "orientation": "LR",
  "groups": [{ "label": "Public edge", "nodes": ["visitor", "cdn"] }],
  "nodes": [
    { "id": "visitor", "label": "Visitor", "shape": "actor" },
    { "id": "cdn", "label": "CDN", "shape": "cloud", "tech": "CloudFront" },
    { "id": "api", "label": "Lead API", "note": "Validates and de-duplicates", "accent": true }
  ],
  "edges": [
    { "from": "visitor", "to": "cdn", "label": "HTTPS" },
    { "from": "cdn", "to": "api", "label": "cache miss" }
  ]
}
```

**4. Validate, then render.**

```bash
python3 scripts/render_diagram.py diagram.json --check      # validate only
python3 scripts/render_diagram.py diagram.json -o out.html  # render
python3 scripts/render_diagram.py diagram.json --svg -o out.svg
```

Validation is strict on purpose. An edge pointing at an undeclared node is an
error, not a silently dropped edge, because a dropped edge produces a diagram
that is confidently wrong. Unknown keys are errors too: a silently ignored key is
how you end up certain you set something that never took effect.

**5. Look at it.** Open the file. Every diagram this skill has produced was
plausible before it was viewed and wrong in some specific way afterwards.

## Authoring rules that decide whether it reads well

**Boundaries are the most valuable thing you can add, and the easiest to get
wrong.** Use `groups` for trust boundaries, network boundaries, or
ownership — the lines that matter when something breaks or is attacked. Do not
group by team or by directory. A node belongs to at most one group, which the
validator enforces, because overlapping boundaries cannot be drawn as a clean
boundary and reviewers cannot reason about them either.

**Direction is meaning.** An edge points the way a request or a record travels,
not the way a dependency is declared. If A calls B and B answers, that is one
edge, `A -> B`; add a return edge only when the response path itself is
interesting, such as a webhook or a callback on a different route.

**Let cycles be cycles.** Retry loops, rollbacks and state machines are cyclic.
The layout detects the edges that close a cycle, routes them through a reserved
strip that no node occupies, and dashes them by default. Do not linearise a state
machine to make it fit.

**Notes earn their place.** `note` should say something the label cannot: a
constraint, a guarantee, a gotcha. "Handles requests" on a node called "API
server" is noise.

**Nine nodes is usually the limit.** Past roughly a dozen, split it. Two diagrams
that each answer one question beat one that answers none. This is also where the
renderer is weakest, for a reason worth knowing before you hit it: see below.

**Shapes carry meaning; pick them deliberately.** `box` service, `round`
start/end state, `cylinder` datastore, `queue` queue or topic, `cloud` managed or
third-party service, `actor` a person, `decision` a branch.

**One accent.** Set `accent: true` on the node or edge the diagram exists to draw
attention to. Accent everything and you have accented nothing.

## Known limitations

Stated here rather than discovered later.

- **Edges are not routed around obstacles.** An edge is a single curve between its
  endpoints. Between neighbouring ranks nothing can be in the way, and that is
  enforced by a test. A longer edge, or the leg of a back edge on its way to the
  reserved strip, **can cross an unrelated node** on a dense graph. On a 25-node
  fully-connected graph most edges cross something. If the result is unreadable,
  the diagram is too dense: split it. Do not expect the router to save it.
- **Text is measured by approximation.** There are no font metrics in the standard
  library, so glyph width is estimated. Wide scripts and unusual fonts are
  therefore laid out a little loosely rather than tightly.
- **A very wide diagram prints small.** It will fit one page, because that is what
  the print rules do, but a 60-node chain on one page is not readable. Print is
  for diagrams of a sane size.
- **No raster export.** Use the browser's print-to-PDF, or the `--svg` output.
  archify does PNG, JPEG, WebP and WebM if you need them.

## What the reader gets

- Pan by dragging, zoom by scrolling about the pointer, **Fit** to reset
- Click a node to isolate it and its immediate neighbours; **Esc** clears
- Filter box to dim everything not matching
- Dark and light, following `prefers-color-scheme`, with a toggle that persists
- Keyboard reachable nodes and an SVG `<desc>` that describes the structure in
  words, so the diagram is not lost to a screen reader
- `prefers-reduced-motion` honoured
- Prints to one page with the chrome removed

## Checking your own work

```bash
python3 scripts/render_diagram.py --self-test   # proves the validator rejects bad input
python3 scripts/generate_schema.py --check      # proves the schema is not stale
python3 -m unittest discover -s tests -v        # contract, security, geometry, render
```

`--self-test` exists because a validator that never fires is indistinguishable
from no validator. It feeds eight documents that must be rejected and one that
must render, and fails if any invalid document is accepted.

The schema is **generated** from the validator's field specs rather than written
alongside them. Two hand-maintained descriptions of one contract drift, and a test
that compares only their enums will not notice.

The test suite is checked by mutation: breaking the swimlane layout, the
orientation handling, text wrapping, parallel-edge separation, the escaping, or
the template substitution each makes it fail. A test that passes when its own
subject is broken is worse than no test, because it is trusted.

## Files

```
scripts/render_diagram.py     CLI: validate, lay out, render HTML or SVG
scripts/diagram_ir.py         authoritative definition of a valid document
scripts/diagram_layout.py     layered graph layout and sequence layout
scripts/generate_schema.py    derives the JSON Schema from diagram_ir's specs
templates/viewer.html         the standalone viewer shell
templates/theme.css           both themes, inlined into every artifact
schemas/diagram.schema.json   GENERATED. Do not hand-edit; regenerate instead.
references/authoring-contract.md   every field, with guidance on choosing
examples/                     three worked documents: architecture, lifecycle, sequence
tests/                        contract, security, geometry and render tests
```

## Review

This skill was reviewed by an independent model instructed to attack it, which
rejected the first version over a working XSS and eight other substantive
findings. [REVIEW.md](REVIEW.md) records every finding, what was fixed, and the
one that was documented as a limitation instead.

## Attribution

The approach — a validated JSON intermediate representation rendered to an
explorable standalone HTML artifact — is taken from
[archify](https://github.com/tt-a1i/archify) by tt-a1i, itself derived from
Cocoon AI's architecture diagram generator. This is an independent
implementation: no code, template, or bundled asset was copied. See
[ATTRIBUTION.md](ATTRIBUTION.md), which also records why archify's bundled brand
marks were deliberately left out.
