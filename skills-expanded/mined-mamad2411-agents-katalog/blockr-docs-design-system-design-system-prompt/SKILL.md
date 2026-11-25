# blockr design-system brief (paste-ready)

Use this as the full context when prompting claude.ai/design (or any artifact-style UI generator) to produce a UI fragment that looks native inside a blockr dashboard. Paste the whole file, then add a one-line description of what to build.

---

## What blockr is

A Shiny-based dashboard toolkit where each "block" is a small, self-contained UI+logic unit (filter, mutate, plot, etc.) composed into a workspace. Blocks are dense, inline-editable, and must render correctly at widths from ~300px (narrow sidebar) to full-screen. UI is **hand-rolled** — no Bootstrap cards, no Tom Select, no shadcn, no Material, no utility-class frameworks. Plain HTML + CSS + vanilla JS.

## Color tokens

CSS variables, Tailwind-aligned greyscale plus a small semantic palette.

| Variable | Hex | Use |
|---|---|---|
| `--blockr-grey-50` | `#f9fafb` | input backgrounds, subtle fills |
| `--blockr-grey-100` | `#f3f4f6` | hover surfaces |
| `--blockr-grey-200` | `#e5e7eb` | borders |
| `--blockr-grey-300` | `#d1d5db` | dividers |
| `--blockr-grey-400` | `#9ca3af` | placeholders, meta text |
| `--blockr-grey-500` | `#6b7280` | labels, secondary text |
| `--blockr-grey-700` | `#374151` | headings in muted context |
| `--blockr-grey-900` | `#111827` | primary text |
| `--blockr-color-text-primary` | `#111827` | main body text |
| `--blockr-color-text-secondary` | `#374151` | de-emphasised text |
| `--blockr-color-text-muted` | `#6b7280` | labels, descriptions |
| `--blockr-color-text-subtle` | `#9ca3af` | placeholders, meta, muted icons |
| `--blockr-color-border` | `#e5e7eb` | all borders |
| `--blockr-color-bg-input` | `#f9fafb` | input / row backgrounds |
| `--blockr-color-bg-hover` | `#f3f4f6` | hover background |
| `--blockr-color-primary` | `#2563eb` | focus rings, active states |
| `--blockr-color-danger` | `#dc2626` | destructive hover (row remove) |
| `--blockr-color-error` | `#dc2626` | validation error text |
| `--blockr-color-warning` | `#f59e0b` | required-empty field border |
| `--blockr-color-warning-bg` | `#fffbeb` | required-empty field background |
| `--blockr-blue-50` | `#eff6ff` | tinted primary background |

Always declare literal fallbacks so components render standalone: `color: var(--blockr-color-text-primary, #111827)`.

## Typography

- **UI text inherits the page font** — never hardcode `font-family` on containers. Use `font: inherit` on form controls.
- **Code input fields** use `'SF Mono', 'Fira Code', 'Consolas', 'Monaco', monospace`.

Sizes:

| Variable | Size | Use |
|---|---|---|
| `--blockr-font-size-base` | `0.875rem` (14px) | body, inputs, select values |
| `--blockr-font-size-sm` | `0.8125rem` (13px) | labels, helper text, options |
| `--blockr-font-size-xs` | `0.75rem` (12px) | meta tags, subtitles, badges |

Weights: `500` (medium) for labels, `600` (semibold) for emphasised / confirmed states. No bold headings inside blocks.

## Heights

| Height | Use |
|---|---|
| **42px** | standalone inputs, bordered selects — universal "input" height |
| **30px** | nested inputs inside rows, number inputs, add-row bar |
| **26px** | icon buttons (gear, remove) |
| **24px** | pill toggles, confirm buttons |

## Border radius

| Radius | Use |
|---|---|
| **8px** | inputs, rows, dropdowns, settings bands |
| **6px** | internal card sub-sections |
| **4px** | pills, small buttons |

## Spacing + interaction

- Row padding: 5px vertical.
- Flex gap between fields: 6–12px.
- Dropdown shadow: `0 4px 12px rgba(0, 0, 0, 0.1)`.
- Focus ring (all focusable elements, no exceptions):
  ```css
  border-color: var(--blockr-color-primary, #2563eb);
  box-shadow: var(--blockr-focus-ring, 0 0 0 3px rgba(37, 99, 235, 0.12));
  ```
