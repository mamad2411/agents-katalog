---
name: email-composer
description: |
  Compose and send individual emails. Use this skill when the user wants to write a new email
  to a single recipient (not bulk/campaign). Supports templates and attachments.
allowed-tools:
  - Bash
  - Read
  - Write
  - TodoWrite
  - AskUserQuestion
---

# 10x Email Composer Skill

Compose and send individual emails with preview and approval.

## When to Use This Skill

Use this skill when the user:
- Wants to compose a new email
- Asks to send an email to someone
- Needs to write a single email (not bulk)
- Wants to create an email draft

## When NOT to Use This Skill

Do NOT use this skill for:
- Bulk/campaign emails → use `outreach-manager`
- Replying to emails → use `reply-generator`
- Reading emails → use `inbox-reader`

## Capabilities

1. **Compose Emails** - Write new emails from scratch
2. **Use Templates** - Apply templates with personalization
3. **Attachments** - Support file attachments
4. **HTML Emails** - Send formatted HTML emails
5. **Preview** - Always preview before sending
6. **Save Draft** - Save to Gmail drafts

## CRITICAL: 3-Mode Workflow with TodoWrite

### Mode 1: PLAN

**Start with TodoWrite:**

```json
[
  {"content": "Gather email details (to, subject, content)", "status": "in_progress", "activeForm": "Gathering details"},
  {"content": "Create email draft", "status": "pending", "activeForm": "Creating draft"},
  {"content": "Preview email to user", "status": "pending", "activeForm": "Previewing email"},
  {"content": "Get user approval", "status": "pending", "activeForm": "Getting approval"},
  {"content": "Send email", "status": "pending", "activeForm": "Sending email"}
]
```

Gather required information:
- To: (recipient email)
- Subject: (email subject)
- Body: (email content)
- Template: (optional)
- Attachments: (optional)

### Mode 2: CLARIFY

Ask for missing information:
- "Who should I send this email to?"
- "What's the subject?"
- "What would you like to say?"
- "Do you want to use a template?"

### Mode 3: IMPLEMENT

**Preview First:**

Present the complete email to user:
```
📧 Email Preview:

To: recipient@example.com
Subject: Your Subject Here

Body:
[Full email content]

---
Send this email?
```

**Only After Approval - Send:**
```bash
python .claude/scripts/gmail_client.py send --to "recipient@example.com" --subject "Subject" --body "Email body here"
```

**Save as Draft:**
```bash
python .claude/scripts/gmail_client.py draft --to "recipient@example.com" --subject "Subject" --body "Email body here"
```

## Using Templates

**List Available Templates:**
```bash
python .claude/scripts/template_loader.py list --platform email
```

**Render a Template:**
```bash
python .claude/scripts/template_loader.py render --path email/outreach/warm_intro --var first_name "John" --var company "Acme"
```

Templates support variables:
- `{{ name }}` - Recipient name
- `{{ company }}` - Company name
- `{{ custom_message }}` - Custom content

## Example Workflow

**User:** "Send an email to john@example.com about the project update"

**Step 1: Create Todo List**
```json
[
  {"content": "Compose email to john@example.com", "status": "in_progress", "activeForm": "Composing email"},
  {"content": "Preview draft to user", "status": "pending", "activeForm": "Previewing draft"},
  {"content": "Get user approval", "status": "pending", "activeForm": "Getting approval"},
  {"content": "Send email", "status": "pending", "activeForm": "Sending email"}
]
```

**Step 2: Draft the email**
Ask user for content or help compose it.

**Step 3: Preview**
```
📧 Email Preview:

To: john@example.com
Subject: Project Update

Hi John,

Here's the latest update on the project...

Best regards,
[Your Name]

---
Does this look good? Send, edit, or save as draft?
```

**Step 4: Approval**
Wait for explicit "yes" / "send" / approval.

**Step 5: Send**
Execute send command and confirm success.

## With HTML Content

```bash
python .claude/scripts/gmail_client.py send --to "recipient@example.com" --subject "Subject" --body "Plain text version" --html "<h1>HTML Version</h1><p>With formatting</p>"
```

## With Attachments

```bash
python .claude/scripts/gmail_client.py send --to "recipient@example.com" --subject "Subject with attachment" --body "Please find attached." --attachment "path/to/file.pdf"
```

## Safety Rules

1. **Always preview** before sending
2. **Get explicit approval** before send
3. **Offer draft option** as alternative
4. **Log sent emails** to output/sent/
5. **Validate email addresses** before sending
