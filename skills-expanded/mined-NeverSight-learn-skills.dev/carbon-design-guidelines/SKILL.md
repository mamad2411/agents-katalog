---
name: carbon-design-guidelines
description: "Guides, references, and tooling for building React UIs with IBM's Carbon Design System (`@carbon/react` v11). Covers design foundations (grid, color, spacing, typography, theming, motion, accessibility), component usage with code samples, design patterns (forms, dialogs, notifications, loading, empty states), and data visualization with `@carbon/charts-react`. Includes an icon/pictogram search CLI. Also use when the user asks for UI that should follow IBM's visual language, even without mentioning Carbon by name."
---

# Carbon Design System

Build React UIs with `@carbon/react` v11. Carbon v11 APIs differ significantly from older versions — do not rely on your own memory of Carbon APIs. Read the files in this skill carefully and patiently before writing code.

This skill contains many documentation files. Use parallel tool calls to read multiple files at once (e.g., read 3-4 foundation or component files in a single message) — this is much more efficient than reading them one by one.

## How to use this skill

For any Carbon-related question, check this skill's files first — foundations, components, patterns, and data-visualization docs are your primary source. Only fall back to reading `@carbon/react` source in `node_modules/` when the skill docs don't answer your specific question. Do not skip the skill docs and go straight to source code or rely on your training data.

Carbon's rules are interdependent — grid mode affects component alignment, theme choice propagates through layers, spacing tokens only exist in SCSS, and accessibility defaults depend on correct prop wiring. Skipping any of these causes rework. Unless you are explicitly instructed to work as fast as possible, follow this workflow: first read the relevant foundations to update your understanding of Carbon's design language, then think about how to design the interface and which components to use, then read the documentation for those components, and only write code after the design is clear. Do not read a few files and start coding immediately.

When the user introduces a new sub-task (e.g. "add dark mode", "add a notification system", "add search"), re-check the Building common UI tasks table for that specific sub-task. Don't assume earlier foundation reads cover it.

Conventions (below) apply to every task — read them first.

Building common UI tasks maps common page types to the foundations, patterns, and components you need. Find your task, then read everything listed in that row before writing code. If your task spans multiple rows, combine the entries. Do not rely on your memory of Carbon APIs — Carbon v11 has significant differences from older versions, and skipping the listed documents causes wrong gutter modes, broken theme wiring, incorrect component choices, and missing accessibility requirements.

Foundations teach the design language: grid, theming, color, spacing, typography. Components teach individual building blocks with usage guidance and code samples. Patterns teach how to compose multiple components for common tasks (forms, dialogs, loading, empty states). Data visualization covers `@carbon/charts-react` — chart types, color palettes, axis rules, legend interaction, and dashboard composition. All four are referenced from the task table — read foundations first, then patterns, then components (and data-visualization when charts are involved).

For new projects, also read `foundations/decisions.md` for key setup decisions (theme, dark mode, grid mode, shell variant). Unless you are explicitly told to complete the task without asking, pause and ask the user for their preferences on these decisions.

After writing code, if your prompt and tooling allow, verify the result. If you have access to a browser tool, use it to visually confirm the page renders correctly — layout, spacing, theming, and component states are much easier to catch visually than by reading code alone. When you run into issues (wrong styling, unexpected behavior, missing props), read the `@carbon/react` source code in `node_modules/` — the component's `.tsx` and `.js` files are the definitive reference.

If you have the ability to spawn subagents and your prompt allows it, use them to help brainstorm interface design — explore different layout approaches, discuss component choices, and compare alternatives before committing to an implementation. Make sure to instruct subagents to read this skill's files so they work from accurate Carbon documentation rather than outdated training data. You can also use subagents to review your finished implementation: have them check your code against the relevant foundation, pattern, and component docs to catch misused props, wrong grid modes, or missing accessibility requirements.

## Bundled scripts

This skill includes a search CLI for the icon and pictogram catalogs at `scripts/carbon-assets-search.mjs` inside this skill's directory. Use it to find icons/pictograms by keyword instead of guessing import names.

```
node <this-skill-directory>/scripts/carbon-assets-search.mjs icon search <keyword>
node <this-skill-directory>/scripts/carbon-assets-search.mjs pictogram search <keyword>
node <this-skill-directory>/scripts/carbon-assets-search.mjs icon category <name>
node <this-skill-directory>/scripts/carbon-assets-search.mjs pictogram category <name>
```

