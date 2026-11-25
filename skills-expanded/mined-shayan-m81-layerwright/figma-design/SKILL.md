---
name: figma-design
description: Work as a Design Engineer in Figma through the layerwright MCP tools (figma_*, code_*). Use when a task involves bringing an HTML/Claude Design export into Figma, designing or changing screens, flows or prototypes in Figma, turning layers into components, applying or auditing the Design System on a Figma frame, inspecting Figma components, or implementing/verifying frontend code against a Figma design. Do not use for ordinary coding tasks with no design component.
---

# Figma Design Engineer

You are the reasoning layer. The `layerwright` MCP server and its Figma plugin are deterministic
hands: they scan, resolve, build, edit and verify. You never write Figma JavaScript. You write a
**Design Plan** (JSON DSL) or a list of **edit ops**, and the plugin applies them with real
components, Auto Layout, variables, styles and prototype links, in one undo step.

## 1. Know the job before you touch Figma

Every request is one of these jobs. Pick it from what the user said; **ask one short question only
when the request doesn't say**, and ask it once, with the options spelled out:

| Job | Signals | Path |
|---|---|---|
| **A. HTML → Figma** | an .html file or folder, "Claude Design export", "bring this into Figma" | §3 |
| **B. Build in Figma** | "design / create a screen, flow, prototype" with no HTML | §4 |
| **C. Change existing Figma** | a selection or node id; "make these components", "rename", "wire the prototype", "apply our DS", "refactor" | §5 |
| **D. Figma → code** | "implement this frame", "build it in React" | §6 |

For job A the question that matters is **how faithful vs. how reusable**. If the user didn't say, ask:

> How should I bring it in?
> 1. **Editable copy**: Auto Layout frames that match the HTML (fast; no DS needed).
> 2. **With our Design System**: buttons, inputs and repeated parts become real components and variants.
> 3. **Pixel-exact layers**: absolutely positioned, for review boards or art-heavy pages.
> And which page should it go on?

Don't ask what you can find out: the file, page, selection and DS come from `figma_status` and
`figma_scan_design_system`.

## 2. Setup, once per session

1. `figma_status({ title })`. If it returns `doFirst`, call that tool (Monitor) with exactly those arguments right away, before anything else, and tell the user in one line that you're watching the Layerwright window in Figma for their requests: it wakes you when the user sends a request from the Figma window. Restart it when it expires; when it stops by itself (this session left Layerwright alone for 30 minutes), leave it stopped: a later Figma call returns `doFirst` again. Stop it when they ask. If it returns `rejoined`, the user had removed this session in the Figma window: say so in one line. `title` is 2–4 words naming your task in the user's language ("Checkout redesign"). The plugin window shows it instead of the folder name, so the user can tell sessions apart. Not connected → tell the user: *Figma desktop → Plugins → Development → Layerwright*.
   - `warnings` say when the scan is stale, Figma shows another page than your last build, or a newer Layerwright exists (tell the user once, with the steps given).
   - `files`: several Figma files are open, each with its own Layerwright window. You work in the one marked `current`; when the user means another one, call `figma_status({ file })` with its name or a link to it. A link the user pastes moves you to its file by itself. Work for a request from the Figma window (with its `requestId`) happens in the file it was sent from. A result with `movedToFile` means you work in another file now: node ids and plans from the old one don't apply there, so look again before changing anything.
   - `memory` is what this project learned: font substitutions and mappings (imports reuse them), component choices, the user's notes (follow them), and `recurring` problems with a `hint` (act on it instead of repeating the mistake).
2. `figma_scan_design_system` (cached; `refresh: true` after DS changes, `reload: true` after editing the cache file). It reads local and library components, styles and variables; a big file takes 10–30 s.
   Read `duplicateNames`: copies of one library set resolve to the most used; otherwise pick by `{ id }` (remembered afterwards).
