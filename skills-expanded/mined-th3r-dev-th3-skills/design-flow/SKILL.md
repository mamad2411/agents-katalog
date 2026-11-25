---
name: design-flow
description: Design screens in Figma with their flowchart drawn right beside them, so each page states what it shows and how it behaves, and a developer can build it from one look. Uses the Figma MCP. Use when the user shares a figma.com/design URL and wants to analyze how the file is organized, add a flow to a screen or menu, design a new page with its flow, check which screens still lack a flow, or turn screen + flow into an implementation checklist. Trigger on "flow on the design page", "flowchart next to the screen", "design with flow", "user flow in Figma", "screen flow handoff", "ออกแบบหน้าพร้อม flow", "ใส่ flowchart ข้างหน้าจอ", "flow ของหน้านี้". Not for standalone FigJam boards with no screens (use figma-generate-diagram) or for plain design-to-code with no flow (use figma-design-to-code).
---

# Design Flow

A screen in Figma shows what the page looks like. A flowchart placed beside it shows what
the page does: which decisions it makes, where it goes on success, which alert it shows on
failure, and which role can see it. This skill keeps the two together on the same canvas
and in the same naming scheme, so the handoff becomes one checklist per screen.

It works on the file's **existing** conventions. It reads them before it draws anything and
does not bring in a style of its own.

Setup, everyday use and the step-by-step agent runbook are in [README.md](README.md). Read
its Part 3 before the first Figma call in a session.

## Before any call

1. Parse the URL: `figma.com/design/<fileKey>/<name>?node-id=<a>-<b>` gives you `fileKey`
   and `nodeId = "<a>:<b>"`.
2. `create_session` with the fileKey and a one-line task description. Pass the returned
   `sessionId` on every later file-tool call.
3. Load the official Figma skills when they're needed. Don't copy their content here:
   - `figma-use` before **any** `use_figma` call. Add `figma-generate-design` before a
     call that makes visible changes.
   - `figma-design-to-code` before `get_design_context`.
   - Tool order and limits come from https://github.com/figma/mcp-server-guide.
4. **Principles.** Read the sibling sub-skill [`../core/SKILL.md`](../core/SKILL.md) (design-core). Its composition, writing and interface-quality
   rules apply to every screen, state screen and flow step this skill makes, and its review
   table is the design half of every check below (stage 5 of the pipeline). For a new page or
   a gap the file's system doesn't cover, also apply its `references/taste.md`: name the kind
   (usually tool or product app here), write the copy before placing, and decide open style
   choices on purpose instead of by habit. The file's own
   system still comes first. It ships in the same `design` install, so it is never
   skipped.
