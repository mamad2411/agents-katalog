---
name: productize-post-launch-feedback-into-v2-improvements-synthesis
description: >-
  Post-launch feedback into v2 improvements synthesis. Use when the user needs a product
  workflow for business analysis related to post-launch feedback into v2 improvements
  synthesis. Trigger terms: pm, business-analysis, iteration, roadmap, feedback.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Post-launch feedback into v2 improvements synthesis

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

- **Skill**: `post-launch-feedback-into-v2-improvements-synthesis`
- **Lifecycle**: Launch & Learn
- **Category**: Discovery
- **Primary artifact**: Post-launch feedback into v2 improvements synthesis launch learning report with release evidence, feedback, decision, and next iteration

Use this skill to run the Productize prompt contract for **Post-launch feedback into v2 improvements synthesis**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{FEEDBACK_SOURCES}}
- {{ANALYTICS_DATA}}
- {{SUPPORT_TICKETS}}
- {{USER_INTERVIEWS}}
- {{PRODUCT_VISION}}
</provided_inputs>

GOAL
Synthesize post-launch signals into a defensible, prioritized v2 improvement plan and phased roadmap.
Success metric:
- Identifies cross-source themes with evidence and impact framing.
- Produces explicit prioritization logic and concrete improvement definitions.
- Delivers a sequenced roadmap with validation and monitoring plans.
- Follows the required output schema exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Use all inputs as evidence sources (`FEEDBACK_SOURCES`, `ANALYTICS_DATA`, `SUPPORT_TICKETS`, `USER_INTERVIEWS`, `PRODUCT_VISION`).
- Synthesize cross-source themes; do not rely on a single source for prioritization.
- Prioritize with explicit criteria at minimum: frequency, severity, reach, business impact, strategic alignment, effort, confidence.
- Use a defensible scoring approach (RICE, ICE, MoSCoW, or explicit custom model) and state the choice.
- For each prioritized theme, define concrete v2 improvements with user impact, solution, success criteria, dependencies, risks, and validation plan.
- Build a phased roadmap (critical fixes, high-impact, polish, future) with timeline, metrics, and go/no-go criteria.
- Include pre-launch and post-launch validation/monitoring loops.
- Keep recommendations actionable and explicitly linked to evidence.
- Explicitly call out assumptions when source quality or coverage is incomplete.

FORMAT
Return exactly this structure:

<v2_improvement_plan>
<executive_summary>
**Feedback Volume:** [Total pieces of feedback analyzed across all sources]

**Time Period:** [When was feedback collected? e.g., "30 days post-launch" or "Q1 2024"]

**Top 3 Themes:**
1. [Theme]: [Brief description] - [X% of feedback mentions this]
2. [Theme]: [Brief description] - [Y% of feedback mentions this]
3. [Theme]: [Brief description] - [Z% of feedback mentions this]

**Recommended v2 Focus:**
[High-level strategy: e.g., "Prioritize onboarding improvements and performance fixes to reduce churn, defer advanced features to v3"]

**Expected Impact:**
[What will improve if we execute this plan? e.g., "Reduce drop-off during signup by 30%, increase feature adoption by 20%, reduce support tickets by 40%"]
</executive_summary>

<feedback_analysis>
<source_breakdown>
## Analytics Data

**Key Findings:**
- [Metric]: [Value] - [Interpretation]
- [Drop-off point]: [X% abandon] - [Hypothesis why]
- [Underused feature]: [Y% adoption] - [Why low?]
- [Performance issue]: [Average load time Z seconds] - [Impact]

**Patterns Observed:**
[Describe usage patterns, unexpected behaviors, segment differences]

**Critical Metrics:**
- Activation rate: [X%]
- Retention (D7/D30): [Y%/Z%]
- Feature adoption: [List top and bottom features]
- Error rate: [N per session]

---

## Support Tickets

**Volume:** [Total tickets in period]

**Top 5 Issues:**
1. [Issue]: [N tickets, X% of total] - [Severity]
2. [Issue]: [N tickets, Y% of total] - [Severity]
3. [Issue]: [N tickets, Z% of total] - [Severity]
4. [Issue]: [N tickets] - [Severity]
5. [Issue]: [N tickets] - [Severity]

**Average Resolution Time:** [Hours/days]

**Escalations:** [How many required engineering/product involvement?]

**Workarounds:** [What are support agents telling users to do?]

---

## User Interviews

**Participants:** [N users, describe demographics/segments]

**Key Quotes:**
- "[Direct quote about pain point]" - [User type]
- "[Direct quote about unmet need]" - [User type]
- "[Direct quote about competitor comparison]" - [User type]

**Jobs-to-be-done:**
[What are users trying to accomplish with the product?]

