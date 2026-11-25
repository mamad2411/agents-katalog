---
name: productize-product-simplification-via-via-negativa-analysis
description: >-
  Product simplification via Via Negativa analysis. Use when the user needs a product workflow
  for business analysis related to product simplification via via negativa analysis. Trigger
  terms: pm, business-analysis, simplification, via-negativa, strategy.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Product simplification via Via Negativa analysis

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

- **Skill**: `product-simplification-via-via-negativa-analysis`
- **Lifecycle**: Think
- **Category**: Strategy
- **Primary artifact**: Product simplification via Via Negativa analysis decision-framing brief with issue tree, assumptions, options, and recommended next step

Use this skill to run the Productize prompt contract for **Product simplification via Via Negativa analysis**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{INPUT}}
</provided_inputs>

GOAL
Apply Via Negativa to simplify `INPUT` by removing non-essential elements while preserving core purpose and functional integrity.
Success metric:
- Clearly defines core purpose.
- Identifies non-essential elements with rationale, benefits of removal, and tradeoffs.
- Produces a simplified version that remains aligned to the core purpose.
- Follows the required output structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required reasoning steps:
  1. Identify core purpose.
  2. Enumerate major elements/components.
  3. Test each element for necessity, value, replaceability, and complexity cost.
  4. Select removals/simplifications that preserve purpose.
  5. Evaluate downside risks of each removal.
- Keep recommendations concrete and grounded in provided input details.
- Prefer removal/simplification over additive fixes.
- Explicitly label assumptions when input details are ambiguous.

FORMAT
Return exactly this structure:

<via_negativa_analysis>
<core_purpose>
Briefly state the identified core purpose or main objective of the input.
</core_purpose>

<non_essential_elements>
List the elements you've identified as non-essential, explaining for each:
- Why it's considered non-essential
- How removing it could benefit the overall input
- Any potential drawbacks of its removal
</non_essential_elements>

<simplified_version>
Provide a simplified version of the input, focusing only on the essential elements that directly contribute to the core purpose.
</simplified_version>

<conclusion>
Summarize how the simplified version aligns better with the principles of Via Negativa and how it improves upon the original input in terms of clarity, efficiency, and focus.
</conclusion>
</via_negativa_analysis>

FAILURE
- Any required schema section is missing or malformed.
- Non-essential elements are listed without rationale, benefit, and drawback analysis.
- Simplified version changes core purpose or omits critical essentials.
- Claims are generic or not grounded in provided input.
- Assumptions are used but not explicitly stated.
