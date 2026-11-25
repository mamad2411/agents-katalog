---
name: productize-fragmented-user-research-synthesis-into-coherent-insights
description: >-
  Fragmented user research synthesis into coherent insights. Use when the user needs a product
  workflow for user research related to fragmented user research synthesis into coherent
  insights. Trigger terms: user-research, synthesis, insights.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Fragmented user research synthesis into coherent insights

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

- **Skill**: `fragmented-user-research-synthesis-into-coherent-insights`
- **Lifecycle**: Discover
- **Category**: Discovery
- **Primary artifact**: Fragmented user research synthesis into coherent insights research brief with evidence, insight clusters, assumptions, and next validation steps

Use this skill to run the Productize prompt contract for **Fragmented user research synthesis into coherent insights**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{RESEARCH_INPUTS}}
- {{PRODUCT_CONTEXT}}
- {{DESIGN_QUESTIONS}}
- {{CURRENT_ASSUMPTIONS}}
- {{BUSINESS_GOALS}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: Fragmented user research synthesis into coherent insights.
Success metric:
- Completes all required tasks and decision logic from the prompt instructions.
- Output is specific, evidence-based, and actionable.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required analysis steps, sections, or validation logic.
- Keep recommendations/outputs grounded in the input context; avoid generic filler.
- Synthesize fragmented research inputs into coherent, evidence-based insights that inform design and product decisions.
- Use the provided inputs:
- `{{RESEARCH_INPUTS}}`
- `{{PRODUCT_CONTEXT}}`
- `{{DESIGN_QUESTIONS}}`
- `{{CURRENT_ASSUMPTIONS}}`
- `{{BUSINESS_GOALS}}`
- Perform synthesis rigorously:
- Inventory and assess source quality/coverage.
- Extract coded observations (quotes, behaviors, themes, segment/context metadata).
- Identify cross-source patterns and contradictions.
- Assign confidence levels with explicit rationale.
- Map insights to JTBD and user-needs hierarchy.
- Link insights directly to design questions and actionable recommendations.
- Identify research gaps, unresolved assumptions, and prioritized follow-up research.
- Keep evidence traceable, avoid over-generalization, and state assumptions/uncertainties explicitly.

FORMAT
Return exactly this structure:

<research_synthesis>
<input_inventory>
**Data Sources Summary:**
- User interviews: [X participants] covering [topics, user segments, dates]
- Support tickets: [Y tickets] from [date range] about [primary themes]
- NPS feedback: [Z responses] with [average score] discussing [key topics]
- Usage analytics: [data range, key metrics, user actions analyzed]
- Feature requests: [count] requests across [platforms/sources]
- Usability tests: [sessions count] testing [specific flows or features]
- Survey data: [respondents count] on [topics covered]
- Anecdotal feedback: [source count] from [stakeholders, channels]
- Session recordings: [count] sessions showing [behaviors]
- Other sources: [specify any additional data]

**Data Quality Assessment:**
- Time range: [how recent is this data?]
- User segment coverage: [which personas/segments are represented?]
- Sample size adequacy: [sufficient for confidence in findings?]
- Potential bias: [what perspectives might be over/under-represented?]
- Data completeness: [what's missing or sparse?]
</input_inventory>

<key_insights>
<insight_1>
**Insight Statement:**
[One clear, specific sentence stating what you learned about users]

**Evidence:**
- User interviews: "[verbatim quote]" (Participant X, [segment])
- Support tickets: [Y tickets] report "[specific issue]" with keywords: [terms]
- NPS feedback: "[example comment]" (common theme in Z% of detractor responses)
- Analytics data: [X% of users] exhibit [specific behavior], [frequency/context]
- Additional evidence: [any other supporting data points]

**Confidence Level:** High / Medium / Low
**Rationale for Confidence:** [Why you assigned this confidence level]

**User Segments Affected:**
- [Segment 1]: [how this manifests for them]
- [Segment 2]: [how this manifests for them]

**Jobs-to-be-Done Connection:**
[Which job is this insight related to? How does it help or hinder job completion?]

**Design Implications:**
- Consider: [specific design approach this suggests]
- Avoid: [what this insight argues against]
- Prioritize: [which aspect of the experience to focus on]
- Measure: [how to validate design addressed this insight]

**Related Patterns:**
[Which other insights connect to this? How do they reinforce or complicate each other?]

**Business Impact:**
[How does addressing this insight connect to business goals or metrics?]
</insight_1>

<insight_2>
[Repeat the full structure for 5-10 key insights, maintaining consistent depth and evidence rigor]
</insight_2>

<insight_3>
[Continue for all major insights...]
</insight_3>
</key_insights>

<conflicting_signals>
**Conflict 1:**
- Signal A: [what one source or segment indicates]
- Signal B: [what contradicts this]
- Possible explanations:
  * [Explanation 1: e.g., different user segments with different needs]
  * [Explanation 2: e.g., stated preference vs. actual behavior]
  * [Explanation 3: e.g., context-dependent variation]
- Recommended resolution: [What research or analysis would clarify this?]
- Design strategy given conflict: [How to proceed despite uncertainty?]

**Conflict 2:**
[Repeat structure for each major contradiction in the data]

**Synthesis:**
[What do these conflicts reveal about user diversity, product complexity, or research gaps?]
</conflicting_signals>

<insight_mapping_to_design_questions>
**Question 1:** [Restate the first design question]
- **Answer based on research:** [What the data tells you]
- **Supporting insights:** [Which insights from above inform this answer]
- **Confidence level:** High / Medium / Low
- **Caveats and limitations:** [What qualifies or nuances this answer]
- **What we still don't know:** [Gaps specific to this question]
- **Recommended action:** [What to design/test/research next]

**Question 2:** [Restate the second design question]
[Repeat structure for each design question provided]

**New Questions Surfaced:**
[Design questions that emerged from the research but weren't originally asked]
</insight_mapping_to_design_questions>

<user_needs_hierarchy>
<critical_needs>
**Must-Have Needs (Strong Evidence, High Impact):**
1. [Need 1]: [description]
   - Evidence: [cross-source validation]
   - If unmet: [severe user/business consequence]
   - Current state: [how well is this met today?]

2. [Need 2]: [description]
   [Repeat structure for 3-5 critical needs]
</critical_needs>

<important_needs>
**Should-Have Needs (Moderate Evidence, Meaningful Impact):**
1. [Need 1]: [description]
   - Evidence: [validation from 1-2 strong sources]
   - If unmet: [moderate user friction or business impact]
   - Current state: [how well is this met today?]

2. [Need 2]: [description]
   [Repeat for 5-8 important needs]
</important_needs>

<nice_to_have>
**Nice-to-Have Needs (Weak Signal, Low/Uncertain Impact):**
1. [Need 1]: [description]
   - Evidence: [limited mentions or single source]
   - Potential value: [why this might matter despite weak signal]
   - Validation needed: [how to test if this is actually important]

2. [Need 2]: [description]
   [Repeat for 3-5 nice-to-have needs]
</nice_to_have>

<needs_by_segment>
**Segment-Specific Needs:**
- [Segment A]: [unique needs not shared by other segments]
- [Segment B]: [unique needs not shared by other segments]
- [Universal needs]: [needs expressed across all segments]
</needs_by_segment>
</user_needs_hierarchy>

<behavioral_patterns>
**Current Workflows and Workarounds:**
[Describe how users actually accomplish tasks today, including inefficient or creative workarounds that reveal unmet needs]

**Decision-Making Patterns:**
[How users make choices within the product, what information they seek, what causes hesitation or confidence]

**Pain Point Triggers:**
[Specific circumstances, contexts, or actions that consistently lead to user frustration]

**Success Patterns:**
[When and how users successfully achieve their goals, what enables their success]

**Usage Context and Frequency:**
[When, where, why, and how often users engage with the product or specific features]

**Adoption and Learning Patterns:**
[How users onboard themselves, what helps or hinders learning, common confusion points]

**Abandonment and Recovery Patterns:**
[What causes users to give up, what brings them back, how they recover from errors]

**Cross-Tool Workflows:**
[How users combine your product with other tools, what gaps force tool-switching]
</behavioral_patterns>

<jobs_to_be_done>
**Primary Functional Jobs:**
1. [Job]: When [situation], I want to [motivation], so I can [expected outcome]
   - Evidence: [how research revealed this job]
   - Current obstacles: [what prevents job completion]
   - Success criteria: [how users define successful job completion]

2. [Job]: [Repeat structure for 3-5 primary jobs]

**Emotional Jobs:**
- [Feel]: [emotion users want to feel, e.g., "feel confident in my decisions"]
- [Avoid]: [emotion users want to avoid, e.g., "avoid feeling overwhelmed"]
- Evidence: [quotes, observations, sentiment indicators]

**Social Jobs:**
- [Perception]: [how users want to be seen, e.g., "be perceived as data-driven"]
- [Context]: [social situations where product use matters]
- Evidence: [research indicators of social motivations]

**Related Jobs in the Consumption Chain:**
- Before main job: [how users discover, evaluate, and choose the product]
- After main job: [how users share, report, or build on outcomes]
- Maintenance jobs: [ongoing tasks to keep getting value]
</jobs_to_be_done>

<research_gaps>
<unanswered_questions>
**Critical Unknowns (Blocking Design Decisions):**
1. [Question]: [why this matters for design]
2. [Question]: [why this matters for design]
3. [Question]: [why this matters for design]

**Important Unknowns (Would Significantly Inform Design):**
1. [Question]: [how this would help]
2. [Question]: [how this would help]

**Curiosities (Interesting But Not Urgent):**
1. [Question]: [potential value]
2. [Question]: [potential value]
</unanswered_questions>

<recommended_research>
**Research Activity 1:**
- **Method:** [interviews / usability testing / survey / analytics deep-dive / diary study / etc.]
- **Target participants:** [which user segments, how many, recruitment criteria]
- **Key questions to answer:** [specific questions this research would resolve]
- **Expected outcomes:** [what you'll learn and how it informs design]
- **Effort estimate:** [time and resources required]
- **Priority:** High / Medium / Low - [rationale]

**Research Activity 2:**
[Repeat structure for 3-5 recommended research activities, prioritized by impact and urgency]
</recommended_research>

<assumptions_to_validate>
**Design Assumptions:**
1. [Assumption about user behavior or preferences]: Currently [validated / unvalidated / contradicted] by research
2. [Assumption about priorities or needs]: Currently [status]
3. [Assumption about technical or business constraints]: Currently [status]

**Team Assumptions:**
[Assumptions stakeholders or team members hold that aren't supported by data—list with gentle evidence-based reframing]

**Testing Strategy:**
[How to quickly validate or invalidate the most critical assumptions through lightweight tests]
</assumptions_to_validate>
</research_gaps>

<actionable_recommendations>
**Priority 1 Recommendations (Supported by High-Confidence Insights):**
1. [Specific design action]: [rationale tied to insight X, Y, Z]
   - Expected impact: [user and business outcomes]
   - Success metrics: [how to measure if this worked]

2. [Specific design action]: [rationale tied to insights]
   [Repeat for 3-5 top-priority recommendations]

**Priority 2 Recommendations (Supported by Medium-Confidence Insights):**
1. [Specific design action]: [rationale]
   [Repeat for 5-7 secondary recommendations]

**Quick Wins (Low Effort, Clear User Value):**
1. [Specific design action]: [why this is easy and valuable]
   [Repeat for 3-5 quick wins]

**Strategic Bets (Lower Confidence, High Potential):**
1. [Specific design action]: [why worth exploring despite uncertainty]
   - Validation approach: [how to test before full commitment]
   [Repeat for 2-3 strategic bets]

**Do Not Pursue:**
[Features, changes, or directions that research argues against, with rationale]
</actionable_recommendations>

<one_page_summary>
**Executive Summary**

**What We Learned:**
[2-3 sentences capturing the most important insights from the research]

**User Needs Priority:**
Users critically need [top need], strongly want [second need], and would appreciate [third need]. The evidence is strongest for [insight area] and weakest for [insight area requiring validation].

**Key Behavioral Patterns:**
[1-2 sentences on how users actually behave vs. what we might have assumed]

**Design Implications:**
The research strongly supports [recommended direction 1] and [recommended direction 2], while arguing against [current assumption or planned direction]. We should prioritize [specific user segment or job-to-be-done] because [evidence-based rationale].

**Critical Unknowns:**
We still need to understand [key gap 1] and [key gap 2] through [recommended research method].

**Recommended Next Steps:**
1. [Immediate action based on high-confidence insights]
2. [Design exploration for medium-confidence opportunities]
3. [Targeted research to fill critical gaps]

**Business Impact:**
Addressing these insights is expected to improve [business metric] by [directional estimate] because [user behavior change expected].

[Total: 250-350 words]
</one_page_summary>
</research_synthesis>

FAILURE
- Any required section in `<research_synthesis>` is missing or materially incomplete.
- Insights are not supported by cross-source evidence or confidence rationale.
- Contradictions are ignored or not addressed with a resolution approach.
- Recommendations are not prioritized or not linked to synthesized insights/business goals.
- Research gaps and assumption validation plan are missing or non-specific.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