Replace `<this-skill-directory>` with the base directory path shown when this skill was loaded. The script is self-contained — it does not depend on the project's node_modules. Run with `--help` to see all subcommands, output format, and usage details.

## Conventions

- Imports: `@carbon/react`, `@carbon/react/icons`, `@carbon/pictograms-react`. NEVER `carbon-components-react` (deprecated).
- Component-first; tokens are an escape hatch. Use `<Stack gap={5}>` over manual padding, `<Layer>` over manual background, `<Theme theme="g100">` over color mapping. Carbon components ship correct colors / spacing / typography baked in.
- When raw tokens are unavoidable: write SCSS, not JSX inline styles. In `.scss` files use SCSS variables (`$spacing-05`, `$layer`, `$text-primary`, `$duration-fast-01`). In JSX inline styles, only color tokens are CSS custom properties — `var(--cds-text-primary)` works (theme-aware), but `var(--cds-spacing-05)` / `var(--cds-duration-*)` / `var(--cds-heading-*)` / `var(--cds-breakpoint-*)` do NOT exist.
- Themes: 4 default — `white` / `g10` (light); `g90` / `g100` (dark). Apply via `<Theme theme="g100">` for runtime, or `with($theme: $g100)` SCSS for compile-time.
- Accessibility: Carbon wires keyboard, focus, ARIA. Your job: supply correct text (labels, descriptions); don't override defaults.
- Per-component constraints / footguns: read the component's `index.md` before writing code.
- Finding an icon or pictogram by purpose: the catalog has ~1300 icons / ~1500 pictograms — don't guess, use the search CLI described in ## Bundled scripts above.
- Reading the referenced images: if you have image-reading capability, open the referenced images alongside the text. Anatomy callouts, do/don't pairs, layout schematics, and spec diagrams carry decision content the text only summarises. Read them when the section involves visual judgment (anatomy / layout / variants / do-don't / style states).

## Building common UI tasks

Match your task to a row below, then read every foundation, pattern, and component listed in that row. If your task spans multiple rows (e.g. a page with both a form and a list), combine the entries.

TASK | FOUNDATIONS | PATTERNS | KEY COMPONENTS
list page — browse / sort / filter / select records | `2x-grid` · `themes` | `filtering` · `search-pattern` · `empty-states-pattern` · `loading-pattern` | DataTable · Pagination · Search · Tag · Button · Modal
form page — collect input in modal or full route | `2x-grid` · `content` | `forms-pattern` · `dialog-pattern` | Modal · Form · TextInput · Select · Checkbox · RadioButton · Button · InlineLoading
dashboard — multiple widgets, each with own state | `2x-grid` · `themes` | `empty-states-pattern` · `loading-pattern` · `status-indicator-pattern` · `notification-pattern` | Tile · DataTable · Loading · Tag · ProgressBar
dashboard with charts — data visualization widgets | `2x-grid` · `themes` | `empty-states-pattern` · `loading-pattern` | Tile · DataTable · Loading — also read `data-visualization/` (separate package `@carbon/charts-react`)
login / signup screen | `content` · `typography` | `login-pattern` · `forms-pattern` · `notification-pattern` | TextInput · PasswordInput · Button · Notification · Link
settings page | `content` · `accessibility` | `forms-pattern` · `disabled-states` · `read-only-states-pattern` | Toggle · Checkbox · Select · Form · Tile
wizard / multi-step flow | `2x-grid` · `content` | `forms-pattern` · `loading-pattern` · `dialog-pattern` | ProgressIndicator · Form · Button · Modal · InlineLoading
detail view — entity header + tabbed sub-content | `2x-grid` · `typography` | `disclosures-pattern` · `overflow-content` · `status-indicator-pattern` | Breadcrumb · Tabs · Tag · Modal · Button · OverflowMenu
search results | `2x-grid` · `content` | `search-pattern` · `filtering` · `empty-states-pattern` · `loading-pattern` | Search · ExpandableSearch · DataTable · List · Tag · Pagination
first-time / empty workspace (onboarding) | `content` · `typography` | `empty-states-pattern` · `dialog-pattern` | Tile · Button · Link · Modal
app shell — global product chrome + nav | `2x-grid` · `themes` · `accessibility` | `global-header` · `overflow-content` | UIShell · OverflowMenu · IconButton · Theme
theme switching / dark mode | `themes` · `decisions` | — | Theme · GlobalTheme

## Foundations

Design language primitives (grid, color, spacing, typography, theming, etc.). Read the ones listed in your task's row in ## Building common UI tasks above.

