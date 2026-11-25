---
name: productize-actionable-user-profiles-with-tasks-and-constraints-from
description: >-
  Actionable user profiles with tasks and constraints from shallow personas. Use when the user
  needs a product workflow for user research related to actionable user profiles with tasks
  and constraints from shallow personas. Trigger terms: user-research, personas, ux.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Actionable user profiles with tasks and constraints from shallow personas

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

- **Skill**: `actionable-user-profiles-with-tasks-and-constraints-from`
- **Lifecycle**: Discover
- **Category**: Discovery
- **Primary artifact**: Actionable user profiles with tasks and constraints from shallow personas research brief with evidence, insight clusters, assumptions, and next validation steps

Use this skill to run the Productize prompt contract for **Actionable user profiles with tasks and constraints from shallow personas**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{EXISTING_PERSONA}}
- {{AVAILABLE_USER_DATA}}
- {{PRODUCT_CONTEXT}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: Actionable user profiles with tasks and constraints from shallow personas.
Success metric:
- Completes all required tasks and decision logic from the prompt instructions.
- Output is specific, evidence-based, and actionable.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required analysis steps, sections, or validation logic.
- Keep recommendations/outputs grounded in the input context; avoid generic filler.
- Transform `{{EXISTING_PERSONA}}` into an actionable user profile using `{{AVAILABLE_USER_DATA}}` and `{{PRODUCT_CONTEXT}}`.
- Replace vague persona language with specific, observable details:
- Concrete tasks and success outcomes.
- Jobs-to-be-done (functional, emotional, social).
- Capabilities, constraints, and behavioral patterns.
- Grounded contextual scenarios.
- Design implications directly tied to profile evidence.
- Explicit research gaps and validation plan for missing/uncertain assumptions.
- Keep all claims evidence-linked; state assumptions when data is incomplete.

FORMAT
Return exactly this structure:

<actionable_user_profile>
<profile_summary>
**Role:** [Specific job title and organizational context]
**Core Responsibility:** [What they're accountable for]
**Primary Goal:** [What success looks like in their role]
</profile_summary>

<jobs_to_be_done>
<functional_jobs>
[List 5-7 specific tasks they need to accomplish related to this product:
- Example: "Create quarterly budget forecast for leadership review"
- Example: "Onboard new team members to project workflows within first week"]
</functional_jobs>

<emotional_jobs>
[List 3-5 emotional needs:
- Example: "Feel confident in decisions without analysis paralysis"
- Example: "Avoid embarrassment from missing important details"]
</emotional_jobs>

<social_jobs>
[List 2-3 social needs:
- Example: "Be seen as data-driven and strategic by leadership"
- Example: "Maintain credibility with engineering team"]
</social_jobs>
</jobs_to_be_done>

<user_capabilities>
**Technical Sophistication:**
[Describe their comfort with technology, tools they know, learning curve tolerance]

**Domain Expertise:**
[Describe their knowledge of the problem domain, industry experience, specialized skills]

**Decision Authority:**
[Describe what they can decide independently vs. what requires approval]

**Time Availability:**
[Describe their time constraints, competing priorities, typical workflow rhythm]

**Resources:**
[Describe what tools, data, people, budget they have access to]
</user_capabilities>

<constraints>
**Organizational Constraints:**
[List policies, processes, approval chains that limit their options]

**Technical Constraints:**
[List system limitations, integrations, legacy tools they must work with]

**Knowledge Constraints:**
[List gaps in their knowledge, areas where they need guidance]

**Time Constraints:**
[List deadlines, recurring obligations, busy periods]

**Resource Constraints:**
[List limitations in budget, headcount, tools, data access]
</constraints>

<behavioral_patterns>
**How They Currently Solve This Problem:**
[Describe their current workflow, tools used, workarounds, pain points]

**Decision-Making Style:**
[Describe how they evaluate options, what evidence they trust, risk tolerance]

**Collaboration Patterns:**
[Describe who they work with, communication preferences, meeting cadence]

**Learning Preferences:**
[Describe how they prefer to learn new tools, documentation vs. experimentation]
</behavioral_patterns>

<contextual_scenarios>
<scenario_1>
**Situation:** [Specific context: when, where, why]
**Goal:** [What they're trying to accomplish]
**Constraints:** [What's limiting them]
**Current Approach:** [How they do it now]
**Pain Points:** [What goes wrong or feels hard]
**Success Criteria:** [What "good" looks like]
</scenario_1>

<scenario_2>
[Repeat structure for 2-3 total scenarios covering different use cases]
</scenario_2>
</contextual_scenarios>

<design_implications>
[List 5-7 specific design implications from this user profile:
- "Must support quick, interrupted workflows due to frequent context-switching"
- "Should provide confidence-building validation since users fear making errors"
- "Must integrate with Slack since that's where they live all day"]
</design_implications>

<research_gaps>
[List specific things you don't know but should validate with real users:
- "How do they currently handle X scenario?"
- "What's their tolerance for Y type of complexity?"
- "How often do they encounter Z situation?"]
</research_gaps>

<validation_plan>
[Describe how to validate this profile with real users:
- Proposed research methods
- Key questions to ask
- Behaviors to observe
- Success signals that profile is accurate]
</validation_plan>
</actionable_user_profile>

FAILURE
- Any required section in `<actionable_user_profile>` is missing or materially incomplete.
- Profile remains generic/buzzword-heavy and not actionable for design decisions.
- Jobs, constraints, scenarios, or implications are not grounded in available data.
- Research gaps/validation plan are missing or non-specific.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
