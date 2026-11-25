---
name: journey-map
description: Orchestrator — detect pre-product vs product-exists mode, recommend journey-mapping frameworks, synthesize outputs into unified lifecycle overview
type: analysis
version: v0.9
argument-hint: "[optional: \"product\" | \"--synthesize\" | app, use case, persona]"
invocation: orchestrator
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `$pack install <pack>` instead of the target skill. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Journey Map — Orchestrator

This is an **orchestrator skill** using the parent router delegation pattern. It detects context, recommends applicable journey-mapping frameworks, and synthesizes their outputs. Individual frameworks live as child skills under `frameworks/`.

## Report-First Approval Gate

Default to report-only: present findings, evidence coverage, assumptions, recommended artifact path, and proposed file changes in a pre-approval alignment page plus a concise conversation summary for user approval before creating or updating canonical research, spec, or task files.

Do not write or overwrite synthesized deliverables until the user explicitly approves, unless the user invoked an explicit write/update/fix mode or clearly asked to write files upfront. Raw evidence capture may be persisted before analysis when reproducibility requires it; report those raw paths separately and still gate synthesized research/report writes.

When stopping for approval, build and attempt to open the alignment preview page first, then ask the user to review it and approve, question, or request adjustments. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

## Prerequisites

- **Hard**: `research/icp.md` (or `research/{slug}/icp.md` in product-path mode) must exist — run `$icp` first.
- **Soft**: Read these if they exist:
  - `research/competitive-analysis.md` — competitor landscape
  - `research/customer-feedback.md` — real customer language
  - Specs, README/CLAUDE, and relevant source files for product context

## Operational Modes

### Mode A: Framework Selection (default first invocation)

Activated by: `$journey-map` or `$journey-map [focus area]` (no special flags).

### Mode B: Synthesis

Activated by: `$journey-map --synthesize`

### Mode C: Product-Exists Shortcut

Activated by: `$journey-map product`

---

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

0b. **Product-path manifest**: Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection. Scope the journey map to the active product path by default. When journey mapping reveals lifecycle stages or user flows that only apply to a deferred product path, add a `## Product Path Implications` section noting the finding and recommending `$product-line fork` if it implies a new product surface.

### 1. Mode Detection

Detect **pre-product mode** (default) or **product-exists mode**:

**Pre-product mode** activates when:
- No production codebase with live users detected, AND
- No `research/customer-feedback.md` with post-launch customer evidence, AND
- `$ARGUMENTS` does not contain "product"

Available frameworks in pre-product mode:
- `jtbd-timeline` (default) — Moesta/Switch timeline with push/pull/anxiety/habit forces
- `experience-map` (default) — Adaptive Path emotional arc with doing/thinking/feeling
- `customer-journey-canvas` (optional) — Stickdorn stage×touchpoints×actions canvas
- `service-blueprint` (optional) — Shostack front-stage/backstage/support lines
- `user-story-map` (optional) — Jeff Patton activity→task→story hierarchy

**Product-exists mode** activates when:
- Production code or deployment exists, OR
- `research/customer-feedback.md` exists with real customer data, OR
- `$ARGUMENTS` contains "product"

Available frameworks in product-exists mode:
- `service-blueprint` (default) — operational gaps visible with a running product
- `user-story-map` (default) — release slicing grounded in real usage
- `customer-journey-canvas` (optional) — full-stage touchpoint audit
- `experience-map` (optional) — emotional arc refresh with real feedback
- `jtbd-timeline` (optional) — switching timeline with post-launch evidence

### 2. Load Context

- Read `research/icp.md` — ICP segments, pain points, value props, trigger events
- Read `research/competitive-analysis.md` if it exists — competitor landscape
- Read `research/customer-feedback.md` if it exists — real customer language
- Read CLAUDE.md, README for product context
- Read any existing `research/journey-map-*.md` intermediate artifacts (from prior runs)

### 3. Mode A — Framework Selection

Build an alignment page with:

1. **Mode explanation**: which mode was detected and why (evidence for detection)
2. **Available evidence summary**: what research exists and what's missing
3. **Multi-select framework section**: checkboxes for each available framework with:
   - Framework name and one-line description
   - Why it's recommended or optional for this context
   - Pre-checked defaults based on detected mode (see mode detection above)
4. **Execution plan explanation**: selected frameworks will be written to `tasks/todo.md` for sequential `$exec` execution
5. **Approval gate**: framework selection confirmation

After user approval via compiled YAML (which includes `selected_frameworks` list):

Write selected frameworks as sequential steps in `tasks/todo.md`:

```markdown
## Journey Map Framework Execution

- [ ] Run `$journey-map/frameworks/jtbd-timeline` — JTBD switching timeline
- [ ] Run `$journey-map/frameworks/experience-map` — Adaptive Path experience map
- [ ] Synthesize: `$journey-map --synthesize` — Combine framework outputs into research/journey-map.md
```

