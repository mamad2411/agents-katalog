---
name: productize-competitive-parity-and-strategic-differentiation
description: >-
  Competitive parity and strategic differentiation. Use when the user needs a product workflow
  for product strategy related to competitive parity and strategic differentiation. Trigger
  terms: competitive-analysis, differentiation, product-strategy, decision-making.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Competitive parity and strategic differentiation

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

- **Skill**: `competitive-parity-and-strategic-differentiation`
- **Lifecycle**: Strategize
- **Category**: Strategy
- **Primary artifact**: Competitive parity and strategic differentiation strategy memo with choices, tradeoffs, risks, and recommended next move

Use this skill to run the Productize prompt contract for **Competitive parity and strategic differentiation**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{COMPETITIVE_FEATURE}}
- {{COMPETITOR_CONTEXT}}
- {{OUR_PRODUCT_STRATEGY}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: "Competitive parity and strategic differentiation".
Success metric:
- Produces a clear parity-vs-differentiation decision grounded in competitive context and product strategy.
- Distinguishes table-stakes matching from strategic differentiation, leapfrogging, or deliberate skipping.
- Provides actionable implementation guidance and monitoring signals tied to the recommendation.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only `{{COMPETITIVE_FEATURE}}`, `{{COMPETITOR_CONTEXT}}`, and `{{OUR_PRODUCT_STRATEGY}}`; if information is missing, state assumptions explicitly.
- Analyze competitor capability, UX, target users/use cases, and positioning before recommending action.
- Classify strategic importance as one of: Table Stakes, Valuable Differentiator, Non-Essential, Strategic Distraction.
- Evaluate four paths: do better, do differently, leapfrog, skip.
- Frame decisions as strategy-led (serving our users and positioning), not reactive feature copying.
- Include user/market implications, recommendation rationale, implementation guidance, and ongoing monitoring metrics/signals.
- Keep claims specific and evidence-oriented; avoid generic statements.

FORMAT
Return exactly this structure:

<competitive_strategy_analysis>
<competitive_feature_analysis>
**What Competitor Built:**  
[Describe capabilities and UX approach]

**Why They Built It:**  
[Infer strategic intent: what user need, what market position, what business goal]

**Who It Serves:**  
[Target users and use cases]

**How They Positioned It:**  
[Marketing/messaging angle]

**Market Reception:**  
[If known: user feedback, adoption, impact]
</competitive_feature_analysis>

<strategic_importance_assessment>
**Classification:**  
[Select one: Table Stakes / Valuable Differentiator / Non-Essential / Strategic Distraction]

**Rationale:**  
[Explain the classification]

**Evidence:**
- User feedback: [What users say about this]  
- Market trends: [Industry direction]  
- Win/loss data: [If relevant to deals]  
- Strategic alignment: [How it fits our positioning]  

**Risk of Not Having:**
- Deal losses: [High/Medium/Low]  
- User churn: [High/Medium/Low]  
- Perception damage: [High/Medium/Low]  

**Opportunity Cost:**  
[What else could we build with the same investment]
</strategic_importance_assessment>

<differentiation_opportunities>
<opportunity_1_better>
**Do It Better:**  
[How we could execute this more effectively than competitor]

**Our Advantages:**  
[What unique capabilities or context we have]

**User Value:**  
[How users benefit from our better approach]

**Effort:**  
[High/Medium/Low to achieve superior execution]
</opportunity_1_better>

<opportunity_2_different>
**Do It Differently:**  
[Alternative approach that serves our users better]

**Why This Works for Us:**  
[How it aligns with our strategy and user base]

**User Value:**  
[Why users would prefer this approach]

**Risks:**  
[What could go wrong with being different]
</opportunity_2_different>

<opportunity_3_leapfrog>
**Leapfrog:**  
[More advanced approach that makes competitor's solution look dated]

**Innovation:**  
[What's novel about this approach]

**User Value:**  
[Why this is significantly better]

**Feasibility:**  
[Can we actually pull this off? What's required?]

**Risk:**  
[Execution risk and market risk]
</opportunity_3_leapfrog>

<opportunity_4_skip>
**Skip Entirely:**  
[Case for not building this at all]

**Alternative:**  
[What we do instead that serves users differently]

**Rationale:**  
[Why skipping aligns with our strategy]

**Communication:**  
[How to position our absence of this feature]
</opportunity_4_skip>
</differentiation_opportunities>

<user_market_implications>
**User Expectations:**  
[What users now expect based on competitor precedent]

**Expectation Flexibility:**  
[Where users are open to alternatives vs. locked into patterns]

**Innovation Readiness:**  
[Would users welcome innovation here or is familiarity valued?]

**Education Required:**  
[If we differentiate, what teaching is needed?]

**Competitive Messaging:**  
[How to position our approach vs. competitor]
</user_market_implications>

<recommended_strategy>
**Recommendation:** [Match / Differentiate / Leapfrog / Skip]

**Specific Approach:**  
[Detailed description of what to build and how]

**Rationale:**  
[Why this approach is strategically right]

**Success Criteria:**  
[How we'll know this was the right decision]

**Timeline:**  
[When to execute]

**Resources Required:**  
[Team, time, budget]
</recommended_strategy>

<implementation_guidance>
**If Match:**
- Core capabilities to replicate: [List]  
- Where we can simplify: [Opportunities]  
- Where we must differentiate UX: [To fit our product]  

**If Differentiate:**
- Key differences: [What's different]  
- User communication: [How to explain our approach]  
- Risk mitigation: [How to validate innovation]  

**If Leapfrog:**
- Technical requirements: [What's needed]  
- User research: [Validation needed]  
- Phasing: [How to de-risk]  

**If Skip:**
- Alternative solution: [What we do instead]  
- Communication strategy: [How to position absence]  
- Monitoring: [What signals would change this decision]
</implementation_guidance>

<ongoing_monitoring>
[What to track to validate the decision:  
- Competitive intelligence: [Watch for X]  
- User feedback: [Listen for Y]  
- Market trends: [Monitor Z]  
- Performance metrics: [Track A, B, C]]
</ongoing_monitoring>
</competitive_strategy_analysis>

FAILURE
- Any required section/tag in `FORMAT` is missing, malformed, or materially incomplete.
- `Classification` is missing or not one of the allowed categories.
- Recommendation is missing or not aligned with prior analysis/evidence.
- User and market implications are omitted or disconnected from the recommended strategy.
- Implementation guidance does not map to the selected recommendation path.
- Monitoring signals/metrics are missing or non-actionable.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
