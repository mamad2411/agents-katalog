---
name: productize-root-cause-and-consequence-analysis-from-a-question
description: >-
  Root cause and consequence analysis from a question. Use when the user needs a product
  workflow for decision making related to root cause and consequence analysis from a question.
  Trigger terms: pm, decision-making, analysis, root-causes, reasoning.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Root cause and consequence analysis from a question

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

- **Skill**: `root-cause-and-consequence-analysis-from-a-question`
- **Lifecycle**: Think
- **Category**: Strategy
- **Primary artifact**: Root cause and consequence analysis from a question decision-framing brief with issue tree, assumptions, options, and recommended next step

Use this skill to run the Productize prompt contract for **Root cause and consequence analysis from a question**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{INITIAL_QUESTION}}
</provided_inputs>

GOAL
Identify plausible root causes and downstream consequences of `INITIAL_QUESTION` using recursive why-analysis and first-principles reasoning.
Success metric:
- Performs a deep why-chain (target depth: at least 5 levels or until a defensible root cause boundary).
- Explores consequence orders from first through fifth (positive and negative where plausible).
- Distinguishes assumptions from inferred facts and flags logic gaps.
- Follows the required output structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required analysis layers:
  1. Recursive why-analysis.
  2. Consequence chain (1st to 5th order).
  3. First-principles reconstruction.
- For why-analysis, explore parallel branches when multiple plausible causes emerge.
- For consequence analysis, include both upside and downside outcomes when credible.
- Keep reasoning neutral and explicit; avoid unsupported certainty.
- Clearly label assumptions and unknowns.

FORMAT
Return exactly this structure:

<analysis>
<root_causes>
[List your "Why?" questions and answers here, showing the progression to the root cause(s)]
</root_causes>

<consequences>
[Describe the potential consequences here, from first-order to fifth-order]
</consequences>

<first_principles>
[Present your first principles analysis here, including fundamental truths, questioned assumptions, and any identified gaps]
</first_principles>

<conclusion>
[Summarize your key findings and insights]
</conclusion>
</analysis>

FAILURE
- Required schema is missing or malformed.
- Why-analysis is shallow (no meaningful depth/branching) or lacks root-cause rationale.
- Consequence analysis does not cover first through fifth order.
- First-principles section does not separate assumptions from fundamentals.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
