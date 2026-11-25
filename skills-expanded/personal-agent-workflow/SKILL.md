---
name: personal-agent-workflow
description: Coordinate a private daily personal agent workflow across calendar, email, chat, Notion, Obsidian, memory, finance watchlists, issue trackers, and user-run handoffs. Use when the user asks for daily planning, personal briefings, inbox triage, meeting prep, cross-workspace action lists, or a combined personal operating-system summary.
---

# Personal Agent Workflow

Use this skill to make personal context useful without overreaching into private systems.

## Operating Rules

- Treat Obsidian/local Markdown and explicit user-provided files as the safest source.
- Use Notion, email, calendar, Slack, Discord, and issue trackers only when configured or supplied by the user.
- Label sources clearly: calendar, email, chat, Notion, Obsidian, memory, finance, web, issue tracker.
- Draft replies, issue updates, Notion payloads, and scripts; do not send or mutate unless the user explicitly asks and the tool supports it safely.
- Save durable preferences, decisions, or lessons to memory when they will help future sessions.

## Workflow

1. Scope
   - Confirm date/timezone only when ambiguous.
   - Identify the user's top goal: plan day, triage inbox, prep meeting, organize notes, or ship tasks.

2. Gather
   - Calendar: summarize events and draft meeting prep.
   - Email/chat: summarize messages and extract action items.
   - Notion/Obsidian: read only relevant notes or pages.
   - Memory/RAG: search prior decisions before creating new assumptions.
   - Finance: include only when the user asks for markets/watchlists.

3. Decide
   - Split work into now, today, later, waiting, and delegated.
   - Convert unclear requests into issue drafts or Obsidian tasks.
   - Keep personal and public/shareable content separate.

4. Produce
   - Provide a concise daily plan or briefing.
   - Include draft replies or issue updates in clearly marked sections.
   - Offer Notion/Obsidian payloads as plans unless asked to apply them.

## Output Shape

For daily planning, end with:

- Today
- Meetings
- Inbox/chat actions
- Notes to save
- Drafts
- Waiting on

