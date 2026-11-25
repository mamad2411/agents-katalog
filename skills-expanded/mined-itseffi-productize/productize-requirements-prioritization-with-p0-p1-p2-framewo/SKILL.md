---
name: productize-requirements-prioritization-with-p0-p1-p2-framework
description: >-
  Requirements prioritization with P0-P1-P2 framework. Use when the user needs a product
  workflow for project management related to requirements prioritization with p0-p1-p2
  framework. Trigger terms: prioritization, product-management, planning, scope.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Requirements prioritization with P0-P1-P2 framework

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

- **Skill**: `requirements-prioritization-with-p0-p1-p2-framework`
- **Lifecycle**: Plan
- **Category**: Delivery
- **Primary artifact**: Requirements prioritization with P0-P1-P2 framework delivery brief with scope, requirements, priorities, risks, and acceptance criteria

Use this skill to run the Productize prompt contract for **Requirements prioritization with P0-P1-P2 framework**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{REQUIREMENTS_LIST}}
- {{PRODUCT_CONTEXT}}
- {{CONSTRAINTS}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: Requirements prioritization with P0-P1-P2 framework.
Success metric:
- Completes all required tasks and decision logic from the prompt instructions.
- Output is specific, evidence-based, and actionable.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required analysis steps, sections, or validation logic.
- Keep recommendations/outputs grounded in the input context; avoid generic filler.
- Prioritize `{{REQUIREMENTS_LIST}}` using the P0/P1/P2 framework in the context of `{{PRODUCT_CONTEXT}}` and `{{CONSTRAINTS}}`.
- Apply explicit prioritization tests for each tier (P0/P1/P2) and challenge “must-have” claims.
- Use effort vs. value to support decisions and identify descoping options if capacity is exceeded.
- Provide rationale, evidence, and acceptance criteria for each requirement.
- Produce a capacity analysis and a stakeholder communication plan.

FORMAT
Return exactly this structure:

<requirements_prioritization>
<prioritization_framework>
**P0 Definition (Launch Blocker):**
[Your specific definition for this project:
- Without this, users cannot [core task]
- Without this, product fails [critical requirement]
- Must-have criteria: [specific tests]]

**P1 Definition (High Value):**
[Your specific definition for this project:
- Significantly improves [key experience]
- Enables [important use case]
- Should-have criteria: [specific tests]]

**P2 Definition (Nice-to-Have):**
[Your specific definition for this project:
- Enhances [aspect of experience]
- Valuable but users can accomplish goals without it
- Nice-to-have criteria: [specific tests]]

**Prioritization Principles:**
[3-5 principles guiding decisions for this project:
- "Core user task enablement trumps convenience features"
- "Baseline quality must be met (P0) before adding polish (P2)"]
</prioritization_framework>

<prioritized_requirements>
<p0_requirements>
[For each P0 requirement:

**Requirement:** [Clear description]

**Why P0:**
[Specific justification using P0 criteria]

**Impact if Missing:**
[Concrete description of what breaks without this]

**User Tasks Blocked:**
[Which core user tasks become impossible]

**Evidence:**
[Data/research supporting this priority]

**Effort Estimate:**
[Time/complexity]

**Dependencies:**
[What else must exist for this to work]

**Acceptance Criteria:**
[Minimum bar for "done" on this requirement]]
</p0_requirements>

<p1_requirements>
[For each P1 requirement:

**Requirement:** [Clear description]

**Why P1:**
[Specific justification using P1 criteria]

**Value if Included:**
[Concrete benefits of including this]

**Impact if Missing:**
[What degrades without this, but doesn't break]

**User Tasks Affected:**
[Which tasks become harder but still possible]

**Evidence:**
[Data/research supporting value]

**Effort Estimate:**
[Time/complexity]

**Could Descope to:**
[Simpler version that captures core value]

**Acceptance Criteria:**
[Minimum bar for "done"]]
</p1_requirements>

<p2_requirements>
[For each P2 requirement:

**Requirement:** [Clear description]

**Why P2:**
[Why it's nice-to-have but not critical]

**Value:**
[What it adds]

**Defer Rationale:**
[Why it's okay to wait]

**Effort Estimate:**
[Time/complexity]

**Post-Launch Timeline:**
[When to revisit]

**Acceptance Criteria:**
[If we did build it, what's the bar]]
</p2_requirements>
</prioritized_requirements>

<challenged_priorities>
[For items originally claimed as "must-have" but deprioritized:

**Requirement:** [Description]

**Originally Claimed As:** [P0/P1]

**Actually:** [P1/P2]

**Why Deprioritized:**
[Reason it's not as critical as claimed]

**Supporting Evidence:**
[Why this priority is more accurate]

**Alternative:**
[How users can accomplish goal without this, or simpler version]]
</challenged_priorities>

<effort_value_matrix>
[Create a 2x2 showing:
**High Value / Low Effort (Do First):**
- [List requirements]

**High Value / High Effort (Evaluate):**
- [List requirements]
- [For each: Is value worth effort? Can we simplify?]

**Low Value / Low Effort (Nice-to-have):**
- [List requirements]
- [Consider: Worth including or better to focus elsewhere?]

**Low Value / High Effort (Descope):**
- [List requirements]
- [Rationale for cutting]]
</effort_value_matrix>

<capacity_analysis>
**Total Requirements:**
- P0: [count] items = [estimated effort]
- P1: [count] items = [estimated effort]
- P2: [count] items = [estimated effort]
- Total: [total effort]

**Available Capacity:**
[Team capacity for this release]

**Gap Analysis:**
- P0 fit: [Yes/No - if no, how much over?]
- P0 + P1 fit: [Yes/No - if no, which P1 to defer?]
- P0 + P1 + P2 fit: [Almost certainly no]

**Conclusion:**
[What's realistic to complete]
</capacity_analysis>

<descoping_options>
[If capacity is exceeded, propose descoping approaches:

**Option 1: Defer All P2**
- What's cut: [List P2 items]
- What's preserved: [All P0/P1]
- Impact: [Minimal - nice-to-haves wait]

**Option 2: Defer Low-Effort P1 + All P2**
- What's cut: [Specific P1 items]
- What's preserved: [High-value P0/P1]
- Rationale: [Why these P1 items can wait]
- Impact: [Description]

**Option 3: Simplify High-Effort P1**
- What's simplified: [Specific items]
- Simplified version: [Description]
- Value preserved: [What's kept]
- Impact: [Tradeoffs]

**Recommended Approach:**
[Which option, with rationale]]
</descoping_options>

<decision_documentation>
**Prioritization Decision Log:**
[Template for documenting:
- Requirement
- Priority assignment (P0/P1/P2)
- Rationale
- Decision maker
- Date
- Conditions that would change priority]
</decision_documentation>

<communication_plan>
**How to Present Prioritization:**
[Guidance for sharing with stakeholders:
- Lead with framework and principles
- Show evidence for priorities
- Be explicit about tradeoffs
- Invite challenge on specific items
- Document decisions]

**Handling "Everything is P0" Stakeholders:**
[Tactics for managing pushback:
- Apply prioritization tests consistently
- Show capacity constraints
- Offer descoping choices
- Escalate if needed]
</communication_plan>
</requirements_prioritization>

FAILURE
- Any required section in `<requirements_prioritization>` is missing or materially incomplete.
- Requirements lack evidence-based rationale or acceptance criteria.
- Capacity analysis or descoping options are missing when P0+P1 exceed capacity.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
