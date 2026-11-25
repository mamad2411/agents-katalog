---
name: internal-comms
description: Use when drafting, rewriting, structuring, or reviewing internal communications such as team updates, company newsletters, FAQs, status announcements, policy explanations, launch notes, incident summaries, leadership updates, or internal change messages. Prefer this Skill when the message needs audience fit, clear ask, tone control, fact discipline, reusable communication format, or separation of shareable copy from internal notes.
meta:
  version: 1
  display_name: 内部沟通
  source: claude-office-skills/skills official-skills/internal-comms
  license: Apache-2.0
---

# Internal Comms

## Purpose

Draft clear internal communications that help employees, teams, managers, or leaders understand what changed, why it matters, what action is needed, and where to find more information.

This Skill adapts the open-source Internal Communications candidate into an XAgent production workflow. It is not tied to any mail, chat, newsletter, or publishing system.

## Use When

Use for:

- Team updates.
- Company or department newsletters.
- Internal FAQs.
- Policy explanation.
- Launch or release announcements.
- Incident or post-incident summaries.
- Leadership updates.
- Change-management messages.
- Rewriting rough internal notes into clear shareable copy.

## Do Not Use When

Do not use for:

- Weekly status reports with progress/blocker/plan structure; use `weekly-report`.
- Detailed meeting records for attendees; use `meeting-recap`.
- Public crisis statements, investor letters, or external communications unless approved source facts are provided.
- Formal institutional documents; use `official-document-drafting`.
- External customer announcements unless the user explicitly asks for internal-to-external adaptation and provides approved facts.

## Material Gate

Before writing, identify:

- Audience: whole company, department, team, managers, new hires, leadership, or affected group.
- Message type: update, newsletter, FAQ, announcement, incident summary, policy note, or change message.
- Core message, timing, facts, source material, decision status, action required, owner, and deadline.
- Tone: neutral, urgent, reassuring, celebratory, corrective, or formal.
- Sensitivity: confidential, internal-only, leadership-only, or public-safe.

If facts are missing or approval status is unclear, mark `待确认` and avoid final-sounding language.

## Workflow

1. Classify the communication type and audience.
2. Extract the core message in one sentence.
3. Separate must-say facts from optional background.
4. Choose a structure from `references/comms-patterns.md`.
5. Put action needed, deadline, or FYI-only status near the top.
6. Keep tone appropriate to the audience and situation.
7. For FAQ, turn likely employee questions into direct answers and mark unknown answers.
8. For incident or sensitive communication, be transparent about known facts and avoid blame, legal conclusions, or unsupported cause claims.
9. Use `templates/internal-comms.md` when the user wants a durable artifact.
10. Validate with the checks below.

## Checks

- The first paragraph states the main message.
- Audience and action needed are clear.
- Dates, numbers, owners, policy claims, incident causes, and commitments are source-backed.
- Tone matches the situation.
- Unknowns are not hidden.
- Internal-only or confidential details are not exposed beyond the intended audience.
- The message does not overpromise, blame, or imply approval that has not been given.
- FAQ answers are concise and complete enough to use.

## Outputs

Produce one or more of:

- internal announcement
- team update
- newsletter draft
- FAQ
- status announcement
- incident summary
- policy explanation
- leadership update
- review notes for existing communication

## Recovery

If approval or facts are missing, produce a draft labeled as unapproved and include a confirmation checklist. If the audience is unclear, default to internal team audience and label the assumption.

## Boundary

Skill owns internal communication structure, audience adaptation, tone, fact discipline, and reusable message patterns.

It does not own XAgent tool schemas, ToolResult fields, message sending, publishing approval, HR/legal/compliance approval, final executive approval, email/chat access, or external announcements. It must not run shell, Python, Node, MCP, email, Slack, Teams, CMS, newsletter, or document-export commands by itself; those actions belong to XAgent tools visible in the current session.

## Resources

- `references/comms-patterns.md`: patterns for updates, newsletters, FAQs, announcements, and incident summaries.
- `templates/internal-comms.md`: production internal communication template.
- `LICENSE`: source and license notice.
