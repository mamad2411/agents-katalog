---
name: positioning
description: Orchestrator — detect market vs product mode, recommend positioning frameworks, synthesize outputs into unified positioning
type: research
version: v0.9
argument-hint: "[optional: \"product\" | \"--synthesize\" | focus area]"
invocation: orchestrator
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `$pack install <pack>` instead of the target skill. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Positioning — Orchestrator

Invoke as `$positioning`.

This is an **orchestrator skill** using the parent router delegation pattern. It detects context, recommends applicable positioning frameworks, and synthesizes their outputs. Individual frameworks live as child skills under `frameworks/`.

## Report-First Approval Gate

Default to report-only: present findings, evidence coverage, assumptions, recommended artifact path, and proposed file changes in a pre-approval alignment page plus a concise conversation summary for user approval before creating or updating canonical research, spec, or task files.

Do not write or overwrite synthesized deliverables until the user explicitly approves, unless the user invoked an explicit write/update/fix mode or clearly asked to write files upfront. Raw evidence capture may be persisted before analysis when reproducibility requires it; report those raw paths separately and still gate synthesized research/report writes.

When stopping for approval, build and attempt to open the alignment preview page first, then ask the user to review it and approve, question, or request adjustments. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

Default stance: assume the user has no insider knowledge of the market. The positioning recommendation must stand on research, customer evidence, and codebase reality before asking for user input.

## Evidence And Feedback Handling

Treat user feedback as input to evaluate, not as automatic ground truth.

- For factual, evidentiary, technical, or source-backed claims: verify against available evidence. If the user appears to misunderstand the evidence or states something factually incorrect, push back clearly and cite the evidence. Do not rewrite findings merely to agree.
- For taste, brand, positioning preference, risk appetite, prioritization, or other subjective judgment calls: weigh user feedback heavily and adapt the recommendation unless it conflicts with verified evidence.
- When feedback mixes facts and preference, separate them explicitly: correct the factual part, then incorporate the preference where it is a legitimate judgment call.
- When uncertain, say what is known, what is inferred, and what would change the conclusion.

## Prerequisites

- **Hard**: `research/icp.md` (or `research/{slug}/icp.md`) must exist. If not, tell the user to run `$icp` first and stop.
- **Hard**: `research/competitive-analysis.md` (or `research/{slug}/competitive-analysis.md`) must exist. If not, tell the user to run `$competitive-analysis` first and stop.
- **Strong default**: `research/journey-map.md` (or `research/{slug}/journey-map.md`) should exist before writing canonical positioning. If missing, recommend `$journey-map` first unless the user explicitly needs a provisional positioning analysis.
- **Soft**: Read these if they exist:
  - `research/journey-map.md` — where value is delivered, the aha moment
  - `research/customer-feedback.md` — real customer language about what makes the product different
  - `research/monetization.md` — pricing context for value perception

## Operational Modes

### Mode A: Framework Selection (default first invocation)

Activated by: `$positioning` or `$positioning [focus area]` (no special flags).

### Mode B: Synthesis

Activated by: `$positioning --synthesize`

### Mode C: Product-Positioning Shortcut

Activated by: `$positioning product` or `$positioning post-launch` or `$positioning obviously-awesome`

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

### 1. Mode Detection

Detect **market-positioning mode** (default) or **product-positioning mode**:

**Market-positioning mode** activates when:
- No `research/customer-feedback.md` with post-launch customer evidence, AND
- No production codebase with live users detected, AND
- `$ARGUMENTS` does not contain "product", "post-launch", or "obviously-awesome"

Available frameworks in market mode:
- `jtbd-positioning` — Jobs-to-be-Done positioning analysis
- `strategic-canvas` — Blue Ocean strategic canvas
- `moore-positioning` — Geoffrey Moore positioning hypothesis
- `category-design` — Play Bigger category creation

**Product-positioning mode** activates when:
- `research/customer-feedback.md` exists with real customer data, OR
- `$ARGUMENTS` contains "product", "post-launch", or "obviously-awesome", OR
- Production spec exists AND customer feedback references real users

Available frameworks in product mode:
- `obviously-awesome` — April Dunford (requires real customer evidence)
- `strategic-canvas` — optionally, for category refresh

### 2. Load Context

- Read `research/icp.md`, `research/competitive-analysis.md`
- Read soft prerequisites if they exist
- Read CLAUDE.md, README for product context
- Read any existing `research/positioning-*.md` intermediate artifacts

### 3. Mode A — Framework Selection

Build an alignment page with:

1. **Mode explanation**: which mode was detected and why
2. **Available evidence summary**
3. **Multi-select framework section**: checkboxes with pre-checked defaults:
   - Market mode: `jtbd-positioning` + `strategic-canvas` + `moore-positioning` pre-checked; `category-design` unchecked
   - Product mode: `obviously-awesome` pre-checked; `strategic-canvas` unchecked
