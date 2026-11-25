---
name: productize-product-refinement-session-planning
description: >-
  Product refinement session planning. Use when the user needs a product workflow for project
  management related to product refinement session planning. Trigger terms:
  product-management, refinement, meetings, facilitation.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Product refinement session planning

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

- **Skill**: `product-refinement-session-planning`
- **Lifecycle**: Think
- **Category**: Operations
- **Primary artifact**: Product refinement session planning product artifact with evidence, risks, recommendation, and next action

Use this skill to run the Productize prompt contract for **Product refinement session planning**.

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
Produce a high-quality deliverable for: Product refinement session planning.
Success metric:
- Completes all required tasks and decision logic from the prompt instructions.
- Output is specific, evidence-based, and actionable.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required analysis steps, sections, or validation logic.
- Keep recommendations/outputs grounded in the input context; avoid generic filler.
- Use the refinement guide to plan a session for `{{TOPIC}}`.
- Produce:
- A timeboxed agenda aligned to the guide’s phases.
- 3-5 guide-derived key points relevant to this topic.
- 3-5 topic-specific discussion questions focused on problem exploration.
- A 2-3 sentence closing statement emphasizing refinement value and next steps.

FORMAT
Return exactly this structure:

<refinement_guide>
# Product Refinement Session Guide
## Purpose
A refinement session is NOT about estimating solutions, but rather:
- Understanding problems deeply
- Determining solution requirements
- Building shared team understanding
- Defining clear success criteria
## Pre-Session Preparation
### For Product Manager/Owner
1. Identify key items for refinement
   - Select items that align with current priorities
   - Focus on problems that need immediate attention
2. Share materials in advance
   - Distribute selected items to team 24 hours before session
   - Give team time to review and reflect
   - Include any relevant context or background information
### For Team Members
1. Review shared materials
2. Note initial questions and concerns
3. Consider potential problem areas that need clarification
## During the Session
### 1. Context Setting (15-20 minutes)
- PM/PO clearly articulates:
  - Current business priorities
  - Strategic context
  - Why these items matter now
  - How they align with broader goals
### 2. Problem Space Exploration (40-45 minutes)
- Discuss each refinement item:
  - Define the core problem
  - Identify affected stakeholders
  - Map out dependencies
  - Document constraints
  - Clarify assumptions
### 3. Success Criteria Definition (20-25 minutes)
- Define clear outcomes:
  - What does success look like?
  - How will we measure it?
  - What are the acceptance criteria?
  - What are the non-negotiables?
### 4. Discussion Management
- Timeboxed conversations
- Park tangential discussions
- Document open questions
- Capture action items
### 5. Session Retrospective (10-15 minutes)
- Gather feedback on:
  - Session effectiveness
  - Discussion quality
  - Time management
  - Areas for improvement
  - What worked well
## Post-Session Actions
### 1. Documentation
- Update refinement items with new insights
- Document decisions and rationale
- Share session notes
### 2. Follow-up
- Address parked items
- Schedule any needed deep-dives
- Assign action items
### 3. Preparation for Next Session
- Apply retrospective feedback
- Begin identifying next batch of items
- Update session format based on team input
## Success Indicators
- Team has clear understanding of problems
- Success criteria are well-defined
- Next steps are clearly documented
- Team is aligned on priorities
- Everyone understands their role in solution development
## Common Pitfalls to Avoid
- Jumping to solutions too quickly
- Not timeboxing discussions
- Lack of preparation
- Missing key stakeholders
- Focusing on estimation instead of understanding
</refinement_guide>

<agenda>
[Timeboxed agenda aligned to the guide’s phases]
</agenda>

<key_points>
[3-5 guide-derived points relevant to the session topic]
</key_points>

<discussion_questions>
[3-5 topic-specific questions for problem space exploration]
</discussion_questions>

<closing_statement>
[2-3 sentence closing statement]
</closing_statement>

FAILURE
- Any required section (`<refinement_guide>`, `<agenda>`, `<key_points>`, `<discussion_questions>`, `<closing_statement>`) is missing or materially incomplete.
- Agenda is not timeboxed or does not align to the guide’s phases.
- Questions are generic or not tied to `{{TOPIC}}`.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
