---
name: productize-post-launch-feedback-loop
description: >-
  Post-launch feedback loop. Use when the user needs a product workflow for business analysis
  related to post-launch feedback loop. Trigger terms: pm, feedback-loop, iteration,
  post-launch, continuous-improvement, business-analysis.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Post-launch feedback loop

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

- **Skill**: `post-launch-feedback-loop`
- **Lifecycle**: Launch & Learn
- **Category**: Discovery
- **Primary artifact**: Post-launch feedback loop launch learning report with release evidence, feedback, decision, and next iteration

Use this skill to run the Productize prompt contract for **Post-launch feedback loop**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{CURRENT_PROCESS}}
- {{PRODUCT_CONTEXT}}
- {{LAUNCH_TIMELINE}}
- {{TEAM_STRUCTURE}}
- {{AVAILABLE_DATA_SOURCES}}
</provided_inputs>

GOAL
Design a complete post-launch feedback loop system that turns product signals into prioritized iteration decisions.
Success metric:
- Defines checkpoint cadence with clear purpose and decision outputs.
- Specifies what to measure, how to synthesize signals, and how to prioritize action.
- Connects learnings to roadmap iteration and team operating rituals.
- Follows the required schema exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Keep recommendations grounded in `CURRENT_PROCESS`, `PRODUCT_CONTEXT`, `LAUNCH_TIMELINE`, `TEAM_STRUCTURE`, and `AVAILABLE_DATA_SOURCES`.
- Do not skip required analysis layers:
  - Current-state audit (gaps, latency, silos)
  - Time-based checkpoints (week 1, month 1, month 3, month 6, month 12)
  - Measurement framework (quantitative, qualitative, behavioral, technical)
  - Retrospective and learning capture process
  - Iteration planning integration and triage model
- For each checkpoint, define:
  - key questions,
  - data sources,
  - success criteria,
  - review meeting structure and outputs.
- Include both leading and lagging indicators with definitions, targets, source systems, and review cadence.
- Ensure triage rules are operational (SLA, owner, scoring logic, planning window).

FORMAT
Return exactly this structure:

<feedback_loop_framework>
<current_state_assessment>
[Existing feedback mechanisms, identified gaps, latency issues, and organizational silos/blockers]
</current_state_assessment>

<checkpoint_calendar>
<week_1_checkpoint>[Timeline, primary focus, key questions, data sources, success criteria, meeting/review details]</week_1_checkpoint>
<month_1_checkpoint>[Timeline, primary focus, key questions, data sources, success criteria, meeting/review details]</month_1_checkpoint>
<month_3_checkpoint>[Timeline, primary focus, key questions, data sources, success criteria, meeting/review details]</month_3_checkpoint>
<month_6_checkpoint>[Timeline, primary focus, key questions, data sources, success criteria, meeting/review details]</month_6_checkpoint>
<month_12_checkpoint>[Timeline, primary focus, key questions, data sources, success criteria, meeting/review details]</month_12_checkpoint>
</checkpoint_calendar>

<measurement_framework>
<quantitative_metrics>
[Leading indicators table/list + lagging indicators table/list + technical health indicators with definition, target, source, frequency]
</quantitative_metrics>
<qualitative_insights>
[User research schedule, support analysis method, sales/marketing feedback integration cadence]
</qualitative_insights>
<behavioral_monitoring>
[Unexpected pattern detection, workaround identification, feature misuse tracking]
</behavioral_monitoring>
</measurement_framework>

<retrospective_process>
<template>
[Structured template covering goals/hypotheses, validated and invalidated assumptions, surprises, key learnings, user quotes, quantitative highlights, recommendations]
</template>
<documentation_location>[Where learnings are stored and how they are indexed/retrieved]</documentation_location>
<review_meeting_structure>[Attendees, duration, pre-work, agenda, outputs]</review_meeting_structure>
</retrospective_process>

<iteration_planning_integration>
<triage_framework>
**Critical Issues (Address Immediately):**
- Definition: [What qualifies]
- Response time: [SLA]
- Decision maker: [Who can approve]

**High Priority (Next Sprint):**
- Definition: [What qualifies]
- Scoring formula: [How prioritized]
- Review cadence: [How often re-evaluated]

**Medium Priority (Next Quarter):**
- Definition: [What qualifies]
- Planning cycle: [When incorporated into roadmap]

**Low Priority (Backlog):**
- Definition: [What qualifies]
- Archive criteria: [When to deprioritize]
</triage_framework>
</iteration_planning_integration>
</feedback_loop_framework>

FAILURE
- Any required top-level section is missing or malformed.
- Checkpoint plan lacks timeline, data sources, success criteria, or decision outputs.
- Measurement framework lacks explicit metrics, definitions, or cadence.
- Triage/iteration process is vague or non-operational.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
