---
name: productize-stakeholder-brief-clarification-and-problem-definition
description: >-
  Stakeholder Brief Clarification and Problem Definition. Use when the user needs a product
  workflow for stakeholder management related to stakeholder brief clarification and problem
  definition. Trigger terms: product-design, problem-framing, stakeholder-management,
  user-research, metrics.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Stakeholder Brief Clarification and Problem Definition

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

- **Skill**: `stakeholder-brief-clarification-and-problem-definition`
- **Lifecycle**: Align
- **Category**: Stakeholder Communication
- **Primary artifact**: Stakeholder Brief Clarification and Problem Definition stakeholder narrative with audience, message, risks, asks, and follow-up owner

Use this skill to run the Productize prompt contract for **Stakeholder Brief Clarification and Problem Definition**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{VAGUE_BRIEF}}
- {{STAKEHOLDER_CONTEXT}}
- {{BUSINESS_CONSTRAINTS}}
- {{USER_RESEARCH}}
- {{CURRENT_METRICS}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: Stakeholder Brief Clarification and Problem Definition.
Success metric:
- Completes all required tasks and decision logic from the prompt instructions.
- Output is specific, evidence-based, and actionable.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required analysis steps, sections, or validation logic.
- Keep recommendations/outputs grounded in the input context; avoid generic filler.
- Transform `{{VAGUE_BRIEF}}` into a concrete, measurable problem definition using `{{STAKEHOLDER_CONTEXT}}`, `{{BUSINESS_CONSTRAINTS}}`, `{{USER_RESEARCH}}`, and `{{CURRENT_METRICS}}`.
- Decode subjective language, assumptions, implied intent, symptom vs root cause, and solution bias.
- Extract business drivers, user problems, and concrete success criteria.
- Translate vague terms into observable/measurable design criteria.
- Identify technical, timeline, budget, brand/design, and organizational constraints.
- Generate validation-oriented clarifying questions and actionable next steps.
- Keep analysis objective, evidence-based, and explicit about assumptions and unknowns.

FORMAT
Return exactly this structure:

<problem_statement_analysis>
<vague_language_decoded>
**Subjective Terms Identified:**
[List each vague term with its contextual meaning]

**Embedded Assumptions:**
- [Assumption 1]
- [Assumption 2]
- [Assumption 3]

**Implied But Not Stated:**
[What the stakeholder assumes you know or will infer]

**Root Cause vs. Symptom:**
- Stated symptom: [what stakeholder described]
- Likely root cause: [underlying issue driving the symptom]
</vague_language_decoded>

<underlying_business_needs>
**Primary Business Driver:**
[The core business outcome this request aims to achieve]

**Revenue/Growth Connection:**
[How this impacts company financial goals]

**Strategic Alignment:**
[How this connects to broader company strategy or roadmap]

**Competitive Context:**
[Market forces or competitor actions driving this]

**Internal Stakeholder Pressures:**
[Political, reputational, or organizational dynamics]

**Cost of Inaction:**
[What happens if this problem isn't solved]
</underlying_business_needs>

<user_problems_identified>
**Affected User Segments:**
- [Segment 1]: [specific pain points]
- [Segment 2]: [specific pain points]
- [Segment 3]: [specific pain points]

**User-Reported Pain Points:**
[Direct quotes or themes from user research, support tickets, reviews]

**Behavioral Evidence:**
[Observable user behaviors that indicate this problem exists]

**Current Workarounds:**
[How users compensate for this problem today]

**Impact on User Journeys:**
[Specific tasks or flows where users experience friction]

**Severity Assessment:**
- Frequency: [how often users encounter this]
- Impact: [how much it affects user success]
- User priority: [how users would rank fixing this]
</user_problems_identified>

<concrete_criteria>
**Translation of "[VAGUE_TERM_1]":**
- Criterion 1: [specific, measurable attribute]
- Criterion 2: [specific, measurable attribute]
- Criterion 3: [specific, measurable attribute]

**Translation of "[VAGUE_TERM_2]":**
- Criterion 1: [specific, measurable attribute]
- Criterion 2: [specific, measurable attribute]
- Criterion 3: [specific, measurable attribute]

**Observable Design Characteristics:**
[Specific visual, interaction, or structural attributes that would demonstrate the vague term has been achieved]

**User-Facing Improvements:**
[Concrete changes users would notice and value]
</concrete_criteria>

<success_metrics>
**Primary Success Metric:**
- Metric: [specific measurement]
- Current baseline: [X]
- Target: [Y]
- Timeline: [when to measure]
- Collection method: [how to measure]

**Secondary Metrics:**
1. [Metric]: [baseline] → [target] by [date]
2. [Metric]: [baseline] → [target] by [date]
3. [Metric]: [baseline] → [target] by [date]

**Leading Indicators:**
- [Early signal 1]
- [Early signal 2]
- [Early signal 3]

**Qualitative Success Signals:**
- [User feedback theme or sentiment shift]
- [Stakeholder observation or report]
- [Support ticket reduction in specific category]

**Risks to Monitor:**
[Potential negative metrics that could indicate unintended consequences]
</success_metrics>

<constraint_analysis>
<technical_constraints>
- [Constraint 1 with impact on design options]
- [Constraint 2 with impact on design options]
- [Constraint 3 with impact on design options]
</technical_constraints>

<timeline_constraints>
- Hard deadline: [date and reason]
- Resource availability: [when team is available]
- Dependencies: [what must happen first]
</timeline_constraints>

<budget_constraints>
- Development capacity: [hours or sprints available]
- Research budget: [ability to validate with users]
- Third-party costs: [tools or services needed]
</budget_constraints>

<brand_design_constraints>
- Design system: [existing components and patterns to leverage]
- Accessibility: [WCAG level required, existing debt]
- Brand guidelines: [visual identity rules that apply]
</brand_design_constraints>

<organizational_constraints>
- Approval process: [who must sign off, when]
- Cross-team dependencies: [coordination needed]
- Political considerations: [stakeholder dynamics]
</organizational_constraints>
</constraint_analysis>

<refined_problem_statement>
**Problem Statement:**
We need to [specific design action] for [specific user segment] so that [specific user outcome] and [specific business outcome], as measured by [primary metric] improving from [baseline] to [target] by [date], while considering [key constraints].

**In Plain Language:**
[Restate the problem statement in conversational terms that any stakeholder can understand]

**Scope Boundaries:**
- In scope: [what this problem statement includes]
- Out of scope: [what this explicitly does not include]
- Future consideration: [what might be addressed later]
</refined_problem_statement>

<validation_questions>
**Business Outcome Validation:**
1. What would represent a home-run outcome for this initiative in 6 months?
2. If we could only improve one business metric, which would matter most?
3. What would cause you to consider this effort a failure, even if users liked it?

**User Need Validation:**
4. Which user segment would benefit most from solving this problem?
5. How do we know users actually experience this as a problem vs. our assumption?
6. What would users give up or trade off to get this improvement?

**Scope and Priority Validation:**
7. If we had to cut scope by 50%, what's the core of this request we must keep?
8. What's more important: shipping by [date] or achieving [specific outcome]?
9. How does this compare in priority to [other initiative on roadmap]?

**Constraints Validation:**
10. What technical limitations should we absolutely not try to work around?
11. Are there brand or design standards we could flex if it meant better user outcomes?
12. What budget or timeline assumptions should we validate before proceeding?

**Success Criteria Validation:**
13. How will we know if we've succeeded in 3 months? 6 months? 12 months?
14. What user feedback or behavior would make you confident we solved this?
15. What business metrics matter more than hitting the launch date?
</validation_questions>

<recommended_next_steps>
1. **Validate assumptions:** [Specific research or conversations needed to confirm problem understanding]
2. **Baseline metrics:** [Establish current measurements for success criteria]
3. **Exploratory design:** [Create lightweight concepts to test problem framing]
4. **Stakeholder alignment:** [Schedule review of refined problem statement with key stakeholders]
5. **Technical feasibility:** [Partner with engineering to validate constraints and opportunities]
6. **User validation:** [Test problem statement against actual user pain points through interviews or surveys]
7. **Prioritization:** [Compare this problem statement against other roadmap items]
</recommended_next_steps>
</problem_statement_analysis>

FAILURE
- Any required section in `<problem_statement_analysis>` is missing or materially incomplete.
- Problem statement is not measurable (missing baseline/target/date/constraints).
- Clarifying questions are not actionable or do not address business, user, scope, constraints, and success validation.
- Metrics and constraints are generic or not traceable to the provided inputs.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
