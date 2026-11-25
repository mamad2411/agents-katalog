---
name: drawspec
description: Draw an explanatory diagram (a process, swimlanes, hierarchy, loop, state machine, sequence diagram, ER or class model, gantt plan, kanban board, fishbone, mind map, argument map, family tree or pedigree, RAG status report, clock face for teaching time, venn, journey map, timeline, comparison, matrix or heatmap, pyramid, funnel, small chart, quadrant, scatter, curve, treemap, sankey or directory tree) as clean SVG by writing a declarative drawspec JSON document instead of SVG by hand. Use when a document, README, design note or answer needs a diagram, or when asked to "draw", "diagram" or "chart" something for a page. Do NOT use for exploring data (use a plotting library), for anything whose point is where things are (a map, a floor plan), for a list or a table that prose would carry, or to edit SVG directly.
---

# drawspec

You write what the diagram **means**; drawspec decides every coordinate. This
skill is a pointer — the format itself lives in `AGENTS.md`, which you read
rather than guess at.

1. **Install.** `pip install drawspec`. If your client speaks MCP and the
   `drawspec-mcp` server is available (`pip install 'drawspec[mcp]'`), use its
   `list_kinds`, `get_example`, `get_schema`, `validate_document` and
   `render_document` tools instead of the shell commands below.
2. **Read the format.** `drawspec agents` prints `AGENTS.md` as shipped with
   the installed version — read it whole, once. It is the copy that matches what
   your drawspec accepts; the one on GitHub `main` may describe kinds a released
   package refuses. `drawspec kinds` lists the kinds and `drawspec example <kind>`
   prints a minimal valid document. All of it works offline. If your installed drawspec has no `agents`
   command, upgrade it (`pip install -U drawspec`) before reading anything else.
3. **Decide whether to draw at all.** A list is bullets, attributes are a table,
   one step is a sentence. Pick the kind by what the reader must understand.
4. **Write the JSON.** No coordinates, sizes or colours — they are refused by
   name. Meaning goes in `kind` and `role`.
5. **Check.** `drawspec validate diagram.json` prints every violation with its
   JSON pointer. Fix each one at that pointer, then validate again until clean.
6. **Render.** `drawspec render diagram.json -o diagram.svg`. Where an SVG
   cannot go (a chat, a slide, an attachment), `-o diagram.png` writes a PNG —
   `--background dark` for a dark page; it needs `pip install 'drawspec[png]'`.

A refusal is the tool working: a readability-budget refusal means split into an
overview plus detail diagrams; an emphasis refusal means mark at most two things
`emphasis`; a fit refusal means shorten labels or split. Never work around one by
emitting SVG yourself.
