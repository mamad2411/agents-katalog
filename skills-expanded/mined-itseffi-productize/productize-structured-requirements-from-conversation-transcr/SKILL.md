---
name: productize-structured-requirements-from-conversation-transcripts
description: >-
  Structured requirements from conversation transcripts. Use when the user needs a product
  workflow for business analysis related to structured requirements from conversation
  transcripts. Trigger terms: pm, business-analysis, requirements, analysis, transcripts.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Structured requirements from conversation transcripts

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

- **Skill**: `structured-requirements-from-conversation-transcripts`
- **Lifecycle**: Plan
- **Category**: Delivery
- **Primary artifact**: Structured requirements from conversation transcripts delivery brief with scope, requirements, priorities, risks, and acceptance criteria

Use this skill to run the Productize prompt contract for **Structured requirements from conversation transcripts**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{CONVERSATION_TRANSCRIPT}}
- {{CONTEXT}}
</provided_inputs>

GOAL
Convert `CONVERSATION_TRANSCRIPT` (+ `CONTEXT`) into a MECE-structured requirements set, then provide a rigorous self-critique of extraction quality.
Success metric:
- Requirements are clear, actionable, and grouped with MECE logic.
- Each requirement is source-traceable and includes dependency/relationship notes where relevant.
- Self-criticism identifies weaknesses without proposing solutions.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip these analysis steps:
  1. Identify explicit requests, constraints, concerns, and implied needs.
  2. Organize requirements into MECE categories / issue-tree logic.
  3. Write requirements in precise, actionable language.
  4. Annotate source traceability and dependency relationships.
- Keep language unambiguous and implementation-relevant without over-specifying design/engineering internals.
- In self-criticism, identify issues only; do not propose fixes.
- Explicitly label assumptions inferred from context.

FORMAT
Return exactly this structure:

<requirements_analysis>
<executive_summary>[Main themes and scope]</executive_summary>
<requirements_categories>[MECE categories and issue-tree structure]</requirements_categories>
<individual_requirements>[Numbered requirements per category with source/dependency notes]</individual_requirements>
<dependencies_and_relationships>[Cross-references between requirements]</dependencies_and_relationships>
<assumptions>[Implied assumptions not explicitly stated in transcript]</assumptions>
</requirements_analysis>
<self_criticism>
<inconsistencies>[List only]</inconsistencies>
<contradictions>[List only]</contradictions>
<over_specification>[List only]</over_specification>
<under_specification>[List only]</under_specification>
<missing_elements>[List only]</missing_elements>
<scope_creep>[List only]</scope_creep>
</self_criticism>

FAILURE
- Any required schema section is missing or malformed.
- Requirements are generic, non-actionable, or not traceable to transcript/context.
- MECE structure is absent or internally overlapping/confusing.
- Self-criticism includes solution proposals instead of issue identification only.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
