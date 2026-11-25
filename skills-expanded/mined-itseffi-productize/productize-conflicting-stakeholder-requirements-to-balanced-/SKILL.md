---
name: productize-conflicting-stakeholder-requirements-to-balanced-design
description: >-
  Conflicting stakeholder requirements to balanced design approach. Use when the user needs a
  product workflow for stakeholder management related to conflicting stakeholder requirements
  to balanced design approach. Trigger terms: stakeholder-management, design-strategy,
  conflict-resolution.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Conflicting stakeholder requirements to balanced design approach

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

- **Skill**: `conflicting-stakeholder-requirements-to-balanced-design`
- **Lifecycle**: Design
- **Category**: Design
- **Primary artifact**: Conflicting stakeholder requirements to balanced design approach UX/design review with findings, constraints, fixes, and acceptance checks

Use this skill to run the Productize prompt contract for **Conflicting stakeholder requirements to balanced design approach**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{CONFLICTING_REQUIREMENTS}}
- {{STAKEHOLDER_PRIORITIES}}
- {{PROJECT_CONTEXT}}
- {{USER_RESEARCH_INSIGHTS}}
- {{TECHNICAL_CONSTRAINTS}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: Conflicting stakeholder requirements to balanced design approach.
Success metric:
- Completes all required tasks and decision logic from the prompt instructions.
- Output is specific, evidence-based, and actionable.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required analysis steps, sections, or validation logic.
- Keep recommendations/outputs grounded in the input context; avoid generic filler.
- Reconcile `{{CONFLICTING_REQUIREMENTS}}` using `{{STAKEHOLDER_PRIORITIES}}`, `{{PROJECT_CONTEXT}}`, `{{USER_RESEARCH_INSIGHTS}}`, and `{{TECHNICAL_CONSTRAINTS}}`.
- Map conflict types, stakeholder positions, severity, and dependencies.
- Identify root causes, then propose win-win solutions and explicit tradeoffs.
- Provide a recommendation with rationale, decision framework, communication plan, and validation plan.

FORMAT
Return exactly this structure:

<conflict_reconciliation>
<executive_summary>
**Project:** [Project name]
**Conflicting Requirements Count:** [Number of major conflicts identified]
**Stakeholders Involved:** [List key stakeholders and their roles]
**Conflict Severity:** [Low/Medium/High - overall assessment]
**Resolution Approach:** [Win-win solutions possible / Tradeoffs required / Phased approach needed]
**Decision Timeline:** [When final decision needed]
**Recommendation:** [One-sentence summary of proposed path forward]
</executive_summary>

<conflict_mapping>
Map each significant conflict clearly with all relevant details, stakeholder positions, user research insights, and dependencies.

## Conflict #1: [Name]

**Requirement A:** [Full description]
**Stakeholder:** [Name, role, underlying goal, success metric]

**Requirement B:** [Full description]
**Stakeholder:** [Name, role, underlying goal, success metric]

**Conflict Type:** [Classification]
**Severity:** [Level and why]
**Impact:** [What's affected]
**User Research:** [What data says]
**Alignment:** [Who supports each side]
**Dependencies:** [Related conflicts]

[Repeat for each major conflict]
</conflict_mapping>

<root_cause_analysis>
Identify fundamental causes driving conflicts:

**[Root Cause Category]:**
[Detailed explanation of this underlying issue]
**Examples:** [Specific manifestations]
**→ Root cause:** [One-line summary]

[Continue for all root cause categories identified]

**Key Insights:**
[Major patterns and observations]
</root_cause_analysis>

<win_win_solutions>
## Solution for Conflict #[X]: [Name]

**Approach: [Solution Name]**

**How It Works:**
[Detailed 3-5 bullet explanation of the creative solution]

**Why It's Win-Win:**
- ✅ [Stakeholder A benefit]
- ✅ [Stakeholder B benefit]
- ✅ [User benefit]
- ✅ [Business benefit]

**Implementation:**
- Phase 1: [Details, timeline]
- Phase 2: [Details, timeline]
- Phase 3: [Details, timeline]

**Validation:**
[How to test this works]

**Potential Risks:**
[What could go wrong and mitigations]

[Repeat for each win-win solution]
</win_win_solutions>

<tradeoff_analysis>
## For Conflict #[X]: [Name] (Requires Tradeoff)

### Option A: [Name] (Favors [Stakeholder])

**Approach:** [What we'd do]
**Gains:** [What winning party gets]
**Losses:** [What losing party sacrifices]
**User Impact:** [Effects on users]
**Business Impact:**
- Short-term: [Impact]
- Long-term: [Impact]
**Complexity:** [Level]
**Timeline:** [Duration]
**Risk:** [Assessment]
**Reversibility:** [How hard to change]

### Option B: [Name] (Favors [Other Stakeholder])

[Same structure]

### Option C: [Balanced Approach] (Recommended)

**Approach:** [Compromise solution]
**Everyone Gains Partially:** [How it balances]
**Implementation:** [Detailed plan]
**Quality Gates:** [Must-meet criteria]
**Why Recommended:** [Justification]
**Tradeoffs Accepted:** [Explicit acknowledgment]
**Success Metrics:** [How to measure]

[Repeat for conflicts needing tradeoff decisions]
</tradeoff_analysis>

<decision_framework>
## For Unresolved Conflicts

**Decision Criteria:**
1. [Criterion]: [Description, weight, how to evaluate]
2. [Criterion]: [Description, weight, evaluation method]
[Continue for all criteria]

**Decision Authority Matrix:**
[Table showing who decides what]

**When Stakeholders Disagree:**
1. Try data-driven resolution
2. Structured discussion
3. Escalation if needed
4. Document and commit

**Information Needed:** [Data gaps to fill]
**Timeline:** [When decisions must be made]
**Validation:** [How to verify decisions work]
**Adjustment Triggers:** [Signals to reconsider]
**Rollback Plan:** [How to reverse if wrong]
</decision_framework>

<communication_plan>
## Stakeholder Alignment Strategy

**Pre-Meeting 1:1s:**
[Process for individual conversations]

**Facilitated Group Session:**
**Agenda:**
1. Present conflicts (15 min)
2. Root causes (10 min)
3. Win-win solutions (20 min)
4. Tradeoff discussion (30 min)
5. Make decisions (15 min)
6. Document (10 min)

**Ground Rules:** [Discussion norms]
**Materials:** [What's needed]

**Documentation:**
[Decision record template with rationale, commitments, metrics, review dates]

**Ongoing Communication:**
- Weekly syncs
- Monthly metrics reviews
- Quarterly retrospectives
</communication_plan>

<validation_iteration>
## Testing Assumptions

### Decision: [Name]

**Assumptions:**
1. [Assumption to test]
2. [Assumption to test]

**Validation Approach:**
- Phase 1: [Method, timeline, criteria]
- Phase 2: [Method, timeline, criteria]
- Phase 3: [Method, timeline, criteria]

**Instrumentation:** [What data to collect]
**User Research:** [Qualitative validation]
**Success Criteria:** [Specific thresholds]

**Adjustment Plan:**
If [assumption] proves wrong: [What we'll do]

**Learning Documentation:** [How to capture insights]

[Repeat for each major decision]
</validation_iteration>

<process_improvements>
## Preventing Future Conflicts

**1. [Improvement]**
- Problem Solved: [Pattern prevented]
- Implementation: [How to do it]
- Owner: [Who's responsible]
- Timeline: [When]

[Continue for all process improvements identified]
</process_improvements>

</conflict_reconciliation>

FAILURE
- Any required section in `<conflict_reconciliation>` is missing or materially incomplete.
- Conflict mapping or root cause analysis is shallow or not grounded in inputs.
- Tradeoff analysis or recommendation lacks explicit rationale.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
