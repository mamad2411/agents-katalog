---
name: productize-strategy-curve-blue-ocean
description: >-
  Apply strategy curve and blue ocean analysis to compare an offer against competitors,
  identify factors of competition, plot as-is and to-be value curves, and define breakaway
  moves. Use for marketing strategy, category redesign, differentiation, noncustomer demand
  creation, and competitor value-curve analysis.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Strategy Curve and Blue Ocean

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

- **Skill**: `strategy-curve-blue-ocean`
- **Lifecycle**: Strategize
- **Category**: Marketing
- **Primary artifact**: Strategy Curve and Blue Ocean strategy memo with choices, tradeoffs, risks, and recommended next move

Use this skill when the user needs to redesign an offer, category, or go-to-market strategy by changing the basis of competition.

Do not use it for generic competitor lists, positioning copy only, brand voice, or growth funnel diagnosis unless the user also needs a value-curve comparison.

## Inputs

Collect or infer:

- Industry/category and geography.
- Target customer or noncustomer group.
- Main competitors or strategic groups.
- Current offer and intended offer.
- Known customer frustrations, unmet outcomes, or barriers to adoption.
- Evidence: interviews, reviews, sales notes, market data, pricing, feature tables, usage data.

If evidence is thin, label the analysis as hypothesis-driven.

## Workflow

1. **Define the arena**
   - State the current red-ocean category and the buyer/noncustomer group being analyzed.
   - Name strategic groups separately when the market has clusters such as premium, budget, self-serve, enterprise, incumbent, or substitute.

2. **List factors of competition**
   - Use buyer-facing factors, not internal capabilities.
   - Include price/cost, access, product performance, service, experience, complexity, risk, status, convenience, trust, switching cost, and any category-specific factors.
   - Remove factors that customers cannot perceive or that do not affect choice.

3. **Plot the as-is strategy curves**
   - Score each factor on a consistent 0-5 or Low/Medium/High scale.
   - Plot the current offer and major competitors.
   - Highlight convergence, overinvestment, underinvestment, and factors that serve legacy assumptions more than customer value.

4. **Find blue-ocean openings**
   - Ask where noncustomers are blocked by complexity, intimidation, cost, access, risk, or status codes.
   - Identify where demand could be created rather than fought over.
   - Look for factors the industry treats as mandatory but customers do not actually value.

5. **Design the to-be value curve**
   - Use the four actions:
     - Eliminate: factors the industry takes for granted that can disappear.
     - Reduce: factors over-served relative to customer value.
     - Raise: factors that matter but are under-served.
     - Create: new factors that unlock demand, trust, access, simplicity, or delight.
   - The to-be curve should be visibly different, not just slightly better everywhere.

6. **Translate into strategic moves**
   - Name the projects required to close the gap.
   - Define what must change in product, pricing, channel, service model, communication, and operations.
   - Identify risks, capabilities needed, and proof points to test first.

## Output

Return:

- **Strategic Arena**: category, target customer/noncustomer, competitors.
- **Factors of Competition**: table with factor definitions and why each matters.
- **As-Is Curves**: table of scores for current offer and competitors.
- **Red-Ocean Diagnosis**: where the market converges and where value is wasted.
- **Blue-Ocean Hypothesis**: the new demand or noncustomer unlock.
- **Eliminate/Reduce/Raise/Create**: table with rationale and evidence.
- **To-Be Curve**: target scores and the strategic pattern.
- **Strategic Projects**: actions, owners if known, dependencies, first proof point.
- **Risks and Tests**: assumptions that must be validated before scaling.

## Quality Bar

- Do not recommend being better at everything.
- Tie every factor to buyer behavior or noncustomer barriers.
- Distinguish facts, assumptions, and inferences.
- Make the to-be curve coherent enough that trade-offs are visible.
