---
name: ux-variations
description: Interview and plan multiple UX and UI variations for a product, page, or flow, including onboarding, typical workflows, sharing, collaboration, return use, and interface alternatives users can compare before locking a direction — and concrete visual/layout UI variations with UAT before consolidation
type: planning
version: v0.9
argument-hint: "[optional: app, page, flow, feature, or existing UI spec]"
---

# UX Variations

Invoke as `$ux-variations`.

Use this skill when the user wants to explore multiple UX/UI directions before committing to a final experience. This skill interrogates the full user journey: onboarding, first success, typical workflows, sharing and collaboration, return use, notifications, handoffs, failure recovery, and the interface patterns that support those moments. It then creates variation plans for flows, layouts, navigation models, interaction patterns, component choices, content density, visual tone, and behavior so the user can compare, test, and lock one direction.

Use `$ui-interview` first when the interface has not yet been specified page by page. Use this skill directly when a UI spec, current implementation, screenshot, prototype, or clear feature scope already exists.

When invoked with `--layout-mode` (or when the user says "layout mode", "layout variations", or "UI variations"), this skill operates at the concrete component/layout level — it varies HOW the same content is presented visually, not WHAT the user flow is. Layout-mode takes a fixed content contract from `specs/ui-requirements-[topic].md` or equivalent and generates 2-5 concrete visual/spatial approaches. Each variation must be specified well enough to build as a lightweight implementation, then evaluated through `$uat --variant-evaluation` (check `.agents/project.json.enabled_packs` for `product-testing` — if `product-testing` is not enabled, recommend `$pack install product-testing` first) before `$consolidate-variations`.

## Workflow

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
   - Read `README.md`, `AGENTS.md`, `CLAUDE.md`, relevant `docs/`, `specs/`, `research/`, task files, screenshots, route files, and component implementations when present.
   - Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection. Use `active_paths` as the product/app focuses and treat deferred `product_paths[]` as parked product directions, not required UX variants.
   - Prefer existing `specs/ui-*.md`, product specs, journey maps, ICP research, and user feedback as source evidence.
   - If no credible scope exists, run or recommend `$ui-interview` before developing variants.

2. **Define the decision surface**
   - Identify what the user is deciding: whole app experience, onboarding, activation, typical workflow, sharing flow, collaboration model, purchase flow, editor, dashboard, settings, mobile experience, page layout, or another bounded surface.
   - Identify which dimensions are allowed to vary:
     - First-run onboarding and activation
     - Core workflow sequencing
     - Sharing, invitations, permissions, and collaboration
     - Return-use loops and re-entry points
     - Notifications, reminders, and status surfaces
     - Handoffs between users, roles, devices, or channels
     - Recovery from errors, empty states, and stalled progress
     - Information architecture
     - Navigation
     - Page layout
     - Task flow order
     - Component model
     - Data density
     - Visual hierarchy
     - Motion and transition behavior
     - Copy tone
     - Mobile behavior
   - Identify fixed constraints: brand, stack, design system, must-keep components, accessibility, launch scope, performance, and business requirements.
   - **Layout-mode addition**: In layout-mode, read `specs/ui-requirements-[topic].md` as the fixed content contract. The WHAT is locked; only the HOW varies. Layout dimensions that can vary:
     - Container pattern: card grid, data table, list, kanban, timeline, tree, masonry
     - Detail pattern: sidebar panel, full-page route, modal, drawer, inline expand, popover
     - Navigation: top-nav, side-nav, tab-based, breadcrumb-driven, command-palette, hybrid
     - Density: compact, comfortable, spacious
     - Hierarchy: content-first, chrome-first, action-first
     - Responsive strategy: reflow, collapse, separate mobile layout, progressive disclosure

3. **Surface assumptions before probing**
   - Present a UX Variation Assumptions Manifest before deep questioning.
   - Tag assumptions with `[from spec]`, `[from codebase]`, `[from research]`, `[from artifact]`, or `[inferred]`.
   - Cover:
     - Target users and usage context
     - Primary job or workflow
     - First-run moment, activation event, and "aha" threshold
     - Typical repeat-use workflow
     - Sharing, collaboration, and permission assumptions
     - Return triggers, notifications, and re-engagement assumptions
     - Cross-device, cross-role, or external handoff assumptions
     - Existing pain points or uncertainty
     - Decisions that are locked versus open
     - Evaluation criteria
     - Required variants and desired breadth
     - Prototype fidelity and implementation budget
     - Success metrics and selection method
   - Ask the user to confirm, correct, or flag assumptions before proceeding.

