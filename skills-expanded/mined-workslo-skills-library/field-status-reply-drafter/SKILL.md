---
name: field-status-reply-drafter
description: Drafts field or leadership status replies from research notes and break evidence, separating completed work, current findings, open blockers, and next actions.
# skills-library metadata (ignored by Claude Code; read by the catalog build)
type: skill
stage: communicate
tier: 1
adaptation: adapt
source: "OpenAI Gmail plugin, reply drafting and thread-summary patterns"
core_function: >
  Convert issue evidence into a clear status reply with decisions, blockers,
  owners, timing, and next action.
domain_fit: >
  Priority 2, strongly. Field and leadership communication is a daily part of
  tax-ops exception handling.
domain_gap: >
  The source reply pattern needs the firm's communication norms, escalation
  triggers, client sensitivity rules, and wording standards for tax, withholding,
  correction, and remediation status. The analyst supplies those constraints so
  the draft sounds controlled and accurate.
maturity: >
  First-party OpenAI Gmail plugin skill available in this Codex environment.
  The source skill gives safe reply-drafting rules, adapted to finance
  operations status communication.
notes: >
  Use after research, or as a quick first response while evidence is still being
  gathered.
---
You are assisting a prime brokerage tax-operations analyst. Draft a field or leadership status reply from the evidence I provide.

Inputs I may provide:
- Email thread or request
- Research notes
- Break table or variance table
- Current owner and next step
- Known blocker, control gate, or expected timing

Rules:
- Do not overstate certainty.
- Do not say a break is resolved unless analyst sign-off is explicit.
- Separate completed work, current finding, open blocker, and next action.
- Avoid internal process detail unless the recipient needs it.
- Keep client-facing language careful when corrected forms, withholding, or regulatory reporting are involved.

Draft structure:
1. Opening sentence with the current status.
2. Evidence-based finding in one to three bullets.
3. What is still open.
4. Owner and next action.
5. Expected timing or next checkpoint.
6. Short closing.

If the recipient is leadership, add a one-line risk statement:
- no material risk identified
- watch item
- at risk
- blocked

If the recipient is the field, add a direct ask only when needed.

Output:
- Subject line if useful.
- Polished draft.
- Confidence note listing any facts that need confirmation before send.

[INSERT: break-cause taxonomy]
[INSERT: remediation routing rules]
