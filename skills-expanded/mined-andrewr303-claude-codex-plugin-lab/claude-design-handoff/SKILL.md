---
name: claude-design-handoff
description: >-
  Implement designs handed off from Claude Design (claude.ai/design) into a real
  Next.js/TypeScript/React codebase with 1:1 visual fidelity AND working integration
  with live data and AI features. Use this whenever the user wants to build, implement,
  port, or "make real" a design that came from Claude Design: a handoff bundle (a folder
  whose README starts with "CODING AGENTS: READ THIS FIRST"), an exported .zip or
  standalone HTML, a set of .jsx prototype files plus a primary .html, or the user says
  things like "implement this design," "build this 1:1," "pixel-perfect," "I exported
  this from Claude Design," or "wire this design into the app." Trigger it even when the
  user only attaches a screenshot or PDF of a Claude Design mockup and asks to build it,
  and even when they describe a dashboard/report/genome/page design rather than naming
  Claude Design explicitly. Do not skip this skill in favor of eyeballing a screenshot
  and free-handing components: the failure mode it exists to prevent is exactly that.
---

# Claude Design Handoff Implementer

A bundle exported from Claude Design is a prototype, not production code. Your job is two things at once, and both are required:

1. **1:1 visual fidelity.** The built UI matches the prototype exactly: tokens, type, spacing, radii, shadows, gradients, borders, charts, motion. "Close enough" is a failure.
2. **Real integration.** The UI is wired into the actual codebase: typed data contracts, live Supabase data and AI outputs, server/client split, and the states the prototype never shows (loading, empty, partial, error). A pixel-perfect page fed by hardcoded mock data is also a failure.

The prototype ships scaffolding that looks like production but is not (Babel-in-browser, `window.X` globals, a design-only tweaks panel, duplicated token objects, fixture data). Porting that scaffolding verbatim is the single most common way these implementations go wrong. Recreate the *output*, not the prototype's internals.

This skill is the workflow. The dense material lives in `references/`; read each file when its phase tells you to. Templates live in `assets/`.

---

## Phase 0 — Detect and orient

A Claude Design handoff bundle looks like this:

```
<project-name>/
  README.md                         # starts "CODING AGENTS: READ THIS FIRST"
  project/
    <Primary Design>.html           # the file the user had open = primary target
    *.jsx                           # shared components, loaded via <script src> from the HTML
    icons/  uploads/                # SVG/PNG assets
```

The README names the **primary HTML file** (the one the user had open). That is the design to build unless the user says otherwise. If the user attached only a screenshot/PDF and no bundle, ask whether a handoff bundle exists; the source files are worth far more than an image. If they have no bundle, you can still build from the image, but flag that you are reconstructing values by eye and fidelity will be lower.

Read `README.md` first. It is the design tool's own handoff note and it is correct: read the primary file in full, follow its imports, recreate pixel-perfectly in whatever tech fits, and confirm before building if anything is ambiguous.

---

## Phase 1 — Read everything before writing anything

This is non-negotiable and it is where incomplete implementations come from. Do not skim.

1. **Read the primary HTML top to bottom.** Note: the `<head>` `:root` CSS variables, the global CSS classes (`.card`, `.btn-primary`, `.chip`, `.label`, etc.), the Google Fonts loaded, and `html { font-size: ... }` (often 14px, not 16px, which changes all rem math).
2. **Enumerate every import.** Every `<script type="text/babel" src="...jsx">` is a dependency. List them.
3. **Read every imported .jsx in full.** Each typically declares its own local token object and hangs components on `window.X`.
4. **Build two inventories** before coding:
   - **Section list:** the components composed in the root render (the `App` return), in order. For the athlete genome example that is ~18 sections (HeroBanner, NarrativeReport, RadarCompositeZone, SocialPresence, StatsZone, and so on). Every one must ship. Missing sections is the #1 fidelity gap.
   - **Component inventory:** shared primitives (Label, Chip, Bar, Card, gauges) vs section components vs charts/visualizations vs design-only scaffolding to drop.
5. **Identify what to DROP.** See `references/anatomy.md` for the full list; the recurring ones are the tweaks panel (`TweaksPanel`/`TweakSection`/`TweakSlider`/`useTweaks` and the `__activate_edit_mode` host protocol), the UMD React + Babel loaders, `ReactDOM.createRoot`, and `window.X` global registration. None of it goes to production.
6. **Locate the fixture data.** Inline arrays/objects (`ATHLETE_CAMPAIGNS`, platform stats, radar `interests`, `quality` percentages). This data is a gift: it is the de facto schema for the real data contract, and the seed for dev/empty states. Mark every fixture.

