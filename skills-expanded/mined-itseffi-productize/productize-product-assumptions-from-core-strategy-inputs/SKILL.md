---
name: productize-product-assumptions-from-core-strategy-inputs
description: >-
  Product assumptions from core strategy inputs. Use when the user needs a product workflow
  for user research related to product assumptions from core strategy inputs. Trigger terms:
  user-research, assumptions, product-strategy.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Product assumptions from core strategy inputs

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

- **Skill**: `product-assumptions-from-core-strategy-inputs`
- **Lifecycle**: Discover
- **Category**: Discovery
- **Primary artifact**: Product assumptions from core strategy inputs research brief with evidence, insight clusters, assumptions, and next validation steps

Use this skill to run the Productize prompt contract for **Product assumptions from core strategy inputs**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- `{{PRODUCT_DESCRIPTION}}`: Product concept, scope, and intended value.
- `{{CORE_PROBLEM}}`: Core user/business problem the product addresses.
- `{{TARGET_USER}}`: Primary target user segment(s).
</provided_inputs>

GOAL
Produce a rigorous, testable assumption set underlying the product strategy across desirability, feasibility, viability, and usability.
Success metric:
- Assumptions are specific, falsifiable, and impact-aware.
- Assumptions are non-duplicative across categories and grounded in provided inputs.
- Output follows the required plain-text structure exactly.

CONSTRAINTS
- Use only provided inputs and disciplined inference.
- If any input is missing or vague, proceed with prudent defaults and note gaps only in `SUMMARY`.
- Do not use XML, HTML, angle-bracket tags, or code fences in the model output.
- Return only the required sections in the required order.
- Create exactly four assumption categories in this order:
- Desirability Assumptions
- Feasibility Assumptions
- Viability Assumptions
- Usability Assumptions
- Each category must contain at least 5 assumptions.
- Each assumption must be one numbered item with exactly two labeled lines:
- `Statement:` starts with `We believe that...`, is one idea only, specific/falsifiable, and max 35 words.
- `Impact if wrong:` one concise sentence describing concrete consequence (adoption, cost, timeline, risk, or strategy).
- Avoid repeating the same assumption across categories.
- Include measurable thresholds, segments, conditions, or timeframes where possible.
- Reflect relevant product-strategy realities (for example: compliance, integrations, data quality, reliability/SLOs, scalability, CAC/LTV, retention, pricing power, partner economics).

FORMAT
Return plain text only, using exactly this section structure and order:

ASSUMPTIONS LIST
Desirability Assumptions
1.
Statement: We believe that ...
Impact if wrong: ...

2.
Statement: We believe that ...
Impact if wrong: ...

[at least 5 items]

Feasibility Assumptions
1.
Statement: We believe that ...
Impact if wrong: ...

[at least 5 items]

Viability Assumptions
1.
Statement: We believe that ...
Impact if wrong: ...

[at least 5 items]

Usability Assumptions
1.
Statement: We believe that ...
Impact if wrong: ...

[at least 5 items]

SUMMARY
- Key risk themes across the four categories.
- Most critical assumptions to validate first.
- Any missing/vague input gaps and explicit defaults used.

FAILURE
- Output contains anything other than `ASSUMPTIONS LIST` followed by `SUMMARY`.
- Any category is missing, out of order, or has fewer than 5 assumptions.
- Any assumption is missing either `Statement:` or `Impact if wrong:`.
- Any `Statement:` does not start with `We believe that...`, exceeds 35 words, or contains multiple claims.
- Assumptions are generic, non-falsifiable, duplicated across categories, or not grounded in provided inputs.
- Missing/vague input handling is not explicitly documented in `SUMMARY`.
- Output includes XML/HTML tags, angle-bracket tags, or code fences.
