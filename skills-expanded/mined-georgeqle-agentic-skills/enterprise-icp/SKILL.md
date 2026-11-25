---
name: enterprise-icp
description: Enterprise multi-stakeholder discovery — map personas, deal-killers, and the evaluation-to-renewal lifecycle
type: research
version: v0.9
argument-hint: "[optional: target industry or market segment]"
interview_depth: full
visual_tier: visual
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. After install, tell Codex users to start a fresh Codex CLI session if the `$` skill list remains stale. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Enterprise ICP — Multi-Stakeholder Discovery Interview

Invoke as `$enterprise-icp`.

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the research and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with findings and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, or task files.

Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, spec, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions. Build the `review` HTML alignment page before synthesized research. The page must render the proposed scope, available source categories, known context, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, rank candidates, make recommendations, or write working packets, canonical research, spec, or task files in Stage 1.
2. **Stage 2 - Research and artifact review.** Only after approved research-scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, perform the synthesized research, run required source/code checks, and write only a non-canonical working packet: flat mode uses `research/_working/preliminary-<skill>-research.md`; product-path mode uses `research/{slug}/_working/preliminary-<skill>-research.md`. Replace `<skill>` with this skill's `name` value. Raw evidence or search logs may remain as supporting evidence where this skill already requires them, but synthesized deliverables stay in the working packet. Update the `review` HTML alignment page with the full preliminary packet, evidence matrix, assumptions/confidence register, source coverage gaps, proposed canonical file changes, and artifact approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML for artifact approval only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifacts to the unchanged output paths below, and convert the alignment page to `confirmed` with the approval record preserved.

Canonical output paths remain unchanged. Search logs and other supporting evidence remain allowed only where this skill's output contract already requires them.

## Evidence And Feedback Handling

Treat user feedback as input to evaluate, not as automatic ground truth.

- For factual, evidentiary, technical, or source-backed claims: verify against available evidence. If the user appears to misunderstand the evidence or states something factually incorrect, push back clearly and cite the evidence. Do not rewrite findings merely to agree.
- For taste, brand, positioning preference, risk appetite, prioritization, or other subjective judgment calls: weigh user feedback heavily and adapt the recommendation unless it conflicts with verified evidence.
- When feedback mixes facts and preference, separate them explicitly: correct the factual part, then incorporate the preference where it is a legitimate judgment call.
- When uncertain, say what is known, what is inferred, and what would change the conclusion.

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

1. Read `research/icp.md` (or `research/{slug}/icp.md`) if it exists as a starting point. Read the codebase if one exists. Before asking the user how enterprise differs, use WebSearch to research enterprise buying patterns in this product category (e.g., "[category] enterprise buying process", "[category] enterprise vs SMB"). Present the startup ICP summary alongside enterprise research findings, then ask how enterprise differs.
2. Interview the user one primary decision question per turn by default. Use short follow-up bullets only when they clarify the same enterprise ICP decision, not to batch unrelated questions. Research and recommend by default: assume the user has no insider knowledge unless they explicitly provide it; present findings with data, define relevant terms, state a recommendation, and ask for hard constraints, proprietary facts, or corrections; only ask without a recommendation when evidence cannot resolve the choice. Cover:
   - **Stakeholder Map** — Which personas matter? End users, team admin, IT/Security, procurement, champion (see Champion Enablement & Risk for deep analysis), exec sponsor
   - **Per-Persona Journeys** — What each stakeholder needs to see/do/approve; their deal-killing "no"
   - **Enterprise Buying Stages** — Evaluation → pilot → rollout requirements and blockers. Lifecycle mapping (expansion, renewal) belongs in `$journey-map`
   - **Deal-Killer Requirements** — SSO/SAML, SOC 2, GDPR, HIPAA, audit logs, data residency, RBAC, SLAs
   - **Onboarding Complexity** — Self-serve, team, SSO-provisioned, migration, training needs
   - **Enterprise Requirements Delta** — What enterprise buyers specifically need vs. startup ICP, ROI story. Strategic positioning belongs in `$positioning`
   - **Champion Enablement & Risk** — Champion identification (role, motivations), enablement toolkit (ROI calculator, case studies, exec summary deck), risk assessment (single-champion dependency, mitigation), multi-champion strategy, champion-to-executive bridge, post-sale champion role
   - **Procurement Reality** — Budget cycle timing, budget source (IT/departmental/innovation/exec), procurement path (vendor registration, RFP, security questionnaire, legal, MSA), approval chain. Pricing justification and competitive displacement belong in `$monetization`
   - **Land-and-Expand Patterns (Observed)** — Initial landing zone (smallest deployable unit), observed expansion triggers, expansion blockers. GTM strategy recommendations and account growth projections belong in `$gtm`
   - **Enterprise Segmentation** — Segment definitions (mid-market, large enterprise, strategic/Global 2000), segment differences (buying process, stakeholders, deal size), target segment priority, segment-specific deal-killers. Conditional — include only if product serves multiple enterprise tiers.
   > Areas G-J (Champion, Budget, Land-and-Expand, Segmentation) often surface together in conversation. Let answers inform nearby areas, but keep Codex follow-up questions one primary decision at a time.