Read `references/anatomy.md` now if this is your first handoff or the bundle looks unusual.

Produce an implementation plan before coding. Copy `assets/IMPLEMENTATION_PLAN.template.md`, fill it (section list, drop-list, token reconciliation, data contract sketch, RSC/client split, state coverage, chart inventory, responsive notes, open questions), and keep it as the build checklist. For a large multi-section design in Claude Code, this plan is also the contract that lets you fan work out to subagents without drift (see Phase 3).

---

## Phase 2 — Build the shared foundation first

Do this once, before any section. It is what keeps a big design coherent and lets parallel work not collide.

**1. Reconcile tokens into one source of truth.** Tokens appear in up to three places with divergent values: the HTML `:root` vars, a `const T = {...}` object, and per-file objects (`AX`, etc.). Real example of drift: `T.bg` is `#0a0a0f` while `AX.bg` is `#08090e`. There are also ad-hoc inline hexes (`#fe9a00`, `#f0808f`) and 8-digit alpha-hex shorthands (`${c}10` means hex color + `10` alpha byte ≈ 6% opacity; `28` ≈ 16%). Extract one canonical palette from the primary HTML's `:root`/`T`. Treat per-file objects as the same palette; reconcile divergent values to the canonical and flag any difference large enough to see. Do not scatter raw hex through the components.

**2. Map tokens to the existing design system, do not reinvent it.** Discover the codebase's real Tailwind theme, CSS variables, and existing primitives before adding anything (read the actual `tailwind.config`, globals, and component files; never infer their names or paths). Reuse tokens that already match. Add new ones only for genuinely new values, named to match the existing convention. The Claude Design bundle was generated against the org design system, so most tokens should already have a home.

**3. Watch the rem trap.** If the prototype root is 14px, `1rem` there is 14px; the prototype mostly specifies explicit px anyway (`fontSize: 12`, `borderRadius: 16`). The app root is probably 16px, so Tailwind's rem-based scale will not equal the prototype. Reproduce px values directly; if you use Tailwind spacing/text utilities, verify the rendered px matches the prototype or use arbitrary px values. Do not assume `text-sm` equals the prototype's body size.

**4. Build the primitives as real components.** Translate the prototype's inline-style primitives (Card, Label, Chip, Bar, FitDot, gauges) into the codebase idiom: real component files, typed props, Tailwind classes or CSS modules per house convention. Match every visual detail (see `references/fidelity-checklist.md`): layered box-shadows (the primary button stacks four, including an inset highlight), `backdrop-filter: blur(12px)` on cards, asymmetric borders (`border-top` lighter than the rest), `font-variant-numeric: tabular-nums` on figures, custom thin scrollbars, exact gradient stops.

**5. Define the data contract from the fixtures.** Turn the marked fixtures into strict TypeScript interfaces. This is the bridge between the design and real data. See `references/data-integration.md`.

**6. Build the page shell and state scaffolding.** The container (max width, padding, vertical rhythm), the section ordering, and from the start: loading skeletons that match each section's footprint, an empty state, a partial/enriching state, and an error state. The prototype shows only the happy path; production needs all four.

---

## Phase 3 — Implement sections with fidelity

Work section by section, in render order, against the plan and `references/fidelity-checklist.md`. For each section:

- Recreate the exact layout and every primitive instance.
- Replace inline-style objects with the foundation's components and tokens.
- For charts and bespoke visuals (radar, gauges, bars, calendars, geo maps, category grids), follow `references/charts-and-motion.md`. Match geometry, color, and motion; do not substitute a generic chart that merely resembles it.
- Keep fixtures as the component's dev/Storybook default and as the empty-state shape, but type the props so real data flows in (Phase 4).

**Subagent fan-out (Claude Code, large designs).** Only after Phase 2 is committed (tokens file, primitives, data types, page shell all in the repo) should you split sections across subagents. Give each subagent: the shared foundation paths, the fidelity checklist, the exact prototype source for its section, and the rule "consume the shared primitives and tokens, do not invent new ones." Foundation-first prevents the classic multi-agent failure where every agent re-rolls its own Card and palette. Reserve a final integration pass for yourself to reconcile spacing seams and shared-state wiring.

---

## Phase 4 — Wire real data and AI