`decisions.md` — read before starting a new project. Key setup decisions (theme, dark mode, grid mode, shell variant) with recommended defaults.
`2x-grid/` — read before writing any `<Grid>` / `<Column>` layout. Gutter mode choice (wide / narrow / condensed) affects every component's alignment. Five breakpoints, page-level layout patterns.
`color/` — read when applying color outside a Carbon component (custom borders, backgrounds, status colors). Tokens are role-based (`$text-primary`, not `#161616`); this file teaches which role to pick.
`spacing/` — read when adding margin / padding / gap outside of `<Stack>`. The spacing scale is `$spacing-01` through `$spacing-13` (SCSS-only, no CSS custom properties).
`typography/` — read when setting type styles outside Carbon components. IBM Plex type sets (productive / expressive), utility classes (`cds--type-*`).
`motion/` — read when adding animation or transition. Carbon has standard easing curves and duration tokens; don't invent custom ones.
`themes/` — read when setting up app-level theming, creating light/dark regions, or nesting surfaces. Covers `<Theme>`, `<GlobalTheme>`, `<Layer>`, and the layer model.
`icons/` — read when choosing or placing an icon. ~1300 icons, 4 sizes (16/20/24/32), outlined vs filled. Search CLI: `node scripts/carbon-assets-search.mjs icon search <keyword>`.
`pictograms/` — read when using large illustrative graphics (empty states, hero sections). ~1500 pictograms, min 48px. NOT for UI affordances (use icons).
`accessibility/` — read when wiring ARIA labels, keyboard nav, or checking contrast. Carbon handles most a11y automatically; this covers what YOU must supply.
`content/` — read when writing UI copy (button labels, headings, error messages). Sentence case, action verbs, the common-actions verb glossary.
`carbon-for-ai/` — read when building AI-powered features. AILabel decorator, AI presence styling, revert / explain patterns.

## Components

Each entry below helps you pick the right component. Open `components/<Name>/index.md` for usage details, design guidance, code samples, and props source pointers.

### Actions

`Button/` — trigger an action. Variants: primary / secondary / tertiary / ghost / danger. One primary per screen (header / modal / side panel exempt). NOT for navigation → Link. Inline loading: SWAP submit Button with `<InlineLoading>` (Button has no `loadingStatus`).

`MenuButtons/` — `MenuButton` opens a Menu of 4+ peer-importance actions (primary / tertiary / ghost). `ComboButton` is primary action + caret with related secondaries (primary kind only; `onClick` fires on the primary, not the caret).

`OverflowMenu/` — `...` icon trigger for 2-6 flat actions in a row / card / toolbar. v12 rewrite (selectable, submenus, icons-in-rows) behind `enable-v12-overflowmenu`; `OverflowMenuV2` is a deprecated shim.

`Menu/` — low-level menu primitive. Reach for it only for context menus or non-standard triggers (MenuButton / ComboButton / OverflowMenuV2 are built on it).

`IconButton` — icon-only Button with built-in Tooltip. Common: `kind` ('primary' / 'secondary' / 'ghost' / 'tertiary'), `size` ('sm' / 'md' / 'lg'), `label` REQUIRED (accessible name + tooltip text), `align` (12 positions like 'top-start'), `isSelected`, `enterDelayMs` / `leaveDelayMs`. Use over deprecated `<Button hasIconOnly>`.

`ButtonSet` — horizontal Button group with correct spacing + responsive stack. Common: `stacked`.

`DangerButton` / `PrimaryButton` / `SecondaryButton` — DEPRECATED aliases; use `<Button kind="danger" / "primary" / "secondary">`.

### Navigation

`Link/` — navigate to URL / route / anchor / mailto / tel. Inline (underline) or standalone. NOT for actions / state → Button. Ghost Button shares link color but has Button SEMANTICS — don't substitute.

`Breadcrumb/` — hierarchical location with backward navigation across 2+ levels. NOT primary nav. Truncation: nest `<OverflowMenu>` between BreadcrumbItems.

`Tabs/` — peer-level content switching within a single page. `Tabs` + `TabList` + `TabPanels` + `TabPanel`. NOT for wizards → ProgressIndicator. NOT for primary nav → UIShell. Old `<Tab label="X">` removed; use `<Tab>children</Tab>`.

`ContentSwitcher/` — toggle 2-3 alternate views of the SAME content (grid/list, all/read/unread). `selectionMode` `automatic` (arrow selects) vs `manual` (arrow only focuses) is visually indistinguishable.

