---
name: productize-innovative-product-ideas-from-structured-brainstorming
description: >-
  Innovative product ideas from structured brainstorming. Use when the user needs a product
  workflow for ideation & creativity related to innovative product ideas from structured
  brainstorming. Trigger terms: brainstorming, product-ideas, structured-ideation, creativity,
  product-management.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Innovative product ideas from structured brainstorming

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

- **Skill**: `innovative-product-ideas-from-structured-brainstorming`
- **Lifecycle**: Think
- **Category**: Discovery
- **Primary artifact**: Innovative product ideas from structured brainstorming product artifact with evidence, risks, recommendation, and next action

Use this skill to run the Productize prompt contract for **Innovative product ideas from structured brainstorming**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{TOPIC}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: "Innovative product ideas from structured brainstorming".
Success metric:
- Produces a complete structured brainstorming session from divergence to convergence.
- Generates non-obvious product ideas grounded in the topic and validated via bias checks.
- Returns exactly 3 top ideas with clear innovation rationale in abstract terms.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only `{{TOPIC}}`; if scope is unclear, state assumptions explicitly.
- Run all stages: free association, mind map, SCAMPER expansion, bias check, top-idea selection, summary.
- Avoid banal, overhyped, or clichéd outputs.
- Top ideas must be described abstractly; do not use specific tech buzzwords such as `AI`, `blockchain`, or `VR`.
- Ensure ideas are distinct and traceable to earlier brainstorming artifacts.

FORMAT
Return exactly this structure:

<brainstorming_session>

<free_association>
1. [Word or phrase]
2. [Word or phrase]
...
[Total 8-10 items]
</free_association>

<mind_map>
[Topic]
- [Main branch 1]
  - [Sub-branch 1a]
  - [Sub-branch 1b]
- [Main branch 2]
  - [Sub-branch 2a]
  - [Sub-branch 2b]
- [Main branch 3]
  - [Sub-branch 3a]
  - [Sub-branch 3b]
[At least 3 main branches; each with 2-3 sub-branches]
</mind_map>

<scamper>
- Branch: [Name]
  - Technique 1: [SCAMPER letter + method]
    - Application: [How applied]
    - New ideas:
      - [Idea]
  - Technique 2: [SCAMPER letter + method]
    - Application: [How applied]
    - New ideas:
      - [Idea]
[Repeat for 3 branches]
</scamper>

<bias_check>
- Bias: [Name]
  - Evidence in ideas: [How it appears]
  - Countermeasure: [Concrete action]
[At least 1 bias]
</bias_check>

<top_ideas>
1. [Idea title]
   - Description (2-3 sentences): [Abstract description]
   - Why innovative/non-obvious: [Rationale]
   - Topic fit (abstract): [How it addresses topic]
2. [Idea title]
   - Description (2-3 sentences): [Abstract description]
   - Why innovative/non-obvious: [Rationale]
   - Topic fit (abstract): [How it addresses topic]
3. [Idea title]
   - Description (2-3 sentences): [Abstract description]
   - Why innovative/non-obvious: [Rationale]
   - Topic fit (abstract): [How it addresses topic]
</top_ideas>

<summary>
[Brief recap of process and why final ideas are stronger after SCAMPER and bias checks]
</summary>

</brainstorming_session>

FAILURE
- Root tag `<brainstorming_session>` or any required sub-tag is missing, malformed, or incomplete.
- `free_association` has fewer than 8 or more than 10 items.
- `mind_map` has fewer than 3 main branches or insufficient sub-branches.
- `scamper` does not cover 3 branches with 2 techniques each.
- `top_ideas` does not contain exactly 3 ideas.
- Top ideas include banned specific-technology terms (`AI`, `blockchain`, `VR`).
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