5. **Privacy.** File contents are the user's. Don't copy real labels, node IDs, or
   screenshots into this skill, into commits, or into any public artifact. Examples
   use mock labels; see [references/flow-conventions.md](references/flow-conventions.md#mock-labels).

## Rule: the file's design system first, never raw values

Every layer this skill creates or imports uses the file's own **components, variables and
text/effect styles**. A raw hex, px size, or font is a gap to report, not a value to invent.

1. Before building, take an inventory: local variable collections, text, paint and effect
   styles, and components (`search_design_system` covers published libraries too).
2. If something exists, use it: instances of components, `setBoundVariableForPaint` for
   colors, `setTextStyleIdAsync` for text, and bound variables for spacing and radius.
3. If something is missing (no components, or a color with no variable), **stop and tell
   the user** exactly what is missing and ask whether they want it added
   (`figma-generate-library`). Don't create tokens or components without that yes.
4. After any import, run `python3 scripts/figma_js.py tokenize --page <id> --root <id>`
   and pass its output as `code` to `use_figma`. It binds exact-match colors to variables,
   maps captured fallback fonts back to the real family (`--font-map "Fallback=Real"`),
   applies the text style of the same size, and returns what stayed unmatched.

## Tools and backends

Everything is Python. Figma edits run as Plugin API JavaScript inside Figma, through one of
two backends:

| Backend | How | Limits |
|---|---|---|
| **figma-bridge** (default) | [gethopp/figma-mcp-bridge](https://github.com/gethopp/figma-mcp-bridge) server in a container + its Figma desktop plugin. Tools: `run_script`, `import_html_layers`, `get_document`, `create_*`, `set_*`… | No Figma API/MCP quota. Needs Figma **desktop** with the plugin running in the file |
| Official Figma MCP | `use_figma`, `generate_figma_design`, `get_screenshot` | Counts against the plan's MCP tool-call limit (Starter runs out fast) |

Python can't edit layers directly. The Plugin API only exists inside Figma, and the REST API
can't write nodes. So [`scripts/figma_js.py`](scripts/figma_js.py) renders the JS templates in
`scripts/js/`, and the agent passes that output to `run_script` (or `use_figma`).

| Command | Does |
|---|---|
| `bridge.py up --work DIR --run-script` | builds and starts the bridge container (podman or docker): `127.0.0.1:1994` for the plugin, `DIR` mounted at `/work` |
| `bridge.py mcp` | the MCP command; each session `exec -i`s into the container (first = leader, others follow) |
| `bridge.py status / logs / down` | container lifecycle |
| `capture.py ... --to layers --out DIR` | page → html-figma JSON for `import_html_layers` (no quota; absolute layout). `--fake-ok REGEX` answers matching writes with HTTP 200 inside the browser, so success dialogs can be captured without changing data |
| `capture.py ... --to figma --capture ID` | page → Figma via `generate_figma_design` capture ids (auto layout, binds variables; uses quota) |
| `figma_js.py swap` | layers that match a component variant (structure, size, radius, fill token, vector geometry) → instances, texts carried over |
| `figma_js.py flow-kit --tokens t.json` | builds the design-mode flow kit (Flow/Node, Flow/Decision, Flow/Marker, Flow/Element Row) from your tokens |
| `figma_js.py flow --spec flow.json` | UI → flow → UI: element on screen → kit steps → next screen, lines routed around everything (A*) |
| `figma_js.py state --spec state.json` | target state screen: copy + dialog overlay, or captured page + accurate sidebar; `max_height: 1080` crops it to one viewport |
| `figma_js.py make-room` | shift a section right and widen its label so a flow fits (ask first); `--y-from/--y-to` limit it to one row band; `--from-y/--dy` instead shift everything below a y down (room for a band of state screens) |
| `figma_js.py extract` + `design_graph.py` | design knowledge graph: `build`, `dupes`, `impact`, `tour`, `gaps` |
| `figma_js.py images` | fill the raster images `capture.py` split into `<slug>.images.json` (run right after the import) |
| `figma_js.py autolayout` | absolute frames → auto layout (rows and columns inferred, deepest first) |
| `figma_js.py tokenize` | raw values → the file's variables and text styles |
| `figma_js.py place` | new screen → placeholder slot (replace) or old screen slot (version card + old at 0.5) |
| `ui_scan.py` + `ui_components.py` | code scan → component plan → build/extend components with simple `State`/`Label`/`Icon` controls → swap copies for instances |
| `flow_review.py DIR` | strict 1–10 review of rendered flows from their graph JSON (hard gates: a line ending on a marker or an anchor that never reaches a screen ≤5; orphans/missing ≤6; forced, backward, ANY line crossing a line, nested anchors ≤8; pass ≥9) |
| `*.py --self-test` | built-in checks |

One-time setup: `claude mcp add figma-bridge -s user -- python3 <skill>/scripts/bridge.py mcp`.
Then in Figma desktop: Plugins › Development › Import plugin from manifest (the `plugin/manifest.json`
from the bridge release), and run it in each file. `run_script` executes arbitrary code in the open
file, so it stays off unless `--run-script` is passed. Pass `allowRemove: true` for `place`.
Write `--to layers` output inside the `--work` folder and give `import_html_layers` the path relative to `/work`.
`capture.py`, `figma_js.py` and `flow_review.py` only read and write files inside the folder they run from, so run them from the work
folder.

## Converting things into Figma (all with auto layout)

| Source | Tool | Then |
|---|---|---|
| Live web page (public or signed-in) | `capture.py url --to layers` → `import_html_layers` (or `--to figma` with capture ids) | `autolayout` (layers only), `tokenize`, swap repeated blocks for components |
| Local HTML file or folder | `capture.py html` (serves on 127.0.0.1) | same |
| Many pages | `capture.py jobs jobs.json` | same |
| Image or screenshot | `upload_assets` puts the image on the canvas as a locked reference; rebuild over it with `use_figma` from components and `figma.createAutoLayout()`; compare with `get_screenshot`; delete the reference | — |

`capture.py` runs headless Chrome via `uv run`. It blocks every write to the target host
unless you pass `--allow-writes`, so a signed-in capture can't change data. `login` saves a
Playwright session file and never prints credentials. `--to figma` captures come back mostly as
auto layout with variables bound (poll `generate_figma_design` until `completed`). `--to layers`
captures come back absolutely positioned, so always follow them with `autolayout`, then `tokenize`.

## Canvas layout: read top, work down

Many files mark each product area with a very large section label: an instance of a title
component stretched across the area's full width at the top of the page (for example
`App A`, `App B`, `Mobile`). Smaller labels for role, then menu, sit below it, and the screens
go below those. Read the page from the top down.

- Before placing anything, find the section labels (wide instances of the title component near
  the page top) and their x-ranges. A new screen goes **inside the x-range of its section**,
  under its role and menu label. It never goes at the page edge or (0,0).
- A new section gets its own label instance of the same component, to the right of the last
  section, at the same y.
- Replacing a placeholder keeps its slot, so the order is already right.

## Versioning on the canvas

When a screen that already has a design changes:

- The **new version** takes the screen's place and keeps the breadcrumb name.
- A **version card** sits above it: a large frame built from the file's tokens (largest
  text style, theme color variables) that says `New version`, the app version or date, and
  what changed in one line.