`Pagination/` — page-size + range readout + next/prev for table-style data; 1-indexed. `PaginationNav` is numeric page buttons for content (galleries, articles); 0-indexed. `totalItems` means rows for Pagination, pages for PaginationNav.

`UIShell/` — persistent product chrome. Three surfaces:
- Header (`header.md`) — 48px top chrome. Always wrap in `HeaderContainer` (render-prop supplies `isSideNavExpanded` + `onClickSideNavExpand`; installs Esc-to-collapse).
- Side nav (`left-panel.md`) — `SideNav` for secondary nav, up to 2 tiers. Variants: fixed (always visible), rail (icons + hover-expand), hosted (default; hidden until hamburger).
- Right panel (`right-panel.md`) — `HeaderPanel` flyouts for notifications / account / app switcher (`Switcher` + `SwitcherItem`).
- `SkipToContent` MUST be first focusable child of `Header`; its `href` must match `<Content>` `id` (default `main-content`).
- Carbon does NOT detect current route — set `isActive` / `aria-current` from your router.

### Form input

`TextInput/` — single-line text. NOT for selection from finite set → Dropdown / Select / RadioButton. NOT for steppered numbers → NumberInput.

`NumberInput/` — narrow-range numeric with stepper buttons; user typically nudges ±1-10. NOT for wide ranges → Slider. NOT for free-form numeric strings (IDs, phones) → TextInput.

`Slider/` — wide-range continuous value where visual position matters (~20+ values). `onChange` fires per drag tick (16ms throttle); `onRelease` fires once after release — use `onRelease` for expensive operations.

`Search/` — find-within-content input with clear button. `ExpandableSearch` collapses to magnifier for tight toolbars / shell headers. NOT for form-field input → TextInput.

`DatePicker/` — date selection on Flatpickr. `datePickerType="simple"` (no calendar), `"single"` (1 input), `"range"` (REQUIRES exactly 2 `DatePickerInput` children in start-then-end order). `value` lives on DatePicker, not Input. `appendTo` essential inside Modals / portals. `locale` is Flatpickr codes, not browser Intl.

`Checkbox/` — binary or multi-select within a form. Wrap with `CheckboxGroup`. Indeterminate is `aria-checked="mixed"` (NOT `checked={null}`); Carbon doesn't auto-compute parent state. NOT for mutually exclusive → RadioButton. NOT for instant settings → Toggle.

`RadioButton/` — mutually exclusive selection. Wrap with `RadioButtonGroup`. NOT for binary on/off → Toggle. NOT for >7 options → Dropdown.

`Toggle/` — instant binary switch that auto-commits (settings, dark mode). Tie-breaker vs Checkbox: if downstream Save → Checkbox; if instant → Toggle.

`Dropdown/` — pick exactly ONE from a predefined list with per-option JSX / icons. `ComboBox` for free-text or long / async lists with autocomplete. `MultiSelect` for many selections (per-option checkboxes + select-all + counter tag). Use `Select` instead for form-submission fields, mobile, or zero-styling needs. NOT for 2 options → RadioButton.

`Select/` — native `<select>` wrapper. `Select` + `SelectItem` + `SelectItemGroup`. Mobile-friendly, no custom item rendering. NOT for <3 options → RadioButton. NOT for actions / filtering → Dropdown.

`FileUploader/` — file input. Three composition levels:
- `FileUploader` (composite): simple, Carbon manages list, no drag-drop, global `filenameStatus`.
- `FileUploaderButton`: button + hidden input; you render the list.
- `FileUploaderDropContainer` + `FileUploaderItem`: drag-drop + per-row mixed states.
- `filenameStatus` state machine is AGENT-DRIVEN. `uuid` on item is load-bearing — filenames aren't unique.

`Form/` — thin `<form>` wrapper. Real work is `FluidForm` (FormContext.isFluid=true triggers all `Fluid*` input variants — flush-to-edges for tearsheets / DataTable inline edit / side panels). `FormGroup` bundles related inputs under a shared `<legend>`. → `patterns/fluid-styles/index.md`.

`ComboBox` — Dropdown + free-text autocomplete. Adds `allowCustomValue`, `shouldFilterItem`. Use over Dropdown for long / async lists.

`MultiSelect` + `FilterableMultiSelect` — multi-pick Dropdown variants. Adds `selectionFeedback` ('top' / 'fixed' / 'top-after-reopen'), `clearSelectionLabel`. Filterable adds search input.