**Unmet Needs:**
[What can't users do today that they wish they could?]

**Surprises:**
[Unexpected learnings about how users think about the product]

---

## App Store / Reviews

**Average Rating:** [X.X stars]  
**Total Reviews:** [N]

**Rating Distribution:**
- 5 star: [X%]
- 4 star: [Y%]
- 3 star: [Z%]
- 2 star: [W%]
- 1 star: [V%]

**Common Themes in Reviews:**
- Positive: [What users love]
- Negative: [What users hate]
- Feature requests: [What users ask for]

**Competitor Mentions:**
[How are users comparing to alternatives?]

---

## Sales/Customer Success Feedback

**Deal Blockers:** [Features missing that prevent sales]

**Churn Reasons:** [Why are users leaving?]

**Feature Parity Gaps:** [What do competitors have that we don't?]

**Implementation Challenges:** [What makes onboarding difficult?]

---

## Internal Stakeholder Input

**Engineering Concerns:**
[Technical debt, scalability issues, maintenance burden]

**Design Concerns:**
[Design debt, inconsistent patterns, accessibility gaps]

**Operations Concerns:**
[Support burden, deployment challenges, monitoring gaps]

**Business Concerns:**
[Revenue impact, competitive threats, strategic misalignment]
</source_breakdown>

<thematic_clustering>
For each identified theme, provide:

## Theme 1: [Theme Name]

**Description:** [What is this theme about?]

**Frequency:** [X mentions across Y sources]

**Affected Users:** [What % of users? Which segments?]

**Severity:** [Critical/High/Medium/Low - how much does this hurt?]

**Sources:**
- Analytics: [Specific data points]
- Support: [N tickets, common complaints]
- Interviews: [Key quotes or findings]
- Reviews: [Rating impact, common mentions]

**User Impact:**
[Describe how this affects users' ability to accomplish their goals]

**Business Impact:**
[Effect on key metrics: conversion, retention, revenue, NPS, support costs]

**Current Workarounds:**
[How are users coping with this problem today?]

**Root Cause Hypothesis:**
[Why does this problem exist? Design flaw? Technical limitation? Missing feature?]

---

[Repeat for Theme 2, Theme 3, etc.]

</thematic_clustering>

<prioritization_analysis>
<scoring_framework>
**Framework Used:** [RICE / ICE / MoSCoW / Custom]

**Scoring Criteria:**
- [Criterion 1]: [How we measure it]
- [Criterion 2]: [How we measure it]
- [Criterion 3]: [How we measure it]
- [Criterion 4]: [How we measure it]

**Thresholds for Prioritization:**
- Must-fix: [Score > X or meets Y criteria]
- High priority: [Score > Z]
- Medium priority: [Score > W]
- Low priority / Defer: [Score < W]
</scoring_framework>

<prioritized_themes>
Rank themes by priority with clear rationale:

**Priority 1: [Theme Name]**
- Score: [Numeric score if using framework]
- Rationale: [Why this is top priority - combine frequency, severity, business impact, strategic fit]
- Reach: [X% of users affected]
- Impact: [Expected improvement in key metric]
- Confidence: [How sure are we this is the right priority?]
- Effort: [Estimated work - S/M/L/XL]
- ROI: [High/Medium/Low]

**Priority 2: [Theme Name]**
[Same structure]

**Priority 3: [Theme Name]**
[Same structure]

---

**Deferred Themes:**
[Themes that didn't make the cut and why - e.g., "Low frequency, high effort, doesn't align with strategic direction"]
</prioritized_themes>
</prioritization_analysis>

<v2_improvements>
For each high-priority theme, define specific improvements:

## Improvement 1: [Name]

**Addresses Theme:** [Theme name]

**Problem Statement:**
[Clear description of what's broken and why it matters]

**User Impact:**
- **Who:** [User segment(s) affected]
- **How:** [How does this problem hurt them?]
- **Frequency:** [How often do they encounter this?]

**Proposed Solution:**
[Describe what you'll build/fix/improve - be specific but not prescriptive about implementation]

**User Stories:**
1. As a [user type], I want [capability], so that [benefit]
   - Acceptance criteria: [Specific, testable requirements]
2. [Additional user stories as needed]

**Success Criteria:**
[How will we know this improvement worked?]
- Metric: [Specific metric] improves from [current] to [target]
- User feedback: [Qualitative signal - e.g., "Support tickets about X decrease by 50%"]
- Adoption: [Y% of users use this feature within 30 days]

**Design Requirements:**
- [Specific UX/UI needs]
- [Accessibility requirements]
- [Responsive behavior]
- [Error states and edge cases to handle]

**Technical Requirements:**
- [API changes]
- [Database schema updates]
- [Performance targets - e.g., "Load in <200ms"]
- [Third-party integrations]
- [Security considerations]

**Dependencies:**
[What needs to happen before this can be built?]

**Risks:**
- [What could go wrong?]
- [How will we mitigate?]

**Effort Estimate:** [S/M/L/XL or sprint count]

**Priority:** [Must-have / Should-have / Could-have]

**Validation Plan:**
[How will we test this before launch?]
- User testing: [With whom, testing what?]
- A/B test: [Control vs. variant, success metric]
- Beta: [Rollout to X% of users for Y days]

---

[Repeat for Improvement 2, 3, etc.]

</v2_improvements>

<v2_roadmap>
<phase_1_critical_fixes>
**Timeline:** [Weeks or months]

**Goal:** [What must be fixed before anything else?]

**Improvements Included:**
1. [Improvement name]: [One-line description] - [Effort] - [Impact on metric]
2. [Improvement name]: [One-line description] - [Effort] - [Impact on metric]

**Success Metrics:**
- [Metric]: Improve from [X] to [Y]
- [Metric]: Reduce [problem] by [Z%]

**Go/No-Go Criteria:**
[What must be true to move to Phase 2?]

**Risks:**
[What could delay or derail Phase 1?]
</phase_1_critical_fixes>

<phase_2_high_impact>
**Timeline:** [Weeks or months after Phase 1]

**Goal:** [What strategic improvements drive key metrics?]

**Improvements Included:**
1. [Improvement name]: [One-line description] - [Effort] - [Impact on metric]
2. [Improvement name]: [One-line description] - [Effort] - [Impact on metric]

**Success Metrics:**
- [Metric]: Improve from [X] to [Y]

**Go/No-Go Criteria:**
[What must be true to move to Phase 3?]

**Risks:**
[What could delay or derail Phase 2?]
</phase_2_high_impact>

<phase_3_polish>
**Timeline:** [Weeks or months after Phase 2]

**Goal:** [What delights users and differentiates from competitors?]

**Improvements Included:**
1. [Improvement name]: [One-line description] - [Effort] - [Impact on metric]
2. [Improvement name]: [One-line description] - [Effort] - [Impact on metric]

**Success Metrics:**
- [Metric]: Improve from [X] to [Y]
- User sentiment: [NPS or satisfaction score improvement]

**Go/No-Go Criteria:**
[What must be true to consider v2 complete?]
</phase_3_polish>

<phase_4_future>
**Timeline:** [Post-v2, v3 timeframe]

**Goal:** [What longer-term bets are worth exploring?]

**Improvements Under Consideration:**
1. [Improvement name]: [Why deferred - needs more research, high uncertainty, strategic pivot]
2. [Improvement name]: [Why deferred]

**Research Needed:**
[What questions must be answered before prioritizing these?]
</phase_4_future>

<resource_requirements>
**Team Needed:**
- Engineering: [X people for Y weeks/months]
- Design: [X people for Y weeks/months]
- Product: [X people for Y weeks/months]
- QA: [X people for Y weeks/months]
- Other: [Content, legal, ops, etc.]

**Total Effort Estimate:** [Person-months or sprint count]

**Target Launch Date:** [When will v2 ship?]

**Milestones:**
- [Date]: Phase 1 complete
- [Date]: Phase 2 complete
- [Date]: Phase 3 complete
- [Date]: v2 launch

**Budget Considerations:**
[Any costs beyond team time - infrastructure, tools, licensing, contractors]
</resource_requirements>
</v2_roadmap>

<validation_and_monitoring>
<pre_launch_validation>
**User Testing:**
- Participants: [N users from segments X, Y, Z]
- Testing: [Prototypes, beta builds, specific workflows]
- Success criteria: [Task completion rate >X%, satisfaction score >Y]

**A/B Testing Plan:**
- Control: [Current experience]
- Variant: [New v2 improvements]
- Rollout: [Gradual - 5% → 25% → 50% → 100%]
- Primary metric: [What are we optimizing for?]
- Secondary metrics: [What else are we tracking?]
- Duration: [How long to run test?]
- Decision criteria: [What result causes us to ship/rollback?]

**Beta Program:**
- Participants: [N users, selection criteria]
- Duration: [X weeks before public launch]
- Feedback collection: [Surveys, interviews, in-app prompts]
- Success criteria: [What feedback validates we're ready to launch?]
</pre_launch_validation>

<post_launch_monitoring>
**Week 1 Monitoring:**
- Track: [Key metrics daily]
- Alert on: [Regressions, errors, drop-offs]
- Review: Daily standups to assess impact

**Week 2-4 Monitoring:**
- Track: [Key metrics weekly]
- Review: Weekly summaries of adoption, satisfaction, support tickets

**Month 2-3 Monitoring:**
- Deep dive: Did we achieve success criteria?
- User feedback: Survey users who adopted v2 features
- Support analysis: Did tickets decrease as expected?

**Success Criteria Review:**
- [Metric]: Target was [X], achieved [Y] - [Met/Missed/Exceeded]
- [Metric]: Target was [A], achieved [B] - [Met/Missed/Exceeded]

**Learnings:**
[What worked? What didn't? What would we do differently for v3?]
</post_launch_monitoring>

<iteration_plan>
**Feedback Loops:**
- User interviews: [Every X weeks with Y users]
- Analytics review: [Weekly/monthly cadence]
- Support ticket analysis: [Weekly summaries]
- NPS surveys: [Quarterly]

**v3 Planning:**
[When will we start gathering feedback for the next iteration?]
</iteration_plan>
</validation_and_monitoring>
</v2_improvement_plan>

FAILURE
- Any required top-level section in `FORMAT` is missing or malformed.
- Output does not use cross-source evidence for themes and prioritization.
- Prioritization lacks clear scoring logic or rationale.
- Improvements are vague, non-actionable, or not tied to user/business impact.
- Roadmap phases are missing sequencing, success metrics, or go/no-go criteria.
- Validation/monitoring plans are missing or superficial.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
