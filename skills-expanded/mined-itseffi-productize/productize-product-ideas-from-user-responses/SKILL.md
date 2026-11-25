---
name: productize-product-ideas-from-user-responses
description: >-
  Product ideas from user responses. Use when turning user answers, pain descriptions,
  workflow notes, or founder/customer responses into grounded product ideas for startups,
  internal tools, AI products, growth bets, or new product lines.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Product ideas from user responses

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

- **Skill**: `product-ideas-from-user-responses`
- **Lifecycle**: Discover
- **Category**: Venture / 0-1
- **Primary artifact**: Product opportunity brief with idea shortlist, target users, pains, wedges, value propositions, assumptions, and validation plan

Use this skill to run the Productize prompt contract for **Product ideas from user responses**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- `{{USER_RESPONSES}}`: User answers describing goals, workflow, pain points, constraints, and attempted solutions.
</provided_inputs>

GOAL
Generate software product ideas grounded in user responses. Ideas may be startup products, internal tools, AI-builder products, growth bets, workflow automations, or new product-line concepts depending on the user's context.
Success metric:
- Ideas directly map to concrete pains/opportunities in the provided responses.
- Output includes exactly ten distinct ideas with clear value propositions.
- Each idea is concise, specific, and formatted exactly as required.

CONSTRAINTS
- Use only `{{USER_RESPONSES}}`; if information is missing, state assumptions briefly before the ideas.
- Analyze responses for:
- User's overall goal.
- Process steps and current stage.
- Workflow location of the problem.
- Time/money-heavy pain points.
- Problem frequency.
- Previously attempted solutions.
- Propose only software product concepts or productized workflow concepts (conceptual feasibility is acceptable).
- Generate diverse ideas (avoid minor variants of the same concept).
- Each idea must include:
- A unique number.
- A catchy product name.
- A 40-80 word description.
- Each description must explain who it is for, what pain it addresses, and how it reduces friction, time, cost, risk, or uncertainty in the user's workflow.

FORMAT
Return exactly ten separate `<idea>` blocks in this pattern:

<idea>
[Number]. [Name]: [Description in 40-80 words]
</idea>

Rules:
- Numbering must run from `1` to `10` with no gaps or duplicates.
- Each `<idea>` block must be a separate paragraph.

FAILURE
- Fewer or more than 10 ideas are returned.
- Any idea is missing number, name, or description.
- Any description is outside 40-80 words.
- Ideas are generic, repetitive, or not grounded in `{{USER_RESPONSES}}`.
- Output does not use the required `<idea>` block format.
- Assumptions are needed but not explicitly stated.
