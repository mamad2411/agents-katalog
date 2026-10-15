---
name: taste-saas
description: Build a tasty internal-tool / management-console style SaaS frontend in one shot — sidebar shell, list pages with sticky header + filter chips + server-side filters, wireless detail pages, KPI / chart dashboards, and a global Cmd+K command palette. Linear / Vercel / Notion / Stripe density depending on the archetype you pick. Use when the user is starting a SaaS console, admin dashboard, internal tool, B2B web app, analytics view, or asks for a "taste-saas" / "console" / "management UI" / "stats page". Framework-agnostic — patterns transfer to React (any router), Vue, Svelte, Solid, etc. Code samples happen to be in React for clarity. Not for marketing pages, landing pages, or storefronts (use taste-skill / impeccable / frontend-design instead).
---

# taste-saas

Build a console-style SaaS that feels deliberate from the first commit. The "tasty" feeling decomposes into three layers, picked in order on every project:

1. **Structural archetype** — pick ONE of 4 (Linear floating-card / Vercel flush-pane / Notion document / Stripe data-table). Decides sidebar bg, main wrapper, breadcrumb location, row style, card chrome.
2. **Visual style knobs** — pick values within the archetype's allowed ranges for brand hue/saturation/radius/density/shadow/type.
3. **Universal mechanics** — alignment laws, wireless tokens, DataTable bones, overlay mechanics, redundancy hunt. These apply equally to ALL archetypes.

The biggest failure mode of this skill (historical) was defaulting to Archetype A (Linear floating-card) for every prompt. **NEVER** default. If the user hasn't said which feel they want, ASK them via AskUserQuestion with the 4 archetype names.

## Reference index — read in workflow order