4. **Interview for variation goals**
   - Codex interview cadence is one primary decision question per turn by default. Use short follow-up bullets only when they clarify the same variation decision, not to batch unrelated questions.
   - Default to maximally contrasting archetypes. Do not ask how different variants should be — assume dramatic contrast unless the user explicitly requests graduated steps.
   - Default evaluation method is: build each variation, then run `$uat --variant-evaluation` (check `.agents/project.json.enabled_packs` for `product-testing` — if `product-testing` is not enabled, recommend `$pack install product-testing` first) so the user has task-based evidence before consolidation.
   - When presenting a design decision with 3+ plausible answers during the interview, always include "Make this a variant axis (test all approaches)" as an option. When the user has already chosen "test all" for a prior question in the same session, default subsequent ambiguous decisions to variant axes without asking.
   - Establish:
     - Assume solo evaluator building and gut-checking unless the user states otherwise
     - What they must be able to accomplish
     - How a new user arrives, signs up, understands the product, and reaches first value
     - What the normal repeat workflow looks like after onboarding
     - What users create, save, share, export, invite others into, or hand off
     - What roles or permission levels exist, and how collaboration should feel
     - What notifications, reminders, status updates, or activity feeds users expect
     - How users resume work after hours, days, or weeks away
     - What happens when a workflow is abandoned, blocked, invalid, offline, or partially complete
     - Which current interface parts are working
     - Which current interface parts feel wrong, uncertain, slow, confusing, too dense, too sparse, or too generic
     - What would make a variant unacceptable
     - What evidence will decide the winner
   - When the user is unsure, recommend a practical default and explain why.
   - **Layout-mode interview additions**: When in layout-mode, also ask:
     - What is the primary user task on this page? (scan, search, create, compare, monitor, triage)
     - How much data will typically be visible? (5 items, 50 items, 500 items)
     - Are there reference apps or pages the user admires for this type of content?
     - Are any layout patterns explicitly off the table?
     - What is the build budget per variation? (quick prototype, medium fidelity, production-ready)
     - What must the user do in each built variant before they are ready to consolidate?

5. **Create distinct variation concepts**
   - Produce 5 variations by default. Present the concepts for adjustment — do not ask the user to choose a count first.
   - Each variation must be meaningfully different, not just a color or spacing change.
   - At this stage, keep each concept lightweight: name, thesis, archetype, best-fit user/context, core workflow difference, major tradeoff, and rough complexity. Do not fully specify screens, controls, or implementation details yet.
   - Useful archetypes include:
     - Task-first workflow
     - Data-dense operator console
     - Guided step-by-step flow
     - Onboarding-first activation path
     - Collaboration-first workspace
     - Sharing-first artifact flow
     - Notification/status-driven workflow
     - Role-based handoff workflow
     - Visual canvas or board
     - Command/search-first interface
     - Mobile-first progressive disclosure
     - Familiar SaaS dashboard
     - Editorial or showcase layout
   - Only choose archetypes that fit the product and user context.
   - **Layout-mode archetypes** (use these instead of the UX-flow archetypes above when in layout-mode):
     - Card grid: visual items in a responsive grid, good for browsing and scanning
     - Data table: dense rows with sortable/filterable columns, good for operators and power users
     - List + detail panel: master list on left, detail sidebar on right, good for email/messaging patterns
     - Full-page detail: list view navigates to full-page item view, good for content-heavy items
     - Kanban / board: columns representing states or categories, good for workflow and status tracking
     - Timeline / feed: chronological stream, good for activity, logs, and social patterns
     - Dashboard mosaic: mixed widget grid with charts, lists, and stats, good for monitoring and overview
     - Split-pane workspace: resizable panels for parallel content, good for editors and comparison
     - Command-first minimal: search/command bar with minimal chrome, good for keyboard-heavy power users
     - Sidebar-driven: persistent sidebar navigation with content area, good for settings and multi-section apps

6. **Concept selection checkpoint**
   - Before fully specifying any variant, ask the user to adjust the concept set.
   - Use bounded wording such as: "How should I adjust these UX variants before writing the final spec?"
   - Present clear options:
     - Keep all concepts
     - Make one concept bolder or more extreme
     - Add another concept
   - Do not ask the user to remove or merge concepts before they have been built. Pre-build narrowing is consistently rejected.
   - Ask the user to name the affected concept and briefly describe the change when they choose anything other than keeping all concepts.
   - Recommend a practical default when evidence supports it; do not imply that variants have already been built or committed.
   - Revise the concept set based on the answer before moving on.

