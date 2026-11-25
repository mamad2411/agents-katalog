---
name: n8n-workflow-map
description: >-
  Turn exported n8n workflow JSON into a Figma workflow map and an architecture
  map that non-n8n readers can follow: zone panels from the canvas stickies,
  one chip per node coloured by role, elbow edges with yes/no labels, error
  outputs collapsed to a marker, plus a hand-modelled systems page showing
  what each stand-in becomes on the customer's instances. Use when a customer,
  a reviewer or a handoff needs "what does this actually do" on one board, or
  when the user says workflow map, architecture map, Figma diagram of the
  workflows.
---

# Workflow JSON to a Figma map

`scripts/workflow-map.py` (stdlib Python, in this skill folder) computes the whole layout from the
workflow JSON and writes one self-contained Figma Plugin API script per page.
The Figma MCP `use_figma` tool runs each script. Nothing is drawn by hand, so a
rebuild after a workflow change is a regenerate and a re-run.

Requires the Figma MCP server (`use_figma`, `create_new_file`, `get_screenshot`,
`whoami`) connected to the agent.

Precondition: the workflows carry zone stickies from `n8n-canvas-docs` (every
node inside one zone, `## Title` plus a body). The map reuses the zone titles,
bodies and bounds; a workflow without zones still renders, as one board with
no panels.

## Procedure

1. **Export the workflows** to `workflows/<env>/` (`./scripts/export-all.sh`) so
   the JSON is the instance's truth. Note the file names.
2. **Write the two config files** in the engagement, `docs/maps/`:
   - `pages.json`: `{"Page name": ["file.json", ...]}`. One page per big
     workflow, small ones grouped. Boards stack vertically on a page.
   - `architecture.json`: the systems page, hand-modelled (shape below). This
     is where the lab, PoC and production columns live; keep it in step with
     the handoff's architecture table.
3. **Generate**:
   ```
   python3 scripts/workflow-map.py model workflows/dev/*.json -o /tmp/map.json
   python3 scripts/workflow-map.py figma /tmp/map.json --pages docs/maps/pages.json \
     --arch docs/maps/architecture.json --out-dir /tmp/js --replace
   ```
   `--replace` makes each script clear its page before drawing, so a re-run
   replaces the boards instead of adding a second copy. Syntax-check each
   script with node before sending it: the scripts use top-level `await`, so
   wrap the text in an async function constructor,
   `new ((async () => {}).constructor)(text)`, not `new Function`.
4. **Figma**: `whoami` for the plan key, `create_new_file` once in the Figma team
   that owns the engagement. Then one `use_figma` call that creates every page named
   in `pages.json` plus the architecture page and returns their ids. Only then
   fan out: one `use_figma` per page, in parallel, each with its script as the
   `code`. Creating pages inside the parallel calls races on the default page.
5. **Screenshot loop**: `get_screenshot` on each frame id the scripts return;
   tall boards at `maxDimension` = frame height, sliced with `sips -c` on macOS
   (Pillow is often missing). Look for labels on lines, text past a chip edge,
   column headers under a wrapped subtitle, legends past the right margin.
   Fix in the generator, regenerate, re-run with `--replace`. Never patch the
   Figma file by hand; the next regenerate would lose it.
6. **Deliver**: save the renders to `docs/maps/*.png`, write `docs/maps/README.md`
   with the Figma link and the regenerate commands, link it from the handoff.
   A file in your own Figma org is not shareable by link to the customer;
   export PNG or PDF for them.

## What the generator decides

- **Role colours** from node type (trigger, code, decision, ai, tool,
  sub-workflow, data, http, file, wait, notify). Dark palette by default;
  `--theme light` for a light surface. Inter, which every Figma plan has.
- **Edges**: straight when on one row, elbow otherwise; a wrap to a lower zone
  drops into the gutter between the zones and comes back along the left
  margin; a loop back inside a zone routes below the chips; an error edge to
  the node directly above in the same column takes a short lane and enters
  from the right.
- **Error outputs**: the node most error edges land on is the failure sink.
  Those edges are not drawn; the source chip gets a pink dot and the sink a
  caption. An error edge to the same node as the main edge is dropped (it
  reads as "continues on error"). Other error edges draw in pink.
- **Labels**: If outputs are `yes`/`no`, Switch outputs use their renamed
  output keys. Labels sit at the target end, right-aligned, so fan-outs never
  pile up at the source.
- **Chip detail**: webhook method and path, HTTP method and path, sub-workflow
  name, wait mode, model id, Postgres operation. Anything containing an
  expression is dropped. Text is measured in Figma and truncated to the chip.

## architecture.json shape

```json
{"page": "Architecture", "title": "...", "subtitle": "...", "colW": 340, "gap": 132,
 "legendRoles": ["trigger", "subworkflow", "ai", "data", "http", "wait", "notify", "code"],
 "columns": [{"title": "Order sources", "cards": [
    {"id": "gmail", "role": "trigger", "title": "...", "rows": {"Lab": "...", "PoC": "...", "Prod": "..."}}]}],
 "edges": [{"from": "gmail", "to": "intake", "label": "pull", "dy": 0, "dy2": -10, "kind": "main|error|ai"}],
 "bands": [{"role": "data", "title": "Application Postgres", "rows": {"Tables": "..."}}],
 "footer": ["Volume ...", "What does not change ..."]}
```

Three columns is the shape that avoids crossings: sources, workflows, systems
called. Column 2 to column 3 edges route through the gap, so they never cross
a card as long as every system is in column 3. `dy`/`dy2` separate edges that
share a card edge; `dx` shifts a vertical edge between cards in one column.
Full-width material (the trace database, chargeback) goes in `bands`, not a
fourth column.

## Known limits

- A vertical lane can cross a zone's body text when the only free column is
  inside the panel. Readable, not pretty. Widen the zone or move the node on
  the canvas and regenerate.
- The map mirrors the canvas layout. A canvas that fails the `n8n-canvas-docs`
  checker produces a map with the same overlaps; fix the canvas first.
- `use_figma` is transactional per call: a throw rolls the whole page back.
  Fix the script and re-run; nothing partial survives.
