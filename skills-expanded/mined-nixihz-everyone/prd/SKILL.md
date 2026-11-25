---
name: prd
description: Draft, update, review, and maintain product requirement documents (PRD, user stories, scope statements, acceptance criteria) in Markdown. Triggered when the user needs to structure scattered requirements, refresh an existing PRD, review a requirement doc for gaps, or align documentation with Atlassian-style best practices.
---

# PRD

Use this skill to produce concise, living requirement documents that help product, design, and engineering align on problem, scope, and success criteria.
Prefer shared understanding over exhaustive early specification. Keep the main document readable in one pass, and link supporting artifacts instead of dumping everything inline.

## Choose the document mode

Classify the task before writing:
- `PRD` for product goals, background, assumptions, user stories, success metrics, scope, and unresolved questions
- `User Story Pack` for feature-level story decomposition and acceptance criteria
- `Scope` for project boundaries, deliverables, exclusions, constraints, and WBS-style breakdown
- `Doc Refresh` for updating an existing requirement doc while preserving stable sections
- `Requirement Review` for diagnosing gaps, anti-patterns, ambiguity, stale assumptions, and scope creep risk

Prefer `User Story Pack` instead of a bloated PRD when the request is feature-level and solution details are still unsettled.

## Build context

Gather source context before drafting:
- Read the current doc if one already exists
- Extract business goal, target users, problem statement, success metric, scope boundary, constraints, dependencies, and unresolved questions
- Separate confirmed facts from assumptions
- If context is thin, write explicit `Assumptions` and `Pending Decisions` sections instead of inventing certainty
- Preserve original terminology unless it is clearly wrong or inconsistent
- Keep links to interviews, design files, Jira items, or technical deep dives instead of duplicating them
- If the source clearly refers to Confluence/Jira workflow, preserve that operating model instead of flattening everything into plain prose

## Draft the document

Choose the closest template from `assets/templates/` and adapt it instead of starting from scratch.
Draft for alignment, not ceremony:
- Keep the main page readable in one pass
- Prefer a one-page dashboard entry with links out to deeper material
- Use tables only when they improve scanning
- State `In Scope` and `Out of Scope` explicitly whenever delivery boundaries matter
- Turn ambiguous statements into concrete, testable acceptance criteria where possible
- If a metric is missing, write `TBD metric` rather than fabricating one
- If a decision is unresolved, record owner and next checkpoint instead of hiding the uncertainty in prose

## Maintain and update

When refreshing an existing document:
- Keep existing decisions unless the new source contradicts them
- Preserve stable structure if the document is still serviceable
- Add a short `This Update` section when change history matters
- Add an `Open Questions` or `Pending Decisions` section for unresolved items
- Highlight stale assumptions, missing success metrics, and missing owners
- Do not silently remove risks or open issues unless the new source clearly resolves them
- Mark sections that are now outdated, superseded, or pending validation

## Write with Atlassian-style discipline

Apply these rules while writing:
- Write in the user's preferred language; default to Chinese for Chinese-speaking teams unless the user asks for English
- Use precise language and avoid ceremonial filler
- Distinguish facts, assumptions, decisions, risks, and open questions
- Convert vague goals into SMART-style outcomes when enough information exists
- For user stories, use `As a [role], I want [goal] so that [value]`
- For acceptance criteria, make each item clear, testable, and preferably measurable
- Avoid over-specifying implementation details before product, design, and engineering have aligned on problem and value
- Treat the document as a living alignment page, not a one-time approval artifact
- Favor collaboration language and shared context over PM single-author voice
- Encourage design and engineering participation in customer understanding when the source material supports it

## Use the canonical structures

### PRD

When the user asks for a fresh Atlassian-style PRD, start from the Confluence 5-step flow:
1. Cover basic information
2. List goals and success metrics
3. Record assumptions and requirement options
4. Attach supporting material
5. Track open questions and prevent scope creep

Prefer this 8-part structure:
- `Project Details`
- `Team Goals and Business Goals`
- `Background and Strategic Fit`
- `Assumptions`
- `User Stories and Success Metrics`
- `User Interaction and Design`
- `Open Questions / Pending Decisions`
- `Out of Scope`

Expand with these practical sections when useful:
- `Overview`
- `Project Details`
- `Project Background and Strategic Fit`
- `Goals and Success Metrics`
- `Users and Scenarios`
- `Assumptions`
- `Requirements / User Stories`
- `Design and Interaction`
- `Open Questions / Pending Decisions`
- `In Scope`
- `Out of Scope`
- `Risks and Dependencies`
- `Supporting Documents / Attachments`

Ensure the PRD remains a shared alignment page rather than a frozen implementation spec.
Call out anti-patterns when the draft:
- becomes a giant upfront spec before engineering discovery
- relies on heavy sign-off culture instead of iterative alignment
- hides open issues because the doc is treated as final
- was written without design or engineering collaboration
- blurs problem framing and implementation detail

Preserve these Atlassian-style strengths when relevant:
- one page as the single source of entry
- flexibility to adapt structure instead of forcing one rigid format
- linked background instead of pasting every detail inline
- live linkage to delivery artifacts when available
- room for comments and contributions from other teams
- useful visuals or embeds when they clarify the problem
- collaborative drafting rather than solo authorship

Surface these ongoing risks when maintaining the doc:
- the page may become stale after delivery starts
- participation may remain weak if the team lacks a shared documentation culture

### User Story Pack

For each story, include:
- story statement
- business/user value
- acceptance criteria
- optional notes, dependencies, edge cases, non-goals, or related metrics

Apply the 3C principle:
- `Card`: concise story statement
- `Conversation`: discussion notes or unresolved detail
- `Confirmation`: acceptance criteria that define done

Differentiate `Acceptance Criteria` from `DoD`:
- `Acceptance Criteria` answers whether this specific story is complete and correct
- `DoD` answers whether the team-wide delivery quality bar is met

### Scope

Use for boundary control and expectation-setting.
Include:
- SMART project objective
- deliverables
- WBS or equivalent breakdown
- in-scope items
- out-of-scope items
- constraints such as budget, timeline, staffing, or external dependencies
- stakeholders when relevant
- project charter style framing when the team still needs to validate whether the work is worth doing

Use this 5-step scope workflow when drafting from scratch:
1. Define the project objective
2. List deliverables
3. Break work into WBS-style parts
4. State out-of-scope items explicitly
5. Capture constraints

### Doc Refresh

When updating an existing doc:
- preserve stable sections and terminology
- revise outdated metrics, assumptions, dependencies, and scope
- add a short `This Update` section if the change history matters
- do not silently remove open risks unless the new source clearly resolves them

### Requirement Review

When asked to review a requirement document, check for:
- missing goal or success metric
- no explicit `Out of Scope`
- untestable acceptance criteria
- implementation detail crowding out problem framing
- stale assumptions presented as facts
- missing links between requirement, story, and delivery artifacts
- unresolved questions hidden inside prose instead of listed explicitly
- inconsistent terminology across sections
- user stories that describe output but not user value
- scope statements that do not define exclusions or constraints
- documents spread across too many systems without a single entry point

## Resources

Read `references/atlassian-doc-best-practices.md` for the condensed Atlassian principles, anti-patterns, and structural guidance behind this skill.
Start from the Markdown templates in `assets/templates/` when creating a fresh document or performing a heavy rewrite.
