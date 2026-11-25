---
name: ui-interview
description: Interview page by page to define a complete UI specification, including layout, hierarchy, controls, links, spacing, sizing, responsive behavior, visual states, and implementation-ready interface details — supports a requirements-only mode that establishes data, actions, and states without locking layout or component decisions
type: planning
version: v0.9
argument-hint: "[optional: app, page, flow, feature, or draft UI]"
---

# UI Interview

Invoke as `$ui-interview`.

Use this skill when the user needs to turn a rough product idea, feature, page, wireframe, screenshot, or existing app surface into a detailed implementation-ready UI specification. This skill focuses on the interface itself: pages, regions, components, buttons, links, labels, spacing, element size, visual hierarchy, state, responsive layout, and accessibility.

Use `$ux-variations` after this skill when the user wants multiple experience concepts or interface variants to compare before locking the final direction.

When invoked with `--requirements-only` (or when the user says "just requirements", "requirements only", or "content requirements"), this skill stops after establishing what the page needs — data, actions, states, and constraints — without committing to any layout, component, or spatial decisions. This mode feeds directly into `$ux-variations --layout-mode` to explore multiple concrete visual approaches for the same content contract.

## Process

### 0. Product-Path Scope Resolution

Resolve research scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the ICP, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target unless this skill explicitly supports cross-path output.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint. Suggest creating a missing `research/{slug}/` product path when code clearly exposes an app, but do not require code or monorepo detection before using `research/{slug}/`.

When product path `{slug}` is active, read and write research under `research/{slug}/`, specs under `specs/{slug}/`, and treat top-level `research/*.md` files as flat-mode documents or cross-path summaries.

1. **Resolve context**
   - Read `.agents/project.json` if it exists.
   - Read `README.md`, `AGENTS.md`, `CLAUDE.md`, relevant `docs/`, `specs/`, `research/`, route files, component directories, screenshots, and design artifacts when present.
   - If the request is for an existing UI, inspect the current implementation before interviewing.
   - If multiple apps or surfaces are plausible, ask the user which app, flow, or page to cover first.

2. **Treat inputs as draft material**
   - Do not assume the current UI, prompt, screenshot, or mockup is final.
   - Product specs, ICP documents, and journey maps are reference material, not locked constraints. The user may override any product decision during the interview. When a user's interview answer contradicts an existing spec, adopt the interview answer and note the divergence.
   - Preserve explicit constraints, but challenge unclear defaults before they become implementation decisions.
   - Distinguish product behavior decisions from UI presentation decisions.

3. **Surface assumptions before probing**
   - Present a UI Assumptions Manifest before deep questioning.
   - Tag each assumption with:
     - `[from spec]` - explicitly stated in a spec, prompt, or issue
     - `[from codebase]` - derived from existing routes, components, styles, or assets
     - `[from research]` - derived from ICP, audience, journey, feedback, or product research
     - `[from artifact]` - derived from screenshot, mockup, image, Figma export, or wireframe
     - `[inferred]` - filled in by judgment
   - Cover at least:
     - Product and user context
     - Pages, routes, and entry points
     - Prototype-first boundary for new product or substantial feature work: what the user should be able to click through first, whether multiple route-based experiments should be built, what data can be fake, fixture-backed, or in-memory, and which infrastructure must be represented visually but not implemented yet.
     - Primary tasks per page
     - Navigation model
     - Information hierarchy
     - Layout grid and spatial density
     - Component inventory
     - Button and link semantics
     - Form fields, validation, and error display
     - Empty, loading, disabled, success, warning, and failure states
     - Responsive breakpoints and mobile behavior
     - Accessibility requirements
     - Visual language, typography, color, iconography, and asset usage
     - Implementation constraints from the existing stack or design system
   - Ask the user to confirm, correct, or flag assumptions before continuing.

4. **Interview page by page**
   - Codex interview cadence is one primary decision question per turn by default. Use short follow-up bullets only when they clarify the same page or interface decision, not to batch unrelated questions.
   - Move through the interface in this order unless the user asks otherwise:
     - Global shell: header, sidebar, footer, navigation, account controls, notifications
     - Page inventory: every route, modal, drawer, overlay, and important empty state
     - Page purpose: user goal, task priority, and success condition
     - Prototype calibration: first clickable journey, route-based experiment set, fixture/fake data boundaries, infrastructure-only states to mock rather than implement, and taste/feel questions the prototype must answer before database, auth, payment, analytics, deployment, admin, or multi-tenant work is planned.

