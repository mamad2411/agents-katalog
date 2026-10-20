---
name: event-followup-ops
description: Prepare repeatable event operations packets for community, youth sports, athlete, sponsor, host, and business-development events. Use when the user asks to plan or follow up on an event from Calendar, such as "run event follow-up", "prepare my event packet", "make stakeholder emails", "draft thank-yous", "create social posts", "invoice reminder", "reflection after the event", or similar pre-event/post-event workflows involving stakeholders, hosts, athletes, partners, LinkedIn, Instagram, invoices, and personal optimization.
---

# Event Follow-up Ops

## Core Rule

Prepare source-backed drafts and checklists. Do not send messages, publish posts, create invoices, change calendars, or contact stakeholders unless the user explicitly asks for that action after reviewing the packet.

Keep public and private material separate:

- Attendee-facing, host-facing, stakeholder-facing, and social copy must not include private logistics, budget notes, internal criticism, invoice strategy, personal self-assessment, or confidential partner context.
- Private reflections, positioning notes, time-optimization notes, and invoice/admin steps belong only in the private operating packet.

## Workflow

1. Identify the event.
   - If the user names a calendar event, inspect Calendar details when tools are available.
   - If tools are unavailable or the event is ambiguous, ask for the event title/date instead of guessing.
   - Capture event name, date, location, host, user role, stakeholders, participating athletes, expected outcomes, and deadlines.

2. Gather source context.
   - Use Google Workspace sources through `gws` first when relevant and available.
   - Use Slack, Drive, Calendar, or Sheets connectors only when available and appropriate.
   - Prefer approved docs, event pages, calendar descriptions, prior recap notes, invoices, and direct user-provided context.
   - Mark unsupported claims, missing names, missing emails, unclear approvals, and unclear payment terms as open questions.

3. Build the packet.
   - Read `references/event-packet.md` for the required output structure.
   - Read `references/message-templates.md` when drafting emails, texts, DMs, or follow-up questions.
   - Read `references/social-admin-reflection.md` when preparing social posts, invoice/admin items, or the user's reflection.

4. Optimize for the user's goals.
   - Treat community work, youth sports development, service promotion, time protection, and polished in-person presence as first-class outcomes.
   - Create practical preparation steps for wardrobe/appearance, arrival timing, talking points, content capture, relationship follow-up, and business development.
   - Keep recommendations specific to the event and grounded in sources or user-provided preferences.

5. Produce review-ready output.
   - Put drafts in clearly labeled sections by recipient group.
   - Include a private checklist with owners, due dates, approval status, and open questions.
   - Include a source appendix listing where each concrete detail came from.
   - Use placeholders like `[email needed]`, `[amount needed]`, and `[approval owner needed]` rather than inventing details.

## Default Packet Sections

Use these sections unless the user asks for a different format:

1. Event snapshot
2. Stakeholder map
3. Pre-event actions and emails
4. Day-of checklist
5. Post-event thank-you emails
6. Internal reflection and improvement notes
7. Business/service follow-up opportunities
8. Invoice and admin checklist
9. Social media drafts
10. Open questions
11. Source appendix

## Automation Guidance

When the user asks to automate this workflow, recommend a two-part setup:

1. Run this skill manually on one or two real events until the packet format is trusted.
2. Then create a scheduled task that checks upcoming calendar events and prepares a draft packet for review.

Scheduled runs should produce drafts and reminders only. They should not send, post, invoice, or modify live systems without explicit approval.

## Provenance

- `created_by: Codex`
- `date_created: 2026-08-05`
- Own-authored Baza skill based on Kamilla's event follow-up workflow needs. No upstream text or code was copied.
