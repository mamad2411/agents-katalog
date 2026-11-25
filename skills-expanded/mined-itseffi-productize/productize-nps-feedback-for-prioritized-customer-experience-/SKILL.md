---
name: productize-nps-feedback-for-prioritized-customer-experience-initiatives
description: >-
  NPS feedback for prioritized customer experience initiatives. Use when the user needs a
  product workflow for business analysis related to nps feedback for prioritized customer
  experience initiatives. Trigger terms: pm, business-analysis, nps, customer-experience,
  prioritization.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# NPS feedback for prioritized customer experience initiatives

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

- **Skill**: `nps-feedback-for-prioritized-customer-experience-initiatives`
- **Lifecycle**: Plan
- **Category**: Delivery
- **Primary artifact**: NPS feedback for prioritized customer experience initiatives delivery brief with scope, requirements, priorities, risks, and acceptance criteria

Use this skill to run the Productize prompt contract for **NPS feedback for prioritized customer experience initiatives**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{NPS_FEEDBACK}}
</provided_inputs>

GOAL
Translate `NPS_FEEDBACK` into a prioritized initiative backlog that reduces detractor pain and amplifies promoter value.
Success metric:
- Separates detractors (0-6) and promoters (9-10) correctly.
- Identifies top recurring themes with evidence (frequency + representative quote).
- Produces prioritized initiatives with transparent scoring and clear ownership-ready descriptions.
- Follows the required output structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Treat only scores `0-6` as detractors and `9-10` as promoters; ignore or label neutral scores (`7-8`) if present.
- Identify top 5 detractor pain themes and top 5 promoter benefit themes from recurring signals.
- For each theme, include:
  - short theme label,
  - brief description,
  - frequency signal (count or relative frequency),
  - at least one representative quote.
- For each proposed initiative, provide a `Priority Score` from `1-5` based on:
  - Frequency (how often theme appears),
  - Impact (customer experience importance),
  - Feasibility (implementation realism).
- Keep initiatives concrete and implementation-ready (avoid generic statements).

FORMAT
Return exactly this structure:

<output>
<theme_analysis>
<detractor_themes>
1. [Theme]
   - Description: [Brief description]
   - Frequency: [Count or relative frequency]
   - Representative Quote: "[Quote]"
[Repeat to top 5]
</detractor_themes>
<promoter_themes>
1. [Theme]
   - Description: [Brief description]
   - Frequency: [Count or relative frequency]
   - Representative Quote: "[Quote]"
[Repeat to top 5]
</promoter_themes>
</theme_analysis>

<detractor_initiatives>
1. [Initiative Name] (Priority Score: X)  
   - Description: [Brief description of the initiative]  
   - Addresses: [Pain point being addressed]  
   - Scoring Rationale: [Frequency / Impact / Feasibility rationale]
   - Representative Quote: "[Direct quote from feedback]"

[Repeat for top 3-5 detractor initiatives]
</detractor_initiatives>

<promoter_initiatives>
1. [Initiative Name] (Priority Score: X)  
   - Description: [Brief description of the initiative]  
   - Amplifies: [Benefit being amplified]  
   - Scoring Rationale: [Frequency / Impact / Feasibility rationale]
   - Representative Quote: "[Direct quote from feedback]"

[Repeat for top 3-5 promoter initiatives]
</promoter_initiatives>

<summary>
[Provide a brief summary of the key findings and the potential impact of implementing these initiatives]
</summary>
</output>

FAILURE
- Detractor/promoter segmentation is incorrect or not shown.
- Theme analysis is missing top recurring themes, frequencies, or quotes.
- Initiatives are missing priority scores or scoring rationale.
- Recommendations are generic or not linked to identified themes.
- Required schema is missing, malformed, or incomplete.
- Assumptions are used but not explicitly stated.