Only include frameworks the user selected. Always append the synthesis step last.

Stop after writing `tasks/todo.md`. The user runs `$exec` to execute each framework sequentially.

### 4. Mode B — Synthesis (`$journey-map --synthesize`)

Read all intermediate framework outputs:
- `research/journey-map-jtbd-timeline.md`
- `research/journey-map-experience-map.md`
- `research/journey-map-customer-journey-canvas.md`
- `research/journey-map-service-blueprint.md`
- `research/journey-map-user-story-map.md`

At least one must exist. If none exist, tell user to run framework selection first.

Synthesize into unified `research/journey-map.md`:

**Synthesis includes:**
- Unified customer lifecycle: trigger, discovery, evaluation, onboarding, aha moment, conversion, transaction, retention, expansion, advocacy, churn, recovery
- User journey map per key persona with core use cases, entry points, task steps, decision points, happy path, failure modes
- Critical moments: the 3-5 moments where the product wins or loses the user/customer
- Evidence matrix: each claim mapped to which framework(s) support it
- Confidence levels per claim (strong/moderate/hypothesized)
- Stage detail index: links to deeper stage docs when they exist
- Journey gaps: stages needing deeper analysis
- Mode header: `> Mode: Pre-Product (hypothesized)` or `> Mode: Product-Exists (grounded)`

Build alignment page for synthesis approval with:
- Full proposed `research/journey-map.md` content
- Evidence matrix combining all framework sources
- Confidence/assumption register
- Critical-moment evidence matrix
- Proposed file changes gate
- Approval gate

After approval: write `research/journey-map.md`, then emit next-step routing.

### 5. Mode C — Product-Exists Shortcut

Skip multi-select. Build an alignment page for the shortcut execution plan with:

1. **Shortcut explanation**: product-exists shortcut selected and why `service-blueprint` + `user-story-map` are the queued defaults
2. **Evidence readiness**: available product/customer evidence and any caveats
3. **Proposed execution plan**: the exact `tasks/todo.md` framework queue shown below
4. **Approval gate**: require final compiled YAML approval before writing `tasks/todo.md`

Do not write `tasks/todo.md` before alignment approval. The next action is review of the HTML alignment page.

After user approval via final compiled YAML, write this execution plan to `tasks/todo.md`:

```markdown
## Journey Map Framework Execution

- [ ] Run `$journey-map/frameworks/service-blueprint` — Shostack service blueprint
- [ ] Run `$journey-map/frameworks/user-story-map` — Jeff Patton user story map
- [ ] Synthesize: `$journey-map --synthesize` — Write research/journey-map.md
```

Stop — user runs `$exec`.

### 6. Next Steps (after synthesis only)

Priority-ordered decision tree — recommend the **first** match:

1. **Blocking optional research trigger** — the overview exposed a stage, fit, measurement, or product-loop risk that must be resolved before positioning or UX choices harden → use the Optional Research Trigger Map below. Cite the exact journey evidence, why it blocks the next AFPS step, and which existing framework skill owns it.
2. **Positioning missing** (`research/positioning.md` does not exist) → check `.agents/project.json.enabled_packs` for `business-discovery` — if `business-discovery` is not enabled, recommend `$pack install business-discovery` first; if `business-discovery` is enabled, recommend `$positioning` — Positioning needs ICP, competitive analysis, and journey evidence, so it is the natural next step.
3. **Positioning done, user-flow map missing** → check `.agents/project.json.enabled_packs` for `product-design` — if `product-design` is not enabled, recommend `$pack install product-design` first; if `product-design` is enabled, recommend `$user-flow-map` — Map screen flow, decisions, branches, states, and low-fidelity wireframe structure before UI requirements.
4. **Never** recommend `$spec-interview` from this skill — it is many steps downstream in the AFPS chain.

## Optional Research Trigger Map

These detours are conditional framework owners, not required AFPS chain links. Use them only when the journey evidence shows that the answer will change positioning, product-loop direction, flow/design shape, or prototype choices. When the trigger is absent, continue to `$positioning` or `$user-flow-map` using the decision tree above.