3. **Present findings before writing.** Summarise with evidence: stakeholder map (citing interview responses and research data), critical deal-killers (citing competitor requirements, industry standards, or research findings), lifecycle friction points (citing specific examples or research findings), and key insights. Ask: "Which enterprise constraints, missing stakeholders, or weak assumptions should change this analysis?" Continue with follow-up questions until all non-trivial details are nailed down.
4. Only after user confirms, write the output files.

## Deliverables

- `research/enterprise-icp.md` (or `research/{slug}/enterprise-icp.md`) — Stakeholder map, per-persona journeys, enterprise buying stages, deal-killers, onboarding matrix, enterprise requirements delta, champion enablement & risk, procurement reality, land-and-expand patterns, enterprise segmentation (conditional), signals for downstream research, next steps
- `research/enterprise-icp-interview.md` (or `research/{slug}/enterprise-icp-interview.md`) — Raw interview log

The output file must end with a `## Next Steps` section with a **Recommended** item and **Other options** (2–4 alternatives). Use this format in the output:

## Next Steps

**Recommended:** [recommended skill] — [one-line reason why this is the highest-impact next action given current state]

Other options:
- `$skill` — [description]
- ...

**Recommendation priority** (first applicable becomes the recommendation):
1. IF codebase exists: check `.agents/project.json.enabled_packs` for `business-ops` — if `business-ops` is not enabled, recommend `npx skillpacks install business-ops` from the project shell, first; if `business-ops` is enabled, recommend `$scale-audit` — evaluate whether the codebase meets enterprise deal-killer requirements
2. Otherwise: check `.agents/project.json.enabled_packs` for `customer-lifecycle` — if `customer-lifecycle` is not enabled, recommend `npx skillpacks install customer-lifecycle` from the project shell, first; if `customer-lifecycle` is enabled, recommend `$journey-map enterprise` — map the multi-stakeholder journey before building

**Other options** (include all applicable items not chosen as recommended, based on which files exist):
- IF codebase exists: check `.agents/project.json.enabled_packs` for `business-ops` — if `business-ops` is not enabled, recommend `npx skillpacks install business-ops` from the project shell, first; if `business-ops` is enabled, recommend `$scale-audit` — Evaluate codebase against enterprise requirements
- check `.agents/project.json.enabled_packs` for `business-ops` — if `business-ops` is not enabled, recommend `npx skillpacks install business-ops` from the project shell, first; if `business-ops` is enabled, recommend `$scale-audit` — Evaluate enterprise readiness against stakeholder map and deal-killers
- IF no `research/journey-map.md`: check `.agents/project.json.enabled_packs` for `customer-lifecycle` — if `customer-lifecycle` is not enabled, recommend `npx skillpacks install customer-lifecycle` from the project shell, first; if `customer-lifecycle` is enabled, recommend `$journey-map enterprise` — Map enterprise stakeholder journeys
- IF no `research/journey-map.md` and `research/icp.md` exists: check `.agents/project.json.enabled_packs` for `customer-lifecycle` — if `customer-lifecycle` is not enabled, recommend `npx skillpacks install customer-lifecycle` from the project shell, first; if `customer-lifecycle` is enabled, recommend `$journey-map` — Map general user journeys
- `$competitive-analysis` — Research enterprise competitive landscape (if no `research/competitive-analysis.md`)

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- Stay in problem space — do not prescribe solutions.
- Do not assume enterprise ICP is startup ICP scaled up — explicitly explore what changes.
- Continue until all 10 areas are covered.
- Do not overwrite existing `research/enterprise-icp.md` (or `research/{slug}/enterprise-icp.md`) without asking the user first.
- Present before writing — never write until findings are validated.
- `## Next Steps` must be the final section in the output file, with a recommended next step and 2–4 other options.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/enterprise-icp-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
