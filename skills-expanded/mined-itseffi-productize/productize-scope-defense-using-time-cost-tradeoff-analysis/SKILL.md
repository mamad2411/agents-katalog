---
name: productize-scope-defense-using-time-cost-tradeoff-analysis
description: >-
  Scope defense using time-cost tradeoff analysis. Use when the user needs a product workflow
  for project management related to scope defense using time-cost tradeoff analysis. Trigger
  terms: scope-management, prioritization, product-design, stakeholder-management.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Scope defense using time-cost tradeoff analysis

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

- **Skill**: `scope-defense-using-time-cost-tradeoff-analysis`
- **Lifecycle**: Plan
- **Category**: Delivery
- **Primary artifact**: Scope defense using time-cost tradeoff analysis delivery brief with scope, requirements, priorities, risks, and acceptance criteria

Use this skill to run the Productize prompt contract for **Scope defense using time-cost tradeoff analysis**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{CURRENT_SCOPE}}
- {{NEW_REQUEST}}
- {{PROJECT_CONSTRAINTS}}
- {{TEAM_CAPACITY}}
- {{EXISTING_PRIORITIES}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: Scope defense using time-cost tradeoff analysis.
Success metric:
- Completes all required tasks and decision logic from the prompt instructions.
- Output is specific, evidence-based, and actionable.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required analysis steps, sections, or validation logic.
- Keep recommendations/outputs grounded in the input context; avoid generic filler.
- Use `{{CURRENT_SCOPE}}`, `{{NEW_REQUEST}}`, `{{PROJECT_CONSTRAINTS}}`, `{{TEAM_CAPACITY}}`, and `{{EXISTING_PRIORITIES}}` to quantify tradeoffs.
- Provide a full effort breakdown (design/engineering/QA/documentation) plus indirect costs.
- Assess timeline, scope, quality, team health, and stakeholder impacts.
- Evaluate user, business, technical, and strategic value with explicit scoring.
- Present at least the five decision options (add/extend, swap, defer, MVP, reject) and recommend one.
- Provide decision criteria, escalation triggers, assumptions, and next steps.

FORMAT
Return exactly this structure:

<scope_tradeoff_analysis>
<request_summary>
## New Request Overview

**Requested by:** [Person/team/stakeholder]
**Request date:** [When request was made]
**Context:** [Why this is being requested - user feedback, competitive pressure, stakeholder priority, etc.]

**Description:**
[Clear, concise description of what's being requested]

**Stated rationale:**
[Why requester believes this is important]

</request_summary>

<comprehensive_cost_analysis>
## Effort Breakdown

### Design Effort

**Research and Discovery:** [X hours]
- [Specific task 1]
- [Specific task 2]
- [Continue...]

**Concept and Ideation:** [X hours]
- [Specific task]
- [Continue...]

**Detailed Design:** [X hours]
- [Specific task]
- [Continue...]

**Iteration and Refinement:** [X hours]
- [Specific task - design reviews, stakeholder feedback, usability testing]
- [Continue...]

**Design System Work:** [X hours]
- [Specific task - new components, variants, documentation]
- [Continue...]

**Handoff and Specification:** [X hours]
- [Specific task - redlines, developer collaboration, design QA]
- [Continue...]

**Total Design Effort:** [X hours] = [Y days]

### Engineering Effort

**Technical Discovery:** [X hours]
- [Specific task - architecture decisions, feasibility assessment, spike work]
- [Continue...]

**Frontend Implementation:** [X hours]
- [Specific task - UI components, styling, interactions, responsive behavior]
- [Continue...]

**Backend Implementation:** [X hours] (if applicable)
- [Specific task - API changes, database schema, business logic]
- [Continue...]

**Integration Work:** [X hours]
- [Specific task - connecting frontend to backend, third-party services, etc.]
- [Continue...]

**Testing and Quality:** [X hours]
- [Specific task - unit tests, integration tests, cross-browser testing]
- [Continue...]

**Performance Optimization:** [X hours]
- [Specific task]
- [Continue...]

**Code Review and Refactoring:** [X hours]
- [Specific task]
- [Continue...]

**Total Engineering Effort:** [X hours] = [Y days]

### QA and Validation Effort

**Test Planning:** [X hours]
- [Specific task]
- [Continue...]

**Manual Testing:** [X hours]
- [Specific task - functional, cross-browser, responsive, device testing]
- [Continue...]

**Automated Testing:** [X hours] (if applicable)
- [Specific task]
- [Continue...]

**Regression Testing:** [X hours]
- [Specific task - ensuring no breakage in existing functionality]
- [Continue...]

**Accessibility Testing:** [X hours]
- [Specific task - keyboard navigation, screen reader, WCAG compliance]
- [Continue...]

**Edge Case Testing:** [X hours]
- [Specific task]
- [Continue...]

**Bug Fixing Cycles:** [X hours]
- [Expected iteration time based on complexity]

**Total QA Effort:** [X hours] = [Y days]

### Documentation and Communication

**User Documentation:** [X hours]
- [Help articles, tooltips, onboarding content]

**Technical Documentation:** [X hours]
- [Technical specs, API docs, architecture decisions]

**Stakeholder Communication:** [X hours]
- [Updates, demos, alignment meetings]

**Team Onboarding:** [X hours]
- [Training team members on new feature]

**Total Documentation:** [X hours]

### Total Direct Effort

**Total Hours:** [Sum of all above] hours
**Total Days:** [Accounting for parallel work] days
**Confidence Level:** [High / Medium / Low]
- [Explanation of confidence - e.g., "Medium confidence - design is straightforward but engineering unknowns exist"]

## Hidden and Indirect Costs

**Technical Debt:**
- [Description of shortcuts or compromises this introduces]
- [Future cost to address this debt: X days]
- [Impact on codebase maintainability or complexity]

**Future Maintenance Burden:**
- [Ongoing cost to support, enhance, and troubleshoot this feature]
- [Estimated: X hours per quarter]

**Complexity Tax:**
- [How this increases overall product or codebase complexity]
- [Impact on future development speed or onboarding]

**Opportunity Cost:**
- [What else could be accomplished with this time?]
- [Specific alternatives: e.g., "Could complete [other feature] or [technical improvement]"]

**Context Switching Cost:**
- [Cost of interrupting current work to accommodate this]
- [Estimated productivity loss: X hours]

**Risk Additions:**
- [New failure modes introduced: e.g., "Additional error states to handle"]
- [Increased testing surface area]
- [Potential user confusion: e.g., "Adds complexity to already complex flow"]

**Total Indirect Cost:** [Estimated in hours or qualitative assessment]

</comprehensive_cost_analysis>

<impact_assessment>
## Impact on Timeline

**Current Committed Deadline:** [Date]
**Revised Deadline (if adding this):** [New date] (+X days/weeks)

**Milestone Slippage:**
- [Milestone 1]: [Original date] → [New date]
- [Milestone 2]: [Original date] → [New date]
- [Continue...]

**Dependencies Affected:**
- [Team/project depending on original timeline] - [Impact]
- [Continue...]

**Market/Business Timing Concerns:**
- [Product launch window, competitive deadline, seasonal timing, customer commitments, etc.]

## Impact on Scope (If Timeline Holds)

**What must be deprioritized or cut to fit this in:**

**Item 1:** [Feature or work item]
- **Description:** [What this is]
- **Current status:** [In progress, planned, etc.]
- **Value lost:** [User and business impact of cutting this]
- **Effort saved:** [X days]

**Item 2:** [Feature or work item]
[Same structure]

[Continue for all items that would need to be cut]

**Total scope reduction:** [X days saved] (offsetting [Y days] required for new request)

## Impact on Quality and Risk

**Testing Coverage:**
- [Impact on test coverage if timeline is constrained]
- [Higher bug risk in: specific areas]

**Design Quality:**
- [Areas where design would be rushed or less polished]
- [UX debt created: e.g., "Inconsistency with design system," "Less iteration on interaction model"]

**Technical Quality:**
- [Code shortcuts required to meet deadline]
- [Long-term maintenance issues created]

**Accessibility:**
- [Risk of cutting accessibility work if time is tight]
- [Compliance and usability impact]

**User Experience Consistency:**
- [Risk of poor integration with existing features]
- [Design system alignment compromised]

## Impact on Team Health

**Morale:**
- [Effect of constant scope changes on team confidence and trust]

**Burnout Risk:**
- [If timeline doesn't adjust, team must absorb increased work]
- [Current team utilization: X% - adding this increases to Y%]

**Context Switching:**
- [Cost of disrupting current focused work]
- [Productivity impact]

**Trust and Commitments:**
- [Impact on team's trust if commitments repeatedly change]

## Stakeholder and Communication Impact

**Who needs to be informed:**
- [Leadership, marketing, sales, customers, partners, etc.]

**External commitments affected:**
- [Press releases, customer promises, partnerships, events, etc.]

**Credibility impact:**
- [Effect on credibility of missing committed dates]
- [Relationship impact with stakeholders]

</impact_assessment>

<value_evaluation>
## User Impact Assessment

**Affected Users:**
- **Percentage/Number:** [e.g., "30% of active users" or "All new users during onboarding"]
- **Personas:** [Which specific user types benefit]

**Use Case Frequency:**
- [How often users encounter this scenario]
- Daily / Weekly / Monthly / Rare edge case

**Severity of Need:**
- [ ] **Blocker:** Users cannot accomplish core task without this
- [ ] **Major friction:** Users can accomplish task but with significant difficulty/inefficiency
- [ ] **Minor improvement:** Nice-to-have that slightly improves experience
- [ ] **Delight feature:** Pure enhancement with no functional necessity

**User Workarounds:**
- [How users currently achieve this goal (if possible)]
- [Cost/pain of workaround: time, frustration, error rate]

**User Impact Score:** [X/10]
- **Calculation:** [# users] × [frequency] × [severity]
- **Rationale:** [Explanation of score]

## Business Impact Assessment

**Revenue Impact:**
- [Does this directly affect revenue?]
- **Quantified:** [e.g., "Expected to increase conversion by 5%, worth $200K annually"]
- **Qualitative:** [e.g., "Required for enterprise sales" or "Reduces churn risk"]

**Cost Savings:**
- [Does this reduce operational costs, support burden, technical debt?]
- [Quantified if possible]

**Strategic Alignment:**
- [ ] **High:** Core to strategic direction, unlocks future initiatives
- [ ] **Medium:** Supports strategy but not critical path
- [ ] **Low:** Tangential or unrelated to strategic priorities
- **Explanation:** [How this fits or doesn't fit strategy]

**Competitive Necessity:**
- [ ] **Must-have:** Competitors all have this, we're behind without it
- [ ] **Nice-to-have:** Would match competitors but not falling behind without it
- [ ] **Differentiator:** Opportunity to exceed competitors and stand out
- **Explanation:** [Competitive landscape context]

**Market Timing:**
- [Does this need to launch with initial release?]
- [Reason: competitive window, customer commitment, seasonal timing, etc.]

**Business Impact Score:** [X/10]
- **Rationale:** [Explanation based on revenue + strategy + competitive factors]

## Technical and Strategic Impact

**Enables Future Work:**
- [Does this create foundation for future features?]
- [Specific examples of what this unlocks]

**Reduces Technical Debt:**
- [Does this pay down existing debt or prevent future debt?]

**Platform Investment:**
- [Does this strengthen platform/design system for long-term benefit?]

**Learning Value:**
- [Does this teach us something important about users or technology?]
- [Validation or de-risking value]

## Relative Value Comparison

**Value of New Request:** [User impact score + Business impact score] = [Total]

**Value of Work That Would Be Delayed/Cut:**
- **Item 1:** [Name] - [User impact X/10 + Business impact Y/10] = [Total]
- **Item 2:** [Name] - [User impact X/10 + Business impact Y/10] = [Total]
- [Continue...]

**Comparison:**
[Is new request higher or lower value than what it would replace?]

**Opportunity Cost Analysis:**
[What else could be accomplished with same effort - specific alternatives and their value]

**Value Ranking:**
1. [Highest value item]
2. [Second highest]
3. [Continue...]

**Conclusion:** [Is new request top priority compared to alternatives?]

</value_evaluation>

<decision_options>
## Option 1: Add to Scope with Timeline Extension

**Description:** Include new request, extend deadline to accommodate full effort

**Timeline Change:**
- **Original deadline:** [Date]
- **New deadline:** [Date] (+X days/weeks)

**Cost:**
- **Delayed launch:** [Business impact - e.g., "Miss Q4 launch window"]
- **Missed market timing:** [If applicable - competitive announcement, seasonal timing]
- **Stakeholder impact:** [Who this affects and how]
- **Team impact:** [Extended project, potential fatigue]

**Benefit:**
- Full scope delivered with quality
- No compromises to existing commitments
- Team has adequate time for quality work
- All value realized: [New request + existing scope]

**Tradeoff Summary:** More complete product, later delivery

**When to Choose:** Market timing is flexible and complete feature set is more important than launch date

**Risks:**
- [Market window may close]
- [Competitor may launch first]
- [Team morale if project extends too long]

## Option 2: Swap for Existing Scope (Maintain Timeline)

**Description:** Include new request, cut other work to maintain timeline

**What Gets Cut:**

**Cut Item 1:** [Name]
- **Description:** [What this is]
- **Value lost:** [User impact X/10, Business impact Y/10]
- **Justification for cut:** [Why this is lower priority than new request]
- **Effort saved:** [X days]

**Cut Item 2:** [Name]
[Same structure]

[Continue...]

**Cost:**
- Lost value from cut items: [Total value score]
- Potential technical debt: [If cutting quality work]
- Future rework: [If cut items need revisiting later]

**Benefit:**
- Maintain original timeline
- Deliver new request at launch
- Value of new request realized: [Score]

**Tradeoff Summary:** Different scope, same timeline

**When to Choose:** New request is higher value than what would be cut, and timeline is immovable

**Risks:**
- [Value judgment may be wrong - cut item may prove more important]
- [User confusion if expected features are missing]

## Option 3: Defer to Next Phase/Release

**Description:** Maintain current scope and timeline, add new request to future backlog

**Next Opportunity:** [When this could be addressed - e.g., "Q2 2025 release"]

**Cost:**
- Short-term: Users don't benefit from new request at launch
- Temporary workaround: [How users handle gap until next release]
- Potential competitive gap: [If this is competitive feature]

**Benefit:**
- Maintain scope, timeline, quality of current release
- Team delivers committed work excellently
- Validate need post-launch: [Can gather user feedback first]
- Time to implement properly: [More thoughtful with v1 learnings]

**Tradeoff Summary:** Launch on time with committed scope, add later

**When to Choose:** Current scope is sufficient for launch and new request can wait for v2

**Risks:**
- [Users may complain about missing feature]
- [Competitive gap if feature is table stakes]

## Option 4: Deliver Simplified/MVP Version

**Description:** Include reduced version delivering core value with less effort

**Simplified Scope:**
- **Included:** [Core functionality in MVP]
- **Deferred:** [Advanced features, edge cases, polish saved for v2]

**Effort Comparison:**
- **Original estimate:** [X days]
- **Simplified version:** [Y days]
- **Savings:** [Z days]

**Cost:**
- Reduced functionality: [What users don't get]
- Future enhancement needed: [Likely to revisit]
- Potential user confusion: [If simplified version has limitations]

**Benefit:**
- Partial value realized now
- Lower cost and risk
- Validate before full investment
- Enhance in future based on usage

**Tradeoff Summary:** Some value now, full value later

**When to Choose:** Core value can be delivered simply and full version can wait for validation

**Risks:**
- [Users may be confused by limitations]
- [May create technical debt if MVP not architected for future expansion]

## Option 5: Reject (Maintain Current Plan)

**Description:** Do not include new request in current project

**Cost:**
- Value of request not realized
- Requester may be disappointed
- Potential missed opportunity

**Benefit:**
- Team maintains focus
- Delivers committed work with quality
- Preserves timeline and stakeholder commitments

**Tradeoff Summary:** Focused delivery of original scope

**When to Choose:** New request is significantly lower value than committed work and can be addressed separately (or not at all)

**Risks:**
- [Requester pushback]
- [May have been right that this was important]

</decision_options>

<recommendation>
## Recommended Approach

**Selected Option:** [Option number and name]

**Rationale:**

**Value Analysis:**
- [How value of new request compares to alternatives]
- [Whether value justifies cost and tradeoffs]

**Cost-Benefit:**
- [Effort required: X days]
- [Value delivered: Y score]
- [Comparison to alternatives]

**Strategic Fit:**
- [Alignment with company/product goals and priorities]
- [Long-term vs. short-term considerations]

**Risk Assessment:**
- [Key risks identified]
- [How chosen option mitigates or accepts risks]

**Key Deciding Factors:**
1. **[Factor 1]:** [e.g., "Market timing is critical - launch date cannot slip"]
2. **[Factor 2]:** [e.g., "New request has 8/10 user impact vs. cut item with 4/10"]
3. **[Factor 3]:** [e.g., "Simplified version delivers 80% value for 30% effort"]

**Confidence Level:** [High / Medium / Low]
- **Explanation:** [Why this confidence level - known vs. unknown factors]

**Alternative if Context Changes:**
- **If [assumption/constraint changes]:** [Consider alternative option]
- **Example:** "If launch deadline extends by 3 weeks, reconsider Option 1 (full scope with timeline extension)"

</recommendation>

<decision_framework>
## Questions to Guide Decision

**Must-Have Test:**
- Is this absolutely required for product to be useful/sellable at launch?
- Why or why not?
- What's the minimum viable version needed?

**User Workaround Assessment:**
- Can users accomplish their goal without this feature?
- What's the cost of that workaround (time, frustration, errors)?
- Is the workaround acceptable short-term?

**Delay Cost Analysis:**
- What happens if we launch without this and add it in next release?
- Do we lose customers, revenue, or competitive position?
- Or is delay impact minimal?

**Value Comparison:**
- Is this higher priority than what it would delay or replace?
- Run the value scores side-by-side
- What do users and business need most?

**Risk Tolerance:**
- Are we willing to accept quality/timeline tradeoffs to include this?
- What risks are acceptable vs. unacceptable?
- What's our risk appetite right now?

**Strategic Lens:**
- Does this advance our strategic vision and differentiation?
- Or is this a distraction from core value proposition?

## Decision Criteria

**Inclusion threshold:**
- If [User impact score × Business impact score] ≥ [Threshold - e.g., 50], strongly consider including
- If below threshold, likely defer or reject

**Capacity check:**
- If [Effort estimate] > [Available capacity buffer], timeline MUST extend or scope MUST swap
- If within buffer, can potentially absorb

**Timeline constraint:**
- If [Timeline delay] > [Acceptable window - e.g., 2 weeks], must cut other scope or reject
- If within acceptable delay, timeline extension is option

**Authority escalation:**
- If requester is [C-level or VP], escalate to [decision maker at same level]
- Ensure tradeoffs are visible to appropriate decision-making level

## Escalation Triggers

**Escalate to [Leadership Level] if:**
- Timeline impact exceeds [X weeks]
- Scope change affects previously communicated external commitments (customer, press, partnerships)
- Multiple senior stakeholders disagree on priority
- Request comes from executive leadership (requires executive tradeoff discussion)
- Team flags significant technical risk, debt, or feasibility concerns

**Decision Owner:** [Role - PM, Design Lead, Director, VP, etc.]

**Decision Timeline:** Decision must be made by [Date] to avoid impacting project critical path

</decision_framework>

<assumptions_and_next_steps>
## Key Assumptions

**Assumption 1:** [e.g., "Effort estimate assumes no major technical blockers"]
- **Validation needed:** [Engineering spike or deeper technical review]
- **If wrong:** [Impact on recommendation]

**Assumption 2:** [e.g., "User impact score based on current usage patterns"]
- **Validation needed:** [User research or analytics review]
- **If wrong:** [Impact on recommendation]

**Assumption 3:** [e.g., "Timeline extension assumes no dependencies on other teams"]
- **Validation needed:** [Confirm with dependent teams]
- **If wrong:** [Impact on recommendation]

[Continue for all key assumptions]

## Validation Needed

**Before final decision:**
- [ ] Engineering review of effort estimate for technical accuracy
- [ ] Stakeholder confirmation of whether timeline can extend (if considering Option 1)
- [ ] Product/business review of value assessment
- [ ] Team capacity check for bandwidth to absorb (if considering Option 2 or 4)

## Next Steps

**Immediate:**
1. Share this analysis with decision maker and key stakeholders
2. Schedule decision meeting by [Date]
3. Gather validation inputs listed above

**Post-Decision:**

**If approved (Option 1, 2, or 4):**
- Update project plan with new scope
- Adjust milestones and timeline
- Communicate changes to team and affected stakeholders
- Update external commitments (if timeline changed)
- Reprioritize backlog (if scope swapped)

**If deferred (Option 3):**
- Add to backlog with full context from this analysis
- Set review date for next planning cycle [Date]
- Communicate decision and rationale to requester
- Document why deferred for future reference

**If rejected (Option 5):**
- Document decision and rationale
- Communicate thoughtfully to requester (explain tradeoffs, not just "no")
- Note for future: if this request returns, reference this analysis

**Communication Plan:**
- [Who to inform of decision]
- [What to communicate (decision, rationale, timeline impact)]
- [When to communicate (immediately post-decision)]

</assumptions_and_next_steps>
</scope_tradeoff_analysis>

FAILURE
- Any required section in `<scope_tradeoff_analysis>` is missing or materially incomplete.
- Cost breakdown, impact assessment, or value evaluation is missing or superficial.
- Recommendation lacks clear rationale or does not reference tradeoff options.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
