---
name: productize-churn-reduction-from-customer-data-and-exit-survey-analysis
description: >-
  Churn reduction from customer data and exit survey analysis. Use when the user needs a
  product workflow for business analysis related to churn reduction from customer data and
  exit survey analysis. Trigger terms: pm, business-analysis, churn, retention, analytics.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Churn reduction from customer data and exit survey analysis

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

- **Skill**: `churn-reduction-from-customer-data-and-exit-survey-analysis`
- **Lifecycle**: Growth
- **Category**: Growth
- **Primary artifact**: Churn diagnosis with retention levers, experiments, and follow-up research

Use this skill to run the Productize prompt contract for **Churn reduction from customer data and exit survey analysis**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{CHURN_DATA}}
- {{EXIT_SURVEY_RESPONSES}}
- {{ACTIVE_CUSTOMERS_BY_PERIOD_COHORT}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: Churn reduction from customer data and exit survey analysis.
Success metric:
- Completes all required tasks and decision logic from the prompt instructions.
- Output is specific, evidence-based, and actionable.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required analysis steps, sections, or validation logic.
- Keep recommendations/outputs grounded in the input context; avoid generic filler.
- Follow these task requirements:
<task_requirements>
- Use only evidence from `CHURN_DATA`, `EXIT_SURVEY_RESPONSES`, and `ACTIVE_CUSTOMERS_BY_PERIOD_COHORT`; if data is missing, state assumptions explicitly.
- Use these metric definitions:
  - Customer churn rate = `churned_customers_in_period / active_customers_start`.
  - MRR churn rate = `churned_mrr_in_period_usd / active_mrr_start_usd`.
  - "Average customer lifetime" must be labeled as `churned-user tenure proxy` unless full customer lifecycle data is provided.
- Compute churn rate using denominator data from `ACTIVE_CUSTOMERS_BY_PERIOD_COHORT`; include overall and cohort-level rates when possible.
- If denominator data is insufficient for any requested slice, state "not computable for this slice" and use explicit proxy metrics (churn events, churned MRR) for that slice.
- Analyze both quantitative patterns (rate, lifetime, segment/time trends) and qualitative churn reasons (theme categories from exits).
- Prioritize interventions by estimated impact x feasibility.
- Include short-term (0-30 days), medium-term (31-90 days), and long-term (90+ days) actions.
- Every recommendation must trace to a specific churn reason or segment pattern.
- For each prioritized key insight, provide at least one specific strategy.
- If churned-user sample counts in `CHURN_DATA`/`EXIT_SURVEY_RESPONSES` differ from denominator totals in `ACTIVE_CUSTOMERS_BY_PERIOD_COHORT`, explicitly disclose the mismatch and treat sample-derived insights as directional.
- Do not add impact estimates from overlapping cohorts (e.g., `incident_exposed` and `price_change_seen`) as if independent; call out overlap risk.
- Do not give generic advice without a data link.
</task_requirements>

FORMAT
Return exactly this structure:

<churn_reduction_plan>
1. Data Analysis Summary
- Current churn rate (overall + by key period/cohort), churned-user tenure proxy, and relevant baseline metrics
- Denominator coverage check (which churn rates are computable vs not computable)
- Sample alignment check (sample sizes, coverage, and mismatch disclosure if present)
- Churned-user profile patterns (segments, behavior, timing)
- Exit-survey theme breakdown with frequency or relative weight

2. Key Insights (3-5, prioritized)
- Insight title
- Evidence (data points/themes supporting it)
- Why it matters for churn reduction

3. Targeted Strategies
- Linked insight:
- Issue to solve:
- Action plan:
- Time horizon: Short-term | Medium-term | Long-term
- Owner suggestion:
- Success metrics (leading + lagging):
- Expected effect on churn:

4. Monitoring and Adjustment
- Review cadence
- Instrumentation and dashboard checks
- Decision rules for doubling down, iterating, or stopping actions

5. Expected Impact
- Estimated churn reduction range using scenario bands: Conservative | Base | Aggressive
- Time to observe impact
- Key assumptions and risks
</churn_reduction_plan>

FAILURE
- Output misses required sections, steps, or reasoning required by `<task_requirements>`.
- Required format/schema is missing, malformed, or incomplete.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
