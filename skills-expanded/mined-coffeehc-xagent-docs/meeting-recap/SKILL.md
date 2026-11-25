---
name: meeting-recap
description: Use when producing, rewriting, organizing, or reviewing meeting notes, meeting minutes, post-meeting recaps, standup notes, client-call notes, brainstorm notes, transcript excerpts, agenda artifacts, or mixed raw meeting material. Prefer this Skill when the output must structure notes, segment topics, highlight decisions, capture actions with owners and dates, reconcile planned versus actual agenda, flag missing owners, preserve source uncertainty, or produce a shareable recap artifact.
meta:
  version: 1
  display_name: 会议复盘
  source: product-on-purpose/pm-skills foundation-meeting-recap
  license: Apache-2.0
---

# Meeting Recap

## Purpose

Produce meeting notes or post-meeting recaps for attendees and light distribution. The output may be quick structured notes, an action-only extraction, or a full topic-segmented recap. It explains what happened, what was decided, what actions were created, what remains unresolved, and what needs follow-up.

This XAgent built-in Skill adapts `foundation-meeting-recap` from `product-on-purpose/pm-skills` and absorbs the lightweight `meeting-notes` candidate from `claude-office-skills/skills`. The XAgent version is self-contained and does not assume Zoom, Meet, Otter, Fireflies, Krisp MCP, Slack, Office, or any other external integration exists unless the current session exposes those materials or tools.

## Use When

Use after a meeting when:

- Rough notes need to be cleaned into a clear meeting record.
- Raw notes, transcript, audio summary, chat log, agenda, or rough bullets need to become a structured recap.
- Attendees need a reliable reference of topics, decisions, actions, and open questions.
- A prior agenda should be reconciled with what actually happened.
- The user needs an action list grouped by owner.
- A rough recap needs review for missing owners, fabricated decisions, or unclear next steps.
- The user asks for meeting minutes, standup notes, client-call notes, brainstorm notes, or action-only extraction.

## Do Not Use When

Do not use for:

- Pre-meeting preparation; use `meeting-brief`.
- Drafting a separate internal announcement from meeting outcomes; use `internal-comms`.
- Live transcription or recording.
- Cross-meeting research synthesis across many meetings unless the user explicitly asks for recap consolidation.
- Formal institutional meeting minutes where official-document conventions dominate; consider `official-document-drafting`.

## Material Gate

Before writing, identify:

- Meeting title, date, audience, attendees, absent decision-makers, and meeting purpose.
- Source quality: transcript, structured notes, rough bullets, prior agenda, chat notes, or user summary.
- Output mode: quick notes, full recap, action-only extraction, standup notes, client-call notes, project-review notes, brainstorm notes, or formal minutes draft.
- Whether a related agenda, prior brief, prior recap, or stakeholder update is provided or visible through current XAgent tools.
- Whether output should be shareable, internal only, or saved as an artifact.
- Any confidentiality constraints.

If owners, dates, decisions, attendees, or sources are missing, mark them as `unassigned`, `not specified`, `inferred`, or `待确认`. Never invent them.

## Workflow

1. Read all provided meeting material and classify input quality: high, medium, or low.
2. Select the output mode:
   - quick notes: lightweight cleanup with summary, key points, decisions, actions, next steps, and parking lot.
   - full recap: topic-segmented recap with shareable/internal boundary and optional agenda reconciliation.
   - action-only: extract decisions, actions, owners, due dates, and follow-up questions.
   - specialized notes: standup, client call, project review, or brainstorm; use `references/note-modes.md`.
3. If an agenda or meeting plan is provided, use it as the initial topic skeleton for full recap. If no agenda exists, infer topic segments from discourse markers and repeated themes.
4. Produce a short inference summary only when material is ambiguous enough that proceeding could misrepresent decisions, owners, or action scope.
5. Segment full recap by topic rather than chronology. For quick notes, keep the structure compact.
6. For each topic or note section, capture:
   - discussion summary
   - decisions made
   - actions with owner, due date, and dependency
   - open questions
7. Apply the fabrication rules in `references/recap-rules.md`.
8. If many actions lack owners or any high-priority action lacks an owner, add an ownership reconciliation section.
9. Group all actions by owner after the topic sections when the output is full recap or action-heavy.
10. Use `templates/meeting-recap.md` for full recap artifacts and `templates/quick-meeting-notes.md` for lightweight notes.
11. Validate the output against the checks below.

## Checks

- Input quality and source basis are visible.
- Decisions are not invented. Inferred decisions include confidence markers.
- Every action has owner or explicit `unassigned`, due date or `not specified`, and enough context to act.
- Full recap topic sections include discussion, decisions, actions, and open questions, even when some are empty.
- Quick notes remain easy to scan and do not become a long report unless requested.
- Agenda reconciliation is present when an agenda exists and the selected mode needs it.
- Ownership problems are surfaced near the top, not hidden in the action table.
- Shareable summary is short and safe to paste when a shareable output is requested.
- Internal evidence notes are separated from shareable content.

## Outputs

Produce one or more of:

- meeting recap
- quick meeting notes
- informal meeting minutes
- standup notes
- client-call notes
- brainstorm notes
- shareable summary
- topic-by-topic recap
- action table by owner
- decisions log
- open questions list
- ownership reconciliation note
- review notes for an existing recap

## Recovery

If the transcript is too messy, produce a partial recap with confidence markers and a missing-information section. If sources conflict on a decision or owner, preserve the conflict and do not pick a fact without evidence.

## Boundary

Skill owns recap workflow, topic segmentation, decision/action extraction, source uncertainty handling, ownership reconciliation, and Markdown structure.

It does not own XAgent tool schemas, ToolResult fields, transcript capture, recording access, chat export, calendar access, external meeting platforms, file path selection, artifact persistence, email sending, Office/DOCX export, or formal approval. It must not run shell, Python, Node, MCP, calendar, Slack, Teams, Notion, Office, transcription, or document-export commands by itself; those actions belong to XAgent tools visible in the current session.

## Resources

- `references/recap-rules.md`: fabrication rules, ownership reconciliation, input quality, and agenda reconciliation.
- `references/note-modes.md`: quick notes, standup notes, client-call notes, project-review notes, brainstorm notes, and action-only extraction.
- `templates/meeting-recap.md`: production recap template.
- `templates/quick-meeting-notes.md`: production lightweight meeting notes template.
- `examples/meeting-recap-example.md`: example shape for a source-backed recap.
- `LICENSE`: source and license notice.