- The **old version** moves directly to the right of the new one (200 px gap), gets
  `opacity = 0.5`, and has its version added to its name: `Role ▸ Menu ▸ Screen (v1.2.20)`.
  Never delete it.
- A screen that only held a "not started" placeholder has no old version. Replace the
  placeholder.
- `figma_js.py place` decides which case applies. When a card token or text style is missing it
  returns `blocked` with the list, and the agent asks the user instead of inventing one.

## Rule: every component is used in the design

A component that sits only in the Components band is unfinished work. Creating one is one step; the work is done
only when the design uses it:

1. **Create → swap in the same run.** `ui_components.py apply` builds a component and replaces its copies on every
   screen, then reports anything still unused.
2. **After building anything new** (capture, state screens, new pages), run
   `ui_components.py sync --page <ui page> --ignore '^Flow/'`. It swaps every component into every screen, including
   screens built after the component existed.
3. **Check:** `figma_js.py usage --page <ui page>` (read-only) lists instance counts per component and variant.
   `unused` and `unusedVariants` must be empty. If a component or variant still has 0 instances, either make it
   match its copies (fix the variant) or remove it. A duplicate of another component gets merged into it. Never
   leave a component idle.
4. New screens are built from instances. A plain frame that matches a component is a bug, not a style choice.

## Components from the codebase (fastest path)

The app's code already says what each component is and which states it has, so build Figma components from it
instead of guessing from repeated pixels:

```bash
python3 scripts/ui_scan.py scan <src dirs> --out inventory.json        # every JSX component used, with props
python3 scripts/ui_components.py names --map map.json --out names.json  # code component → layer-name regex
python3 scripts/figma_js.py ui-samples --page <ui page> --spec names.json -o samples.js   # run: read-only
python3 scripts/ui_components.py plan --inventory inventory.json --samples samples.json --map map.json --out plan.json
python3 scripts/ui_components.py apply plan.json --page <ui page> --components-page <page>
```

- `ui_scan.py` (stdlib, under a second for about 800 files) counts uses per component and import source, and records
  literal prop values (`variant`, `size`, `bg`, `theme`…) and state flags (`disabled`, `loading`, `checked`,
  `isInvalid`, `readOnly`). It also records label texts and icon use. It ignores TS generics, comments, spreads and
  layout plumbing (`Col`, `Row`, `Controller`…).
- `map.json` gives each code component a **simple** Figma name and the layer-name regex captures use
  (e.g. `{"Form.Control": {"figma": "Input", "layers": "^(Input|FormControl)$", "text": ["Value"]}}`).
- `ui-samples` groups matching layers by structure and splits each group by fill token: each group is one component,
  and each fill in it is one variant.