4b. **Requirements gate (requirements-only mode)**
   - In requirements-only mode, stop here — do not proceed to layout anatomy, component inventory, or spatial decisions.
   - For each page, confirm:
     - Data fields and entities with cardinality: one, many, nested, or polymorphic
     - User actions: create, edit, delete, filter, sort, export, navigate, bulk-select, reorder
     - States: empty, loading, error, partial, full, offline, permission-denied
     - Constraints: real-time updates, offline support, accessibility requirements, performance budgets
     - Content hierarchy: primary, secondary, tertiary information
     - Relationships between data elements: parent-child, peer, reference, aggregate
   - Present a **Content Requirements Manifest** summarizing all pages, then ask the user to confirm before writing deliverables.
   - Write `specs/ui-requirements-[topic].md` and `ui-requirements-[topic]-interview.md`.
   - After writing files, recommend `$ux-variations --layout-mode` to explore multiple visual approaches for these requirements, or `$ui-interview` without the flag to proceed directly to a single deep UI specification, or check `.agents/project.json.enabled_packs` for `agent-work-admin` — if `agent-work-admin` is not enabled, recommend `$pack install agent-work-admin` first; if `agent-work-admin` is enabled, recommend `$roadmap` — if the interface is ready to sequence into work.
   - Stop. Do not continue to step 5 or beyond.

5. **Full UI specification** (no `--content-only` flag):

     - Layout anatomy: top-to-bottom and left-to-right regions, alignment, density, scroll behavior
     - Component inventory: tables, lists, cards, forms, charts, media, editors, maps, canvases
     - Controls: every button, icon button, segmented control, checkbox, radio, toggle, input, menu, tab, link, and destructive action
     - Copy: headings, labels, helper text, validation text, confirmation text, empty-state text
     - States: default, hover, focus, active, selected, disabled, loading, error, success, partial, offline
     - Spatial details: element prominence, approximate sizes, gaps, padding, fixed or fluid dimensions, sticky regions, overlap rules, max widths
     - Responsive behavior: desktop, tablet, mobile, wide desktop, touch target sizing, collapsed controls
     - Accessibility: keyboard order, focus traps, labels, contrast, reduced motion, screen reader names. Include color-blind safe patterns, keyboard navigation, reduced motion support, and screen reader labels by default in every spec. Do not present accessibility features as optional checkboxes. Only ask about domain-specific accessibility when the product context warrants it.
   - When a page includes repeated items, define one canonical item and its variations rather than asking about every row individually.

5. **Research and recommend by default**
   - Use project evidence and established UI conventions before asking the user to invent details.
   - For material decisions, present options, a recommendation, rationale, tradeoffs, and mitigation.
   - Recommend familiar controls over novel patterns unless the product has a strong reason to deviate.
   - For frontend work, respect the existing design system, component library, and implementation patterns.
   - Reference and inspiration questions are low-priority. Ask once early, accept any answer including "none" or "let's experiment," and move on. Do not block the interview on reference input.

6. **Coverage checkpoint**
   - Before concluding, present a concise checklist of pages, components, controls, states, responsive behavior, and unresolved risks.
   - Ask whether anything is missing or should be revisited before writing deliverables.

## Deliverables

- Write the completed UI specification to `specs/ui-[topic].md`.
- Write the interview log to `ui-[topic]-interview.md`.

The UI specification must include:

- Scope and source evidence
- UI Assumptions Manifest with confirmations and corrections
- Page inventory and route map
- Global shell and navigation rules
- Detailed page-by-page anatomy
- Component inventory and reuse guidance
- Control inventory with labels, destinations, actions, disabled rules, and confirmation behavior
- Link inventory with destinations and external/internal classification
- Layout, spacing, sizing, and responsive rules
- Visual style direction and asset requirements
- Interaction states and accessibility requirements
- Implementation notes tied to the existing stack
- Open questions, risks, and explicit non-goals
- For new product interfaces or substantial feature interfaces, a prototype-first section naming the first clickable journey, experiment route map when multiple alternatives should be tested, fake/fixture data, visually mocked infrastructure states, deferred production infrastructure, and the evidence required before implementation planning promotes any deferred infrastructure.

The interview log must include:

- The manifest as presented
- Every question asked
- Options and recommendations presented
- User responses and final decisions
- Notable changes from the initial draft, current implementation, or artifact

After writing files, recommend `$ux-variations` if variants are needed before implementation, or check `.agents/project.json.enabled_packs` for `agent-work-admin` — if `agent-work-admin` is not enabled, recommend `$pack install agent-work-admin` first; if `agent-work-admin` is enabled, recommend `$roadmap` — if the interface is ready to sequence into work.

### Alignment Page

Build and attempt to open `alignment/ui-interview-{topic}.html` before writing or replacing `specs/ui-[topic].md` or the interview log.

**Page layout contract.** After the page title and short summary, include a top-of-page "Table of Contents" section with anchor links to the major review sections and the bottom compile section. Keep the Table of Contents in normal document flow. Do not use a sidebar, side rail, drawer, split-shell layout, or sticky navigation for the Table of Contents unless the user explicitly asks for that layout. Do not place compile, copy, feedback, or answer controls in a sticky or fixed bottom banner/footer. Bottom compile controls must appear as ordinary content in a bottom compile section, so they scroll with the page and do not cover content at high zoom.

**Alignment gates.** Treat gates as explicit review sections inside the HTML page. Include evidence coverage, assumptions/confidence, scope/non-goals, candidate/verdict decisions, artifact destination, proposed file changes, coverage checkpoint, and approval gates. Render surfaced assumptions, the UI or content requirements manifest, page inventory, route map, component/control/link inventories, prototype-first boundary, and every proposed deliverable section with no context loss from source evidence or interview notes.

