---
name: agent-surface-design-system
version: 0.5.0
description: >
  A design-system lens for building browser-based and agent-adjacent surfaces
  where humans review, annotate, approve, or steer coding agents. Extracted
  from Plannotator, Open Design's annotation system, and practical
  canvas-overlay experiments, then generalized into reusable laws, patterns,
  and component decisions for agentic interaction UIs.
triggers:
- "design an agent review UI"
- "human-in-the-loop agent interface"
- "agent plan approval UI"
- "annotate agent output"
- "build an agent feedback surface"
- "design system for agent tools"
- "pair an agent with a design system"
- "MCP server for design artifacts"
---

# Agent Surface Design System

A pattern library for building surfaces where humans and coding agents meet.
The patterns below are abstracted from
[Plannotator](https://github.com/backnotprop/plannotator),
[Open Design](https://github.com/nexu-io/open-design)'s annotation system, and a
lightweight browser canvas overlay, then framed as reusable laws, layout decisions,
interaction patterns, and integration strategies.

Use this skill whenever you are designing a UI that an agent produces, a human
reviews, and the result flows back to the agent.

---

## Core surface laws

## Law 1: The surface is a seam, not a replacement

**Don't reimplement the agent. Don't replace the CLI. Inject a review seam into
the agent's existing lifecycle.**

The most effective agent surfaces hook into moments the agent already exposes:

| Agent moment | What the surface does |
|--------------|----------------------|
| `ExitPlanMode` / `Stop` / `exit_plan_mode` | Pause, open browser, wait for human decision |
| Tool-use boundaries | Intercept agent output before it becomes action |
| End-of-turn | Render the agent's output for review before the next turn |
| Explicit slash command | Let the user summon the surface on demand |

**Pattern:** expose a single long-lived CLI command (e.g. `plannotator`) that the
agent invokes with a very long timeout (e.g. 345600 ms). The command starts a
local server, opens the browser, blocks on user input, then returns structured
feedback to the agent's stdout/stdin loop.

---

## Law 2: Output first, chrome second

**The agent's artifact is the hero. Every piece of chrome must justify its
presence against the artifact.**

Default layout priority:

1. **The artifact** — plan, diff, markdown, HTML, diagram — gets the center and
the most screen real estate.
2. **Navigation/structure** — TOC, file tree, diff file list — gets a narrow
left sidebar.
3. **Human input** — annotations, comments, AI chat, approve/deny — gets a right
sidebar or bottom panel.

```
┌─────────────────────────────────────────────────────────┐
│ Minimal header: title + mode + primary actions          │
├──────────┬──────────────────────────────┬───────────────┤
│ Structure│         Artifact             │ Human input   │
│ sidebar  │   (maximize readability)     │ / annotation  │
└──────────┴──────────────────────────────┴───────────────┘
```

**Pattern:** start with the artifact at full width; add sidebars only when the
user needs them. Use collapsible panels, not permanent chrome.

---

## Law 3: Approve is a first-class action

**The primary job of the surface is to produce a decision: proceed, revise, or
abort. Optimize every layout and shortcut around that decision.**

Primary actions should be visually dominant and available without scrolling:

- **Approve / LGTM** — green, top-right, keyboard shortcut (e.g. `Cmd+Enter`).
- **Request changes** — secondary but prominent, opens annotation/comment mode.
- **Exit / skip** — tertiary, de-emphasized to prevent accidental dismissal.

**Pattern:** after a "request changes" decision, the surface should diff the
next revision against the previous one so the user can verify the agent
addressed every point.

---

## Law 4: Annotations are the feedback protocol

**Humans communicate with agents through annotations on the agent's own output.**

Annotations are the bridge between human review and agent revision. Support at
least these four forms:

| Type | Use case |
|------|----------|
| Inline text | Comment on a sentence, requirement, or code line |
| Range/selection | Comment on a block, function, or multi-line change |
| File-level | Overall feedback on a file or section |
| Threaded reply | Conversation about a previous annotation |

**Pattern:** serialize annotations into a structured feedback payload that the
agent can parse and act on. The agent should be able to map each annotation back
to a location in its own output. For the mechanics of capturing and scoping
annotation targets, see the Annotation laws (Law 31 onward).

---

## Law 5: One surface, many agents

**The surface should not be coupled to one agent. Each agent gets a thin
adapter; the surface stays generic.**

Thin-agent, thick-surface architecture:

```
Agent A ──► adapter A ──┐
Agent B ──► adapter B ──┼──► generic surface ──► human review
Agent C ──► adapter C ──┘        │
                                 ▼
                         structured feedback
                         routed back to caller
```

**Pattern:** keep agent-specific code in small adapter packages or plugins. The
surface consumes a normalized payload (plan, diff, markdown, annotations) and
returns a normalized decision. The adapter translates between agent conventions
and the surface's protocol.

---

## Law 6: Local-first, share-optional

**The surface must work fully on the user's machine without a backend. Sharing
and collaboration are opt-in layers.**

Benefits:

- Works offline and in restricted environments.
- No latency for the core review loop.
- Privacy: sensitive plans/diffs never leave the machine unless the user chooses.

**Pattern:** serve the UI from a local HTTP server spawned by the CLI. For
sharing, encode small payloads in the URL hash; for large payloads, use
client-side encryption with a paste service that stores only ciphertext.

---

## Law 7: Remote ergonomics are first-class

**SSH, devcontainers, and remote servers are normal. The surface must not assume
a local browser.**

Patterns:

- Detect remote environments and switch to a fixed port (`19432` is a reasonable
default) instead of a random one.
- Print the local URL to the terminal when browser-open fails or is suppressed.
- Keep all WebSockets and terminal traffic on the same origin/port as the main
UI to avoid extra port forwarding.
- Provide `BROWSER=/usr/bin/true` or equivalent for CI/automation harnesses.

---

## Law 8: Agent context belongs in the same workspace

**When the user wants to run an agent while reviewing, embed it; don't open a
second tool.**

A review or annotation surface can optionally embed a terminal/agent panel
alongside the artifact. The design rules for embedded agents:

- **No auto-start.** The agent must not start until the user explicitly starts it.
- **One agent at a time.** Avoid multi-agent complexity in v1.
- **Same origin/port.** Proxy terminal WebSockets through the main server.
- **Graceful cleanup.** Interrupt, then kill; never orphan PTY processes.
- **Fallback UI.** If the terminal runtime can't load, disable the panel with a
clear message; don't break the rest of the surface.

---

## Law 9: Use proven primitives, don't invent layout

**The surface is dynamic. Use a layout system that supports resizing, tabs,
panels, and persistence out of the box.**

Recommended stack decisions from Plannotator:

| Concern | Choice | Rationale |
|---------|--------|-----------|
| Layout framework | `dockview-react` | Resizable, tabbed, draggable panels with API-driven state |
| Component primitives | Radix UI | Accessible dialogs, menus, tooltips, popovers |
| Styling | Tailwind CSS + CSS variables | Theme tokens, dark/light/system modes |
| Icons | `lucide-react` | Consistent, lightweight |
| Toasts | `sonner` | Non-blocking feedback |
| Motion | `motion` | Subtle transitions without heavy motion |
| Syntax highlighting | highlight.js in a worker pool | Keep the main thread free |

**Pattern:** theme tokens should be semantic (`bg-card`, `border-border`,
`text-muted-foreground`) so components look correct across light/dark/system
modes without per-component overrides.

---

## Law 10: Human input should feel like annotation, not form-filling

**The best feedback is created by pointing at something and typing a short
note. Minimize modal forms and prefilled fields.**

Interaction patterns:

- **Select → comment.** Highlight text or a diff range, then type.
- **Floating toolbar.** Show annotation tools only when text is selected.
- **Pinpoint overlay.** Let users click anywhere on an HTML artifact to drop a
comment.
- **Quick labels.** One-click labels (e.g. "question", "blocking", "nit") plus
optional freeform text.
- **Keyboard-first.** Shortcuts for create comment, approve, next file, next
annotation.

---

## Law 11: Diff is a first-class artifact

**When reviewing code, the diff is the document, not the file.**

Patterns for code review surfaces:

- Render diffs with syntax highlighting and line numbers.
- Support side-by-side and unified views.
- Allow comments on added/removed/context lines.
- Track "viewed" state per file.
- Show semantic diff or AI-generated summary as an optional panel.
- Keep file tree in sync with diff navigation.

---

## Law 12: Make revision history visible

**Humans don't trust agents to revise correctly. Show what changed between
versions.**

Patterns:

- Store prior versions of the artifact.
- Render a diff between the current version and the previous version.
- Highlight annotations that were addressed, partially addressed, or untouched.
- Let the user click an annotation and see the corresponding change in the new
version.

---

## Law 13: Agent jobs are ambient, not blocking

**Background agent work should be visible but not steal focus.**

Patterns:

- A dedicated panel or badge shows running agent jobs.
- Logs are available on demand, not streamed into the main view.
- Jobs can be inspected, cancelled, or restarted from the surface.
- Completed jobs surface their output as annotations or file changes.

---

## Law 14: External tools can push into the surface

**The surface should accept input from tools outside the agent that spawned it.**

Patterns:

- Expose an SSE or WebSocket endpoint for external annotations.
- Accept file-change events from a filesystem watcher or git status.
- Let other tools add comments, labels, or status checks.
- Treat external input the same as native input in the UI.

---

## Law 15: Persistence is explicit, not automatic

**Don't auto-save every keystroke in a way that surprises the user. Make save,
export, and archive explicit actions.**

Patterns:

- Auto-save drafts locally, but surface a "save" or "submit" action for the
final decision.
- Export feedback as markdown, JSON, or a GitHub review.
- Archive approved plans/decisions to a knowledge base (e.g. Obsidian) with clear
metadata and backlinks.

---

## Canvas-overlay laws

## Law 16: A canvas overlay is a valid surface

**You don't need a full SPA to annotate a page. A single `<canvas>` overlay can
be enough.**

For quick, page-native annotation:

- Create one full-page `<canvas>` with `position: absolute; z-index: 2147483647`.
- Store annotations in **page coordinates** (`clientX + scrollX`, `clientY + scrollY`)
  so they scroll with the content — no per-frame redraw on scroll.
- Use `pointer-events: none` by default; enable only when a drawing tool is active.
- Resize the canvas to `max(scrollWidth, innerWidth)` and redraw on `resize` and
  `ResizeObserver` events.

This pattern is for lightweight, page-native overlays that work on any web page
without modifying the host app's code. For structured visual marks inside a
preview surface, see Law 32.

---

## Law 17: Tools should be keyboard-first

**Avoid modal toolbars. Plain keys switch modes instantly.**

From browser-annotate:

| Key | Tool |
|-----|------|
| `F` | Freehand |
| `A` | Arrow |
| `S` | Shape / ellipse |
| `T` | Text |
| `H` | Highlight/select DOM element |
| `Z` | Undo |
| `R` | Redo |
| `C` | Copy selections |
| `Q` | Clear all |
| `Ctrl+D` | Toggle overlay on/off |

**Pattern:** one global toggle (e.g. `Ctrl+D`) to enter/exit the surface; once
inside, single keys map to tools. Show the shortcuts in a small, non-blocking
badge so users learn them.

---

## Law 18: Select real DOM elements, not just pixels

**Pixel annotations are expressive but fragile. Combine them with structured
DOM selections for agent-usable references.**

In "highlight" mode:

- Use `document.elementFromPoint(x, y)` to find the element under the cursor.
- Draw a hover outline around the candidate element.
- On click, record a structured selection: tag, id, classes, CSS selector,
  bounding box, truncated text, and outer HTML.
- Assign each selection a numbered `data-sel` attribute so the page itself marks
  what was selected.
- Generate a stable CSS selector path (id first, then classes, then
  `:nth-of-type()` fallback) so the agent can re-find the element later.

**Pattern:** copy selections as structured text the agent can parse:

```
[sel 1] <rect> selector="div#eligibility > svg > g > rect:nth-of-type(3)"
        text="" rect=67,353,680x119
```

---

## Law 19: Annotations should be movable and undoable

**Treat annotations like objects, not permanent paint.**

- **Implicit move:** on hover near an existing annotation, change the cursor to
  `grab`; on drag, move the annotation and redraw.
- **Hit-test backward** so the topmost annotation is picked first.
- **Undo/redo stack:** maintain `operations` and `redoStack`; `Z` pops from
  `operations`, `R` pushes back from `redoStack`.
- **Clear all:** a single shortcut (`Q`) removes everything with confirmation
  implied by the destructive nature of the key.

---

## Law 20: Expose a global handle for programmatic access

**Let the host environment (or the agent) read the surface state.**

Attach a namespace to `window` and expose a small, serializable API. See
[resources/global-surface-api.js](resources/global-surface-api.js) for a
copy-pasteable implementation that strips private `_el` references before
returning data.

**Pattern:** keep the public API small and serializable. Strip internal DOM
references (`_el`) before returning data.

---

## Law 21: Inject via init scripts for persistence

**If the surface must survive navigations, register it as an init script.**

For browser-automation surfaces (cmux, Playwright, Puppeteer, etc.):

- Use `addInitScript` so the overlay is injected into every new document in the
  same browser context.
- Also `eval` the script into the current page for immediate effect.
- Wrap the script to handle both `document.body` already present and
  `DOMContentLoaded` for late injection. See
  [resources/init-script-overlay.js](resources/init-script-overlay.js) for a
  copy-pasteable init script.

**Pattern:** a thin shell wrapper can auto-inject the overlay whenever a browser
surface is opened, so the user doesn't run a manual install step each time.

---

## Law 22: Jank is acceptable if the interaction is right

**A janky but predictable overlay beats a polished tool you never use.**

Browser-annotate explicitly accepts limitations:

- Works only on already-open surfaces; it does not auto-apply to future surfaces
  in all contexts.
- Uses a fixed-position toolbar, not a docked panel.
- Text input is a `<textarea>` absolutely positioned over the canvas.
- Selections are not persisted across page reloads unless the host environment
  saves them.

The lesson: optimize for the core loop (toggle → annotate → copy → send to
agent). Polish the edge cases later.

---

## Design-system laws

## Law 23: Pair every skill with a design system

**Agent output gains taste when you separate *what to build* from *how it should
look*.**

Open Design composes every request from three layers:

```
BASE_SYSTEM_PROMPT            (output contract: wrap in <artifact>, no code fences)
  + active DESIGN.md body     (palette, typography, layout, voice)
  + active SKILL.md body      (workflow and output rules)
```

**Pattern:** keep skills as content (Markdown + optional assets) and design
systems as brand contracts (`DESIGN.md`). The front-door skill scans existing
systems, picks the right one, then routes to a specialist skill for the artifact
type (prototype, deck, image, video).

---

## Law 24: Treat `DESIGN.md` as the brand contract

**A single markdown file can encode everything an agent needs to stay on-brand.**

A `DESIGN.md` design system typically includes:

1. Visual theme & atmosphere
2. Color palette & roles
3. Typography
4. Layout & spacing
5. Components
6. Motion & interaction
7. Iconography & imagery
8. Voice & tone
9. Edge cases & variations

**Pattern:** store design systems in a discoverable folder
(`design-systems/<brand>/DESIGN.md`). The agent scans them at runtime and loads
the matching system into context. Multiple systems per project are fine — one
for product, one for marketing, one for decks.

---

## Law 25: Parse agent output into a sandboxed preview

**Don't show the user raw markdown or code. Extract the artifact and render it.**

Open Design streams agent output, parses `<artifact>` tags, and renders the HTML
in a sandboxed iframe.

Patterns:

- Define a clear output contract (e.g. "wrap the artifact in `<artifact>`").
- Strip code fences before parsing.
- Render generated HTML in a sandboxed iframe with restricted permissions.
- Provide download/export buttons for the artifact (HTML, PDF, PPTX, MP4, image).
- Keep the raw agent transcript available but secondary.

---

## Law 26: Offer an MCP server, not just a CLI

**Let agents discover the surface through their native tool system.**

Open Design ships `od mcp install <agent>` to wire an MCP server into Claude
Code, Codex, Cursor, Copilot, Gemini, OpenCode, and many others.

**Pattern:** build the core as an MCP server with clear tools, then provide
one-line install commands for each agent host. This is more portable than
agent-specific hooks and lets the surface expose multiple capabilities
(generate, preview, export, handoff) as discrete tools.

---

## Law 27: Support multiple artifact types from one studio

**The same design system should stream out many outputs.**

Open Design's Studio produces:

- **Prototypes** — single-page HTML artifacts (web, desktop, mobile).
- **Decks** — pitch decks navigable by keyboard, exportable to PPTX/PDF.
- **Images** — brand-grade visuals.
- **HyperFrames** — programmatic motion graphics rendered to MP4.
- **Live dashboards / artifacts** — interactive HTML surfaces.

**Pattern:** one front-door skill routes to specialist skills by artifact type.
Each specialist knows the output medium; the design system provides the shared
visual language.

---

## Law 28: Automate repeat workflows without removing the human

**Repetitive design tasks should be repeatable, but the human stays in control.**

Open Design's Automation page lets users turn repeat workflows into reusable,
schedulable automations. Apply this pattern when:

- The same brief shape appears often.
- The user wants batch generation with review checkpoints.
- Outputs need to be regenerated when inputs change.

Keep a manual review step before final export or handoff.

---

## Law 29: Hand off to implementation cleanly

**Design surfaces should close the loop by producing artifacts a coding agent can
consume.**

Open Design's `handoff-to-claude-code` skill turns a finished design into
implementation instructions for a coding agent.

Patterns:

- Export design tokens as CSS variables or JSON.
- Generate component-level implementation notes.
- Provide a brief with constraints, not just screenshots.
- Include the original `DESIGN.md` or a distilled subset.
- Mark what is firm (tokens, layout) versus flexible (copy, edge cases).

---

## Law 30: Let the community extend the surface

**A healthy agent surface is an ecosystem of skills and plugins, not a single
monolithic UI.**

Open Design's plugin page lets users browse, install, and distribute workflow
plugins. Similarly, skills live as Markdown folders that contributors can fork.

Patterns:

- Define a minimal skill folder: `skills/<name>/SKILL.md` with YAML frontmatter.
- Allow relative references to assets inside the skill folder.
- Validate for portability (no escaping references, no runtime code in skills).
- Provide a contribution skill (`od-contribute`) with validators and templates.

---

## Annotation laws

## Law 31: Bind every comment to a preview target

**Every annotation must carry enough context for the agent to find the element again.** In Open Design a preview comment includes filePath, elementId, selector, position, label, currentText, htmlHint, and computedStyle.

- Capture the DOM element under the cursor, not just pixel coordinates.
- Snapshot computed style (color, backgroundColor, fontSize, fontWeight, lineHeight, textAlign, fontFamily, padding, borderRadius) so the agent can recognize the element even if selectors are unstable.
- Trim context text and HTML hints to bounded lengths (e.g. 160/180 chars) before serialization.

**Pattern:** serialize a `PreviewCommentSnapshot` with `{ filePath, elementId, selector, label, text, position, htmlHint, style, selectionKind }`.

---

## Law 32: Treat visual marks as first-class comments

**A box, a pen stroke, or a click on a preview is a comment, not a second-class attachment.** Open Design's `PreviewDrawOverlay` supports box select and pen tools; the resulting mark is classified as `click`, `stroke`, or `click+stroke`.

- Composite visual marks onto a screenshot so the agent sees exactly what the user highlighted.
- Hide the overlay's own chrome during capture, then repaint marks onto the captured image.
- Classify the mark kind and include it in the feedback payload so the agent knows whether the annotation points to a single element, a drawn region, or both.

**Pattern:** emit `{ file, note, markKind, bounds, target }` via a CustomEvent (`opendesign:annotation`) so the host can route it to the agent.

---

## Law 33: Hard-scope the agent with attached comments

**When annotations feed back to the agent, explicitly forbid scope creep.** Open Design renders attached preview comments as an `<attached-preview-comments>` block with the directive: "Hard scope: change ONLY the elements identified below by selector / position / pod members."

- Include selector, position, currentText, htmlHint, and computedStyle for each comment.
- For visual marks, instruct the agent to inspect the screenshot and modify the marked region first.
- For multi-element selections ("pod" selections), list every member element.

**Pattern:** append the rendered comment block to the user's message content
before sending it to the agent. See
[resources/attached-preview-comments-template.md](resources/attached-preview-comments-template.md)
for a ready-to-use template.

---

## Law 34: Offer queue, draft, and send as distinct actions

**Don't conflate capturing feedback with dispatching it.** Open Design's draw toolbar exposes three actions: `draft` (add to input composer), `queue` (stage for next turn), and `send` (dispatch now).

- `draft` lets the user build a message without committing it.
- `queue` stages feedback while an agent job is running.
- `send` dispatches immediately when the composer is active.

**Pattern:** make the primary toolbar action depend on context (e.g. disabled when an agent job is running, with `queue` still available).

---

## Law 35: Distill annotations into durable memory

**Review feedback should outlive the current chat turn.** Open Design's memory distiller converts preview comments into memory entries (rules and feedback) and writes them into the project's memory store.

- Auto-keep feedback and rule entries; skip empty comments.
- Drop non-durable candidates (e.g. transient project notes) returned by the distiller.
- Link new entries into `MEMORY.md` so they are injected into future agent context.

**Pattern:** after a review session, run a distiller over the annotations and user message, persist rules and feedback entries, and emit a non-blocking signal carrying the source and count.

---

## Law 36: Generate review artifacts from diff-review

**For code changes, produce deterministic review files that the agent can consume.** Open Design's diff-review atom writes `review/diff.patch`, `review/summary.md`, `review/decision.json`, and `review/meta.json`.

- `diff.patch` is a receipt-derived summary, not a line-by-line diff; precise hunks live in `plan/receipts/`.
- `summary.md` walks through each step with stats and rationale.
- `decision.json` records accept / reject / partial; partial decisions must cover every touched file.
- `meta.json` records generation time, atom digest, and plan revision.

**Pattern:** write the review artifacts deterministically, then let a GenUI surface write `decision.json`; when a decision arrives, re-run the atom and auto-promote the handoff manifest.

---

## Law 37: Render annotation toolbars outside the scroll frame

**In scaled or clipped previews, a toolbar inside the scroll area scrolls away or gets clipped.** Open Design portals `PreviewDrawOverlay`'s toolbar into `.viewer-body` so it stays pinned below the device frame.

- Resolve the toolbar host in a layout effect so the first paint is already portaled.
- Use a floating pill-style toolbar with compact icon clusters.
- Keep toolbars accessible via pointer and keyboard; show tooltips on hover/focus.

**Pattern:** wrap the annotation UI in a portal that targets a stable ancestor outside the preview scroll area.

---

## Law 38: Redline specs are static annotations

**Annotated wireframes are a valid annotation output format, not just interactive markup.** Open Design's `wireframe-annotated` skill produces a two-column page: greybox canvas on the left, spec panel on the right, numbered pins linked to engineering notes.

- Each numbered pin on the canvas has exactly one matching spec row.
- Use one accent color only for pins and spec numbers; everything else stays greyscale.
- Wrap the artifact in `<artifact>` tags with `type="text/html"`.

**Pattern:** for handoff annotations, generate an HTML artifact where every
callout is mirrored by a structured note the agent can read. See
[resources/wireframe-annotated-template.html](resources/wireframe-annotated-template.html)
for a complete two-column redline template.

---

## Examples

Concrete surface layouts and workflows live in `examples/`:

- [examples/plan-review-surface.md](examples/plan-review-surface.md) — approve / request changes on a markdown plan.
- [examples/design-generation-surface.md](examples/design-generation-surface.md) — generate a design inside a sandboxed iframe preview.
- [examples/annotation-workflow.md](examples/annotation-workflow.md) — capture, scope, and dispatch preview annotations to an agent.

## Resources

Copy-pasteable primitives referenced by the laws:

- [resources/global-surface-api.js](resources/global-surface-api.js) — serializable `window.__agentSurface` handle.
- [resources/init-script-overlay.js](resources/init-script-overlay.js) — `addInitScript`-friendly overlay bootstrap.
- [resources/attached-preview-comments-template.md](resources/attached-preview-comments-template.md) — hard-scope comment block template.
- [resources/wireframe-annotated-template.html](resources/wireframe-annotated-template.html) — two-column redline wireframe artifact.

---

## Related Skills

- `build-review-interface` — generic browser annotation interfaces
- `mcp-builder` — when the integration surface is an MCP server instead of a UI
- `claude-code-plugin` — Claude Code plugin/hook specifics
- `frontend-design` — distinctive aesthetic direction for agent-generated UI

## Source

Patterns extracted from:

- [Plannotator](https://github.com/backnotprop/plannotator) by backnotprop —
  agent plan/code review surface with annotation capabilities.
- [Open Design](https://github.com/nexu-io/open-design) by nexu-io — agentic
  design workspace with annotation system, skills, design systems, and MCP
  integration.
- A lightweight browser canvas overlay for DOM selection and drawing.
