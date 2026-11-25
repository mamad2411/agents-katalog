---
name: email-summarizer
description: |
  Summarize emails from inbox. Use this skill when the user wants email summaries, digests,
  or to understand their inbox at a glance. Supports daily/weekly digests and batch summarization.
allowed-tools:
  - Bash
  - Read
  - Write
  - TodoWrite
  - AskUserQuestion
---

# 10x Email Summarizer Skill

Generate summaries and digests of your emails.

## When to Use This Skill

Use this skill when the user:
- Wants a summary of their emails
- Asks for an inbox digest (daily/weekly)
- Needs to summarize specific emails
- Wants to know what needs attention
- Asks for email reports

## When NOT to Use This Skill

Do NOT use this skill for:
- Reading full email content → use `inbox-reader`
- Sending emails → use `outreach-manager`
- Replying to emails → use `reply-generator`

## Capabilities

1. **Summarize Recent** - Summarize N recent emails
2. **Daily Digest** - Today's email summary
3. **Weekly Digest** - Past week's summary
4. **Search & Summarize** - Summarize search results
5. **Export Reports** - Markdown, JSON, or text
6. **Action Detection** - Identify emails needing response

## CRITICAL: 3-Mode Workflow with TodoWrite

### Mode 1: PLAN

**Start with TodoWrite:**

```json
[
  {"content": "Authenticate with Gmail", "status": "in_progress", "activeForm": "Authenticating"},
  {"content": "Determine summarization scope", "status": "pending", "activeForm": "Determining scope"},
  {"content": "Fetch emails for summarization", "status": "pending", "activeForm": "Fetching emails"},
  {"content": "Generate summaries", "status": "pending", "activeForm": "Generating summaries"},
  {"content": "Display digest to user", "status": "pending", "activeForm": "Displaying digest"}
]
```

### Mode 2: CLARIFY

Ask if unclear:
- "How many emails should I summarize?"
- "Do you want a digest for today, this week, or custom range?"
- "Should I export the summary to a file?"

### Mode 3: IMPLEMENT

**Commands:**

**Summarize Recent Emails:**
```bash
python .claude/scripts/email_summarizer.py --summarize 10
```

**Summarize Unread Only:**
```bash
python .claude/scripts/email_summarizer.py --summarize 10 --unread
```

**Today's Digest:**
```bash
python .claude/scripts/email_summarizer.py --digest today
```

**Yesterday's Digest:**
```bash
python .claude/scripts/email_summarizer.py --digest yesterday
```

**Weekly Digest:**
```bash
python .claude/scripts/email_summarizer.py --digest week
```

**Monthly Digest:**
```bash
python .claude/scripts/email_summarizer.py --digest month
```

**Search and Summarize:**
```bash
python .claude/scripts/email_summarizer.py --search "from:important@company.com"
```

**Export to Markdown:**
```bash
python .claude/scripts/email_summarizer.py --digest today --export markdown
```

**Export to JSON:**
```bash
python .claude/scripts/email_summarizer.py --summarize 20 --export json
```

## Summary Categories

Emails are categorized as:
- 🚨 **Urgent** - Contains urgent keywords
- 💰 **Financial** - Invoices, payments, receipts
- 📅 **Meeting** - Calendar, schedule related
- 📰 **Newsletter** - Digests, newsletters
- 📦 **Order** - Shipping, delivery updates
- 📧 **General** - Everything else

## Action Detection

The summarizer detects potential actions:
- "please reply" → May need response
- "deadline" → Time-sensitive
- "can you" / "could you" → Request
- "meeting" → Calendar item

## Output Example

```markdown
# Email Digest: Today
*Generated: 2024-01-15 10:30*

Total Emails: 15

## 🚨 Urgent
- **Project Deadline Tomorrow** from Boss

## ⚠️ May Need Response
- **Question about proposal** from Client
- **Meeting confirmation needed** from HR

## 💰 Financial (2)
- Invoice #1234 (Vendor)
- Payment received (Bank)

## 📧 General (10)
- Newsletter from Company
- Update from Service
...
```

## Export Location

Exports saved to:
- `output/reports/email_summary_YYYYMMDD_HHMMSS.md`
- `output/reports/digest_today_YYYYMMDD_HHMMSS.json`

## Example Workflow

**User:** "Give me a summary of today's emails"

**Todo List:**
```json
[
  {"content": "Authenticate with Gmail", "status": "in_progress", "activeForm": "Authenticating"},
  {"content": "Fetch today's emails", "status": "pending", "activeForm": "Fetching emails"},
  {"content": "Generate daily digest", "status": "pending", "activeForm": "Generating digest"},
  {"content": "Display summary to user", "status": "pending", "activeForm": "Displaying summary"}
]
```

Then execute the digest command and present formatted results.
