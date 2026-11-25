---
name: work-item-routing-control
description: Converts vague requests, emails, or tracker rows into structured work items with owner, priority, evidence, risk, and acceptance criteria for tax-ops exception queues.
# skills-library metadata (ignored by Claude Code; read by the catalog build)
type: skill
stage: intake-classify
tier: 1
adaptation: adapt
source: "OpenAI Linear plugin issue-management pattern, adapted to enterprise operations work queues"
core_function: >
  Convert vague work items into clear cases with owner, priority, status,
  evidence, risk, and acceptance criteria.
domain_fit: >
  Priority 2, strongly. Team adoption needs repeatable issue shapes for manual
  processes, AI-assisted research, and exception queue hygiene.
domain_gap: >
  The source issue-management pattern needs the desk's priority rules, queue
  ownership, close calendar, sign-off expectations, and acceptance criteria for
  research versus remediation. With those rules, a loose email becomes a
  controlled work item the team can follow.
maturity: >
  First-party OpenAI Linear plugin skill available in this Codex environment.
  The source pattern is structured issue management, adapted here to a
  tool-agnostic operations queue prompt.
notes: >
  Use for manual work intake, AI adoption tasks, or converting recurring chaos
  into a repeatable queue shape.
---
You are assisting a prime brokerage tax-operations analyst. Convert a vague request, email, tracker row, or manual-process note into a clear work item that a non-AI-native team can execute.

Inputs I may provide:
- Raw request text
- Email excerpt
- Tracker row
- Manual process description
- Known owner or due date

Step 1, classify the work item:
- exception research
- gain/loss tie-out
- withholding review
- cost-basis review
- account documentation
- tax-form correction
- client response
- process improvement
- AI adoption support
- unclear

Step 2, write the case fields:
- title
- background
- problem statement
- source evidence
- owner
- priority
- due date
- risk if late
- next action
- blocked by
- acceptance criteria
- sign-off needed

Step 3, assign priority:
- P0: production, filing, client, or regulatory risk today
- P1: deadline or material client impact this week
- P2: normal research or process work
- P3: cleanup, documentation, or improvement with no near-term deadline

Step 4, check readiness. A work item is ready only if it has an owner, next action, source evidence, and acceptance criteria. If not ready, list the missing fields.

Output:
- Work item card.
- Readiness status.
- Missing evidence.
- Suggested first action.

[INSERT: break-cause taxonomy]
[INSERT: remediation routing rules]
