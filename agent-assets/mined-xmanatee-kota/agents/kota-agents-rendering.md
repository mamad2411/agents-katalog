# Rendering Module

Typed terminal rendering for KOTA. Every operator-facing surface routes
through this module instead of writing raw ANSI or hand-rolled padding
to a stream.

## Inverted Seam

Core does not import `#modules/rendering/*`. The module registers a
`RenderingProvider` during `onLoad` for `CliTransport`, `ReplChrome`,
terminal prompts, diagnostics, and stderr passthrough. Core callers
(loop constructor, REPL host, core tools, and module-runtime diagnostics)
resolve it through `getRenderingProvider()` in
`#core/modules/provider-registry.js`; protocol types live in
`#core/modules/provider-types.js`. Deployments that omit this module
degrade to `NullTransport` for the agent stream; interactive REPL and
prompt tools refuse to start without a renderer. The repo-wide import
direction remains core protocol → module implementation; do not reverse it.

## Vocabulary

Primitives are a discriminated union. Surfaces describe *what* they want
to show; the renderer decides how the current theme, width, and TTY
state paint it. New primitives extend the union rather than smuggling
raw strings through an escape hatch.

Today's primitives cover three categories. **Text-flow:** lines, text
spans, headings, separators, section rules, blanks, stacks, and
width-aware wrapped prose. **Structured blocks:** key/value blocks,
status banners, lists, panels, tool calls, agent messages, diffs, JSON,
aligned multi-column tables, and role-aware groups. **Live state:**
sectioned dashboards that visually separate state from activity, plus
spinner and progress primitives. A surface that cannot be modeled with
the current vocabulary adds the missing primitive here — it does not
reach around the module with a raw `console.log`.

Layout-heavy primitives keep their fitting math (column distribution,
prose word-wrap, spinner/progress frames) in `layout.ts` so the type
file stays focused on the discriminated union and the helpers stay
pure-and-unit-testable on their own.

Surfaces that emit structured output (JSON streams, machine-parseable
payloads) do not render through this module. Those stay on their own
typed I/O path; the module is for human-facing terminal output only.

## Transport

The terminal transport owns theme detection, width detection, and the
pipe-vs-TTY split. Callers pass a `RenderNode` to `print` or build a
transport explicitly when they need stderr, a buffered writer, or a
custom theme.

Environment contract:

- A non-TTY stream resolves to the `no-color` theme with a safe fallback
  width, so piped output and CI logs stay machine-parseable.
- `NO_COLOR=1` forces the `no-color` theme even on a TTY.
- `KOTA_RENDERER_THEME=ascii` forces ASCII icons for terminals that do
  not render the default Unicode glyphs.
- `KOTA_RENDERER_THEME=no-color` forces the `no-color` theme.

Themes are declarative mappings from semantic role and status kind to
ANSI SGR codes, icons, and label strings. Add a theme by filling in the
same shape; never branch on theme name at a call site.

## Pure Renderer

`render(node, ctx)` is pure. It takes a node plus a `RenderContext`
(theme, width, indent) and returns the exact string the transport would
write. Unit tests assert the rendered tree without touching a real TTY,
and surfaces that still depend on string return values continue to work
while migration is in flight.

Animation lives in the transport, not in render-tree primitives. The
spinner primitive's pure render emits a single static frame so non-TTY
consumers (CI logs, piped output) stay machine-parseable; the
transport's `startSpinner` owns the redraw loop and final-frame
finalize for an interactive TTY.

## Migration Pattern

When migrating a surface:

1. Build a `RenderNode` from the surface's typed data with a pure
   `buildXNode(...)` helper whose only inputs are domain values and
   whose only output is a node. Tabular surfaces return a `ColumnsNode`
   with explicit `ColumnSpec[]`; nested or hierarchical surfaces return
   a `GroupNode` whose body is a recursive node; section blocks return
   a `StackNode` with `sectionRule`/`group` children.
2. Surface the node through `print` for CLI entry points, or through
   `renderToString` when another string consumer reads the result.
3. Delete any local padding, ANSI, or width code the surface no longer
   needs. Do not keep both paths — drop the old `buildXLines` /
   `LineNode[]` shape in the same change.
4. Tests assert via `renderToString` against the typed node, not by
   capturing stdout or asserting line-array shape. Assert the surface
   wording and a narrow-width case when its column choices can lose content.
   Theme and ANSI behavior belongs to the rendering owner tests; do not
   repeat a theme matrix for every surface.
5. Columns whose text can run long (`Title`, `summary`, `path`,
   `Description`) declare a `maxWidth` so they truncate cleanly under a
   narrow terminal instead of overflowing. Role-aware coloring stays
   on the cell `TextSpan`'s `role` (or the `ColumnSpec.role` fallback);
   no surface paints ANSI directly.
6. Machine-parseable output paths (JSON, JSONL, bare-id stdout) stay
   on their existing typed I/O — the migration is for human-facing
   rendered output only.

Do not introduce a second rendering DSL, a parallel theme object, or a
per-surface color palette. All of those go here.
