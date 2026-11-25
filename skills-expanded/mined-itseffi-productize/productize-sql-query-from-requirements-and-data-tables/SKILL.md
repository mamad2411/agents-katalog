---
name: productize-sql-query-from-requirements-and-data-tables
description: >-
  SQL query from requirements and data tables. Use when the user needs a product workflow for
  business analysis related to sql query from requirements and data tables. Trigger terms: pm,
  sql, analytics, data, business-analysis.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# SQL query from requirements and data tables

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

- **Skill**: `sql-query-from-requirements-and-data-tables`
- **Lifecycle**: Design
- **Category**: Analytics
- **Primary artifact**: SQL query from requirements and data tables UX/design review with findings, constraints, fixes, and acceptance checks

Use this skill to run the Productize prompt contract for **SQL query from requirements and data tables**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{DATA_TABLES_OVERVIEW}}
- {{QUERY_CRAFTING_REQUIREMENTS}}
</provided_inputs>

GOAL
Produce a correct, performant, and maintainable SQL query from `DATA_TABLES_OVERVIEW` and `QUERY_CRAFTING_REQUIREMENTS`.
Success metric:
- SQL satisfies requirements and uses valid joins/filters/aggregations.
- Query is optimized for readability and execution efficiency.
- Major logic choices and assumptions are clearly explained.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required SQL design steps:
  - relevant table joins,
  - filter conditions,
  - aggregations/calculations,
  - subqueries/CTEs where helpful.
- Prefer explicit selected columns (avoid `SELECT *` unless explicitly required).
- Use meaningful aliases and readable formatting.
- Add concise inline comments only for non-obvious logic.
- Include assumptions when schema or requirements are ambiguous.
- If requirements are under-specified, produce best-effort SQL and state what data/constraints would finalize it.
- Default policy for ambiguities (apply unless `QUERY_CRAFTING_REQUIREMENTS` explicitly overrides):
  - **Top-5 rule:** return exactly 5 rows per month using `ROW_NUMBER()` with deterministic tie-break (`ORDER BY net_revenue_usd DESC, category ASC`).
  - **Multi-category revenue attribution:** allocate order revenue proportionally by category share of item extended value (`quantity * unit_price`) within each order; do not attribute full order revenue to every category.
  - **Payment-attempt attribution by category:** attribute payment attempts/failures to each category touched by an order (order-category level attribution), and explicitly disclose that summed category-level counts can exceed overall totals.
  - **Payment time scope:** when reporting period filters are defined for orders, filter payment attempts to the same period using `payments.attempted_at` unless explicitly instructed otherwise.
- SQL must be executable with standard ASCII SQL syntax:
  - Use `'single quotes'` for string literals.
  - Use `--` for line comments.
  - Do not use typographic quotes/dashes or other smart punctuation.
- Keep explanation plain text (no unusual control characters, copy artifacts, or decorative bullets).
- If metrics are attributed to multiple categories (for multi-category orders), explicitly state that totals across categories may exceed overall order/payment totals.

FORMAT
Return exactly this structure:

<sql_query>
-- SQL query with formatting and comments
</sql_query>
<query_explanation>
- Join strategy and why each join type is used
- Filter logic and business-rule mapping
- Aggregations/calculations rationale
- Performance considerations (indexes, cardinality, scan reduction, CTE/subquery choices)
- Assumptions and known limitations
</query_explanation>

FAILURE
- Missing `<sql_query>` or `<query_explanation>` section.
- SQL does not match stated requirements.
- Uses `SELECT *` without explicit requirement.
- Join/filter/aggregation logic is unclear or unsupported in explanation.
- SQL contains non-ASCII smart punctuation that breaks execution (e.g., `‘ ’`, `“ ”`, `–`).
- Explanation contains copy artifacts or unreadable formatting.
- Output violates default ambiguity policies (top-5 cardinality, revenue attribution, payment attribution, or payment time scope) without explicit requirement override.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