| Journey signal | Existing owner | Trigger threshold |
| --- | --- | --- |
| Signup, setup, activation, first-success, or time-to-value path is unclear | `$onboarding-map` | The journey cannot identify the first success path, onboarding drop-offs, or activation criteria well enough to shape UX. |
| Evaluation, trial, pricing decision, objections, or buyer roles are unresolved | `$conversion-map` | Conversion decision logic affects the primary screen flow, offer, or proof sequence. |
| Purchase, checkout, payment, fulfillment, refund, dispute, or trust state is material | `$transaction-map` | Transaction mechanics create product risk before UX/prototype choices. |
| Repeat-use job, return trigger, churn risk, recovery path, or retention signal is unclear | `$retention-map` | The product needs a natural return model before designing engagement, lifecycle messages, or saved state. |
| Stage instrumentation, leading indicators, or lifecycle handoff metrics are unclear | `$lifecycle-metrics` | The journey has stage risks but needs measurement before growth or implementation planning. Prefer this over `$hook-model` for enterprise, infrastructure, transactional, or naturally infrequent products. |
| Product value depends on repeat use, habit formation, engagement loops, retention triggers, saved state, social rewards, or investment compounding | Check `.agents/project.json.enabled_packs` for `business-growth` — if missing, recommend `$pack install business-growth`; if enabled, recommend `$hook-model` | Use only for consumer, prosumer, PLG, marketplace, community, or B2B-with-consumer-component products where habit-loop design should shape flow and prototype choices before `$user-flow-map`. Do not force this on B2B/enterprise, infrastructure, transactional, or naturally infrequent products; route those to `$lifecycle-metrics` or, when `business-growth` is enabled and a broader success framework is needed, `$metrics`. |
| Expansion, upgrade, seat growth, referral, advocacy, or land-and-expand path is material | `$expansion-map` | Expansion mechanics change lifecycle sequencing, account roles, or product surface priorities. |
| Jobs, pains, gains, aha moment, or solution fit are weak, disputed, or need explicit scoring | Check `.agents/project.json.enabled_packs` for `business-discovery` — if missing, recommend `$pack install business-discovery`; if enabled, recommend `$value-prop-canvas` | Use the existing Strategyzer-style framework only when fit risk would make positioning or UX premature. |
| Revenue, channel, cost, defensibility, or unfair-advantage assumptions are material risks | Check `.agents/project.json.enabled_packs` for `business-discovery` — if missing, recommend `$pack install business-discovery`; if enabled, recommend `$lean-canvas` | Use the existing Ash Maurya Lean Canvas framework when the journey exposes business-model risk before UX/prototype decisions. |
| Pricing gates, packaging, free-to-paid timing, or willingness-to-pay moments are central to the journey | Check `.agents/project.json.enabled_packs` for `business-growth` — if missing, recommend `$pack install business-growth`; if enabled, recommend `$monetization` | Use when pricing architecture must be grounded before conversion, transaction, or prototype choices. |
| Acquisition source, launch channel, messaging route, or early traction mechanism is a journey blocker | Check `.agents/project.json.enabled_packs` for `business-growth` — if missing, recommend `$pack install business-growth`; if enabled, recommend `$gtm` | Use after enough ICP/competitive/journey evidence exists and the channel path changes product or UX priorities. |

`$growth-model` is an existing Reforge-style framework owner for compounding acquisition, retention, and monetization loops, but do not route to it directly from `journey-map` unless metrics/GTM prerequisites are already satisfied. In most AFPS cases, `$hook-model`, `$metrics`, `$monetization`, or `$gtm` is the earlier business-growth detour.

## Output

### Mode A output: `tasks/todo.md` update

Framework execution steps (see section 3 above).

### Mode B output: `research/journey-map.md` (or `research/{slug}/journey-map.md`)

```markdown
# Journey Map

> Based on: [list of framework outputs used]
> Date: [current date]
> Mode: Pre-Product (hypothesized) | Product-Exists (grounded)
> Frameworks applied: [list]

## Summary

## User Journeys

## Customer Lifecycle

## Critical Moments

## Evidence Matrix

| Claim | Supporting Framework(s) | Evidence | Confidence |
|-------|------------------------|----------|------------|
| [claim] | JTBD Timeline / Experience Map / Service Blueprint / User Story Map / Customer Journey Canvas | [source] | Strong / Moderate / Hypothesized |

## Stage Detail Index

## Journey Gaps

## Next Steps
```

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/journey-map-{topic}.html`.

**Journey research translation.** Render the lifecycle overview as approval-ready research, not a chat-only summary. The alignment page must include the proposed `research/journey-map.md` content, proposed file changes, evidence coverage by journey stage, assumptions/confidence register, critical-moment evidence matrix, and approval gates before canonical research files are created or updated.

Before approval, the next action is review of `alignment/journey-map-{topic}.html` and compiled YAML answers from that page. Do not treat a plain-text lifecycle summary as a substitute for the HTML alignment preview.

## Constraints

- **Parent does not execute frameworks.** It selects and queues them. `$exec` handles execution.
- **Synthesis requires at least one framework output.** Do not synthesize from zero evidence.
- **Mode detection is evidence-based.** Do not override mode detection without user confirmation.
- Ground every important step in ICP, research, specs, feedback, or codebase evidence.
- Do not prescribe UI or architecture.
- Present findings before writing.
- Follow the archive-first replacement policy for canonical research/spec documents.
- Do not overwrite existing `research/journey-map.md` without asking the user first.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