**Required inline questions.** Ask whether the evidence is sufficient for the UI decisions, whether any assumptions or confidence levels are wrong, whether page/component decisions and non-goals are acceptable, whether the proposed canonical file changes are approved, and whether any downstream route should remain blocked.

**Section feedback controls.** Add lightweight section-feedback controls to every major section of the page: approve as-is, reject or flag a concern, and clarification needed. Selecting a control reveals a multi-line section-feedback textarea placed directly under or beside the thumbs up/down/clarify controls. This textarea is separate from gate-question text inputs, so it still appears near the feedback controls even when the same section also has required gate questions with their own text boxes. These controls are optional for final approval and do not replace required gate questions. They also power the separate feedback-only YAML path so the user can send concerns or clarification requests before answering every required gate question.

**Feedback-only YAML contract.** Provide feedback-only YAML in two places: locally under each selected section-feedback textarea, and globally in the bottom compile section. When a section-feedback control is selected, show local "Compile Feedback YAML" and "Copy YAML" controls plus a read-only YAML textarea directly under that section's feedback textarea. The local feedback compile generates YAML with `alignment_page: alignment/{skill-name}-{topic}.html`, `feedback_status: revision-request`, `approval_status: not-approved`, `unanswered_required_questions`, and a `section_feedback` list containing the single selected section-feedback entry for that local control. The bottom "Compile Feedback YAML" control generates the same YAML shape but aggregates every selected section-feedback entry on the page. Enable both local and bottom feedback compile controls as soon as at least one section-feedback control is set, even if required inline gate questions are unanswered. Populate `alignment_page` from the known repo-relative output path used to write the HTML page, not from the page title, browser URL, window location, or any display label. Each feedback entry uses `section`, `feedback` (`up`, `down`, or `needs-clarification`), optional `notes` from that section's feedback textarea, and `requested_agent_action` (`accept-as-is`, `investigate-and-revise`, or `clarify-before-approval`). For `down` and `needs-clarification` feedback, the YAML must tell the agent to evaluate the feedback, investigate further when needed, and contextually amend the HTML alignment page before asking again for final approval answers. Copy and display feedback YAML locally or at the bottom with the same clipboard retry and textarea fallback behavior as final gate YAML. Do not render the bottom feedback compile controls as a sticky or fixed banner.

**Gate YAML contract.** At the bottom of the page, include an ordinary in-flow compile section with a "Compile Feedback YAML" button for selected section feedback and a separate "Compile Answers" button for final approval answers. The bottom compile section must not be sticky, fixed, floating, or styled as a persistent banner. The "Compile Answers" button compiles final approval answers into YAML with `alignment_page: alignment/{skill-name}-{topic}.html`, `approval_status: ready-for-agent-review`, `section`, `gate_type`, `status`, `decision`, `notes`, and `approved_file_changes` fields. Populate `alignment_page` from the known repo-relative output path used to write the HTML page, not from the page title, browser URL, window location, or any display label. The final approval button remains disabled until every required question has a selection. The final YAML may also include any section feedback the user set, using the feedback-only YAML `section_feedback` shape. The page must automatically attempt to copy the YAML to the clipboard, provide an explicit "Copy YAML" button, and fall back to selecting the textarea contents.

**Pre-approval stop.** Before user approval, the next action is review of the HTML alignment page. Ask the user to review the page and provide either local or bottom feedback-only YAML for concerns/clarification, or final compiled YAML answers when ready. Do not require the user to answer every gate before sending negative feedback or clarification needs. When feedback-only YAML is provided, treat it as a revision request: evaluate the feedback, investigate further when needed, archive and amend the HTML alignment page contextually, highlight the changes, and ask again for review. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after final compiled YAML has been provided and the approved artifacts have been written or updated.

## Constraints

- Do not skip small interface elements. Buttons, links, icons, menus, and empty states are part of the spec.
- Do not collapse UI detail into generic phrases such as "standard dashboard layout" or "normal form behavior."
- Do not create high-fidelity implementation plans until the page anatomy and control behavior are decision-complete.
- Do not treat visual polish as separate from implementation. Size, spacing, hierarchy, and responsive behavior must be specified well enough for a developer to build.
- When recommending a skill from another pack, verify the pack is installed via `.agents/project.json` `enabled_packs`. If not installed, prepend `$pack install <pack-name>` to the recommendation.

## Archive-First Replacement Policy

- Before replacing or substantively rewriting an existing canonical research/spec document (`research/**/*.md`, `specs/**/*.md`, or `docs/specifications/**/*.md`), copy the current file to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-relative-path>`.
- Preserve the archived snapshot exactly as it existed before the change; do not edit the archived copy after creating it.
- After the archive snapshot exists, write the updated document to the original canonical path.
- Report both the archive path and the updated canonical path in the final output.
- New files do not need archive snapshots. Append-only updates do not need archive snapshots unless an existing section is regenerated or rewritten.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