`TextArea` — multi-line TextInput. Same `labelText` / `helperText` / `invalid` API; adds `rows`, `maxCount`, `enableCounter`.

`PasswordInput` — TextInput with show/hide toggle. Adds `hidePasswordLabel`, `showPasswordLabel`, `tooltipPosition`. Lives in `TextInput/PasswordInput`, not its own folder.

`TimePicker` + `TimePickerSelect` — text input + AM/PM + timezone selectors. Composition similar to DatePicker.

### Containers and lists

`DataTable/` — full-featured table (sort / filter / select / expand / batch / pagination / inline edit). Render-prop API. `getXxxProps` returns MUST be spread on the matching component (`getRowProps={...}` on TableRow, `getSelectionProps()` on TableSelectAll, `getSelectionProps({row})` on TableSelectRow). Row `id` is load-bearing for state, expansion, React keys. Use plain `Table` (no DataTable wrapper) for read-only static tables. `TableSlugRow` / `TableHeader.slug` deprecated → `TableDecoratorRow` / `decorator`.

`StructuredList/` — read-only labeled rows OR single-select pickers (StructuredListInput renders `<input type="radio">`). Min-width 500px. `aria-label` on StructuredListInput is REQUIRED — Carbon does NOT auto-wire `aria-labelledby`. NOT for narrow panels → ContainedList.

`ContainedList/` — compact labeled list for cards / sidebars / popovers. `kind="on-page"` (default; honors `size`) or `"disclosed"` (overrides `size` with fixed 32/48 dims). Supports per-row action slots, clickable rows, search/filter integration.