7. **Specify each approved variation enough to build**
   - For each variation, define:
     - Name and design thesis
     - Target user fit
     - Page and flow changes
     - Onboarding and activation model
     - Typical workflow sequence
     - Sharing, collaboration, and permissions model
     - Return-use and notification model
     - Failure recovery and abandoned-workflow behavior
     - Navigation model
     - Screen-by-screen layout
     - Key components and controls
     - Button and link behavior
     - Spatial density, sizing, and hierarchy
     - Responsive behavior
     - Visual tone
     - Strengths, risks, and failure modes
     - Implementation complexity
     - What to prototype first
     - What user signal would make this the winner
   - **Layout-mode variation spec additions**: In layout-mode, each variation spec must also include:
     - Content-to-component mapping: which content requirement maps to which UI component
     - Page regions with approximate proportions (e.g., sidebar 280px, content fluid, detail panel 400px)
     - Primary content component
     - Detail view pattern
     - Action placement
     - Navigation pattern and placement
     - Responsive behavior at 3 breakpoints (mobile <=640px, tablet <=1024px, desktop >1024px)
     - Density approach
     - States rendering
     - Implementation file list
     - Estimated build time
     - Variant evaluation task: the user task to perform in this variation before consolidation
     - Evidence to capture: screenshots, notes, time-to-complete, friction points, and acceptance/rejection signals

8. **Plan experimentation**
   - Recommend serial full buildout of all approved variants when the user is using layout-mode or explicitly wants to compare built interfaces. Do not recommend building a subset first unless the user asks for a smaller experiment.
   - For prototype-stage product or feature work, prefer numerous small route-based experiments over one merged prototype when multiple workflows, layouts, densities, copy approaches, navigation models, or interaction patterns remain plausible. Name the route for each experiment, such as `/experiments/table-first`, `/experiments/command-first`, or the project's equivalent, and keep shared production infrastructure out of those routes unless explicitly approved.
   - If route experiments imply materially different products, apps, ICPs, or product lines, update `research/.progress.yaml` with experiment product-path entries instead of making every divergent path a required UX variation. Include `id`, `label`, `source_skill: ux-variations`, `scope_path`, `status`, `reason`, `archive_reason`, `archived_at`, `promoted_at`, `evidence_refs`, `revisit_trigger`, `next_skill`, `pipeline_stage: ux-variations`, and `last_touched`.
   - After variants are built, recommend `$uat --variant-evaluation` (check `.agents/project.json.enabled_packs` for `product-testing` — if `product-testing` is not enabled, recommend `$pack install product-testing` first) before `$consolidate-variations`. Consolidation is premature until evaluation evidence exists or the user explicitly says they reviewed the variants and is ready to converge.
   - Define the cheapest useful validation method:
     - Static mockups for visual direction
     - Clickable prototype for navigation and flow
     - Feature-flagged implementation for real usage
     - A/B test only when traffic and metrics are credible
     - Human UAT when target-user acceptance is the question
   - Define comparison criteria before selecting a winner.
   - Include a lock-in checklist so the chosen direction becomes a decision record, not a vague preference.
   - Include a UAT handoff checklist:
     - Target task for each variant
     - Success criteria and non-acceptance signals
     - Side-by-side comparison questions
     - Evidence to capture
     - Tradeoffs to notice
     - Readiness criteria for `$consolidate-variations`

9. **Coverage checkpoint**
   - Before concluding, summarize the variants, the decision criteria, and the proposed experiment plan.
   - Ask whether any decision criteria, risks, validation steps, or implementation constraints are missing before writing deliverables.

## Deliverables

- Write the variation plan to `specs/ux-variations-[topic].md`.
- Write the interview log to `ux-variations-[topic]-interview.md`.
- Update `research/.progress.yaml` only when variant or route experiments create materially different product paths; downstream research remains active-path-only until a path is activated.

### Alignment Page

Build and attempt to open `alignment/ux-variations-{topic}.html` before writing or replacing `specs/ux-variations-[topic].md` or the interview log.

**Alignment gates.** Treat gates as explicit review sections inside the HTML page. Include evidence coverage, assumptions/confidence, scope/non-goals, candidate/verdict decisions, artifact destination, proposed file changes, coverage checkpoint, and approval gates. Render surfaced assumptions, variation manifest, concept selection, experiment plan, UAT handoff checklist, and every proposed deliverable section with no context loss from source evidence or interview notes.