| Stage | Read | File |
|---|---|---|
| **Step 0 — pick the structural archetype** (decides shell + main + row + card philosophy) | 4-way comparison matrix, decision flow | `references/structural-archetypes.md` |
| Step 0a — deep dive on the chosen archetype | Full structural recipe (sidebar bg, main wrapper, row style, card chrome) per archetype | `references/archetype-a-floating-card.md` (Linear/Cron/Height) / `references/archetype-b-flush-pane.md` (Vercel/GitHub/Sentry) / `references/archetype-c-document.md` (Notion/Linen) / `references/archetype-d-data-table.md` (Stripe/Plaid/Retool) |
| **Step 1 — pick visual style knobs** (within the archetype's allowed ranges) | 8 independent knobs (brand hue/saturation/stage tint/contrast/radius/type/density/shadow). ASK USER if no hint. | `references/visual-style.md` |
| **Step 2 — write tokens** | Universal token NAMES, closed scales, focus rings, FOUT, reduced-motion. Values come from Steps 0+1. | `references/wireless-tokens.md` |
| Step 3 — build the shell | Universal alignment laws (three top rows on one baseline, cross-seam first-row, icon SLOT, cross-state invariants, measurement-as-spec) | `references/alignment-invariants.md` |
| Building a list view | DataTable `<table>` + `<colgroup>` mechanics, filters, server-side contract (universal); row visual style comes from the archetype file | `references/datatable-mechanics.md` |
| Building an entity detail page | 3 detail layouts (single col / right rail / 3-pane), activity feed, inline edit | `references/detail-pages.md` |
| Building a dashboard or time-axis view | KPI / chart primitives, timeline / gantt / calendar / log stream | `references/dashboards-and-time-axis.md` |
| Building settings/profile/members | Form layout, section anchors, dirty-state, destructive confirmation | `references/settings-pages.md` |
| Data-entry (any form shape) | 3 form shapes (inline edit / single-field-add / wizard), validation, no native `<select>` | `references/forms.md` |
| Wiring Cmd+K, modals, keyboard chords | Overlay wrapper, palette four-sections, `g+letter`, `j/k`, `?` | `references/overlays-and-keyboard.md` |
| **Sheet (slide-in panel)** — row preview vs Modal vs detail page | When to pick each, geometry, expand-to-fullscreen | `references/sheets.md` |
| Contextual menus (NOT Cmd+K) | DropdownMenu / ContextMenu / Popover / SlashCommandMenu disambiguated | `references/menus.md` |
| Multi-row operations | Selection model + action bar (replaces toolbar in-place) + destructive confirmation | `references/bulk-actions.md` |
| Notifying user of completed async events | When to toast vs banner vs inline; position; undo | `references/toast.md` |
| Empty / loading / error states | Skeletons, zero-state CTAs, error banners | `references/empty-states.md` |
| **Debugging — something looks "almost right"** | Symptom-indexed catalog | `references/debug-playbook.md` |

`check.mjs` (skill root) is a relation-based audit — run after a build: `node ~/.claude/skills/taste-saas/check.mjs <project-root>`. Checks viewport lock, x-axis alignment, sticky thead, etc. Warnings advisory, fails are real bugs.

## Stack — capabilities, not a framework

Patterns are framework-agnostic. Code samples are in React for clarity; map to your stack:

| Capability | Concrete picks |
|---|---|
| Routing with attachable metadata | React Router `handle`, TanStack Router `meta`, Next.js segment config, Vue Router `meta`, SvelteKit `+page.ts` |
| Token-based styling | Tailwind v4 (recommended), Panda CSS, vanilla CSS modules, StyleX |
| Themable accessible primitives | shadcn/ui, Park UI, Mantine, Chakra, Headless UI, raw Radix |
| Async cache (stale-while-revalidate) | TanStack Query (any framework), SWR, Apollo, urql, hand-rolled signal cache |
| Headless table state | TanStack Table or a 100-line custom reducer — UI MUST be `<table>` + `<colgroup>` |
| Imperative toast | sonner, react-hot-toast, Mantine Notifications |
| Form validation | react-hook-form + zod, TanStack Form, VeeValidate, plain controlled state for ≤3 fields |
| Icon family | lucide / Phosphor / Heroicons / Tabler — pick ONE, single stroke weight |
| Charts | Recharts, visx, Tremor, Chart.js, ECharts |
| Command palette | cmdk, ninja-keys, Mantine Spotlight |

## Non-negotiables — true regardless of stack OR archetype

These are the universal contracts:

- **Structural archetype is per-project — NEVER default.** Step 0 is `references/structural-archetypes.md`. Ask the user if no hint via AskUserQuestion with 4 options.
- **Visual style is per-project, decomposed into 8 independent knobs.** Step 1 is `references/visual-style.md`. Within the archetype's allowed ranges.
- **Wireless design**: every visible spacing/height/gap is either a CSS token or a `calc()` over tokens. Hard-coded pixels in component code is a bug. Token NAMES are universal (`--page-pl`, `--row-h`, `--brand`, etc.); VALUES per archetype + visual-style. See `references/wireless-tokens.md`.
- **No lines, no backdrop dim on overlays.** Modal/sheet/popover headers/footers separate via whitespace, not `border-b`/`border-t`. Overlay backdrops are `bg-transparent` — modal/sheet rely on shadow + border. See `references/overlays-and-keyboard.md`.
- **Stable anchor on growth.** Every overlay (modal/popover/sheet/cmdk) anchors on ONE edge and never re-centers as content grows. Modals + cmdk anchor TOP at `top: 15vh`. Growable inner content sets `height` in pixels with `transition: height` + a cap.
- **Cold-starting a new component? Read the existing peers FIRST.** Match their color/height/padding/transition tokens, file structure, ARIA model. A single mismatched backdrop or button height breaks visual coherence.
- **Three top rows on one baseline** — universal alignment law. The specific ELEMENTS differ per archetype (A's stage row vs B/D's inline top bar vs C's page title), the LAW is universal.
- **`html, body, #root { height: 100%; overflow: hidden }`** — viewport lock. Universal.
- **DataTable = real `<table>` + `<colgroup>` + `table-layout: fixed`.** Hand-rolled div+flex columns drift. Universal mechanics in `references/datatable-mechanics.md`; row visual treatment (pill/hairline/zebra) per archetype.
- **Server-side filter contract**: `?status=`, `?q=`, `?sort=field:dir`, error envelope `{ type, error: { type, message } }`. Frontend dispatches on `error.code`, NEVER `error.message.includes(...)`.
- **Stale-while-revalidate data layer**: previous data shows during refetch; dedup of in-flight; refetch on focus; mutations invalidate keys. NEVER `useEffect`+`fetch`+local state, NEVER `setInterval`.
- **Cmd+K** is global, dual-key (Cmd+K AND Ctrl+K), four sections in fixed order: Recent / Actions / Navigate / Search. Server-side `q`.
- **Redundancy is the cardinal sin**: every label appears exactly once. Breadcrumb > PageHeader > body. Pill > "Status: In Progress" label.
- **Closed scales**: heights `h-7/8/9/11/28/56/72`, type `text-xs/sm/base/lg/xl/3xl` (no half-step), icons `size-3.5` or `size-4`, lucide `stroke-width=2` always.
- **No native `<select>`.** Popover-driven picker chips everywhere. See `references/forms.md` → *Form controls — closed primitive set*.

## Order of operations — build the bones first

1. **Pick archetype** (`references/structural-archetypes.md`). Ask user if no hint.
2. **Pick visual knobs** within the archetype's range (`references/visual-style.md`).
3. **Tokens** — write `index.css` with names from `references/wireless-tokens.md`, values from step 1+2 + archetype guidance.
4. **AppShell** following the chosen `references/archetype-X.md` recipe; layout invariants from `references/alignment-invariants.md`.
5. **Sidebar** per archetype's nav style (flat / tree / labeled-sections).
6. **Breadcrumb** — derive from route metadata (location varies per archetype: stage row in A, top bar in B/D, page title in C).
7. **PageHeader slot** — portal/Teleport target above `<main>`.
8. **DataTable** — real `<table>` + `<colgroup>` per `references/datatable-mechanics.md`. Row treatment per archetype's `<td>` className recipe.
9. **Async data layer** — stale-while-revalidate.
10. **Modal wrapper + Cmd+K** — global mount, dual-key, four sections.
11. **Pages** in nav order.
12. **Server contract** — filter params, error envelope, `?sort=field:dir`.
13. **Polish** — reduced motion, focus rings, FOUT gate, keyboard chords.
14. **Audit before declaring done** — start the dev server, inject `audit-overlay.snippet.js`, call `window.__taste.run()`, screenshot, read all four drift reports. Fix anything `ok: false`. See *Visual layout audit* below.

## When something looks "almost right"

Stop and read `references/debug-playbook.md`. It's symptom-indexed — find your visible issue (cross-seam drift, sidebar collapse jitter, modal shrunk to 384px, sticky thead failing, etc.) and the catalog tells you the cause and the fix. Don't keep eyeballing — **measurement is the spec**. `getBoundingClientRect()` is faster than guessing.

## Cross-state invariants — always check

Stateful components (sidebar collapse, loading→loaded, empty→filled) need paired before/after measurement. A stable anchor (e.g. "first icon under brand row") MUST have the same `centerY` in both states. Drift = some CSS source contributes layout in one state that doesn't in the other. See `references/alignment-invariants.md` → *Cross-state invariant*.

## Visual layout audit — agent-driven, tool-agnostic

After the dev server is up, run the overlay audit BEFORE declaring done. It is a single JS snippet (`audit-overlay.snippet.js` in the skill root) — inject it into the page via whatever browser tool is available (chrome-devtool MCP, agent-browser, raw Puppeteer/Playwright, or the devtools console). The snippet paints labeled rectangles on every layout-critical element, draws dashed alignment guides through every coordinate shared by 2+ elements, and returns a JSON index with four drift reports.

**Workflow:**

1. Read the snippet:
   ```bash
   cat ~/.claude/skills/taste-saas/audit-overlay.snippet.js
   ```
2. With the dev server running, inject the snippet and call `window.__taste.run()`. Capture the JSON return value AND a screenshot of the page.
3. Read the screenshot AND the JSON. The screenshot shows the **grid skeleton** (every shared x/y, intensity = how many elements share that line) — drift shows as parallel lines where there should be one. The JSON gives you machine-readable drift reports:
   - `sidebarSlotDrift` — every sidebar icon should share one x. If `ok: false`, `hint` names the offender (usually brand/footer rows missing the inner padding wrapper that nav rows use).
   - `mainChromeLeftDrift` — chrome row left edges (toolbar, filter bar, pagination) should match.
   - `mainTextAnchorDrift` — the alignment line your eye actually sees: first text x for page title, filter chips, table thead, first cell. These must coincide; row borders aren't enough.
   - `gridComplexity` — `uniqueX > 15` or `uniqueY > 20` means ad-hoc paddings are leaking. `topXLines` ranks the skeleton lines by how many elements share them.
4. Edit the offender. Each item has `text` (60-char snippet for grep), `className`, `bbox`, `firstTextX`, and `source.file:line` from React fiber (dev build only — null in production builds; fall back to grepping `text`).
5. Re-run `window.__taste.run()`. Repeat until every `*.ok` is true.

API on `window.__taste` (stable shell, safe to re-inject):
- `run()` — paint overlay, return JSON
- `clear()` — remove overlay
- `get()` — last JSON without re-running
- `find(n)` — item by badge number
- `findText(s)` — items whose text contains `s`
- `drift()` — `{sidebarSlot, mainChromeLeft, mainTextAnchor, crossSeam}`
- `complexity()` — `gridComplexity`

This replaces "add a new alignment rule every time a bug shows up". The agent reads the screenshot + JSON, edits the file, re-audits. No new skill rules per new failure mode.
