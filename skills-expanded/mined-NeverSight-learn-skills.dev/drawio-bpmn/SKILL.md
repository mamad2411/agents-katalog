---
name: drawio-bpmn
version: 1.0.0
description: Use when the user asks for a BPMN diagram, swimlane diagram, business process map, or workflow diagram with roles/lanes and phases. Builds with the declarative layout engine using canonical mxgraph.bpmn stencils (events, gateways, typed tasks) in horizontal swimlanes (pool → lanes × phases), validates (BPMN semantic rules plus geometry), runs a render-based vision self-check. Default output is .drawio; PNG/SVG only on request.
license: MIT
---

# Draw.io BPMN

Produce correct BPMN (Business Process Model and Notation) swimlane diagrams in
draw.io. This skill is a thin frontend; the deterministic engine, validator, and
rules live in the `drawio-ai-kit` package, reached via the `drawio-ai` CLI.

## 0. Preflight — the CLI must be installed

```bash
command -v drawio-ai >/dev/null 2>&1 || echo "Install the Kit first:  npm i -g github:sparklabx/drawio-ai-kit"
```

If `drawio-ai` is **not** on PATH, stop and tell the user to run
`npm i -g github:sparklabx/drawio-ai-kit`. **Never run `npm i -g` yourself** — nothing mutates the
user's global environment without their say-so.

## 1. Shared Workflow

```bash
drawio-ai workflow
```

Prints the build → validate → render → write-to-project-path loop every diagram
follows. Read it; it is the source of truth for the process.

## 2. Domain rules

```bash
drawio-ai principles --mode bpmn
```

Returns the BPMN rules + shared principles + catalog shape groups.

## 3. Build with the engine, then validate + render

Resolve the Kit's install dir, then `import` the engine by absolute path (the
Shared Workflow shows the exact pattern):

```bash
ROOT="$(drawio-ai root)"     # absolute path to the installed Kit
```

Build with the declarative layout engine (NO hand-written coordinates) using the
`src/bpmn.mjs` creators and the `pool()` primitive, then:
`drawio-ai validate <file>` → `drawio-ai render <file> -o <file>.png` (`Read`
the PNG for the vision self-check) → write the `.drawio` to an **absolute path
under the user's project** (never the Kit, never `cwd`).

## Domain notes

Structure: `pool → lanes (roles) × phases (milestones)`. Use the creators in
`src/bpmn.mjs` — `start`, `intermediate`, `end`, `gateway` (exclusive/parallel/
inclusive/event), typed tasks (`userTask`, `serviceTask`, `manualTask`,
`scriptTask`, `businessRuleTask`), plain `task`, `subProcess`. Each node carries
`{ lane, col }` cell tags; the engine places them automatically.

A gateway MUST split (≥2 outgoing) or merge (≥2 incoming) — never neither. Red
accent ONLY for blocker end events (error/cancel/terminate); everything else is
monochrome. Sequence flow: solid lines, rounded corners. One start event (no
incoming flow); end events on the right (no outgoing flow). Horizontal by default;
pass `orientation: "vertical"` to `pool()` for vertical swimlanes.

## Self-check (before delivering)
- [ ] Built with the layout engine — no hand-written coordinates.
- [ ] `drawio-ai validate` → ok, no warnings, no advice.
- [ ] Every icon came from `drawio-ai search` (category colors intact).
- [ ] `drawio-ai render` vision self-check passed.
- [ ] Output written under the user's project, not the Kit.
