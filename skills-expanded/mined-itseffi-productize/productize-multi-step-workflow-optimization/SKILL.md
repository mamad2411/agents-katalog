---
name: productize-multi-step-workflow-optimization
description: >-
  Multi-step workflow optimization. Use when the user needs a product workflow for design &
  prototyping related to multi-step workflow optimization. Trigger terms: ux, workflow,
  friction, funnels, optimization.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Multi-step workflow optimization

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

- **Skill**: `multi-step-workflow-optimization`
- **Lifecycle**: Design
- **Category**: Design
- **Primary artifact**: Multi-step workflow optimization UX/design review with findings, constraints, fixes, and acceptance checks

Use this skill to run the Productize prompt contract for **Multi-step workflow optimization**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{CURRENT_WORKFLOW}}
- {{USER_ANALYTICS}}
- {{DROP_OFF_DATA}}
- {{USER_FEEDBACK}}
- {{BUSINESS_CONSTRAINTS}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: "Multi-step workflow optimization".
Success metric:
- Produces a full current-state workflow diagnosis with per-step friction and necessity classification.
- Proposes a lower-friction workflow that improves completion/time while preserving required safeguards.
- Includes a measurable validation plan (A/B or staged rollout) and post-launch iteration logic.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs; if data is missing, state assumptions explicitly.
- Analyze the current workflow end-to-end before proposing changes.
- Provide per-step diagnosis including purpose, required inputs, validation, completion/time, errors, friction type, and necessity.
- Identify top friction points across redundancy, repetition, validation friction, progress clarity, save/resume, cognitive load, technical friction, and emotional friction.
- Propose optimizations that reduce steps/time/drop-off while preserving required legal, security, and quality checkpoints.
- Keep recommendations specific, testable, and measurable against baseline metrics.
- Include experimentation and rollout plan with success criteria, rollback conditions, and post-launch monitoring.
- If exact metrics are unavailable, provide directional estimates and clearly mark them as assumptions.

FORMAT
Return exactly this structure:

<workflow_optimization>
<executive_summary>
**Current State:**
- Total steps: [X]
- Average completion rate: [Y%]
- Average time to complete: [Z minutes]
- Primary drop-off point: [Step N - why]

**Proposed State:**
- Total steps: [X - reduced by N]
- Expected completion rate: [Y + N%]
- Expected time to complete: [Z - N minutes]
- Key improvements: [3-5 bullet points]

**Expected Impact:**
- [Metric]: [Current → Target]
- [Metric]: [Current → Target]
- [Business impact]: [e.g., "10% increase in signups = $X additional revenue/month"]
</executive_summary>

<current_workflow_analysis>
**Overall Metrics:**
- Steps: [Total count]
- Completion Rate: [X% - what percent of users who start actually finish]
- Average Time: [Minutes/seconds]
- Median Time: [If significantly different from average, indicates confusion for some users]
- Abandonment Rate: [100 - completion rate]

**Drop-off Analysis:**
- Step 1: [Name] - [Y% complete this step] - [W% abandon]
- Step 2: [Name] - [Y% complete] - [W% abandon] ⚠️ [High drop-off? Why?]
- Step 3: [Name] - [Y% complete] - [W% abandon]
- [Continue for all steps]

**Top 3 Friction Points:**
1. [Step/Issue]: [X% abandon] - [Why this is painful]
2. [Step/Issue]: [Y% abandon] - [Why this is painful]
3. [Step/Issue]: [Z% abandon] - [Why this is painful]

**Detailed Step Analysis:**

For each step, provide:

**Step 1: [Name]**
- **What user does:** [Actions required - e.g., "Enter name, email, phone number"]
- **Why step exists:** [Purpose - e.g., "Account creation requires contact info"]
- **Inputs required:** [List of fields]
  - [Field]: [Required/Optional] - [Source of data - user memory, lookup, calculation]
- **Validation:** [What's checked - e.g., "Email format, phone number format"]
- **Completion rate:** [X%] - [Y% drop off at this step]
- **Average time:** [Z seconds]
- **Common errors:** [What goes wrong - e.g., "15% of users enter invalid email format"]
- **Friction type:** [Redundant/Complex/Unclear/Tedious/Unnecessary]
- **Problem statement:** [What makes this step difficult or annoying]
- **Necessity:** ✅ Required (cannot remove) / ⚠️ Required but could be improved / ❌ Unnecessary (can remove or defer)

**Step 2: [Name]**
[Same detailed structure]

[Continue for all steps]

</current_workflow_analysis>

<optimization_strategies>
[Describe which of the strategies above you are applying to this workflow, and how.]
</optimization_strategies>

<optimized_workflow>
[Describe the new, optimized workflow step-by-step, including which steps were removed, combined, or deferred, and the expected impact on metrics.]
</optimized_workflow>

<what_we_keep>
[List the critical checkpoints, validations, and safeguards you are intentionally preserving, and why they remain necessary.]
</what_we_keep>

<testing_plan>
[Outline the A/B test or rollout approach you will use to validate the improved workflow.]
</testing_plan>

<monitoring_and_iteration>
[Describe how you will monitor post-launch performance and iterate based on data and feedback.]
</monitoring_and_iteration>
</workflow_optimization>

FAILURE
- Any required section/tag from `FORMAT` is missing, malformed, or materially incomplete.
- Current workflow analysis lacks per-step necessity or friction classification.
- Proposed optimizations remove required safeguards without justification.
- Testing plan lacks control/variant definition or clear decision criteria.
- Monitoring plan lacks actionable metrics or iteration logic.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