`List/` — `OrderedList` / `UnorderedList` / `ListItem` for prose-style markers. `nested` MUST be set manually on the inner list (Carbon doesn't auto-detect). `isExpressive` doesn't cascade. NOT for tabular data → DataTable / StructuredList / ContainedList.

`TreeView/` — hierarchical data nav, arbitrary depth. `selected` (array, drives `aria-selected`) vs `active` (single id, drives `aria-current`) are distinct. `depth` auto-computes via DepthContext. NOT for one-level disclosure → Accordion. NOT for primary nav → UIShell.

`Accordion/` — flat list of collapsible sections. `align="start"` puts chevron on left; `isFlush` silently ignored when align=start. `onHeadingClick` signature is `({ isOpen, event })` (object, not `(event, ...)`). `renderExpando` deprecated → `renderToggle`. NOT for ≥3-level hierarchy → TreeView.

`Tile/` — selectable / expandable / clickable container surfaces. (Folder pre-existed; details in `index.md`.)

### Disclosure / overlay

`Modal/` — overlay that interrupts the workflow. Variants: passive / transactional / danger / acknowledgment / progress. Pass `primaryButtonText` / `secondaryButtonText` / `secondaryButtons` — don't hand-roll the footer. Set `danger` for irreversible actions; Carbon focuses Cancel on open. `preventCloseOnClickOutside` enforced when `passiveModal=false`. Composable parts (ModalHeader / ModalBody / ModalFooter) live in `ComposedModal/` (later batch).

`Popover/` — low-level floating surface. Tooltip / Toggletip / Dropdown / OverflowMenu are built on it. Reach for it only when those don't fit. `onRequestClose` does NOT fire on Esc — wire `onKeyDown` manually.

`Tooltip/` — brief non-interactive text on hover / focus. `DefinitionTooltip` for inline term definitions. Most Carbon components (IconButton, CopyButton) ALREADY render their own tooltip via `iconDescription` — don't wrap them. CANNOT contain interactive elements (links, buttons) → Toggletip.

`Toggletip/` — click / Enter triggered popover that CAN contain interactive elements. Has NO controlled `open` / `onClose` (only `defaultOpen`). For controlled, drop to Popover directly.

`ComposedModal` + `ModalHeader` + `ModalBody` + `ModalFooter` — structural Modal alternative when Modal's convenience props don't fit (custom footer layouts, scrollable body with fixed header). Same `open` / `onClose` API; you compose the pieces.

### Status, feedback, progress

`Notification/` — system-state messaging. Variants:
- `InlineNotification` — persistent feedback in flow / form.
- `ToastNotification` — short-lived time-based event (top-right; mirror to notification center).
- `ActionableNotification` — needs one follow-up; use `inline={true}` inside forms.
- `Callout` — pre-action context loaded with the page; NOT screen-reader-announced. Restricted to `kind="info"` / `"warning"`.
- `StaticNotification` deprecated → Callout.
- NOT for blocking decisions → Modal. NOT for interactive content in Inline / Toast → Actionable.

`Tag/` — categorize / label / filter. Four interactive variants:
- Read-only Tag — passive label.
- DismissibleTag — user-removable filter chips.
- SelectableTag — toggled selection chip (no `type` prop).
- OperationalTag — clickable; reveals overflow / detail (rejects `type="high-contrast"` / `"outline"`).
- NOT for navigation. NOT for high-severity status → Notification.

`AILabel/` — system-wide "AI is present" affordance. Pass via host component's `decorator` prop (Tag / Modal / Tile / TextInput / Dropdown / DataTable / etc.). Replaces deprecated `slug`. Each host coerces size/kind: Tag → sm+inline; Modal → sm; CheckboxGroup → mini+default; TextInput / Dropdown / NumberInput → mini. NOT for AI ACTIONS (e.g., "Regenerate") → IconButton.

`Loading/` — full-screen / container indeterminate spinner with optional blocking overlay. Default `aria-live="assertive"` (interrupts reader); `active=false` doesn't remove overlay — UNMOUNT to dismiss. NOT for known layouts → Skeleton. NOT for button-level → InlineLoading. NOT for determinate progress → ProgressBar.

`InlineLoading/` — small spinner + label transitioning `inactive` → `active` → `finished` → `error`. Canonical pattern: SWAP submit Button with `<InlineLoading>` (NOT child of Button); manually disable paired Cancel.

`ProgressBar/` — single operation with known 0-100% value. Indeterminate detection: omit `value` while `status="active"` (no boolean prop). `status` `finished` / `error` overrides any `value`. NOT for multi-step → ProgressIndicator. NOT for sub-5s waits → Loading.

`ProgressIndicator/` — linear multi-step wizard (≥3 steps). `ProgressIndicator` + `ProgressStep` + `currentIndex`. Step state precedence: disabled > invalid > complete (`index<currentIndex`) > current (`index===currentIndex`) > pending. NOT for any-order steps → Tabs.

### Code presentation

`CodeSnippet/` — read-only copyable code. `type="single"` (one-line), `"multi"` (collapse-to-N-rows), `"inline"` (in-prose pill). Show-more silently hides when `maxExpandedNumberOfRows ≤ maxCollapsedNumberOfRows`. v11 has no `copyLabel` — use `aria-label`. NOT when user must edit.

### Layout

`Stack` — vertical (default) or horizontal container with consistent gap. Common: `gap` (1-12, maps to `$spacing-*`), `orientation` ('vertical' / 'horizontal'), `as`. Use over manual margin / padding.
`Grid` + `Column` — 16-col (4 below `md`) responsive grid. Grid: `narrow` (gutter 16/0), `condensed` (gutter 1px), `fullWidth`, `as`. Column: `sm` / `md` / `lg` / `xl` / `max` (each `number | { span, offset, start, end }` or bool), plus shorthand `span` / `offset`. → details: `foundations/2x-grid/index.md`.
`FlexGrid` + `Row` + `Column` — older flexbox grid; same Column API. Prefer `Grid` (CSS Grid) for new work.
`Layer` — wraps children to bump their `$layer` token to next level (max 3). Common: `level` (0/1/2; auto-increments), `as`. Use over manual `background` color.
`AspectRatio` — locks child to ratio. Common: `ratio` ('16x9' / '9x16' / '2x1' / '1x2' / '4x3' / '3x4' / '3x2' / '2x3' / '1x1'), `as`.
`Theme` + `GlobalTheme` — wraps subtree in a theme; cascades CSS variables. Common: `theme` ('white' / 'g10' / 'g90' / 'g100'). Use over manual color mapping.
`HideAtBreakpoint` — conditionally hide. Common: `at` / `until` ('sm' / 'md' / 'lg' / 'xl' / 'max').
`Heading` + `Section` — auto-leveled headings. Wrap content in `<Section>`; `<Heading>` renders `h1`...`h6` based on Section nesting depth. Pass `level` to override.

### Status indicators and skeletons

`BadgeIndicator` — small dot for new / unread / count. Common: `count`.
`IconIndicator` — icon + label. Common: `kind` ('failed' / 'incomplete' / 'in-progress' / 'pending' / 'success' / 'undefined'), `size` (16 / 20), `label` REQUIRED.
`ShapeIndicator` — solid colored shape (square / circle / hexagon) + label. Same `kind` enum as IconIndicator; `label` REQUIRED.
`SkeletonText` — line(s) of skeleton. Common: `paragraph` (bool), `lineCount`, `width`, `heading`.
`SkeletonPlaceholder` — generic block; size via `className` / CSS.
`SkeletonIcon` — sized icon-shaped block. Common: `size`.
`AISkeletonText` / `AISkeletonPlaceholder` / `AISkeletonIcon` — AI-themed skeleton variants with shimmer.

### Infrastructure and utilities

`FeatureFlags` — opt subtree into v12 component rewrites + experimental APIs. `<FeatureFlags enableV12Overflowmenu enableExperimentalFocusWrapWithoutSentinels>...</FeatureFlags>`. Flag list: `@carbon/styles/scss/_feature-flags.scss` + `@carbon/react` source `src/components/FeatureFlags/`.
`Copy` — generic copy-to-clipboard wrapper. Common: `feedback`, `feedbackTimeout`, `onClick`.
`CopyButton` — Button + Copy combined. Common: `feedback`, `iconDescription`.
`Portal` — render children into `document.body` (or `target`). Used internally by overlays.
`ErrorBoundary` + `ErrorBoundaryContext` — React error boundary with Carbon styling. Common: `fallback`.
`ClassPrefix` / `IdPrefix` — change `cds--` prefix or generated id prefix. Rare.

### Internal / advanced

`ListBox` (internal to Dropdown / ComboBox / MultiSelect), `ContextMenu` (use Menu), `Disclosure` (use Accordion), `OverflowMenuV2` (deprecated shim — use `OverflowMenu` with `enableV12Overflowmenu`), `ToggleSmall` (deprecated alias for `<Toggle size="sm">`), `Switch` / `IconSwitch` (internal to ContentSwitcher) — usually wrap in the higher-level component instead.

## Patterns

Multi-component compositions and cross-cutting design rules. Read the ones listed in your task's row in ## Building common UI tasks above.

`empty-states-pattern/` — read when a container might have no data (first-time use, no search results, errors, permissions). Teaches the layout recipe: `Tile` + typography + `Button` + optional image.
`forms-pattern/` — read when building any form. Covers validation, helper text, error states, autosave, dirty tracking, submit flow, and multi-column layout. Split into 4 sub-files.
`dialog-pattern/` — read when you need to interrupt the user's workflow. Routes between Modal / Tearsheet / SidePanel / FullScreen by interruption depth and decision weight.
`notification-pattern/` — read when showing system feedback (success, error, warning, info). Routes between Toast / Inline / Actionable / Callout / Modal by urgency and dismissibility.
`loading-pattern/` — read when showing progress during data fetches. Routes between Skeleton / InlineLoading / Loading / ProgressBar by determinacy and expected duration.
`disabled-states/` — read when deciding whether to disable, hide, or make read-only. Style and a11y rules per input type.
`read-only-states-pattern/` — read when displaying form data the user cannot edit. Exact rendering per input type (not just `disabled`).
`fluid-styles/` — read when building forms in tearsheets, side panels, or inline DataTable edit. Covers `<FluidForm>` and the 12 `Fluid*` input variants.
`disclosures-pattern/` — read when progressively revealing content. Routes between Tooltip / Toggletip / Popover / OverflowMenu / Accordion / Modal by interactivity and persistence.
`status-indicator-pattern/` — read when communicating entity status (running, failed, pending). Routes between IconIndicator / ShapeIndicator / BadgeIndicator / Tag by visual weight.
`filtering/` — read when letting users narrow a data set. Routes between Search / Dropdown / DatePicker / Tag (active-filter chips) by data type and cardinality.
`search-pattern/` — read when implementing search (global, scoped, contextual, instant). Composition of Search + ExpandableSearch + result presentation.
`overflow-content/` — read when content exceeds its container. Routes between truncation / scroll / OverflowMenu / horizontal patterns.
`global-header/` — read when composing the app shell. Wires HeaderContainer, SideNav, HeaderPanel, SkipToContent, route-driven `isActive`.
`text-toolbar-pattern/` — read when building a rich-text editing toolbar. Composition of IconButton + ContentSwitcher + Tooltip.
`login-pattern/` — read when building a login or signup screen. Layout, copy, and error handling.
`common-actions/` — read when naming buttons and menu items. Verb glossary: Add vs Create, Save vs Submit, Delete vs Remove, Cancel vs Discard, etc.

## Data visualization

Charts and dashboards with `@carbon/charts-react` — a separate package from `@carbon/react`. Install it alongside `@carbon/react` when the UI includes charts.

`data-visualization/index.md` — read first. Installation, basic usage, chart type selection table (24 chart types across 6 categories), chart anatomy reference.
`data-visualization/color-palettes.md` — read when choosing chart colors. Categorical, sequential (monochromatic + diverging), and alert palettes. Rules for gradient use.
`data-visualization/axes-and-labels.md` — read when configuring chart axes. Zero-start rules (always for bar/area, optional for line/scatter), gap handling, axis breaks, time series landmark labels.
`data-visualization/legends.md` — read when configuring chart legends. Position, hover-to-highlight (30% opacity), click-to-isolate, overflow handling, mobile hidden-legend pattern.
`data-visualization/dashboards.md` — read when composing multiple charts on one page. Presentation vs exploration dashboards, best practices (F-pattern, linked charts, consistent colors).
`data-visualization/spatial-charts.md` — read when building heat maps, tree maps, circle packs, or geospatial charts. Includes Mapbox theme URLs for the 4 Carbon themes.
`data-visualization/flow-charts.md` — read when building alluvial/sankey, network diagrams, parallel coordinates, or tree diagrams. Includes elkjs integration example.
`data-visualization/gantt-charts.md` — design guidance only. Gantt charts are not yet implemented in `@carbon/charts`.

## File conventions

`components/<Name>/` — `index.md` (landing + `## Props` with source pointers) + optional `formatting.md` / `content.md` / `variants.md` / `modifiers.md` / `accessibility.md` + `images/`.

`foundations/<name>/` — `index.md` + optional sub-files + `images/`.

`patterns/<name>/` — `index.md` (or folder with sub-files for large patterns like `forms-pattern/`) + `images/`.

Tag protocol — sub-files use `<PascalCaseTag>...</PascalCaseTag>` markers to wrap distinct sections. When a cross-reference says `→ details: formatting.md @ <ButtonGroups>`, grep the file for the literal string `<ButtonGroups>` and read from there to `</ButtonGroups>`. Example of what the tagged region looks like inside the file:

```
<ButtonGroups>
...section content...
</ButtonGroups>
```

Tables use Format A — not standard markdown. UPPERCASE headers, single-space `|`, no `|---|` separator row, no leading/trailing `|`. Example:

```
PROP | TYPE | DEFAULT
size | 'sm' | 'md' | 'lg' | 'md'
kind | 'primary' | 'secondary' | 'primary'
```

## How to read Carbon source

Source reading is a verification step, not a substitute for this skill's docs. Always read the relevant `components/<Name>/index.md` or `foundations/<topic>/index.md` first. Go to `node_modules/` only when the docs don't answer your specific prop or mixin question.

To verify props against the installed version:

PATH | CONTAINS
`node_modules/@carbon/react/lib/components/<Name>/<Name>.d.ts` | TypeScript prop types — always current with installed version
`node_modules/@carbon/react/lib/components/<Name>/<Name>.js` | Compiled JS — defaults visible in destructure (`function Foo({ kind = 'primary', ... })`); JSDoc stripped
`node_modules/@carbon/react/lib/components/<Name>/index.js` | Re-exports — enumerates ALL named exports from a folder (multi-export folders like Modal / Tag / DataTable / Tabs / Form / Notification / FileUploader / OverflowMenu)
`node_modules/@carbon/react/lib/index.d.ts` | Master export list across the whole package

The original TSX source (with JSDoc comments per prop) and Storybook stories are also available in the installed package at `node_modules/@carbon/react/src/components/<Name>/`.

Defaults are in the function destructure, NOT the type. Type says `kind?: ButtonKind`; the default `'primary'` lives in `function Button({ kind = 'primary', ... })` in the .tsx / .js. Read both type AND destructure.

Multi-export folders — start at `index.js` to enumerate folder exports, then read each export's file individually. Some exports live in unexpected places: `PasswordInput` in `TextInput/`, `RadioTile` in `Tile/`, `DismissibleTag` / `SelectableTag` / `OperationalTag` in `Tag/`, `ProgressStep` in `ProgressIndicator/`.

Polymorphic `as` prop — `Stack`, `Tile`, `Link`, `Heading`, `Section`, `Grid`, `Column`, `Layer`, `AspectRatio`, etc. accept `as: React.ElementType` to swap the underlying tag. Type narrows props via generic. Default tag varies per component (often `'div'`).
