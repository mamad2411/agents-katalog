---
name: productize-metric-drops-diagnosis-with-rigorous-stepwise-decomposition
description: >-
  Metric drops diagnosis with rigorous stepwise decomposition. Use when the user needs a
  product workflow for business analysis related to metric drops diagnosis with rigorous
  stepwise decomposition. Trigger terms: pm, business-analysis, analytics, metrics, diagnosis.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Metric drops diagnosis with rigorous stepwise decomposition

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

- **Skill**: `metric-drops-diagnosis-with-rigorous-stepwise-decomposition`
- **Lifecycle**: Strategize
- **Category**: Analytics
- **Primary artifact**: Metric drops diagnosis with rigorous stepwise decomposition strategy memo with choices, tradeoffs, risks, and recommended next move

Use this skill to run the Productize prompt contract for **Metric drops diagnosis with rigorous stepwise decomposition**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{METRIC_NAME}}
- {{FORMULA}}
- {{BASELINE_VALUE}}
- {{CURRENT_VALUE}}
- {{TIMEFRAME}}
- {{COMPARISON_WINDOWS}}
- {{DATA_SOURCES}}
- {{SEGMENT_DIMENSIONS}}
- {{KNOWN_EVENTS}}
</provided_inputs>

GOAL
Diagnose the root cause of a metric drop using stepwise decomposition from metric-level to driver-level to segment-level causes.
Success metric:
- Identifies whether the drop is real vs artifact.
- Isolates top driver(s), break timing, and highest-impact segment(s).
- Produces 1-3 testable hypotheses with confirm/refute criteria and next actions.
- Follows the required output structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Analyze in this exact sequence:
  1. Confirm drop validity (artifact checks).
  2. Decompose metric into 2-3 drivers from formula.
  3. Trend drivers to find break timing/pattern.
  4. Segment culprit driver and rank impact.
  5. Compare bad vs stable segments.
  6. Produce 1-3 ranked, testable hypotheses.
- For each subproblem include:
  - Goal
  - Method (queries/breakdowns/plots)
  - Decision rule
  - Findings
  - Next step
- Use explicit calculations where possible (delta or contribution attribution).
- If SQL schema is incomplete, provide minimal-field request plus pseudocode with placeholders.
- Always label confidence (`High`, `Med`, `Low`) and all assumptions.
- Do not stop at symptom-level statements; identify driver, segment, break date, and likely causal mechanism.

FORMAT
Return exactly this structure:

<metric_drop_diagnosis>
<subproblem_1>
[Goal, method, decision rule, findings, next step]
[Include table: period -> metric -> numerator/denominator -> data quality signals]
[Verdict: Real drop | Measurement artifact | Baseline skew]
</subproblem_1>
<subproblem_2>
[Driver tree]
[Driver table: driver -> baseline -> current -> % change -> contribution]
[Top culprit driver(s)]
</subproblem_2>
<subproblem_3>
[Break-date analysis by driver: break date, pattern (step/gradual), confidence]
[Candidate correlates from KNOWN_EVENTS]
</subproblem_3>
<subproblem_4>
[Impact-ranked segment table: segment -> baseline -> current -> delta -> volume share -> impact score]
[Largest contributing segment or broad-based note]
</subproblem_4>
<subproblem_5>
[Side-by-side comparison of bad vs stable segments]
[3-5 discriminative differences with numbers]
</subproblem_5>
<subproblem_6>
[1-3 ranked hypotheses]
Hypothesis:
Evidence so far:
Prediction:
Test:
Confirm if:
Refute if:
Owner/next action:
</subproblem_6>
<recommended_next_actions>[Immediate mitigations, next data pulls, experiments/rollbacks]</recommended_next_actions>
</metric_drop_diagnosis>

FAILURE
- Any required subproblem section is missing or out of sequence.
- Output lacks methods/decision rules/findings/next-step per subproblem.
- No driver decomposition or no impact-ranked segmentation.
- Hypotheses are not testable (missing confirm/refute criteria).
- Claims are generic or not grounded in provided inputs.
- Assumptions or confidence labels are missing.
- Required schema is malformed or incomplete.
