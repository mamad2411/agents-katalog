# Daily Brief Skill

**IMPORTANT:** This skill runs autonomously. Do NOT ask for confirmation or show intermediate results. Just gather data and send the email.

## Prerequisites

### Required: Google Workspace MCP Server

This skill requires the Google Workspace MCP server for Gmail and Calendar access:

```bash
claud mcp add taylorwilsdon/google_workspace_mcp
```

**Repository:** https://github.com/taylorwilsdon/google_workspace_mcp

Make sure to configure your Google OAuth credentials as described in the MCP server documentation.

## Execution Flow

1. Query iMessage → Query WhatsApp → Fetch Gmail/Calendar via Google Workspace MCP → Generate HTML → Send email
2. Only output: "Daily brief sent to [USER_EMAIL]"

## Data Collection

### iMessage
```bash
sqlite3 ~/Library/Messages/chat.db "SELECT datetime(m.date/1000000000 + 978307200, 'unixepoch', 'localtime'), COALESCE(h.id, 'Unknown'), substr(m.text, 1, 150), m.is_from_me FROM message m LEFT JOIN handle h ON m.handle_id = h.ROWID WHERE m.text IS NOT NULL AND m.text <> '' ORDER BY m.date DESC LIMIT 30;"
```

### WhatsApp
```bash
sqlite3 "~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite" "SELECT datetime(ZMESSAGEDATE + 978307200, 'unixepoch', 'localtime'), ZFROMJID, ZTOJID, ZISFROMME, substr(ZTEXT, 1, 150) FROM ZWAMESSAGE WHERE ZTEXT IS NOT NULL AND ZTEXT <> '' ORDER BY ZMESSAGEDATE DESC LIMIT 30;"
```

### Gmail & Calendar

Use the Google Workspace MCP server tools:
- Gmail: Use MCP tools to fetch unread emails and sent messages
- Calendar: Use MCP tools to fetch upcoming events (next 5 days)

## HTML Email Sections

| Section | Content |
|---------|--------|
| RESPOND TO | Unanswered messages needing YOUR reply |
| CALENDAR | Today → next 5 days, mark external meetings |
| MEETING PREP | Web search background on external attendees |
| ACTIVITY | Your sent messages (last 24h) |
| HANDLED | Already completed items |
| FILTERED | Newsletters, promos, ignorable |
| MESSAGES (FYI) | Personal/family, no action needed |

## Rules

1. **NO questions** - run fully autonomous
2. **NO confirmations** - just do it
3. **NO intermediate output** - only final "Daily brief sent" message
4. Use **Google Workspace MCP** for Gmail/Calendar (not Python)
5. Keep summaries **concise** (1-2 sentences max)
6. Web search only for **external meeting prep**