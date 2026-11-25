---
name: docs-product-requirements
description: Create and maintain evidence-based Product Requirements Documents (PRDs). Use when writing, reviewing, or revising product requirements, initiative scope, success measures, or product decisions before technical design and delivery planning.
---

# Docs Product Requirements

Create concise, living PRDs that explain why a product change matters, who it serves, what outcomes and behavior are required, and how success will be evaluated. Keep implementation design and delivery planning in their own documents.

## Resource Map

- Use `assets/doc-starters/product-requirements-doc.md` when creating or substantially rewriting a PRD.
- Read `references/product-requirements-example.md` when you need a worked example of the expected evidence and product-level depth.

## When to Use

- A new product, initiative, or substantial feature needs product requirements
- An existing PRD needs review, revision, or evidence updates
- Stakeholders need alignment on users, outcomes, scope, requirements, or validation
- A product idea must be shaped before feature design, technical design, or task decomposition

## Do Not Use

- Accepted user-visible behavior that belongs in `docs-feature-design`
- APIs, schema, runtime behavior, deployment, or implementation detail that belongs in `docs-components-design`
- System topology or cross-component architecture that belongs in `docs-architecture`
- Strategic sequencing across initiatives that belongs in `docs-product-roadmap`
- Engineering issue creation that belongs in `linear-task-planning`

## Workflow

1. Identify the artifact and its authority.
- Classify the work as a greenfield product, initiative PRD, feature PRD, revision, or review
- Find existing product strategy, research, analytics, roadmap, feature docs, designs, decisions, and contributor guidance before asking for information already recorded
- Reuse the repository's product-doc location and naming convention; otherwise default to `docs/product/PRD.md`
- Clarify the audience and decision the PRD must support

2. Build an evidence ledger.
- Separate facts, inferences, assumptions, decisions, and unknowns
- Attribute evidence to a source and date; preserve links to interviews, analytics, support signals, market research, and prior decisions
- Treat competitor claims as market context, not proof of customer demand
- Flag stale, conflicting, weak, or segment-mismatched evidence
- Never invent users, quotes, metrics, baselines, deadlines, research, or constraints

3. Resolve decision-critical gaps.
- Summarize the current understanding before questioning
- Ask short, prioritized rounds about the problem, target users, desired outcome, evidence, scope, constraints, and risks
- Ask only questions whose answers could change the product decision or document
- Accept `unknown` and turn it into an owned research or validation action
- Do not require a fixed number of questions when the supplied context is already sufficient

4. Check readiness before polishing.
- Confirm the problem or opportunity, target user, desired outcome, and at least one meaningful scope boundary
- Confirm whether the initiative is exploratory, proposed, approved, or committed
- If evidence is insufficient, offer an evidence-gap or research plan instead of presenting an unsupported PRD as validated
- A draft may retain explicit assumptions and open questions when stakeholders need a decision artifact before every uncertainty is resolved

5. Draft at product level.
- Start with the problem, evidence, users, outcomes, and strategic fit
- Define scope through capabilities, use cases, behavior, and testable requirements without prescribing internal implementation
- Give requirements stable identifiers only when traceability adds value
- Define success with a metric, baseline when known, target, population, measurement window, data source, and guardrail
- Make non-goals, dependencies, constraints, risks, and unresolved decisions visible
- Right-size the document; omit optional sections that do not improve the decision

6. Handle technology carefully.
- State required capabilities, constraints, and non-functional outcomes before naming technologies
- In an existing product, treat confirmed stack and architecture decisions as constraints rather than reopening them without cause
- When a technology choice is genuinely open, compare two or three viable options by fit, delivery speed, cost, security and privacy, operability, scale, team capability, integration, lock-in, and reversibility
- Cite current authoritative documentation for claims that depend on present product or vendor behavior
- Label the result as a recommendation, confirmed decision, or open engineering question
- Propose a technical spike or engineering review when feasibility evidence is weak
- Link technical design instead of embedding architecture, API, schema, or file-level plans in the PRD

7. Review before writing.
- Present the complete proposed PRD or a precise change preview
- Call out assumptions, unsupported claims, conflicts, and open decisions
- Ask for explicit approval before creating or editing the document
- After approval, make the smallest coherent write and preserve unrelated existing content

8. Verify the result.
- Trace important requirements to an outcome or documented constraint
- Check that acceptance criteria describe observable product behavior
- Check that metrics are measurable and do not define success as merely shipping
- Check that optional technical guidance is conditional and does not masquerade as a product requirement
- Check links, status, owner, review date, open questions, and decision history
- Re-read linked roadmap and feature docs for contradictions

## Writing Rules

- Make reasoning visible: record why the problem, outcome, and scope were chosen
- Prefer evidence-backed diagnosis over stakeholder request restatement
- Use concrete, testable language and avoid unsupported words such as "fast", "intuitive", or "scalable"
- Do not force every requirement into a user-story format; use the form that communicates the behavior most clearly
- Do not convert the PRD into an implementation plan, backlog, architecture document, or release calendar
- Keep examples and placeholders visibly illustrative so they cannot be mistaken for evidence
- Treat the PRD as a versioned decision artifact that changes when evidence or decisions change

## Quality Checklist

- The problem, target users, and strategic rationale are clear
- Evidence is attributed and uncertainty is explicit
- Outcomes include measurable success and guardrails where relevant
- Scope, non-goals, requirements, and acceptance criteria agree
- Assumptions, dependencies, constraints, risks, and open questions are actionable
- Technology guidance is optional, current, and separated from confirmed requirements
- Feature, technical design, architecture, roadmap, and delivery details are linked rather than duplicated
- The document was reviewed before writeback and has a clear status
