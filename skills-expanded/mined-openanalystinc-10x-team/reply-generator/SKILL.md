---
name: reply-generator
description: |
  Generate and send email replies with single approval workflow. Use this skill when the user wants to
  reply to an email. Shows draft for ONE approval, then sends without further confirmation.
allowed-tools:
  - Bash
  - Read
  - Write
  - TodoWrite
  - AskUserQuestion
---

# 10x Reply Generator Skill

Generate, preview, and send email replies with a **single approval** workflow.

## When to Use This Skill

Use this skill when the user:
- Wants to reply to an email
- Says "reply to this email"
- Asks to respond to a message
- Needs help drafting a reply

## When NOT to Use This Skill

Do NOT use this skill for:
- Composing new emails → use `email-composer`
- Bulk outreach → use `outreach-manager`
- Just reading emails → use `inbox-reader`

## Capabilities

1. **Email Analysis** - Understand the original email
2. **Draft Generation** - Create appropriate reply drafts
3. **Multiple Templates** - Acknowledge, confirm, decline, followup, custom
4. **Single Preview** - Show draft once for approval
5. **Autonomous Send** - Send immediately after approval

## CRITICAL: Single Approval Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                  REPLY WORKFLOW                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. READ original email                                    │
│   2. GENERATE draft reply                                   │
│   3. SHOW draft for ONE approval                            │
│   4. SEND immediately after "yes"                           │
│                                                             │
│   ❌ NO multiple confirmations                              │
│   ❌ NO "are you sure?" after showing draft                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Find & Read Email

```json
[
  {"content": "Find the email to reply to", "status": "in_progress", "activeForm": "Finding email"},
  {"content": "Read email content", "status": "pending", "activeForm": "Reading email"},
  {"content": "Generate reply draft", "status": "pending", "activeForm": "Generating draft"},
  {"content": "Show draft for approval", "status": "pending", "activeForm": "Showing draft"},
  {"content": "Send reply", "status": "pending", "activeForm": "Sending reply"}
]
```

```bash
python .claude/scripts/inbox_reader.py --search "from:john subject:meeting"
```

### Step 2: Read Email Content

```bash
python .claude/scripts/inbox_reader.py --read MESSAGE_ID --body
```

### Step 3: Generate & Show Draft

Present the complete draft for ONE approval:

```
═══════════════════════════════════════════════════════════════
                    REPLY DRAFT
═══════════════════════════════════════════════════════════════

ORIGINAL EMAIL:
From: john@example.com
Subject: Meeting Tomorrow
Date: Jan 15, 2024
"Hi, can we meet tomorrow at 2pm to discuss the project?"

───────────────────────────────────────────────────────────────

DRAFT REPLY:
To: john@example.com
Subject: Re: Meeting Tomorrow

Hi John,

Thank you for reaching out. Yes, 2pm tomorrow works perfectly
for me. I'll see you then.

Best regards,
[Your Name]

═══════════════════════════════════════════════════════════════
Send this reply? (yes/no/edit)
═══════════════════════════════════════════════════════════════
```

### Step 4: Single Approval & Immediate Send

**After user says "yes":** Send immediately, no further questions.

```bash
python .claude/scripts/reply_generator.py --reply MESSAGE_ID --type confirm --message "Yes, 2pm tomorrow works perfectly for me."
```

**If user says "edit":** Let them provide changes, show updated draft, ask ONCE more.

**If user says "no":** Cancel without sending.

## Reply Types

| Type | Use When |
|------|----------|
| `acknowledge` | Quick confirmation of receipt |
| `confirm` | Confirming a request or meeting |
| `decline` | Politely declining |
| `followup` | Following up on previous email |
| `custom` | User provides custom message |

## Commands

**Generate reply with auto-send after approval:**
```bash
python .claude/scripts/reply_generator.py --reply MESSAGE_ID --type TYPE
```

**With custom message:**
```bash
python .claude/scripts/reply_generator.py --reply MESSAGE_ID --type custom --message "Your message here"
```

**Save as draft (alternative to send):**
```bash
python .claude/scripts/reply_generator.py --reply MESSAGE_ID --save-draft
```

## Example Workflow

**User:** "Reply to the email from John about the meeting"

1. **Find email** - Search for John's meeting email
2. **Read content** - Get full email body
3. **Generate draft** - Create appropriate reply
4. **Show ONCE** - Display draft for approval
5. **Ask ONCE** - "Send this reply?"
6. **Send immediately** - After "yes", send without further questions
7. **Confirm sent** - "Reply sent successfully!"

## What NOT to Do

- ❌ Show draft, then ask "Is this good?", then ask "Should I send?"
- ❌ Ask "Are you sure?" after user already said yes
- ❌ Request multiple confirmations
- ❌ Show draft multiple times

## What TO Do

- ✅ Show complete draft ONCE
- ✅ Ask for approval ONCE (yes/no/edit)
- ✅ Send IMMEDIATELY after "yes"
- ✅ Allow editing if user wants changes
- ✅ Confirm sent with brief message

## Batch Reply Mode

For replying to multiple emails:

1. Show list of emails to reply to
2. Show draft template for all
3. Ask for ONE approval: "Reply to 5 emails with this template?"
4. After "yes" - send ALL replies autonomously
5. Report results when complete

```
═══════════════════════════════════════════════════════════════
                    BATCH REPLY COMPLETE
═══════════════════════════════════════════════════════════════

✅ Sent: 5 replies
❌ Failed: 0

Replied to:
• john@example.com - Re: Meeting Tomorrow
• jane@company.com - Re: Project Update
• bob@startup.io - Re: Question
• alice@corp.com - Re: Follow Up
• mike@firm.com - Re: Proposal

═══════════════════════════════════════════════════════════════
```