This is the half that makes it integrate. Full method in `references/data-integration.md`. The spine:

1. **Discover the live schema.** Read the actual Supabase tables, columns, and types, and any AI-output JSON shapes, from the running codebase. Never infer table or column names. Map each fixture field to its real source, and note fields the design shows that no source yet produces (those are either new columns, new AI outputs, or values to flag as not-yet-available rather than faked).
2. **Split server vs client.** Default to React Server Components for data fetching and static-after-load sections. Make a component a Client Component only for genuine interactivity (toggles, the model switcher, hover/expand, charts that need client rendering). Push interactivity to leaf components so most of the tree stays server-rendered.
3. **Fetch with types and error handling on every external call** (Supabase, AI Gateway, any fetch), per the codebase's data-access conventions. Server Actions for mutations.
4. **Stream AI-generated sections.** Genome narrative, recommendations, and similar AI outputs should stream where the UX benefits, through the codebase's existing AI Gateway setup. Long enrichment runs belong in Trigger.dev jobs that write results back to Supabase, with the UI reflecting job status (this is the partial/enriching state from Phase 2).
5. **Honor the real states.** Loading uses the skeletons; empty/partial/error are first-class. Never show fabricated metrics to fill a layout. If a real value is missing, render the empty/loading treatment, not a placeholder number presented as real.

---

## Phase 5 — Responsive pass

The prototype is desktop-first (a fixed max width such as 1440px) and gives no mobile guidance. Add it deliberately. See `references/responsive.md` for per-pattern breakpoint behavior (multi-column grids stacking, radar/charts reflowing, sticky panels becoming inline, tables scrolling, hero metrics wrapping). Pick the same breakpoints the codebase already uses. Verify on a narrow viewport, not just by resizing in your head.

---

## Phase 6 — Verify against the acceptance gate

Do not call it done until all of these pass. The full gate is in `references/fidelity-checklist.md`; the summary:

- **Visual diff.** Render the prototype (open the bundle's HTML or build it locally) and the new build side by side. Reading the source is how you build; a final pixel comparison is how you confirm. Walk every section.
- **Token audit.** No stray raw hex; all colors/spacing/radii/shadows resolve to the reconciled tokens; gradients and alpha shorthands reproduced exactly.
- **Section completeness.** Every section from the inventory is present and in order. Nothing from the drop-list leaked in (no tweaks panel, no `window.X`, no Babel loaders).
- **State coverage.** Loading, empty, partial, and error states exist and look right.
- **Data integrity.** Every displayed value traces to a real source or a typed prop; no fabricated metrics.
- **Responsive.** Renders correctly at mobile, tablet, desktop.
- **Build health.** Type-check, lint, and build pass; external calls have error handling.
- **Accessibility.** Contrast holds on the dark surfaces; interactive elements are reachable and labeled.

---

## Using an attached screenshot or PDF

The user often attaches a screenshot or PDF of the design. The bundle's source is the source of truth for *values* (exact colors, spacing, sizes); the image is a holistic reference that guards against misreading the layout from code and serves as the acceptance target for the final visual diff. Use the image to confirm overall composition and to catch anything you misread; measure from the source. If there is no bundle and only an image, reconstruct values by eye and say so plainly: fidelity will be lower and some numbers are estimates.

---

## When to ask

Infer scope from the bundle and the codebase. Ask one specific question only when something is genuinely blocking and unrecoverable from the source: which page is primary if the README is ambiguous and several look plausible, or which real data source backs a section when the codebase has more than one candidate and the choice changes the architecture. Then proceed. Do not interview.

---

## Reference map

- `references/anatomy.md` — what a handoff bundle contains, every prototype pattern, and the full drop-list of scaffolding that must not ship.
- `references/fidelity-checklist.md` — the pixel-level checklist and the Phase 6 acceptance gate.
- `references/data-integration.md` — deriving the TS contract from fixtures, Supabase/AI wiring, RSC vs client, streaming, Trigger.dev, and state coverage.
- `references/charts-and-motion.md` — recreating bespoke visualizations (radar, gauges, bars, calendars, geo maps) and motion faithfully.
- `references/responsive.md` — adapting desktop-first layouts to mobile and tablet, per layout pattern.
- `assets/IMPLEMENTATION_PLAN.template.md` — the plan/checklist to fill during Phase 1.
- `assets/section-component.template.tsx` — the idiomatic target shape for a section: typed props, server/client split, token use, and all four states.
