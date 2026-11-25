---
name: meeting-brief
description: Use when preparing a private strategic brief before an important meeting, stakeholder review, negotiation-adjacent conversation, approval meeting, executive briefing, client discussion, or decision session. Prefer this Skill when the user needs stakes, stakeholder reads, desired outcomes, key messages, anticipated questions, risks, asks, success signals, low-confidence inference flags, or a private prep artifact distinct from an attendee-facing agenda.
meta:
  version: 1
  display_name: 会前简报
  source: product-on-purpose/pm-skills foundation-meeting-brief
  license: Apache-2.0
---

# Meeting Brief

## Purpose

Create a private preparation document for meetings where context, stakes, positioning, decisions, or stakeholder dynamics matter. The brief helps the user know what they want, how to say it, what risks to watch, and what to ask for.

This Skill is distinct from an agenda: an agenda is shared with attendees; a meeting brief is tactical prep for the user or a trusted co-presenter.

## Use When

Use before:

- Stakeholder reviews.
- Executive briefings.
- Approval or decision meetings.
- Client or partner conversations with risk or positioning.
- Negotiation-adjacent discussions.
- First meetings where relationship calibration matters.
- Any meeting where the user needs a specific commitment, decision, or support.

## Do Not Use When

Do not use for:

- Routine standups, simple team syncs, or low-stakes recurring meetings.
- Post-meeting summaries; use `meeting-recap`.
- Post-meeting summaries or async internal updates; use `meeting-recap` or `internal-comms` depending on the requested format.
- Attendee-facing agenda drafting unless the user explicitly wants both.
- Inventing stakeholder positions or politics from no evidence.

## Material Gate

Before preparing the brief, identify:

- Meeting topic, date, format, attendees, roles, decision-maker, and user's desired outcome.
- Prior recaps, stakeholder summaries, project docs, decision notes, risks, or open disputes.
- User's primary ask and fallback position.
- Known stakeholder positions, likely objections, relationship state, and confidence level.
- Whether the brief is private, shared with a co-presenter, or excerpted for a manager.

If stakeholder positions, primary ask, or decision-maker identity are inferred below high confidence, flag them before relying on tactical guidance.

## Workflow

1. Run the anti-meeting check in `references/brief-rules.md`. If the meeting has no synchronous value, suggest an async alternative but continue if the user still wants a brief.
2. Read provided context and visible XAgent artifacts. Do not assume access to calendars, CRM, notes, or documents that are not provided.
3. Infer missing facts only when helpful, and mark confidence.
4. State the user's primary ask. If no ask exists, use a placeholder and recommend clarifying it.
5. Analyze stakeholders: position, stakes, likely concerns, relationship state, influence, and confidence.
6. Rank desired outcomes: must, should, nice.
7. Draft key messages as speakable lines, not only document bullets.
8. Prepare likely questions and responses.
9. Identify risks, tensions, derailers, and mitigation moves.
10. Define concrete asks and success signals.
11. Use `templates/meeting-brief.md` for durable prep artifacts.
12. Validate with the checks below.

## Checks

- The brief states why the meeting should happen synchronously or labels that assumption.
- Primary ask is explicit or marked missing.
- Stakeholder reads include confidence markers when inferred.
- Desired outcomes are ranked, not flat.
- Key messages are phrased for delivery.
- Questions and responses address likely objections.
- Risks include mitigation, not just warning labels.
- Asks name a person or group when known.
- Success signals are observable in the meeting.
- Private content is not mixed into attendee-facing material.

## Outputs

Produce one or more of:

- private meeting brief
- stakeholder readout
- desired-outcomes ranking
- key message bank
- anticipated Q&A
- risks and mitigations
- asks and success signals
- review notes for an existing meeting prep

## Recovery

If context is weak, produce a low-confidence brief with explicit assumptions and a `confirm before use` section. If the user's ask is missing, ask for the ask only when proceeding would produce generic or risky advice.

## Boundary

Skill owns private meeting preparation workflow, stakeholder read structure, inference flags, message preparation, asks, risks, and success signals.

It does not own XAgent tool schemas, ToolResult fields, calendar access, attendee identity truth, CRM access, email sending, meeting scheduling, authority approval, legal/compliance conclusions, or final negotiation strategy. It must not run shell, Python, Node, MCP, calendar, email, CRM, Slack, Teams, Notion, or document-export commands by itself; those actions belong to XAgent tools visible in the current session.

## Resources

- `references/brief-rules.md`: anti-meeting check, low-confidence inference gates, and stakeholder-read rules.
- `templates/meeting-brief.md`: production meeting brief template.
- `examples/meeting-brief-example.md`: example output shape.
- `LICENSE`: source and license notice.
