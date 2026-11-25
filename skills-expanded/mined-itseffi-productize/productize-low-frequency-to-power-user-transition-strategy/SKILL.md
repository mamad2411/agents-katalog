---
name: productize-low-frequency-to-power-user-transition-strategy
description: >-
  Low-Frequency-to-Power-User Transition Strategy. Use when the user needs a product workflow
  for product strategy related to low-frequency-to-power-user transition strategy. Trigger
  terms: product-strategy, engagement, activation, retention.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Low-Frequency-to-Power-User Transition Strategy

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

- **Skill**: `low-frequency-to-power-user-transition-strategy`
- **Lifecycle**: Growth
- **Category**: Growth
- **Primary artifact**: Low-Frequency-to-Power-User Transition Strategy growth playbook with bottleneck, segment, experiments, triggers, and sustainability checks

Use this skill to run the Productize prompt contract for **Low-Frequency-to-Power-User Transition Strategy**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{PRODUCT_DESCRIPTION}}
- {{CURRENT_USE_CASE}}
- {{TARGET_USE_CASE}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: Low-Frequency-to-Power-User Transition Strategy.
Success metric:
- Produces a concrete transition plan from low-frequency to high-frequency usage.
- Aligns strategy to current and target use cases with explicit behavioral gaps.
- Includes metrics, timeline, and rollout/education plans grounded in the inputs.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only `{{PRODUCT_DESCRIPTION}}`, `{{CURRENT_USE_CASE}}`, and `{{TARGET_USE_CASE}}`; if information is missing, state assumptions explicitly.
- Identify the behavioral gap between current and target usage.
- Provide step-by-step transition plan, education/onboarding, and communication strategy.
- Include rollout plan, key metrics, and timeline for measurement.
- Keep recommendations specific and grounded in the provided context.

FORMAT
Return exactly this structure:

<transition_strategy>
1. Current Use Case Analysis:
   [Provide a brief analysis of the current low-frequency use case]

2. Target Use Case Analysis:
   [Provide a brief analysis of the target high-frequency use case]

3. User Behavior and Needs:
   [Summarize key insights about user behavior and needs]

4. Transition Strategy:
   a. Feature Introduction Plan:
      [Outline the step-by-step plan for introducing new features]
   b. User Education and Onboarding:
      [Describe the approach for educating users about the new use case]
   c. Communication Strategy:
      [Outline the key messages and channels for communicating the benefits]
   d. Gradual Rollout Plan:
      [Describe the approach for gradually introducing new functionality]

5. Implementation and Measurement:
   a. Key Metrics:
      [List the primary metrics to track for measuring success]
   b. Timeline:
      [Provide a high-level timeline for implementation and evaluation]
   c. Feedback and Iteration:
      [Describe the plan for collecting user feedback and making improvements]

6. Potential Challenges and Mitigation Strategies:
   [Identify potential obstacles and propose solutions]

7. Conclusion:
   [Summarize the key points of the transition strategy and its potential impact]
</transition_strategy>

FAILURE
- Any required section/tag in `FORMAT` is missing, malformed, or incomplete.
- Behavioral gap or barriers are not explicitly identified.
- Metrics or timeline are missing.
- Strategies are generic or not tied to the given use cases.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