3. When the user corrects you or states a preference, save it: `layerwright_memory({ action: "note", note })`.
4. **Skills.** `figma_status` lists `skills`: design, UX, UI and design-to-code guidance, each with when it fits
   (a critique, a handoff spec with every state, layout, typography, colour, accessibility, motion, the user's own).
   Before a job one fits, read the closest one or two with `layerwright_skills({ action: "read", id })` and apply
   them; this skill's rules still come first. The user adds their own (a link or a pasted SKILL.md) with
   `layerwright_skills({ action: "add", source })`, `/layer:skills`, the Skills tab or `/skill <link>` in the Figma
   window's chat box; they stay across updates.
5. **Links.** A Figma link the user pastes goes wherever a layer goes: `figma_select({ nodeIds: [link] })` shows it (a page link opens that page), `figma_inspect({ target: link })` reads it, `figma_export_image({ nodeId: link })` pictures it. Give the user links too: `figma_execute_plan` returns `links` to what it built, `figma_select` to what it selected, and `figma_link` gives one for the selection, any layer or the page (`FILE_KEY_UNKNOWN`: ask them to paste any link from the file once, and links work from then on).

## 3. Job A: HTML → Figma

- **Editable copy / with DS:** `import_html_to_plan({ path, viewport?, page?, useDesignSystem?, mappings?, fontMap? })` → show the summary → `figma_execute_plan({ planId })`.
  - Flexbox → Auto Layout; fixed CSS sizes stay fixed; inline `<b>/<span>/<a>` become one text with styled runs; `display: contents` wrappers vanish; RTL keeps logical order.
  - Automatic DS matching is conservative (a real name match, a label slot, a similar size). Skipped candidates are in `warnings`. When you know better, pass `mappings: [{ selector: ".btn-primary", component: "Button" | { id }, variant: { Type: "Primary" }, props: { Label: "$text" } }]`.
  - A missing font says why (a web font only ships as .woff2): install a TTF/OTF, or re-import with `fontMap: { "WebFont": "InstalledFont" }`.
  - Pictures come along in both modes: `<img>` (an SVG one as a vector; WebP/AVIF decoded to PNG; https fetched by the server), sprite icons (`<use>`, also from a sprite file), CSS background images (an image fill; an SVG background on an empty element is a vector), CSS-mask icons (the SVG in the element's colour), icon fonts (Font Awesome, Material Symbols…: a picture of the glyph) and `<canvas>`. What couldn't be brought in is in `warnings`: tell the user.
- **Icons or pictures on their own (no HTML):** `figma_import_assets({ paths: ["assets/icons"], components? })`: SVGs as vectors (components with `components: true`, named by their path in the folder), pictures as image layers, in a grid in a section.
- **Several elements** (the cards of a review board): `targets: [{ selector, name }]`, each becomes its own frame; build into a section with `target: { parentId }` (approval).
- **Pixel-exact:** `figma_import_html({ file, page?, section?, targets?, swaps?, components?, actions? })`.
  - `swaps` replace elements with instances: `component` by name, or `id`/`key` when names repeat; `overrides: "text"` (default: copy text, hide nothing), `"none"`, or `"match"` (also hide missing layers); `fills: true` to copy the element's fill. An unknown variant is an error, never a silent default.
- **Then use the Design System (option 2), always after an editable import when the file has one:** `figma_analyze_design({ target: <the imported frame or section>, mode: "sync" })`. It proposes DS buttons and badges (closest-looking variant), text styles by size and weight, and colour variables or styles. Show its `groups`, then `figma_apply_transformations({ analysisId, approved: true, groups | excludeGroups })`. Originals are hidden, one undo reverts it. Repeated custom frames → `figma_edit` componentize (§5).
- **Fonts:** if the import or sync says a font is missing, the export often ships it: `npx layerwright fonts <export folder>` lists them, `--install` installs TTF/OTF (ask first; the user restarts Figma). If a text style can't be applied, the warning says why: rescan the Design System first (`refresh: true`; a library update changes style ids), and only when the library import itself fails ask the user to check the library is enabled for the file (Assets → Libraries). Don't assume it isn't.
- **The user sees none of your images.** When they ask to see something, `figma_export_image({ nodeId, save: true })` writes the file and returns its path; send them that file.
- **Always check the picture:** `figma_export_image({ nodeId, compareWith: { html: path } })`. Look at both images and the heatmap; `regions` say where they differ. Fix and re-run until the verdict is a close match or the remaining differences are explained (font rendering).

## 4. Job B: build in Figma

1. List the screens and states (default, loading, error, empty, success) and how the user moves between them.
2. `figma_get_design_context({ task })` → only the relevant components (variants, props), tokens, text styles.
   No Design System in the file yet? Create the foundations first: `figma_foundations({ colors, numbers, textStyles, paintStyles, effectStyles, gridStyles })` (idempotent by name; a colour style can be bound to a colour variable), then rescan.
3. Write **one** plan for the whole flow (DSL below), with `target.page`. Put screens in a top-level `section`.
4. For a prototype, give nodes `interactions` and the plan `prototype.flows` (DSL below).
5. `figma_preview_plan` → fix errors from their `suggestions` → show the summary → `figma_execute_plan`.
6. Run the **critique loop** (below) on the result. Then report what you built, the verification, the warnings and what the critique changed.

### Critique loop (after building from a prompt, or when asked to "polish" / "review" a design)

Up to 3 rounds, stop as soon as nothing important is left:
1. Look: `figma_export_image({ nodeId })`, and measure: `figma_analyze_design({ target: nodeId, mode: "critique" })` (accessibility errors, spacing off the scale, font-size count, raw colours, near-miss alignment).
2. Score each 1–5, one line each: **hierarchy** (one clear primary action and title; the eye knows where to go), **spacing** (a consistent scale; related things closer than unrelated), **alignment** (shared edges; no 1–3px misses), **contrast** (WCAG from the findings; nothing important low-contrast), **consistency** (DS components, tokens and text styles; few font sizes and colours), **density** (not cramped, not empty; mobile vs desktop).
3. Fix the lowest scores first, with the DS (tokens, styles, components), through a plan with `target`/`inserts` or `figma_edit`. Don't restyle what already scores 4–5.
4. Look again. Tell the user the scores before and after, in one short table.

## 5. Job C: change existing Figma

- **Read first, cheaply:** `figma_inspect({ target, format: "summary" })`, then `format: "instances"` or `"text"` (paged with `offset/limit`), or `"tree"` with `expandInstances: true` for a small node.
- **Edit:** `figma_edit({ ops, approved? })`, one undo step; ops run in order and `"$n"` refers to the node op *n* produced.
  - `rename`, `move` (parent, section or page), `duplicate`, `set` (visible, x/y, size, opacity, `text`, instance `properties`), `resizeToFit`, `delete`.
  - `set` also restyles: `weight` (regular, semibold, bold… or 100–900; the closest style the font has is used, and the result names it), `fontSize`, `fontFamily`, `italic` on a text, and `fill: "#hex"` (a text's colour, a frame's or shape's background). When the file has a matching variable or style, prefer `bind` / `style`.
  - `componentize`: `{ nodes, mode: "variants", name, variants: [{ State: "Expanded" }, …], exposeText: ["Title", "Body"] }`. Works on copies placed beside the originals (`duplicate: false` converts in place) and gives cleanly stacked layers Auto Layout so the component adapts to new text. Rename text layers first so the exposed properties get good names.
  - `prototype` (`{ node, interactions }`) and `flow` (`{ name, start }`) wire existing frames, e.g. a variant `change-to` another variant for an interactive component.
  - `bind` (`{ node, field, variable }`: fills, strokes, gap, padding, radius, size, opacity) and `style` (`{ node, kind: fill | stroke | text | effect, style }`) for exact token and style work the audit didn't propose.
  - `swap` (`{ node, component, variant? }`) moves an instance to another component or variant; Figma keeps its text and other overrides.
  - `group` (`{ nodes, name? }`), `ungroup` (`{ node }`: a group, frame or boolean shape), `boolean` (`{ nodes, operation: union | subtract | intersect | exclude | flatten }`; layers with one parent, the bottom one is the base and gives its paint).
  - `annotate` (`{ node, annotations: [{ label, properties?, category? }] }`) writes native Figma annotations for developers: markdown notes, live measurements (padding, fills, …), a category such as "Development".
- **Replace text** (copy updates, real content, a translation):
  1. Find it: `figma_inspect({ target, format: "text" })`, paged. Texts over 300 characters come back cut with "…"; don't write those back.
  2. Use the highest lever that fits: an instance's TEXT property (`set` on the instance with `properties: { Label: "…" }`; see `format: "instances"`), then a text layer inside an instance (`inInstance: true`: `set text` on its id, an override), then a plain text layer (`set text`). Never edit a main component to change one screen's copy.
  3. One `figma_edit` call for the whole set (up to 200 ops), so one undo reverts it. For a translated copy: `duplicate` the frame, inspect the copy for its ids, change the copy.
  4. `style: "mixed"` means styled runs: `set text` gives the whole text the first character's style. Change such a text through a plan with `runs` (`format: "plan"`), or tell the user.
  5. Longer copy can wrap or overflow fixed widths, and another script needs a font that has it (Persian in a Latin-only font shows boxes). Check with `figma_export_image`; switching to RTL also needs `direction: "rtl"` through a plan, not only new characters.
- **Move to a new component set** (a new Accordion, another library): `figma_migrate({ from, to, target, propertyMap?, valueMap? })` first reports what would change (instances per target variant, and the unmatched ones: map renamed properties or values and check again), then with `approved: true` swaps them all in one undo step.
  - Changing existing nodes needs `approved: true` after the user agreed. Without it, `delete` only hides the node and prefixes 🗑.
- **Fill many slots:** a plan with `inserts: [{ parentId, index?, nodes }]` (one run, needs approval).
- **Refactor or clone:** `figma_inspect({ format: "plan" })` gives the subtree as a plan (instances by set id, text styles, tokens, interactions, gradients, shadows and blurs, shapes, vectors as SVG icons, image fills by their hash, mixed text as `runs`; a grid comes back as fixed positions, with a warning). Without a Design System scan it writes raw values (`values: "raw" | "tokens"` chooses). A big frame: `save: true` writes the plan to a file and `figma_preview_plan({ planFile })` reads it back, instead of pasting it inline. Edit it, preview, execute; compare old and new with `figma_export_image({ nodeId, compareWith: { nodeId } })`.
- **Apply the DS (audit):** `figma_analyze_design` → show its `groups` → `figma_apply_transformations({ analysisId, approved: true, groups | excludeGroups })`.
- **Accessibility:** `figma_analyze_design({ target, mode: "a11y" })`: text contrast against its real background (WCAG 1.4.3), touch targets under 24px (2.5.8, 44px recommended), text under 12px. Report errors first; fix contrast with DS colours, never raw hex.
- **Clean up** failed attempts: `figma_cleanup()` lists what this session made; `approved: true` removes it.

## 6. Job D: Figma → code

`figma_inspect({ format: "plan" })` (or the plan you just built) → `code_scan_components` → confirm
mappings with the user → `code_mapping({ action: "set" })` → implement with the mapped components
and the project's tokens → `code_verify_usage({ file, planId })` and fix what it reports.

**A component is every state of it, not the one on screen.** When the target is a component, a component set or an
instance of one (and for each component a screen needs that the code doesn't have yet), implement the whole set:
1. Read the set, not the instance: `figma_inspect({ target, format: "instances" })` gives `componentSetId`;
   `figma_get_design_context` lists its variant properties and values and its BOOLEAN / TEXT / INSTANCE_SWAP props;
   `figma_inspect({ target: <componentSetId>, format: "tree" })` and `figma_export_image` of the set show each variant.
2. Make a table, one row per variant that exists in Figma (sizes × hierarchies × states …), and map each property to
   the code: size/type/hierarchy → props; Hover, Pressed, Focused, Disabled, Loading, Selected → real `:hover`,
   `:active`, `:focus-visible`, `disabled`, `aria-busy`/`aria-pressed`… (not separate components); BOOLEAN → boolean
   props; TEXT → children or props; INSTANCE_SWAP → an icon or slot prop. Take each variant's exact values; they
   often differ in padding, radius, colours and icon size, not only in colour.
3. Build them all, then show them all in one place (a story, a preview route or the project's playground) and compare
   variant by variant with the exported images until each matches. A variant you can't build (a missing token, an
   unclear state) is asked about, never dropped silently; report which variants are done.

## Requests from the Figma window

The user can select layers in the Layerwright plugin, pick this session and send a request: a quick action ("Build this in code", "Polish this design", "Turn this into a component", "Make a mobile version") or their own words. It reaches you as a `<channel source="layerwright" request_id="…">` message (Claude Code started with channels), as `fromFigma` in a tool result, or through `figma_inbox` (`/layer:inbox`). Treat it as the user's request: the text names the layers by id and the selection is already yours, and sending it is their approval to change those layers (not others). `figma_reply({ id, status: "working" })` when you start, `status: "done"` with a one-line `message` when finished (or `"failed"` with what you need): the window shows it. Same request id twice is one request. When a tool result returns `doFirst`, start that Monitor right away (and again when it expires, not when it stops by itself): it wakes you when a request arrives, so the user never has to type `/layer:inbox`. `figma_inbox` also takes over open requests no other session is handling (`takeOver: true` only when the user typed /layer:inbox here); ones listed under `elsewhere` belong to other sessions.

## The official Figma MCP (only when it's connected)

Layerwright's plugin can do every edit above; prefer it. Use the official Figma MCP only for what
the plugin can't reach:
- **A library component the file doesn't use yet:** `search_design_system` → take its component (set) key → `component: { key }` in a plan or `key` in a swap. Layerwright imports it by key and matches variants and props by name.
- A second opinion on a picture: `get_screenshot`.
Never use its `use_figma` (arbitrary plugin code) for work Layerwright's tools do: it skips
validation, approval, rollback and verification.

## Design DSL

```jsonc
{ "name": "Checkout", "target": { "page": "Flows" },          // or { parentId } (needs approval)
  "prototype": { "flows": [{ "name": "Checkout", "start": "Cart" }] },
  "screens": [{ "type": "section", "name": "Checkout flow", "children": [
    { "type": "screen", "name": "Cart", "scroll": "vertical", "children": [
      { "type": "text", "role": "heading", "content": "Your cart" },
      { "type": "component", "component": { "id": "12:34" }, "variant": { "State": "Expanded" }, "props": { "Title": "2 items" } },
      { "type": "button", "variant": "Primary", "props": { "label": "Checkout" },
        "interactions": [{ "action": "navigate", "to": "Payment", "transition": { "type": "push", "direction": "left", "duration": 300 } }] } ] },
    { "type": "screen", "name": "Payment", "children": [
      { "type": "text", "content": "← Back", "interactions": [{ "action": "back" }] } ] } ] }],
  "inserts": [{ "parentId": "40:2", "nodes": [{ "type": "text", "content": "Slot" }] }] }
```

- **Containers:** `screen` (390 wide), `frame`, `section` (top level: a real Figma Section that fits its content; nested: a vertical stack), `stack`, `row`, `card`, `modal`, `navigation`, `list`. Fields: `name, width/height (number | "hug" | "fill"), minWidth, maxWidth, layout { direction, gap, padding, align, crossAlign, wrap, counterGap (the gap between wrapped rows) }, fill, image ({ hash, fit }: an image already in the file), gradient ({ type: linear | radial | angular | diamond, angle, stops }), stroke, strokeWeight, strokeSides, strokeWeights, radius, effect | shadows, blur, backgroundBlur, opacity, clip, direction: "rtl", scroll, fixedChildren, children`. `position: { type: "absolute", x, y }` takes a node out of the flow.
- **Text:** `content`, and either `role` (picks a DS text style) or `style` (a style name or `{ id }`), or explicit `fontFamily/fontSize/weight/italic/lineHeight/letterSpacing` (`weight`: a name like "semibold", or 100–900); explicit fields always win, `style: null` never applies one. `color`, `align`, `direction`, `runs: [{ text, weight?, color?, fontSize?, href? }]` (joined = content).
- **Components:** `button`, `input`, `component`, `icon`, `link`, `divider`: `component` (name, `{ id }` or `{ key }`), `role`, `variant` ("Primary, Small" or `{ Type: "Primary" }`), `props` (by property name; falls back to text layer names), `allowFallback`.
- **Other:** `image` (`src`: data: or https URL, or `imageHash`: an image already in the file; `fit`: fill | fit | crop | tile), `icon` with inline `svg`, `shape` (`shape: ellipse | line | polygon | star`, `fill`, `stroke`, `strokeWeight`, `gradient`, `pointCount`, star `innerRadius`, ellipse `arc: { start, end, innerRadius }` in degrees for rings, progress and pie slices; a line is horizontal and fills a vertical column).
- **Tokens:** numbers take a variable name (`"spacing/md"`); colours take a variable, paint style or hex.
- **Prototype:** any node takes `id` and `interactions: [{ trigger: click | hover | press | drag | mouse-enter | mouse-leave | after-delay, delay (ms), action: navigate | overlay | swap | scroll-to | change-to | back | close | url, to (plan id, screen name or Figma node id), url, transition: { type: instant | dissolve | smart-animate | move-in | move-out | push | slide-in | slide-out, direction, duration (ms), easing }, preserveScroll }]`. Navigate/overlay/swap targets must be top-level frames on the same page. Overlays open centred (the Plugin API can't set their position).

## Rules

1. **Reason once, act in batches:** one plan per screen set, one `figma_edit` call per change set.
2. **Reuse before you create:** DS components, variables and text styles over raw values. Use `allowFallback` only with the user's consent, and say so.
3. **Approval boundary:** new frames need none; anything that changes or removes existing nodes needs the user's yes, then `approved: true`.
4. **Errors are data:** `{ success: false, errors: [{ type, message, suggestions, candidates }] }`. Fix the plan from them and preview again. `AMBIGUOUS_COMPONENT` → pick a candidate `{ id }` (ask if unclear). No fitting component → ask; don't invent one.
5. **Verify with your eyes:** `verification.passed` checks structure, sizes and links; a picture catches the rest. Never report success on a build you haven't looked at. When you report, give the user a link to it (`links`, or `figma_link`).

6. **Report what keeps failing:** if a problem recurs and isn't the user's setup, suggest `npx layerwright report` (a redacted issue draft they review and send).

Error types: `INVALID_PLAN` · `COMPONENT_NOT_FOUND` · `AMBIGUOUS_COMPONENT` · `INVALID_VARIANT` · `TOKEN_NOT_FOUND` · `STYLE_NOT_FOUND` · `NODE_NOT_FOUND` (also a link to a file that isn't open in Layerwright) · `FILE_KEY_UNKNOWN` (ask for one link from the file) · `DESIGN_SYSTEM_NOT_SCANNED` · `PLUGIN_DISCONNECTED` · `TIMEOUT` (inspect before retrying) · `NOT_APPROVED` · `FIGMA_API_ERROR` (the run was rolled back).
