---
name: docs-product-roadmap
description: Create and maintain outcome-driven product roadmaps. Use when defining, reviewing, or revising product priorities, strategic themes, Now/Next/Later horizons, roadmap phases, dependencies, or criteria for changing direction.
---

# Docs Product Roadmap

Create living product roadmaps that connect strategy to measurable customer and business outcomes. Communicate priorities and uncertainty without turning the roadmap into a feature inventory, delivery backlog, or set of unsupported date commitments.

## Resource Map

- Use `assets/doc-starters/product-roadmap-doc.md` when creating or substantially rewriting a product roadmap.
- Read `references/product-roadmap-example.md` when you need a worked example of outcome-led confidence horizons.

## When to Use

- Product strategy must be translated into prioritized outcomes or themes
- A new roadmap needs Now/Next/Later horizons, phases, or genuine time windows
- An existing roadmap needs review after new evidence, strategy, capacity, or dependencies emerge
- Stakeholders need a clear explanation of what is prioritized, why, and with what confidence

## Do Not Use

- Requirements for one initiative that belong in `docs-product-requirements`
- Accepted behavior for one user-visible capability that belongs in `docs-feature-design`
- APIs, schema, runtime behavior, or implementation design that belongs in `docs-components-design`
- System topology that belongs in `docs-architecture`
- Sprint plans, granular task lists, or issue creation that belongs in delivery planning or `linear-task-planning`

## Workflow

1. Identify the roadmap decision and audience.
- Clarify the product or portfolio, planning horizon, intended audience, and decision the roadmap must support
- Find existing vision, strategy, objectives, PRDs, research, analytics, technical constraints, commitments, and roadmap conventions
- Reuse the repository's roadmap location and format; otherwise default to `docs/product/ROADMAP.md`
- Create audience-specific views only when one view cannot communicate the right level of certainty and detail

2. Establish strategy and source inputs.
- State the product direction, target users, strategic objectives, and measurable outcomes before considering initiatives
- Separate evidence, assumptions, decisions, commitments, and unknowns
- Attribute material evidence and note its date, segment, and limitations
- Never invent strategy, capacity, owners, estimates, deadlines, research, or dependencies
- If strategy or outcomes are missing, stop and resolve them or produce a gap plan rather than arranging an ungrounded feature list

3. Ask decision-relevant questions.
- Summarize current understanding, conflicts, and gaps first
- Ask short rounds about desired outcomes, evidence, candidate opportunities, constraints, dependencies, capacity, commitments, and audience needs
- Accept `unknown` and convert it into discovery, estimation, or decision work
- Do not ask for dates unless coordination or a real commitment requires them

4. Choose the roadmap form.
- Default to an outcome-led Now/Next/Later roadmap when uncertainty is meaningful
- Treat Now, Next, and Later as confidence horizons, not renamed calendar quarters
- Use goal or theme views when communicating strategy across several teams or products
- Use broad time windows only when stakeholders need coordination and the evidence supports them
- Use exact dates only for genuine regulatory, contractual, market-event, funding, migration, or launch commitments; record the driver and consequence
- Keep detailed release, sprint, and task scheduling in a separate delivery plan

5. Define roadmap entries.
- Lead with the outcome or problem, not a predetermined feature
- Connect each entry to a strategic objective and measurable success signal
- Record rationale, evidence, confidence, dependencies, risks, and an owner when one is known
- List solutions as candidate bets or experiments unless they are already approved commitments
- Define what evidence or decision allows an item to enter, advance, pause, or leave a horizon
- Keep Later intentionally coarse; detail should increase as evidence and confidence increase

6. Prioritize transparently.
- Start with strategic fit, outcome contribution, evidence quality, urgency, dependencies, and opportunity cost
- Use value-versus-effort for a lightweight comparison
- Use RICE only when reach, impact, confidence, and effort can be estimated consistently across comparable items
- Use Kano or opportunity scoring only when the required customer research exists
- Use MoSCoW to negotiate scope within an already selected initiative, not to choose product strategy
- Show inputs, uncertainty, and deliberate overrides; never let a score make the decision automatically

7. Review before writing.
- Present the complete proposed roadmap or a precise change preview
- Explain major additions, removals, ordering changes, confidence changes, and real commitments
- Call out assumptions, unsupported dates, conflicts, and open decisions
- Ask for explicit approval before creating or editing the roadmap
- After approval, make the smallest coherent write and preserve unrelated existing content

8. Verify and maintain.
- Confirm every active entry connects to strategy and an outcome
- Confirm dates have explicit drivers and confidence matches the available evidence
- Confirm dependencies and risks can change ordering when necessary
- Confirm the roadmap and linked PRDs do not contradict each other
- Record owner, last review, next review or trigger, and material changes
- Revisit the roadmap when strategy, evidence, constraints, commitments, or achieved outcomes change

## Writing Rules

- Use outcomes, problems, or strategic themes as the primary roadmap units
- Keep candidate initiatives visibly subordinate to outcomes
- Make uncertainty honest and visible instead of manufacturing precision
- Explain why work is prioritized and what is deliberately not prioritized
- Keep the roadmap simple enough for its audience to scan and discuss
- Do not duplicate detailed requirements, architecture, or delivery tasks
- Do not imply that Later items are promises
- Treat the roadmap as a living strategic decision artifact, not a static release contract

## Quality Checklist

- Product direction, audience, horizon, and strategic objectives are clear
- Roadmap entries lead with outcomes or problems and include measurable success signals
- Evidence, confidence, assumptions, dependencies, risks, and commitments are explicit
- Prioritization reasoning is visible and no framework is treated as automatic authority
- Now/Next/Later represents confidence, or an alternative format has a documented reason
- Dates appear only where a real driver justifies them
- PRDs, feature docs, technical designs, and delivery tasks are linked rather than duplicated
- The roadmap was reviewed before writeback and includes a maintenance trigger
