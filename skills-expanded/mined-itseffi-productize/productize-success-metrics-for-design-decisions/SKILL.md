---
name: productize-success-metrics-for-design-decisions
description: >-
  Success metrics for design decisions. Use when the user needs a product workflow for
  business analysis related to success metrics for design decisions. Trigger terms: pm,
  success-metrics, business-analysis, design.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Success metrics for design decisions

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

- **Skill**: `success-metrics-for-design-decisions`
- **Lifecycle**: Design
- **Category**: Analytics
- **Primary artifact**: Success metrics for design decisions UX/design review with findings, constraints, fixes, and acceptance checks

Use this skill to run the Productize prompt contract for **Success metrics for design decisions**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{DESIGN_GOALS}}
- {{PRODUCT_CONTEXT}}
- {{USER_OUTCOMES}}
</provided_inputs>

GOAL
Translate `DESIGN_GOALS`, `PRODUCT_CONTEXT`, and `USER_OUTCOMES` into a measurable success-metrics system for design decisions.
Success metric:
- Defines success from user, business, and product perspectives.
- Produces primary/secondary/guardrail/leading metrics with SMART definitions.
- Includes instrumentation, baseline/target logic, and decision-ready analysis plan.
- Follows the required output structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required metric-design steps:
  1. Define success (user/business/product).
  2. Map metric types (behavior, outcome, business, quality, leading).
  3. Apply SMART criteria to each key metric.
  4. Define measurement approach (instrumentation, tools, sample/stat criteria).
  5. Set baselines and targets (minimum, target, stretch, timeframe).
  6. Add guardrails for unintended consequences.
- Keep metrics decision-oriented and linked to design goals (avoid vanity metrics).
- Explicitly note risks/limitations where metrics may not capture full reality.
- Label assumptions clearly when baseline/tooling/sample data is incomplete.

FORMAT
Return exactly this structure:

<success_metrics_framework>
<success_definitions>
**User Success Means:**
[Describe what improves from user perspective - concrete outcomes]

**Business Success Means:**
[Describe what improves from business perspective - concrete outcomes]

**Product Success Means:**
[Describe what improves in the product - concrete outcomes]
</success_definitions>

<primary_metrics>
<metric_1>
**Metric Name:** [Clear, specific metric name]

**What It Measures:** [Exactly what behavior or outcome]

**Why It Matters:** [How it connects to goals]

**Type:** [Behavior/Outcome/Business/Quality]

**Measurement Method:**
- How: [Specific tracking approach]
- Where: [What system/tool]
- Frequency: [How often measured]
- Sample: [Who/what is included]

**Current Baseline:** [If known, current performance]

**Targets:**
- Minimum acceptable: [X%/number]
- Target: [Y%/number]
- Stretch: [Z%/number]
- Timeframe: [When to measure]

**Statistical Criteria:**
- Sample size needed: [N users/sessions]
- Significance level: [e.g., 95% confidence]
- Minimum detectable effect: [smallest meaningful change]

**Risks/Limitations:**
[What could make this metric misleading? What doesn't it capture?]
</metric_1>

<metric_2>
[Repeat structure for 3-5 primary metrics]
</metric_2>
</primary_metrics>

<supporting_metrics>
[List 3-5 secondary metrics that provide additional context:
- Metric name: [Description, why it's useful]
- Metric name: [Description, why it's useful]]
</supporting_metrics>

<guardrail_metrics>
[Metrics to ensure you're not causing harm:
- Metric: [Description]
- Threshold: [What value would indicate a problem]
- Why: [What unintended consequence this guards against]]
</guardrail_metrics>

<leading_indicators>
[Metrics that predict success before primary metrics show results:
- Indicator: [Description]
- Why it predicts success: [Connection to outcomes]
- When to measure: [Timeline]]
</leading_indicators>

<measurement_plan>
**Implementation Requirements:**
- Events to track: [List specific events]
- Properties to capture: [Data points per event]
- Tools needed: [Analytics platform, A/B test framework, survey tool, etc.]
- Team dependencies: [Who needs to implement]
- Timeline: [When instrumentation will be ready]

**Analysis Plan:**
- Segments to analyze: [User cohorts, use cases, etc.]
- Comparison approach: [A/B test, before/after, cohort comparison]
- Reporting cadence: [Daily/Weekly/Monthly]
- Decision timeline: [When to make go/no-go decision]

**Baseline Collection:**
[If redesign, describe how to establish current state before changes]
</measurement_plan>

<tradeoff_framework>
[How to make decisions when metrics conflict:
- If [Metric A] improves but [Metric B] declines, prioritize [A/B] because [rationale]
- Acceptable tradeoffs: [What you're willing to sacrifice for what gain]
- Unacceptable tradeoffs: [What must never decline]]
</tradeoff_framework>

<qualitative_validation>
[How to supplement quantitative metrics:
- User interviews: [What to ask]
- Usability testing: [What to observe]
- Support tickets: [What patterns to look for]
- Feedback surveys: [What questions to include]]
</qualitative_validation>

<one_page_dashboard>
[Describe what a single-page success dashboard should show:
- Key metric tiles
- Trend visualization
- Segment breakdowns
- Guardrail status
- Action triggers]
</one_page_dashboard>
</success_metrics_framework>

FAILURE
- Any required schema section is missing or malformed.
- Metrics are not SMART or not clearly tied to design goals/outcomes.
- Baselines/targets/timeframes are missing for primary metrics.
- Guardrail or leading indicators are missing.
- Measurement plan lacks instrumentation detail or decision cadence.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
