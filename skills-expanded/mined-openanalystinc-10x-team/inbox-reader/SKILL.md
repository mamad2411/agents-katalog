---
name: inbox-reader
description: |
  Read and search emails from Gmail inbox. Use this skill when the user wants to check their inbox,
  read specific emails, search for emails, or get inbox statistics.
allowed-tools:
  - Bash
  - Read
  - Write
  - TodoWrite
  - AskUserQuestion
---

# 10x Inbox Reader Skill

Read, search, and manage emails from your Gmail inbox.

## When to Use This Skill

Use this skill when the user:
- Wants to check their inbox or unread emails
- Needs to search for specific emails
- Asks to read an email
- Wants inbox statistics
- Needs to find emails by date range

## When NOT to Use This Skill

Do NOT use this skill for:
- Sending emails → use `outreach-manager` or `email-composer`
- Replying to emails → use `reply-generator` skill
- Summarizing emails → use `email-summarizer` skill

## Capabilities

1. **List Emails** - Show recent emails from inbox
2. **Search Emails** - Gmail query syntax support
3. **Read Email** - Get full email content
4. **Inbox Stats** - Unread count, totals, etc.
5. **Date Range** - Filter by date
6. **Export** - Export emails to JSON

## CRITICAL: 3-Mode Workflow with TodoWrite

### Mode 1: PLAN

**Start with TodoWrite:**

```json
[
  {"content": "Authenticate with Gmail", "status": "in_progress", "activeForm": "Authenticating"},
  {"content": "Fetch requested emails", "status": "pending", "activeForm": "Fetching emails"},
  {"content": "Display results to user", "status": "pending", "activeForm": "Displaying results"}
]
```

### Mode 2: CLARIFY

For ambiguous requests, ask:
- "How many emails should I show?"
- "Do you want to include email bodies (slower)?"
- "Any specific search criteria?"

### Mode 3: IMPLEMENT

**Commands:**

**List Recent Emails:**
```bash
python .claude/scripts/inbox_reader.py --list 10
```

**List with Body:**
```bash
python .claude/scripts/inbox_reader.py --list 5 --body
```

**Show Unread:**
```bash
python .claude/scripts/inbox_reader.py --unread
```

**Search Emails:**
```bash
python .claude/scripts/inbox_reader.py --search "from:example@gmail.com"
```

**Get Inbox Stats:**
```bash
python .claude/scripts/inbox_reader.py --stats
```

**Read Specific Email:**
```bash
python .claude/scripts/inbox_reader.py --read MESSAGE_ID
```

**Date Range:**
```bash
python .claude/scripts/inbox_reader.py --date-range 2024/01/01 2024/12/31
```

**List Labels:**
```bash
python .claude/scripts/inbox_reader.py --labels
```

## Gmail Search Query Syntax

| Query | Description |
|-------|-------------|
| `from:email@example.com` | From specific sender |
| `to:email@example.com` | Sent to specific recipient |
| `subject:keyword` | Subject contains keyword |
| `is:unread` | Unread emails |
| `is:starred` | Starred emails |
| `has:attachment` | Has attachments |
| `after:2024/01/01` | After date |
| `before:2024/12/31` | Before date |
| `newer_than:7d` | Last 7 days |
| `older_than:1m` | Older than 1 month |
| `label:important` | Specific label |

## Example Workflows

### "Show me my unread emails"

```json
[
  {"content": "Authenticate with Gmail", "status": "in_progress", "activeForm": "Authenticating"},
  {"content": "Fetch unread emails", "status": "pending", "activeForm": "Fetching unread"},
  {"content": "Display email list", "status": "pending", "activeForm": "Displaying emails"}
]
```

### "Search for emails from John"

```json
[
  {"content": "Authenticate with Gmail", "status": "in_progress", "activeForm": "Authenticating"},
  {"content": "Search for emails from John", "status": "pending", "activeForm": "Searching"},
  {"content": "Display search results", "status": "pending", "activeForm": "Displaying results"}
]
```

## Output Format

Emails are displayed with:
- Date
- From (sender)
- Subject
- Read/Unread status
- Snippet (preview)

## Error Handling

- Authentication fails → Run `python .claude/scripts/auth_setup.py`
- No emails found → Inform user, suggest broader search
- Rate limited → Wait and retry
