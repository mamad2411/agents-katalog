---
name: slack
description: Capture, triage, search, summarize, and follow up on Slack messages for this GTD workspace. Use when the user asks to process Slack notifications, turn Slack messages or threads into tasks, find decisions or commitments in Slack, draft Slack replies, summarize channels/threads, or sync Slack follow-ups into GTD files and Todoist via MCP.
---

# /slack

Use Slack as an input stream for GTD capture, follow-ups, and reference material. Keep the workflow biased toward clear next actions, waiting-for items, calendar commitments, and concise Slack replies.

## Workflow

1. Clarify the Slack source: channel, DM, thread URL, date range, search query, copied transcript, export file, or open browser context.
2. Gather only the relevant messages. Preserve message URLs, authors, channel names, and timestamps when available.
3. Classify each item:
   - `next action`: concrete user-owned action with a physical next step.
   - `waiting for`: someone else owns the next move.
   - `calendar`: time-specific commitment or deadline.
   - `reference`: decision, context, or useful non-actionable information.
   - `reply`: message that needs a Slack response but not a separate task.
4. Write tasks in GTD language: start with a verb, include enough context to act later, and attach the Slack permalink when available.
5. Avoid duplicating existing Todoist/GTD tasks. Search local GTD files and Todoist via MCP if the task may already exist.
6. When drafting replies, keep them short, specific, and action-oriented. Ask for missing owners, dates, or acceptance criteria when needed.

## Outputs

For triage, return a compact summary:

```text
Next actions
- [context] Verb-based task (source: Slack link or channel/date)

Waiting for
- Person: expected outcome by date, if known (source: ...)

Calendar
- Date/time: commitment or deadline (source: ...)

Reference
- Decision/context worth preserving (source: ...)

Suggested replies
- Channel/person: concise reply text
```

When applying changes to this repo, place durable reference notes in `reference/`, daily planning notes in `daily/YYYY-MM-DD.md`, delegated items in `waiting-for.md`, and project tasks in the relevant `projects/active/<project>/tasks.md` file.

## Tooling

Prefer the most direct available source:

- Use a connected Slack MCP/app tool if one is available in the session.
- Use the browser or Chrome plugin when Slack is already open or login is required.
- Use a Slack export file, copied thread transcript, or user-provided message text when available.
- Use the Slack Web API only when credentials are already configured in the environment. Never ask the user to paste secrets into chat.

Before using command-line or API access, read [references/slack-usage-notes.md](references/slack-usage-notes.md).