**Required inline questions.** Ask whether the evidence is sufficient for the variation set, whether any assumptions or confidence levels are wrong, whether the selected variant axes and rejected alternatives are acceptable, whether the proposed canonical file changes are approved, and whether any downstream route should remain blocked.

**Section feedback controls.** Add lightweight section-feedback controls to every major section of the page: approve as-is, reject or flag a concern, and clarification needed. Selecting a control reveals an optional notes textarea. These controls are optional for final approval and do not replace required gate questions. They also power the separate feedback-only YAML path so the user can send concerns or clarification requests before answering every required gate question.

**Feedback-only YAML contract.** Include a "Compile Feedback" or "Compile Feedback YAML" button separate from the final "Compile Answers" button. Enable it as soon as at least one section-feedback control is set, even if required inline gate questions are unanswered. It generates YAML with `alignment_page: alignment/{skill-name}-{topic}.html`, `feedback_status: revision-request`, `approval_status: not-approved`, `unanswered_required_questions`, and a `section_feedback` list containing one entry per section-feedback control that the user actually set. Populate `alignment_page` from the known repo-relative output path used to write the HTML page, not from the page title, browser URL, window location, or any display label. Each feedback entry uses `section`, `feedback` (`up`, `down`, or `needs-clarification`), optional `notes`, and `requested_agent_action` (`accept-as-is`, `investigate-and-revise`, or `clarify-before-approval`). For `down` and `needs-clarification` feedback, the YAML must tell the agent to evaluate the feedback, investigate further when needed, and contextually amend the HTML alignment page before asking again for final approval answers. Copy and display this feedback YAML with the same clipboard retry and textarea fallback behavior as final gate YAML.

**Gate YAML contract.** Compile final approval answers into YAML with `alignment_page: alignment/{skill-name}-{topic}.html`, `approval_status: ready-for-agent-review`, `section`, `gate_type`, `status`, `decision`, `notes`, and `approved_file_changes` fields. Populate `alignment_page` from the known repo-relative output path used to write the HTML page, not from the page title, browser URL, window location, or any display label. The final approval button remains disabled until every required question has a selection. The final YAML may also include any section feedback the user set, using the feedback-only YAML `section_feedback` shape. The page must automatically attempt to copy the YAML to the clipboard, provide an explicit "Copy YAML" button, and fall back to selecting the textarea contents.

**Pre-approval stop.** Before user approval, the next action is review of the HTML alignment page. Ask the user to review the page and provide either feedback-only YAML for concerns/clarification or final compiled YAML answers when ready. Do not require the user to answer every gate before sending negative feedback or clarification needs. When feedback-only YAML is provided, treat it as a revision request: evaluate the feedback, investigate further when needed, archive and amend the HTML page contextually, highlight the changes, and ask again for review. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after final compiled YAML has been provided and the approved artifacts have been written or updated.

## Constraints

- Do not present superficial variants that differ only by color palette, typography, or decorative treatment.
- Do not choose a winner for the user unless the evidence clearly supports it and the user asked for a recommendation.
- Do not defer all decisions to testing. State a recommended variant or experiment when evidence is sufficient.
- Do not ignore implementation cost. A compelling variation still needs a prototype path and selection criteria.
- Do not route directly from built UI variants to `$consolidate-variations`; insert `$uat --variant-evaluation` (check `.agents/project.json.enabled_packs` for `product-testing` — if `product-testing` is not enabled, recommend `$pack install product-testing` first) unless the user explicitly confirms they have already evaluated the variants.
- Do not enforce shared design constraints across variations. Each variation independently decides layout, density, color, navigation, and component choices. Only technical stack is shared unless the user explicitly locks a shared constraint.

## Archive-First Replacement Policy

- Before replacing or substantively rewriting an existing canonical research/spec document (`research/**/*.md`, `specs/**/*.md`, or `docs/specifications/**/*.md`), copy the current file to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-relative-path>`.
- Preserve the archived snapshot exactly as it existed before the change; do not edit the archived copy after creating it.
- After the archive snapshot exists, write the updated document to the original canonical path.
- Report both the archive path and the updated canonical path in the final output.
- New files do not need archive snapshots. Append-only updates do not need archive snapshots unless an existing section is regenerated or rewritten.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
