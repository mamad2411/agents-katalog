---
name: idear
description: Use when a rough software, tool, automation, or AI-product idea needs product clarification, feasibility evidence, comparison with existing solutions, or a development handoff before implementation.
---

# Idear

Idear is an adaptive-depth, evidence-first product-discovery workflow. Answer the user's actual decision at the smallest sufficient depth, from a bounded fact to a defensible feasibility verdict and, only when requested, a development handoff.

Use Idear for product clarification, feasibility research, comparison with existing products or open-source work, and pre-implementation handoff. It does not apply to direct implementation, ordinary code review or debugging, unrelated brainstorming, or a standalone bounded factual question that can be answered directly. If Idear is explicitly invoked for that bounded question, use the `quick` route below without expanding scope.

## Route Before Creating Artifacts

Read `references/scope-routing.md` before creating any file or directory. Infer the shallowest sufficient depth; do not ask the user to choose a mode.

- `quick`: answer a bounded, low-risk fact inline; create no workspace by default.
- `focused`: investigate one named uncertainty and answer in chat by default. Persist only `focused-assessment.md` and `sources.yaml` when useful or requested.
- `full`: run clarification, feasibility research, and the optional handoff under the gates below.

Honor an explicit request for narrower or deeper treatment. Never silently escalate `quick` or `focused` work to `full`; finish the bounded portion when possible, state what remains unresolved, and offer the broader workflow. Resume an existing workspace at its earliest incomplete stage without repeating settled discovery.

## Recover Existing Full Workspaces Before Stage Routing

For an existing `full` workspace, inspect saved state before selecting Stage 1, Stage 2, or Stage 3. If `decision_tree` is missing or empty while a confirmed product definition or completed Stage 2 artifacts exist, read **Legacy workspace migration** in `references/decision-tree.md` and migrate before stage routing or handoff. This rule also applies when the user directly requests Stage 3: perform the migration before evaluating its entry gates.

A representation-only migration must preserve the actual confirmed requirements, constraints, decisions, assumptions, evidence, history, summary revision, and confirmation evidence. Derive stable decision nodes from the existing artifacts, validate the graph, and recompute the frontier; do not re-ask the user or repeat settled discovery. Then enter the earliest incomplete stage. If Stage 1 and Stage 2 are complete and current, continue to the Stage 3 gates. If migration exposes a substantive conflict, apply the summary-revision and reconfirmation rules instead of treating historical approval as current.

## Cross-Stage Invariants

- Follow the user's language in conversation and artifacts.
- Preserve stated constraints and non-goals. Separate verified facts, reasoned inferences, assumptions, and PoC-dependent claims.
- Use current authoritative evidence for drift-prone claims and keep source traceability.
- Do not overwrite reversals or stale conclusions; preserve history and invalidate dependents as defined in `references/decision-tree.md`.
- Keep research and actions legal, ethical, safe, and within the user's authorization. Surface permission, privacy, security, cost, and environment dependencies without implying certainty.
- Do not begin implementation, generate product code, install dependencies, or run a PoC while using this skill. A handoff does not authorize implementation.

## Full Discovery

For `full`, create the workspace at the first applicable location: a user-specified path; `docs/idear/<YYYY-MM-DD>-<slug>/` in the active repository; otherwise `work/idear/<YYYY-MM-DD>-<slug>/`. Use a stable ASCII slug and create an artifact only when its stage needs it. Templates live in `assets/templates/`.

### Stage 1 — Product Clarification

Read `references/decision-tree.md` and `references/stage-1-clarification.md`. Preserve the original wording in `00-raw-idea.md`, maintain the decision tree and confirmation state in `project-context.yaml`, and produce `01-product-definition.md` plus `decision-log.md`.

Ask only ranked frontier questions and preserve ownership: the user decides goals and values; the agent researches facts; environment-dependent claims become PoCs. Stage 1 completes only when every high-impact node is resolved or explicitly classified under the decision-tree rules and the user explicitly approves the latest summary revision. A correction or permission to use assumptions is not by itself approval of that revision.

### Stage 2 — Feasibility Research

Enter only from the latest confirmed product definition. Read `references/stage-2-research.md`, `references/evidence-standards.md`, and `references/report-design.md`. Link every material investigation to an active decision node or focused premise and stop when more evidence is unlikely to change the verdict, principal risks, direction, next PoC, or recommended action.

For `full`, maintain `02-research-dossier.md`, `04-risk-register.md`, `sources.yaml`, `decision-log.md`, and `project-context.yaml`. Create or maintain `03-competitor-analysis.md` only when an active decision node requires competitor, existing-solution, or differentiation evidence. Produce `05-feasibility-report.md` and a PDF when requested or supported. Lead the completion response with the verdict, decisive evidence, blockers, and next action; include closest alternatives only when an active decision node requires that comparison. When no active comparison or differentiation decision node exists, render a localized scope notice in the user's language stating that competitor work was not investigated because it is outside the active decision scope; do not perform competitor or comparison research merely to fill either output. Ask before Stage 3; feasibility alone does not authorize it.

### Stage 3 — Technical Path And Development Handoff

Enter Stage 3 only when the user elects to pursue the idea, asks for an implementation approach, or requests a development handoff. Read `references/stage-3-handoff.md`. Maintain `06-technical-paths.md`, `07-initial-solution.md`, `08-ai-handoff.md`, `decision-log.md`, and `project-context.yaml`.

Keep proposed, recommended, and user-confirmed directions distinct. Preserve requirement-to-architecture-to-acceptance traceability, unresolved gates, and every required PoC. Produce planning and validation artifacts only; transfer any later build request to an appropriate planning or implementation workflow.

## Context Authority

`project-context.yaml` is the authoritative machine-readable state for `full` discovery. Update it after every material clarification, finding, decision, reversal, risk, or Stage 3 state change. Preserve historical nodes and point them to replacements rather than deleting them. Keep generated artifacts synchronized with the current state and revisions.

A later development agent should read `project-context.yaml`, then `08-ai-handoff.md`, then linked evidence before proposing implementation work.
