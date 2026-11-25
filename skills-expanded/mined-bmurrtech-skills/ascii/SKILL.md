---
name: ascii
description: >
  Draw or refine plain-text diagrams when structure beats paragraphs: flows,
  sequences, pipelines, decisions, states, layouts, trees, timelines, topology,
  ownership lanes, matrices, lineage, and before/after views. Use for Markdown
  docs, ADRs, PRDs, stories, and any text-first artifact where relationships,
  order, boundaries, or hierarchy matter.
---

# ascii

Turn a structural question into a fenced monospaced diagram. Prefer several small drawings with one job each over a single crowded mural. Skip this skill when prose already answers clearly.

## Workflow

### 1. State the purpose

One sentence: what should a reader understand after looking?

**Done when:** purpose is named and scoped to one journey, subsystem, decision, or change.

### 2. Pick a form

| Need | Form |
|------|------|
| Call / lifecycle order | Sequence (actors across, time down) |
| Transform chain | Pipeline with named intermediates |
| Branching rules | Decision tree |
| UI behavior | State transitions (not pixels) |
| Spatial UI arrangement | Wireframe only if layout is the question |
| Containment / breakdown | Tree |
| Phases over time | Timeline |
| Parts and couplings | Boxes with labeled edges |
| Trust / capacity / links | Topology with named boundaries |
| Ownership | Swimlanes |
| Coverage / RACI-style | Compact matrix |
| Provenance | Source → transform → destination |
| Entity lifecycle | States + labeled transitions |
| As-is vs to-be | Two comparable views |
| Blast radius | Center node + affected edges |

**Done when:** form matches the purpose.

### 3. Compose

1. Draw the happy path first (the backbone).
2. Label edges that carry meaning (event, payload, guard, constraint).
3. Add only differences that change understanding (branches, joins, loops, parallel paths, failures, trust boundaries).
4. Do not invent nodes, edges, or guarantees; mark guesses and unknowns.
5. If dense, split by layer (context → flow → detail → exceptions) or by question.
6. Fence the result in a `text` (or plain) code block. Spaces not tabs.

**Done when:** a reader can follow the backbone alone and the purpose is answered.

### 4. Exit check

Clear entry and direction? Important edges labeled? Material risk or uncertainty marked? Survives paste into Markdown? Better than the same idea in sentences?

**Done when:** keep, split, simplify, or discard — then stop.

## Glyph kit

Small portable vocabulary. Stay consistent. Prefer plain ASCII when the diagram must survive every paste target; Unicode box drawing is fine when it helps and the audience can render it.

```text
+----------+
| Node     |     noun: component, actor, step, state
| detail   |     keep detail short; paragraphs stay in prose
+----+-----+
     |
     | label
     v

A ---------> B           one-way
A <--------> B           two-way
A =========> B           primary path

     +--> B              fan-out
A ---+
     +--> C

A ---+
     +--> C              fan-in
B ---+

A --[guard]--> B         conditional
A - - - - --> B          weaker / optional (say what dashes mean)

+================+       hard boundary (trust, plane, lane)
|  Boundary      |
|   +--------+   |
|   | Inside |   |
|   +--------+   |
+================+

+----------------+       soft group (scan only — not a dependency)
| related items  |
+----------------+

--- phase ---            section / option / as-is vs to-be

[ note ]                 invariant, external, TBD
...                      deliberately omitted
```

## Defaults

- Boxes ≈ nouns; arrows ≈ verbs (unless the verb *is* the node).
- Proximity and alignment carry meaning — do not imply links that do not exist.
- Crossing lines are a smell: reorder, restack, or split.
- Tag mixed certainty: `[Existing]` `[Proposed]` `[Optional]` `[TBD]` `[Assumption]` `[Deprecated]`.
- Prefer placeholders (`N`, `<protocol>`) over fake precision.
- Aim for roughly 3–7 major nodes on a conceptual view; split when scanning fails.
