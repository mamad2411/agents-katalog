---
name: productize-problem-framing-before-jumping-to-solutions
description: >-
  Problem framing before jumping to solutions. Use when the user needs a product workflow for
  user research related to problem framing before jumping to solutions. Trigger terms:
  user-research, problem-framing, product-design.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Problem framing before jumping to solutions

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

- **Skill**: `problem-framing-before-jumping-to-solutions`
- **Lifecycle**: Discover
- **Category**: Discovery
- **Primary artifact**: Problem framing before jumping to solutions research brief with evidence, insight clusters, assumptions, and next validation steps

Use this skill to run the Productize prompt contract for **Problem framing before jumping to solutions**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- `{{PROPOSED_SOLUTION}}`: The proposed solution idea or concept.
- `{{CONTEXT}}`: Product, user, business, and operational context related to the proposal.
</provided_inputs>

GOAL
Reorient teams from premature solution mode to rigorous, evidence-driven problem framing before solution design.
Success metric:
- The analysis diagnoses solution-jumping clearly and identifies assumptions, evidence, and risks.
- The output defines a user-centered problem statement with measurable success criteria.
- The output provides a concrete validation research plan and preserves collaborative team alignment.

CONSTRAINTS
- Use only provided inputs; if information is missing, state explicit assumptions.
- Diagnose the proposed solution before prescribing alternatives.
- Address all required analysis steps:
- Identify solution-jumping (proposed solution, embedded assumptions, implied problem, evidence status).
- Extract underlying problem (user need, JTBD, desired outcome, current state, constraints).
- Challenge assumptions (validity, evidence, risk if wrong, validation method).
- Frame a complete problem statement (who, where/when, impact, workarounds, success).
- Provide alternative problem framings to widen exploration.
- Propose pre-solution research to validate the problem.
- Recommendations must be specific, testable, and grounded in `{{CONTEXT}}`.
- Maintain a collaborative tone that frames validation as de-risking, not rejection.

FORMAT
Return exactly this structure:

<problem_framing_analysis>
<solution_jumping_diagnosis>
**Proposed Solution:**
[Describe the solution being discussed]

**Embedded Assumptions:**
[List assumptions built into this solution:
- Assumes users need X
- Assumes current problem is Y
- Assumes best approach is Z]

**Implied Problem:**
[What problem is this solution trying to solve?]

**Evidence Status:**
[What evidence exists that this is the right problem to solve? What's missing?]
</solution_jumping_diagnosis>

<underlying_problem_extraction>
**User Need:**
[What fundamental user need is being addressed?]

**Job-to-be-Done:**
[What job is the user trying to accomplish?]

**Desired Outcome:**
[What result does the user want to achieve?]

**Current State:**
[How do users accomplish this today? What goes wrong?]

**Constraints:**
[What limitations exist: technical, business, user, environmental?]
</underlying_problem_extraction>

<assumption_challenges>
[For each key assumption, ask:
- Assumption: [state it]
- Is it validated? [Yes/No/Partially]
- Evidence: [what supports or contradicts it]
- Risk if wrong: [what happens if this assumption is false]
- How to validate: [proposed test]]
</assumption_challenges>

<problem_statement>
**Who:** [Specific user segment]

**Experiences:** [Specific problem or friction]

**When/Where:** [Context and triggers]

**Impact:** [Consequence and severity]

**Current Workarounds:** [What users do today]

**Success Would Be:** [Measurable outcome]

**Problem Statement:**
[Complete: "Users [who] struggle to [what] when [context] because [root cause], which leads to [impact]. Success would mean [outcome]"]
</problem_statement>

<alternative_problem_framings>
<framing_1>
[Present alternative way to frame this problem that might lead to different solutions]
</framing_1>

<framing_2>
[Present second alternative framing]
</framing_2>

<framing_3>
[Present third alternative framing if applicable]
</framing_3>
</alternative_problem_framings>

<validation_research>
**Research Questions:**
[List 5-7 questions that would validate the problem:
- Do users actually experience this problem?
- How frequently and severely?
- What triggers it?
- How do they currently cope?
- What would "solved" look like to them?]

**Proposed Method:**
[Suggest appropriate research approach:
- User interviews focused on problem space
- Observational research of current workflows
- Diary studies to capture problem in context
- Analytics analysis of behavior patterns]

**Success Criteria:**
[What would confirm this is the right problem to solve?]

**Timeline:**
[How long would this research take?]
</validation_research>

<solution_divergence_plan>
**Once Problem Is Validated:**

**Divergence Questions:**
[Questions to open up solution space:
- How might we [solve aspect 1]?
- What if [constraint] didn't exist?
- How do other domains solve similar problems?
- What would the ideal solution look like?]

**Solution Criteria:**
[What should any solution achieve? List must-haves and nice-to-haves]

**Exploration Approach:**
[Suggest how to explore solutions once problem is understood:
- Competitive analysis
- Analogous research
- Design studio
- Rapid prototyping]
</solution_divergence_plan>

<communication_strategy>
**How to Redirect the Team:**
[Suggest how to shift the conversation from solution to problem:
- Acknowledge the solution thinking
- Reframe as problem exploration
- Show value of problem validation
- Set timeline for problem then solution phases]

**Draft Message:**
[Provide a tactful message to the team explaining the value of problem framing]
</communication_strategy>
</problem_framing_analysis>

FAILURE
- Any required section/tag in `FORMAT` is missing, reordered, or materially incomplete.
- Analysis skips core problem-framing steps (solution-jumping diagnosis, problem extraction, assumption challenge, validation plan).
- Claims are generic, not evidence-linked, or not grounded in provided inputs.
- Output proposes solutions before adequately framing/validating the problem.
- Assumptions or uncertainties are used but not explicitly stated.
- Tone is adversarial or dismissive rather than collaborative and de-risking.
