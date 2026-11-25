---
name: productize-aging-research-insight-validation-before-reusing
description: >-
  Aging research insight validation before reusing. Use when the user needs a product workflow
  for user research related to aging research insight validation before reusing. Trigger
  terms: user-research, validation, insights.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Aging research insight validation before reusing

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

- **Skill**: `aging-research-insight-validation-before-reusing`
- **Lifecycle**: Discover
- **Category**: Discovery
- **Primary artifact**: Aging research insight validation before reusing research brief with evidence, insight clusters, assumptions, and next validation steps

Use this skill to run the Productize prompt contract for **Aging research insight validation before reusing**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{EXISTING_RESEARCH}}
- {{CURRENT_CONTEXT}}
- {{TIME_SINCE_RESEARCH}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: Aging research insight validation before reusing.
Success metric:
- Completes all required tasks and decision logic from the prompt instructions.
- Output is specific, evidence-based, and actionable.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required analysis steps, sections, or validation logic.
- Keep recommendations/outputs grounded in the input context; avoid generic filler.
- Evaluate research currency using `{{EXISTING_RESEARCH}}`, `{{CURRENT_CONTEXT}}`, and `{{TIME_SINCE_RESEARCH}}`.
- Assess decay factors (time, market, product, user base, competition, contextual/regulatory changes).
- Classify insights by confidence (`high`, `medium`, `low`) with evidence and caveats.
- Identify stable insight patterns vs decayed patterns.
- Propose validation research (quick validation + deeper follow-up), testable hypotheses, and prioritized research gaps.
- Provide clear guidance on what is safe to use now, what to use cautiously, and what to retire.
- Respect prior research investment while being explicit about limitations and assumptions.

FORMAT
Return exactly this structure:

<research_validation_assessment>
<decay_factor_analysis>
<time_decay>
- Time since research: [X months/years]
- Decay risk: [Low/Medium/High]
- Reasoning: [Why time matters for this research]
</time_decay>

<market_changes>
- Changes: [List significant market shifts]
- Impact on insights: [How these changes affect research validity]
- Decay risk: [Low/Medium/High]
</market_changes>

<product_changes>
- Changes: [List how product has evolved]
- Impact on insights: [Which insights are now outdated]
- Decay risk: [Low/Medium/High]
</product_changes>

<user_base_changes>
- Changes: [How users/segments have changed]
- Impact on insights: [Which user insights may no longer apply]
- Decay risk: [Low/Medium/High]
</user_base_changes>

<competitive_landscape>
- Changes: [How competitors have evolved]
- Impact on insights: [How this affects user expectations/behaviors]
- Decay risk: [Low/Medium/High]
</competitive_landscape>

<contextual_changes>
- Changes: [Regulatory, technology, environmental shifts]
- Impact on insights: [What's different now]
- Decay risk: [Low/Medium/High]
</contextual_changes>
</decay_factor_analysis>

<insight_validity_assessment>
<high_confidence_insights>
[Insights that are likely still valid:

**Insight:** [Original finding]

**Type:** [Fundamental need / Core job / Deep motivation]

**Why Still Valid:**
[Reasoning for confidence]

**Evidence:**
[Any recent signals supporting this]

**Caveat:**
[Any context to consider]

**Recommended Use:**
[How to apply this insight today]]
</high_confidence_insights>

<medium_confidence_insights>
[Insights that should be validated:

**Insight:** [Original finding]

**Type:** [Behavior / Pain point / Preference / Workflow]

**Decay Concern:**
[What might have changed]

**Current Confidence:** [50-75%]

**Validation Needed:**
[Specific questions to answer]

**Quick Validation:**
[Lightweight way to check if still true]

**Use As:**
[Hypothesis to test, not fact to assume]]
</medium_confidence_insights>

<low_confidence_insights>
[Insights that are likely outdated:

**Insight:** [Original finding]

**Why Likely Invalid:**
[Specific decay factors]

**Current Confidence:** [<50%]

**Recommendation:**
[Don't rely on this - research fresh]

**New Research Needed:**
[What to study instead]]
</low_confidence_insights>
</insight_validity_assessment>

<patterns_of_decay>
**What Types of Insights Have Decayed:**
[Common patterns: e.g., "Tool-specific workflows are outdated" or "Pain points around X have been solved"]

**What Remains Stable:**
[Common patterns: e.g., "Core job of [Y] hasn't changed" or "Fundamental need for [Z] still exists"]

**Decay Acceleration Factors:**
[What makes insights go stale faster in this domain]
</patterns_of_decay>

<validation_research_plan>
**Critical Questions to Answer:**
1. [Question that would validate/invalidate high-priority insight]
2. [Question that would validate/invalidate high-priority insight]
3. [Question that would validate/invalidate high-priority insight]

**Proposed Research Approach:**

**Phase 1: Quick Validation (1-2 weeks)**
- Method: [Lightweight approach: surveys, analytics review, stakeholder interviews]
- Purpose: [Confirm or refute medium-confidence insights]
- Sample: [Who to include]
- Key questions: [List]

**Phase 2: Deep Dive (3-4 weeks, if needed)**
- Method: [Rigorous approach: user interviews, observation, diary studies]
- Purpose: [Generate fresh insights on areas of uncertainty]
- Sample: [Who to include]
- Key questions: [List]

**Decision Point:**
- After Phase 1: [Determine if Phase 2 is needed]
- Criteria: [What findings would trigger deeper research]
</validation_research_plan>

<hypothesis_generation>
[Convert old insights into testable hypotheses:

**Old Insight:** [Original finding]

**Current Hypothesis:** [Reformulated as testable statement]

**Test:** [How to validate]

**If True:** [What it means for design]

**If False:** [What it means for design]

**Alternative Hypotheses:**
[Other possibilities to consider]]
</hypothesis_generation>

<research_gaps>
**What We Don't Know:**
[List critical unknowns not covered by old research:
- New user segments
- New use cases
- New competitors/alternatives
- New technologies
- New constraints]

**Priority:**
[Which gaps are most critical to fill]

**Proposed Research:**
[How to fill each gap]
</research_gaps>

<safe_to_use>
**Insights You Can Use Today:**
[List high-confidence insights with caveats]

**Use With Caution:**
[List medium-confidence insights with required validation]

**Don't Use:**
[List low-confidence insights to discard]
</safe_to_use>

<research_hygiene>
**Best Practices Going Forward:**
- Research expiration dating: [Label research with "valid until" or "revalidate by"]
- Decay indicators: [Track market/product changes that invalidate research]
- Continuous learning: [Lightweight ongoing research to keep insights fresh]
- Research library: [System for marking outdated research]
- Validation triggers: [Events that should trigger revalidation]
</research_hygiene>

<communication>
**How to Present to Team:**
[Guidance for explaining which research to trust:
- Be transparent about confidence levels
- Explain decay factors
- Propose validation plan
- Don't dismiss old research entirely - use as starting point]

**Research Debt Message:**
[Draft message explaining need for fresh research while respecting past investment]
</communication>
</research_validation_assessment>

FAILURE
- Any required section in `<research_validation_assessment>` is missing or materially incomplete.
- Confidence classifications are unsupported by decay-factor reasoning.
- Validation plan lacks concrete questions, methods, or decision criteria.
- Safe-to-use guidance does not clearly separate `use now` / `use with caution` / `don't use`.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