- **Simple controls:**
  - `State` variants are named after the code's own values when the fill token matches (green → `success`,
    primary/blue → `primary`, outline → `outline-primary`).
  - Text properties `Label` / `Value` / `Hint`.
  - An `Icon` boolean.

  One switch changes a state. Colors stay bound to variables.
- **Review the plan before `apply`.** Make a contact sheet of every planned component's samples (`get_screenshot`
  on the sample ids) and rename in `plan.json` where the code name misleads. A layer named `Button` or `List Item`
  can be a sidebar header, and two near-identical groups can be different fields (lookup vs date). Keep names short
  and honest, e.g. `Icon Button` with `edit`/`view`, and `Sidebar Item` with `default`/`active`. When an existing set
  already uses a state name for a different look (another app's theme), give the new look its own value instead of
  merging into the wrong one.
- **Icon buttons get one state per icon**, named by the action (`edit`, `delete`, `print`, `refresh`…). `swap`
  matches on vector geometry, so a copy whose icon has no variant stays a plain frame. `ui-samples` splits by
  geometry for exactly this reason. Re-run `ui-samples` after `apply`: whatever is still listed did not match.
- **Components live in the file's own Components band.** `componentize` places its section under the title band
  whose label equals the section name (e.g. a titleInfo "Components"), right of what's already there. When no such
  band exists the result says so: add the band and move the section instead of leaving it at the page's right edge.
- **Existing components are extended, not duplicated:** missing variants are added to the existing set on its own
  axis. Then `swap` replaces every matching copy on every screen with an instance, carrying the texts over.
  Re-run the flow review afterwards; anchors that matched by text still resolve on instances.

## Lines never cross lines

- **No crossing is acceptable.** Your own flow's lines and other flows' lines are both a review fail (capped at 8),
  not a small deduction.
- **Steps sit next to what they come from.** Bands (one per anchor) are stacked in the order their lines leave the
  screen. When the result still crosses, the renderer stacks them again by where each line actually crosses the
  screen's right edge, routes again, and keeps the version with fewer crossings (`reorder: false` turns this off).
- **Titles stay clear.** The strip above a screen, where Figma draws its name, is an obstacle (`title_strip`,
  default 120 px).
- **Anchor by component, not by node id.** `{component: "^Pager Arrow$", state: "^next"}` finds an instance by its
  component and variant, so it survives swaps and rebuilds. A `node` id breaks as soon as the layer is swapped for an
  instance. Use `find` (visible text) or `component`/`state`, and `node` only as a last resort.
- **Anchors must pick the element, not its container.** Two anchors resolving to boxes inside one another (e.g.
  `find: "Search"` hitting the field label's group instead of the button) makes lines that start inside each
  other and cross. The graph lists them as `nested`; fix the spec with `within: "^Button"` or `name`.

## Knowledge graph (adapted from Understand-Anything)

Run `design_graph.py extract --page <id> … --out DIR` and then `build DIR` before larger work.
The graph is deterministic and incremental (fingerprint per screen) and has typed nodes
(screen, component, variable, text_style, label, flow) and edges (uses_component, binds_variable,
uses_text_style, navigates_to, has_flow). Ask it questions instead of re-reading the file:

- `dupes`: structures that repeat across screens but aren't components. These are the next components to make.
- `impact "<token or component>"`: every screen that changes if it changes. Run it before editing a token.
- `tour`: screens top-down per section, with what each uses. Use it for onboarding or review order.
- `gaps`: placeholders, raw paints, unstyled text, screens with no flow.

## Flows: UI → flow → UI

A flow joins **real UI to real UI**. An arrow leaves the actual element on the source screen
(button, card, input, row action), runs through flow-kit steps, and lands on the screen that
comes next: another page, or a copy of the screen in its resulting state (dialog open, alert
shown). A flow is never a separate list of elements.

| Part | How |
|---|---|
| Steps | Flow Kit components (`flow-kit`): Process, Alert, Success, End, Decision. Design files can't create or clone FigJam shapes or connectors (Plugin API limit), so the kit is real components bound to tokens |
| Target states | `capture.py jobs` with `steps` (e.g. click "Import") and `selector` (e.g. the dialog). Then `figma_js.py state`: `overlay` = copy of the screen + scrim + the captured dialog; `page` = captured page + the accurate sidebar moved in from the source. A captured dialog is fitted to its content (captures keep page coordinates). Place with `near: {screen, dx}`: the first free slot right of the source screen, sliding down past anything already there, so state screens never overlap |
| Lines | `figma_js.py flow` routes every edge with **A\* on an orthogonal Hanan grid** built from the edges of nearby objects (with a clearance margin), plus lanes one and two `lane` widths beside earlier lines. Cost = length + bend penalty + per-px penalty for running on or within a lane of an earlier line (other flows' lines included) + a penalty per crossing or touch. Short edges are routed first and long ones (to a remote screen) last. Two passes: the first picks each edge's sides, the second sorts the ends sharing one side of a box by where their lines head and gives them slots in that order, so lines don't swap at the box. An element's first run leaves straight, or jogs into a channel along a nearby element's edge (row divider, toolbar gap), whichever crosses fewer elements; another anchor's element counts triple. Lines never run over other screens or steps |
| Layout | Steps sit on a layered grid: column = steps from the element, rows aligned on their centers, 10px snap. The main path stays on one row; a decision's 2nd branch drops straight below its bottom vertex and its 3rd rises straight above its top vertex. Element bands stack in the order their lines leave the screen (clockwise: top side left→right, right side top→bottom, bottom side right→left), so neighbouring lines nest instead of crossing. A column gap widens when a label would not fit its run |
| Decisions | House convention: 1st outgoing edge from the right vertex (True), 2nd from the bottom (False), 3rd from the top. Labels sit just after the branch point: short ones on the line, longer ones beside it, never on another line or node |
| Room | Flows stay inside their section's x-range. When a section has no room, `figma_js.py make-room --from-x X --dx D --label <section label>` shifts everything right of X (connectors follow their endpoints) and widens the section label. Ask the user first. Moving glued layers this way leaves Figma connectors with their old stored route (the line stretches back to the old spot), and the API can't re-route or create connectors in design files. Run `figma_js.py redraw-connectors` right after: each stale connector is redrawn as a vector with the same ends, magnets, stroke (variables kept), caps and label, and the original is hidden, not deleted |

### Pipeline: design → state → graph → strict review (loop)

Same discipline as a strict figure review: a wrong or missing arrow is never cosmetic.

**Work in stages, and check each one before starting the next.** Don't run everything in one go and look only at
the end. When something is wrong in a single batch run, it's wrong everywhere and the lines hide the cause.

| Stage | Do | Check (show the user, wait for OK) |
|---|---|---|
| 1. Place + states | capture the source screens **and every result state** (`capture.py jobs` with `steps`/`selector` → `figma_js.py state`), each state right after its source in the same row | `figma_js.py place-check`: 0 overlaps, none on a band title. Every spec's anchors reach a state screen (`figma_js.py flow` refuses otherwise). Screenshot one row with screens only, no lines |
| 2. Lines, one row | render the flows of that one row | screenshot of the row with lines: every line lands on a screen, not on a letter or a text box. `flow_review.py`: no crossings, no missing edges |
| 3. Lines, everywhere | render the rest | `flow_review.py` on everything, plus screenshots of the worst-scoring rows |
| 4. Components | `ui_components.py sync` | `figma_js.py usage`: nothing unused |
| 5. Design | `design-core` review table on each row screenshot | every row ≥ 8; copy, states and hierarchy findings fixed or listed |

When a check fails, fix that stage. Don't carry the problem into the next one.

1. **Design (spec):** one spec per screen, from the app source. Every step must be reachable from an element.
2. **State:** capture the target states (`capture.py jobs` with `steps`/`selector`; reports that read by POST need
   `--allow-post <read-only regex>`). Build them with `figma_js.py state` in **one row per source**: source | its
   steps | state 1 | its steps | state 2 … Sources never move. Crop page states to the source height (`clip_to`).
   - **This stage is not optional.** A flow joins picture to picture: the confirm dialog, the success alert, the
     opened edit page are screens on the canvas, not text boxes. A step chain that ends in an `end` box ("close the
     dialog", "open in edit mode") is a state screen you haven't built yet. `figma_js.py flow` refuses a spec whose
     anchors never reach a screen, and `flow_review.py` caps it at 5.
   - **Steps sit beside their source when states go in a band below it** (`align_to_target: false`): otherwise
     the step row lines up with the first state and lands inside the band. Order the band by the buttons that lead
     to it, and leave a bottom button on the side facing its chain (`side`), so neighbouring lines don't cross.
   - **Every line lands on its screen.** Keep targets close instead of hiding the distance: put each state right after
     its own steps, and for "back to the list" use a copy of the list as a state in the same row (`figma_js.py state`
     with `page`) rather than a line back across the page. Don't `make-room` screens thousands of px apart to fit
     flows; that makes every target far.
   - **Lettered markers are opt-in.** `markers: true` ends a chain in a lettered `Flow/Marker` (A, B…) with the same
     letter in front of the far target. Use it only when the user asks for on-page connectors, and review with
     `flow_review.py --allow-markers`. Without that, a marker caps the flow at 5.
   - **A flow stays beside its own screen.** When the next band of steps would run below the screen, beside the next
     screen down, it starts a new column of bands to the right, back at the top (`wrap: false` to turn off). Size
     the gap before the first state for it.
   - Lines leave an element on the side facing the flow. Leaving on the back side wraps around the screen and costs
     `back_side_cost` (2500).
   - Packed pages rule out stacking states in a column: with screens about 1.2× their height apart, only one row
     fits.
3. **Graph:** every `flow` render returns `graph`: what was actually drawn (nodes, edges, `drawn`/`forced`,
   `orphans`, `missing`, `backward`). Save it as `<name>.graph.json` with `<name>.qa.json`.
4. **Strict review:** `flow_review.py DIR` scores every flow 1–10.
   - Hard gates: a line ending on a marker, or an anchor whose chain never reaches a screen, caps the score at **5**;
     a missing edge or orphan step caps it at **6**; a `forced` line (the router fell back) or a
     line reading backward (right→left, bottom→top; returns to a screen are allowed) caps it at **8**.
   - Deductions: lines over objects, label overlaps, crossings.
   - **Pass ≥ 9.** Fix what the notes name (anchor text, states, room, spec fan-out), re-render, and review again,
     for a few rounds at most. Report the pass count and mean, never just "done".
   - The score checks geometry, not intent. Before reporting, look at the row screenshot: if a line doesn't land on
     the picture of what happens next, the flow isn't done, whatever the score says.

Reading order is **left → right, top → down**: bands in the order elements sit on the screen, columns by step
depth, a decision's True to the right and False below. Every node is connected: an edge the router can't place
is retried with a tighter clearance, then drawn as a plain elbow flagged `forced`. It's never dropped.

Spec per source screen (one more per state screen whose elements continue the flow):

```json
{"screen": "<source screen id>",
 "components": {"node": "<Flow/Node set>", "decision": "<Flow/Decision>"},
 "tokens": {"edge": "<var>", "edge_true": "<var>", "edge_false": "<var>", "label_text": "<style>", "chip": "<var>"},
 "anchors": [{"id": "a_import", "find": "Import"},
             {"id": "a_view", "name": "^Button$", "within": "^Table Cell$", "nth": 0, "side": "right"}],
 "screens": [{"id": "s_dialog", "node": "<state screen id>"}],
 "nodes": [{"id": "n1", "type": "process|decision|alert|success|end", "text": "…"}],
 "edges": [{"from": "a_import", "to": "s_dialog"}, {"from": "n1", "to": "n2", "label": "True", "tone": "true"}]}
```

Anchor selectors (combine as needed): `find` = visible text (exact match first, then substring;
the text is lifted to its button or card), `name` = layer-name regex, `node` = exact node id,
`within` = regex on an ancestor's layer name (e.g. a table row), `nth` = which match (0-based,
document order), `side` = `right|left|top|bottom` to pin the exit (default `auto`). A row action
with the same icon in every row needs `name` + `within` + `nth`; `find` alone lands on the header.
An element clipped out by a parent frame is pulled to the frame's visible edge and listed in
`clipped`: fix the state screen when that happens.

The result reports `anchors` (resolved node ids), `exits`, `failed`, `ms`, and `qa`, a measured
quality check: `crossings` (between this flow's lines), `crossOther` (with other flows' lines),
`lineOverObjects` (runs through any box but the edge's own ends), `minParallelGap` (closest
overlapping parallel runs of different lines), `labelOverlaps`, `bends`, `length`, `headInner`
(elements crossed by first runs inside the source screen). Aim for zero `lineOverObjects` and
`labelOverlaps`; compare the rest before and after a change instead of judging by eye.

Take behavior from the app's source (click handlers, dialogs, validation, confirm and success
messages), never from guesses. Re-running replaces that screen's previous flow. Flows that point
at each other's screens see each other's lines, so render them in a fixed order.
`bridge.py ensure` relaunches the plugin when Figma has closed it.

## Workflow 1: Analyze the file

Goal: a map of `role → menu → screen` and a list of which screens already have a flow.

1. `get_metadata` without `nodeId` to list the pages. Then run it on the page or frame
   the user named.
2. If the result is too large (big UI pages run to megabytes), it gets saved to a file.
   Summarize that file with `python3 -I`: walk the XML, print the top 2–3 levels, and
   count node types. Never read it raw.
3. Classify the page's top-level children:

   | Node type | Means |
   |---|---|
   | `frame` around 1920 wide (desktop) or around 390 wide (mobile) | a screen |
   | small `frame`/`instance` with a title component | a section or menu header |
   | `instance` of a "placeholder" or "working" component | a screen that isn't designed yet; read its variant for the status |
   | `shape-with-text` | a flow step (SQUARE = process or alert, DIAMOND = decision) |
   | `connector` | a flow edge |

4. Read the flow edges with **one** read-only `use_figma` call per page. Use the script in
   [references/flow-conventions.md](references/flow-conventions.md#read-the-flow). It
   returns each connector's label, its color, and the names of its endpoints.
5. Report: the screen tree, with screens marked **has flow / no flow / placeholder**, the
   naming pattern in use, and the flow kit you found. Point out names that don't follow
   the pattern or contain typos, but don't rename anything unless asked.

## Workflow 2: Design a page with its flow

1. **Find the flow kit.** This is the page or frame that holds the template shapes and
   connectors. Ask the user which one it is if it isn't obvious. Read it, then copy its
   shape types, fills, connector colors, line type, caps, and label words. The defaults
   in [flow-conventions.md](references/flow-conventions.md#conventions) apply only when
   the file has no kit.
2. **Write the flow as text first** and show it to the user:
   ```
   [Screen 1.1 loads] → <Has permission?> --True--> [Show list]
                                          --False--> [Alert: no access] → [Back to Menu 1]
   ```
   Every decision has exactly two labeled outgoing edges. Every alert has an exit.
3. **Build.** Design-mode files block `figma.createShapeWithText()` and
   `figma.createConnector()`, so **clone** the kit's template nodes (`node.clone()`),
   then set `text.characters` (load the font first), position the clones, and set
   `connectorStart`/`connectorEnd` with `endpointNodeId` and `magnet: 'AUTO'`. If cloning
   is also refused, stop and tell the user. Don't fake the flow with plain rectangles
   and lines unless they ask for that.
4. **Placement.** Put the flow lane to the right of the screen frame, on the same top
   edge, with a 200 px gap. Decisions go in one row and outcomes go below them. Wrap the
   screen and its lane in a `section` named exactly like the screen.
5. **Naming.** The screen frame is named with the breadcrumb `Role ▸ Menu ▸ Screen`. Each
   step's text is the user-visible action or check, written in the file's language.
6. Take one screenshot after composition. Fix what's wrong, take one screenshot after the
   fix, and stop.

Write only where the user pointed you. If they say "try it" or "test", work on a
duplicated page, never on the live screens.

## Workflow 3: Handoff checklist

For each screen, run `get_design_context` on the screen and read its flow (Workflow 1,
step 4), then write:

- **States:** default, empty, loading, and error, taken from the screen frame and its
  placeholder variants.
- **Branches:** one line per decision: `<condition> → True: <step> / False: <step>`.
- **Alerts:** the text and exit of each alert step.
- **Role gates:** decisions that test a role.
- **Navigation:** where each Base edge leads (menu item → screen).
- **Gaps:** decisions with a missing branch, alerts with no exit, and screens that are
  still placeholders.

Use `design-core`'s handoff list (states, behavior, tokens and components, edge cases, gaps) as the frame.
Return the checklist in chat or as a doc the user picks. Code comes from
`figma-design-to-code`. This skill only supplies the behavior side.