- Hover transitions: `0.15s ease`. No other motion.
- Destructive controls (row remove): `opacity: 0` at rest, revealed on row hover, turn `--blockr-color-danger` on button hover.

## Responsive layout — flex-wrap, NOT media queries

Block width is unknown at author time and changes at runtime. **Do not use `@media` or `@container` queries** inside blocks. Use a wrapping flex row where each field claims an equal share above a soft minimum, then wraps:

```css
.xxb-grid  { display: flex; flex-wrap: wrap; align-items: flex-end; gap: 6px 12px; }
.xxb-field { flex: 1 1 160px; min-width: 0; display: flex; flex-direction: column; }
.xxb-field--full { flex: 1 1 100%; }
```

Rules:
- `flex: 1 1 160px` — fields grow equally, shrink to the ~160px soft minimum, then wrap. Tune basis per field (short labels ~120px, long inputs 200px+).
- `min-width: 0` is **mandatory** on flex children holding overflowing content — otherwise intrinsic width prevents shrinking.
- `align-items: flex-end` keeps inputs bottom-aligned when some labels wrap to two lines.

## Naming — BEM + short prefix

**Shared primitives** use BEM with the `blockr-` prefix (reserved): `.blockr-select`, `.blockr-input`, `.blockr-row`, `.blockr-pill`, `.blockr-checkbox`, `.blockr-settings`, `.blockr-gear-btn`, `.blockr-add-row`. Elements use `__`, modifiers use `--`:

```
.blockr-select
.blockr-select__control
.blockr-select--bordered
.blockr-select__option--highlighted
```

**Block-specific** classes use a short letter prefix (initials of block + `b-`): `.fb-` (filter), `.mb-` (mutate), `.plb-` (pivot-longer), `.stb-` (summary-table), etc. One-off structure inside a single block goes under the block prefix; shared layout primitives used by 3+ blocks move up to `blockr-*`.

## Component primitives (expected classes)

- `.blockr-select` — single or multi select, transparent by default (inherits a 30px row slot); add `--bordered` for the 42px standalone size. Options may carry a secondary `.blockr-select__opt-label` at grey-500 / 13px with 8px left margin (ellipsizes on overflow).
- `.blockr-input` — code/expression input with autocomplete popup, monospace font, 42px standalone height.
- `.blockr-row` — horizontal stack of fields (filter condition, mutate expression, etc.), 30px tall, grey-50 background, 8px radius, optional trailing remove button that appears on row hover.
- `.blockr-pill` — 24px tall, 4px radius, small toggle or tag. Only where the label *is* the value (AND/OR, asc/desc); `.blockr-pill--active` marks the current one.
- `.blockr-checkbox` — plain on/off data option. 16px box, 4px radius, primary fill when checked, 13px label, 26px hit area, native `<input>` underneath. Use this, not a self-labelling on/off pill.
- `.blockr-settings` — the block's settings band. Full-width, **in flow** (no absolute positioning, no portal, no z-index), opens between the gear header and the block content and pushes the content down. `flex-wrap` container, fields at `flex: 1 1 190px; min-width: 0`. There is no floating settings popover — do not generate one.
- `.blockr-add-row` — full-width 30px ghost button under a list of rows (`+ Add …`).

## Overall feel

Dense, quiet, editor-like. No drop shadows except the dropdown one above. No gradients. No card chrome around blocks — blocks live directly on the workspace background. No icons larger than 16px. No ornamental dividers; use `--blockr-grey-200` 1px borders only where structure demands it. Copy is terse (imperative verbs, no punctuation at line ends for labels).

## Anti-patterns — do NOT

- Do not use Tom Select, Selectize, Choices.js, react-select, shadcn, Radix, Material, or any component library.
- Do not use Tailwind utility classes in the output; write real CSS with the variables above.
- Do not introduce new color values outside this palette.
- Do not use media / container queries inside a block.
- Do not hardcode a UI font family. Do hardcode the mono stack for code fields.
- Do not put form controls in a floating panel. Settings open in flow, as a band.
- Do not use emojis in UI copy.
