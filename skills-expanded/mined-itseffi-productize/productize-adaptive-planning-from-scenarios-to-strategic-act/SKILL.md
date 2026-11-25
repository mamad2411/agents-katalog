---
name: productize-adaptive-planning-from-scenarios-to-strategic-actions
description: >-
  Adaptive planning from scenarios to strategic actions. Use when the user needs a product
  workflow for product strategy related to adaptive planning from scenarios to strategic
  actions. Trigger terms: strategic-planning, facilitation, product-management,
  decision-making, frameworks.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Adaptive planning from scenarios to strategic actions

## Productize Preamble

Before producing the artifact, implementation step, or code change, classify the work:

- **User/persona**: founder, product leader, AI PM, AI builder, stakeholder, or mixed/unknown.
- **Product stage**: idea, validation, PMF search, growth, scale, pivot, or unknown.
- **Artifact mode**: strategy memo, PRD, research plan, positioning, experiment, deck, roadmap, execution brief, diagnostic, or decision record.
- **Artifact format**: Markdown for short, repo-native, diff-sensitive artifacts; self-contained HTML for long, visual, shareable, interactive, or explicitly requested artifacts.
- **Evidence standard**: what is known, assumed, missing, and risky.
- **Decision mode**: recommend, ask for a blocking input, or proceed with explicit assumptions.

Operating rules:

1. Do not produce generic product strategy filler. Tie every recommendation to the user's context, evidence, stage, and decision pressure.
2. Separate facts from assumptions. Convert high-risk assumptions into tests, research prompts, or instrumentation.
3. Search existing context, attached docs, repo files, or prior Productize artifacts before inventing new structure when those sources are available.
4. Ask only for inputs that materially change the output. If the next step is obvious, proceed and state assumptions.
5. If another Productize skill is a better fit, name it and explain the routing in one sentence before continuing.
6. Enforce the output contract for this skill. Produce the artifact, implementation step, verification evidence, or code change; do not stop at a meta-explanation of the method.
7. End with the concrete next action, decision owner, validation step, metric, or artifact handoff when applicable.
8. Use the user's saved Productize preferences when available, but do not let stale preferences override explicit instructions in the current request.
9. If you must ask a blocking question, use this compact format: `AskUserQuestion: <one question> Why it matters: <decision it changes>`.
10. Record completion status for durable work as `completed`, `blocked`, `deferred`, or `needs-review` when runtime hooks are available.

Artifact format policy:

- Default to Markdown for short notes, repo-native documentation, changelog fragments, or artifacts where clean source diffs matter.
- Use a self-contained HTML file when the user asks for HTML, the artifact is likely to exceed about 100 lines, the reader needs diagrams/tables/comparisons/screenshots, the artifact is meant to be shared, or interaction/export controls would help the user stay in the loop.
- Route by product job first, then choose the format. Do not create a generic HTML workflow when a Productize playbook, gate, or routed skill owns the work.
- HTML artifacts must be local-first and portable: one file, embedded CSS/JS, no remote dependencies unless explicitly requested, readable without a dev server, responsive, accessible, and easy to skim.
- Prefer semantic sections, tables, SVG diagrams, annotated code blocks, status chips, collapsible detail, and copy/export buttons when they improve review speed. Avoid decorative complexity that hides the decision.
- For implementation work with ambiguities, use `$implementation-notes` when the user asks for a running notes file, especially `implementation-notes.html` or `implementation-notes.md`.

Runtime hooks, if available:

- Use `productize-workflow start "<user request>"` at the beginning of durable product work; it restores context, routes the request, records the session, and returns the required artifact contract.
- Use `productize-workflow complete --id <id> --status completed|blocked|deferred|needs-review --artifact-type <type> --summary <summary>` before ending durable product work; it records the artifact, saves context, and logs completion status.
- Use `productize-update-check --strict` at the start of maintenance, setup, release, or generated-output work.
- Use `productize-config` to read or write user/team preferences such as persona, artifact mode, evidence threshold, or update-check policy.
- Use `productize-session-log` to record important workflow decisions.
- Use `productize-artifact-log` when a durable artifact is produced.
- Use `productize-context-restore` before restarting long-running product work from scratch.
- Use `productize-context-save` after producing a durable strategy, research, spec, or stakeholder artifact.
- Use `productize-registry-search` or `productize-skill-router` when routing is ambiguous.
- Use `productize-completion-status` to log whether the workflow completed, blocked, deferred, or needs review.

Telemetry standard:

- Keep telemetry local by default in `.productize/` or `PRODUCTIZE_STATE_DIR`.
- Log artifact type, routing decision, evidence gaps, and completion status; do not log secrets or private customer data unless the user explicitly asks for it.

Current skill metadata:

- **Skill**: `adaptive-planning-from-scenarios-to-strategic-actions`
- **Lifecycle**: Strategize
- **Category**: Strategy
- **Primary artifact**: Adaptive planning from scenarios to strategic actions strategy memo with choices, tradeoffs, risks, and recommended next move

Use this skill to run the Productize prompt contract for **Adaptive planning from scenarios to strategic actions**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{CURRENT_STATE}}
- {{PROJECTED_MESS}}
- {{IDEAL_FUTURE}}
- {{IDEAL_CURRENT_STATE}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: Adaptive planning from scenarios to strategic actions.
Success metric:
- Produces a complete four-quadrant analysis and feedback loop grounded in the provided scenarios.
- Identifies concrete adjustments and capabilities to avoid the projected mess and enable the ideal future.
- Ends with a concise, actionable plan with specific next steps.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only `{{CURRENT_STATE}}`, `{{PROJECTED_MESS}}`, `{{IDEAL_FUTURE}}`, and `{{IDEAL_CURRENT_STATE}}`; if missing data is critical, state assumptions explicitly.
- Address all four quadrants and the feedback loop, grounded in provided inputs.
- Keep analysis specific and actionable; avoid generic leadership or capability lists.
- Action plan must include concrete steps that bridge current to ideal while mitigating projected mess.

FORMAT
Return exactly this structure:

<adaptive_planning_analysis>
<quadrant_1_analysis>
[Your analysis of the Current State]
</quadrant_1_analysis>

<quadrant_2_analysis>
[Your analysis of the Projected Mess]
</quadrant_2_analysis>

<quadrant_3_analysis>
[Your analysis of the Ideal Future]
</quadrant_3_analysis>

<quadrant_4_analysis>
[Your analysis of the Ideal Current State]
</quadrant_4_analysis>

<feedback_loop_analysis>
<current_state_adjustments>
[Your recommendations for current state adjustments]
</current_state_adjustments>

<avoiding_projected_mess>
[Your recommendations for avoiding the projected mess]
</avoiding_projected_mess>

<enabling_ideal_future>
[Your recommendations for enabling the ideal future]
</enabling_ideal_future>
</feedback_loop_analysis>

<summary_and_action_plan>
[Your concise summary and specific, actionable steps]
</summary_and_action_plan>
</adaptive_planning_analysis>

FAILURE
- Any required section/tag in `FORMAT` is missing, malformed, or incomplete.
- Feedback loop omits one of the three adjustment categories.
- Action plan lacks concrete, actionable steps linked to the quadrants.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
