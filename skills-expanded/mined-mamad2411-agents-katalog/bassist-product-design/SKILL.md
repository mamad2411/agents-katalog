---
name: bassist-product-design
description: Product requirement design workflow for turning fuzzy product ideas, feature requests, stakeholder asks, or existing PRDs into clear, aligned, implementable, and testable requirement designs. Use when drafting or reviewing PRDs, feature specs, product plans, requirement documents, user flows, acceptance criteria, or when a product request is ambiguous and needs structured analysis before engineering work.
---

# Bassist Product Design

Use this skill to convert an unclear product request into a requirement design
that product, engineering, design, QA, operations, and stakeholders can align on.

## Operating Principles

- Treat the user's first statement as a starting point, not the final
  requirement.
- Separate the original problem from the proposed solution.
- Prefer explicit goals, constraints, scope boundaries, flows, states, and
  acceptance criteria over generic statements like "optimize experience".
- Do not require a prototyping tool. Describe information architecture, page
  structure, states, and flows in text, tables, or Mermaid when useful.
- Ask concise clarifying questions when missing information would change the
  requirement. If the user wants a first draft, make assumptions and label them.

## Workflow

### 1. Requirement Analysis

Clarify why the requirement exists before designing what to build.

Check:

- What is the original request?
- What user or business problem does it represent?
- Who raised it, and is the source reliable?
- What value should the change create?
- What evidence supports the need?
- What constraints exist: timeline, platform, compliance, technical debt, cost,
  data availability, or dependencies?
- What fallback or lower-cost option exists if the ideal plan is too expensive?

Reject or challenge requests that have no clear goal, no reliable evidence, or a
cost that does not match the expected value.

### 2. Function Breakdown

Turn the goal into a structured feature scope.

Break down:

- User groups and permissions
- Entry points
- Pages or modules
- Core capabilities
- Data objects and fields
- Information hierarchy
- In-scope and out-of-scope behavior
- Reusable or future-facing parts

Use a pyramid structure: user group -> module -> function -> rule/state.

### 3. Flow Design

Design both normal and abnormal paths.

For each important module, cover:

- Happy path
- Empty state
- Loading state
- Error state
- Permission denied or unauthenticated state
- Validation failure
- Network or service failure
- Cancellation, retry, rollback, or recovery path

Prefer one clear flow per module. Use Mermaid only when a flow diagram would be
more readable than prose.

### 4. Detail Completion

Fill the details that make the requirement implementable and testable.

Cover relevant items:

- Business rules
- Interaction rules
- Before/after conditions
- Data creation, update, deletion, retention, and storage rules
- Permission rules, allowlists, denylists, and role behavior
- Notifications, copy, and user-facing messages
- Analytics events and success metrics
- Compatibility, responsive behavior, localization, and accessibility
- Monitoring, alerting, and operational fallback
- Acceptance criteria
- Open questions and assumptions

Keep the detail close to the relevant function or state. Avoid dumping all notes
into a disconnected appendix.

### 5. Alignment Check

Re-read the design from multiple roles before presenting it as ready.

Check as:

- Product: Does the proposal still solve the original problem?
- Engineering: Can the behavior be implemented without guessing?
- QA: Can test cases be written from the document?
- Design: Are information hierarchy and states clear enough to design screens?
- Operations or support: Are failure handling, rollback, and user communication
  covered when needed?
- User: Is the path understandable and does it avoid unnecessary work?

Flag:

- Ambiguous words such as "optimize", "simple", "friendly", "fast", "support",
  or "etc." when they carry unspoken requirements.
- Missing abnormal paths.
- Missing acceptance criteria.
- Unclear scope boundaries.
- Multiple reasonable interpretations.
- High-cost work with weak value evidence.
- Design that drifts away from the original goal.

## Output Modes

Choose the smallest output that satisfies the user request:

- **First draft**: Produce a structured PRD or requirement design with explicit
  assumptions.
- **Review**: Lead with gaps, risks, ambiguities, and missing acceptance
  criteria, then provide a concise improvement plan.
- **Clarification**: Ask the next most important question when the requirement
  cannot be responsibly drafted.
- **Rewrite**: Improve an existing document while preserving its intent and
  calling out any changed assumptions.

When the request is complex, read
`references/five-step-product-design.md` for the expanded checklist and output
template.
