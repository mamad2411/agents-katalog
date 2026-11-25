---
name: productize-exec-feedback-without-context-to-actionable-design-requirements
description: >-
  Exec feedback without context to actionable design requirements. Use when the user needs a
  product workflow for stakeholder management related to exec feedback without context to
  actionable design requirements. Trigger terms: ux-design, executive-communication,
  requirements, feedback-interpretation, stakeholder-management.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Exec feedback without context to actionable design requirements

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

- **Skill**: `exec-feedback-without-context-to-actionable-design-requirements`
- **Lifecycle**: Design
- **Category**: Design
- **Primary artifact**: Exec feedback without context to actionable design requirements UX/design review with findings, constraints, fixes, and acceptance checks

Use this skill to run the Productize prompt contract for **Exec feedback without context to actionable design requirements**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{EXEC_FEEDBACK}}
- {{CURRENT_DESIGN_CONTEXT}}
- {{PROJECT_BACKGROUND}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: Exec feedback without context to actionable design requirements.
Success metric:
- Completes all required tasks and decision logic from the prompt instructions.
- Output is specific, evidence-based, and actionable.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required analysis steps, sections, or validation logic.
- Keep recommendations/outputs grounded in the input context; avoid generic filler.
- Decode `{{EXEC_FEEDBACK}}` into actionable design intent using `{{CURRENT_DESIGN_CONTEXT}}` and `{{PROJECT_BACKGROUND}}`.
- Distinguish concern, desired outcome, feedback type, and whether it is a requirement vs preference.
- Identify missing context required to execute.
- Produce 2-3 concrete interpretations with "done" criteria, implications, effort, and likelihood.
- Provide clarifying questions covering intent, priority, success, and data.
- Propose interim next steps and a respectful communication plan aligned to executive intent.

FORMAT
Return exactly this structure:

<executive_feedback_structure>
<feedback_decoding>
<expressed_concern>
[What problem or opportunity is the executive highlighting?]
</expressed_concern>

<desired_outcome>
[What result is the executive hoping to achieve?]
</desired_outcome>

<feedback_type>
[Classify as: Strategic direction, Quality concern, Risk mitigation, User impact, Personal preference, or Unclear]
</feedback_type>

<requirement_or_preference>
[Assess whether this is:
- Must-have requirement (blocks launch without it)
- Important improvement (should address if feasible)
- Nice-to-have suggestion (consider if time permits)
- Personal preference (may or may not be valid concern)]
</requirement_or_preference>
</feedback_decoding>

<missing_context>
[List specific context needed to action the feedback:
- What defines success for addressing this?
- What are the constraints?
- How urgent/important is this?
- Who has final decision authority?
- When does this need to be resolved?
- What data would inform the decision?]
</missing_context>

<possible_interpretations>
<interpretation_1>
**What This Could Mean:**
[Specific interpretation of the feedback]

**If This Is The Intent, "Done" Looks Like:**
[Concrete, testable criteria for addressing the feedback]

**Design Implications:**
[Specific design changes that would address this interpretation]

**Effort Required:**
[Time/complexity to implement]

**Likelihood:**
[High/Medium/Low based on context]
</interpretation_1>

<interpretation_2>
**What This Could Mean:**
[Alternative specific interpretation]

**If This Is The Intent, "Done" Looks Like:**
[Concrete, testable criteria]

**Design Implications:**
[Specific design changes]

**Effort Required:**
[Time/complexity]

**Likelihood:**
[High/Medium/Low]
</interpretation_2>

<interpretation_3>
**What This Could Mean:**
[Third possible interpretation, if applicable]

**If This Is The Intent, "Done" Looks Like:**
[Concrete, testable criteria]

**Design Implications:**
[Specific design changes]

**Effort Required:**
[Time/complexity]

**Likelihood:**
[High/Medium/Low]
</interpretation_3>
</possible_interpretations>

<clarifying_questions>
<intent_questions>
[Questions to uncover what the executive really wants:
- Example: "When you mentioned X, were you concerned about Y or Z?"]
</intent_questions>

<priority_questions>
[Questions to establish importance:
- Example: "Is this a must-have for launch, or something we should address post-launch?"]
</priority_questions>

<success_questions>
[Questions to define acceptance criteria:
- Example: "What would you need to see to feel confident this concern is addressed?"]
</success_questions>

<data_questions>
[Questions to gather validation data:
- Example: "Would you like to see user research on this, or is this based on strategic direction?"]
</data_questions>
</clarifying_questions>

<interim_next_steps>
[Propose actions that make progress while awaiting clarification:
- Research options for addressing concern
- Create low-fidelity explorations of different interpretations
- Gather data that would inform the decision
- Identify quick wins that address concern partially
- Document implications of different approaches]
</interim_next_steps>

<communication_plan>
**Recommended Approach for Follow-up:**
[Describe how to engage the executive to get needed clarity:
- When to reach out (immediately vs. wait for next check-in)
- How to frame the conversation (focus on outcomes, show options)
- What to prepare (mockups, data, tradeoff analysis)
- Who else should be involved]

**Draft Message:**
[Provide a template message requesting clarification that:
- Acknowledges the feedback
- Shows you've thought about it
- Presents interpretations
- Requests specific input
- Proposes next steps]
</communication_plan>
</executive_feedback_structure>

FAILURE
- Any required section in `<executive_feedback_structure>` is missing or materially incomplete.
- Interpretations are generic, non-testable, or not grounded in provided context.
- Clarifying questions fail to cover intent, priority, success, and data.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