4. **Execution plan**: selected frameworks written to `tasks/todo.md` for sequential `$exec` execution
5. **Approval gate**

After user approval (compiled YAML with `selected_frameworks` list):

Write selected frameworks as sequential steps in `tasks/todo.md`:

```markdown
## Positioning Framework Execution

- [ ] Run `$positioning/frameworks/jtbd-positioning` — JTBD analysis
- [ ] Run `$positioning/frameworks/strategic-canvas` — Blue Ocean gap analysis
- [ ] Run `$positioning/frameworks/moore-positioning` — Positioning hypothesis
- [ ] Synthesize: `$positioning --synthesize` — Combine framework outputs into research/positioning.md
```

Only include selected frameworks. Always append synthesis step last. Stop after writing.

### 4. Mode B — Synthesis (`$positioning --synthesize`)

Read all intermediate framework outputs (`research/positioning-*.md`). At least one must exist.

Synthesize into unified `research/positioning.md`:

**Market-positioning synthesis**: combined hypothesis, Moore template filled with cross-framework evidence, evidence matrix, confidence levels, validation plan. Header: `> Mode: Market Positioning (hypothesized, pre-product)`

**Product-positioning synthesis**: positioning statement from Obviously Awesome, customer-grounded evidence matrix, confidence levels. Header: `> Mode: Product Positioning (customer-grounded)`

Build alignment page for synthesis approval. After approval: write `research/positioning.md`, emit next-step routing.

### 5. Mode C — Product-Positioning Shortcut

Skip multi-select. Build an alignment page for the shortcut execution plan with:

1. **Shortcut explanation**: product-positioning shortcut selected and why `obviously-awesome` is the only queued framework
2. **Evidence readiness**: customer-feedback requirement and any missing evidence caveats
3. **Proposed execution plan**: the exact `tasks/todo.md` framework queue shown below
4. **Approval gate**: require final compiled YAML approval before writing `tasks/todo.md`

Do not write `tasks/todo.md` before alignment approval. The next action is review of the HTML alignment page.

After user approval via final compiled YAML, write this execution plan to `tasks/todo.md`:

```markdown
## Positioning Framework Execution

- [ ] Run `$positioning/frameworks/obviously-awesome` — April Dunford positioning
- [ ] Synthesize: `$positioning --synthesize` — Write research/positioning.md
```

Stop — user runs `$exec`.

### 6. Next Steps (after synthesis only)

- ALWAYS: check for `product-design` pack → recommend `$ux-variations`
- IF no journey-map: check for `customer-lifecycle` pack → recommend `$journey-map`
- IF solution-customer fit weak/disputed: `$value-prop-canvas`
- IF business-model risks: `$lean-canvas`
- IF no GTM: check for `business-growth` pack → recommend `$gtm`
- IF GTM exists: recommend `$gtm` refresh
- IF no monetization: check for `business-growth` pack → recommend `$monetization`
- IF codebase exists: check for `business-ops` pack → recommend `$mvp-gap`

### 7. Downstream Impact Check (after synthesis write)

Check `research/gtm.md`. Classify impact as None/Minor/Major per standard pattern.

## Optional Research Trigger Map

These detours are conditional framework owners, not required AFPS chain links.

| Positioning signal | Owner | Trigger threshold |
|---|---|---|
| Solution-customer fit weak/disputed, value mapping low confidence | `$value-prop-canvas` | Trigger: unique attributes can't be confidently mapped to value. Skip: value mapping clear. |
| Business-model risk exposed by category strategy | `$lean-canvas` | Trigger: risk would change UX or prototype choices. Skip: normal competitive findings. |
| Pricing architecture central to positioning | `$monetization` | Trigger: category/value mapping requires grounded pricing. Skip: pricing not a differentiator. |

## Output

### Mode A: `tasks/todo.md` update (framework execution steps)
### Mode B: `research/positioning.md` (unified synthesis — see claude variant for full template)
### Mode C: pre-approval alignment page, then `tasks/todo.md` update after final compiled YAML approval (obviously-awesome + synthesis)

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable work goes in `tasks/todo.md`.
- Human-only external actions go in `tasks/manual-todo.md`.
- Condition-gated records go in `tasks/record-todo.md`.
- Cadence-based reviews go in `tasks/recurring-todo.md`.

## Constraints

- **Requires ICP + competitive analysis.**
- **Customer-grounded.** Every decision connects to real evidence.
- **Mode detection is evidence-based.** Do not override without user confirmation.
- **Parent does not execute frameworks.** It selects and queues them. `$exec` handles execution.
- **Synthesis requires at least one framework output.**
- **Do not overwrite existing `research/positioning.md`** without asking first.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/positioning-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
