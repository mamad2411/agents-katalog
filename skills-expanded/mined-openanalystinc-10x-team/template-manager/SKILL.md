---
name: template-manager
description: |
  Manage email templates for outreach and campaigns. Use this skill when the user wants to
  create, edit, list, or organize email templates.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - TodoWrite
  - AskUserQuestion
---

# 10x Template Manager Skill

Create and manage email templates for outreach campaigns.

## When to Use This Skill

Use this skill when the user:
- Wants to create a new email template
- Needs to edit an existing template
- Asks to list available templates
- Wants to organize templates

## When NOT to Use This Skill

Do NOT use this skill for:
- Sending emails → use `outreach-manager` or `email-composer`
- Reading inbox → use `inbox-reader`

## Capabilities

1. **List Templates** - Show all available templates
2. **Create Templates** - Create new templates
3. **Edit Templates** - Modify existing templates
4. **Preview Templates** - See template with sample data
5. **Organize** - Categorize templates

## Template Location

Templates are stored in:
```
.claude/templates/
├── email/          # Email templates
│   ├── outreach/   # Cold outreach emails
│   ├── follow-up/  # Follow-up sequences
│   ├── promotional/ # Promotional campaigns
│   └── newsletters/ # Newsletter templates
├── linkedin/       # LinkedIn message templates
├── twitter/        # Twitter message templates
└── instagram/      # Instagram message templates
```

## Template Format

Templates use Jinja2 syntax with optional frontmatter:

```
---
subject: Hello {{ name }}, about {{ topic }}
---
Hi {{ name }},

{{ custom_message }}

Best regards,
{{ my_name }}
```

**Without frontmatter:**
```
Hi {{ name }},

{{ custom_message }}

Best regards,
{{ my_name }}
```

## Available Variables

| Variable | Description |
|----------|-------------|
| `{{ email }}` | Recipient email |
| `{{ name }}` | Full name |
| `{{ first_name }}` | First name |
| `{{ company }}` | Company name |
| `{{ custom_message }}` | Custom content |
| `{{ my_name }}` | Sender name (from .env) |
| Any Sheet column | Custom fields from Google Sheet |

## Commands

**List All Templates:**
```bash
python .claude/scripts/template_loader.py list
```

**List by Platform:**
```bash
python .claude/scripts/template_loader.py list --platform email --category outreach
```

**Read a Template:**
```bash
python .claude/scripts/template_loader.py render --path email/outreach/cold_email
```

**Create New Template:**
Use the Write tool to create:
`.claude/templates/[platform]/[category]/[name].md`

## CRITICAL: 3-Mode Workflow with TodoWrite

### Mode 1: PLAN

```json
[
  {"content": "List existing templates", "status": "in_progress", "activeForm": "Listing templates"},
  {"content": "Determine user's template needs", "status": "pending", "activeForm": "Understanding needs"},
  {"content": "Create/edit template", "status": "pending", "activeForm": "Working on template"},
  {"content": "Preview template", "status": "pending", "activeForm": "Previewing template"}
]
```

### Mode 2: CLARIFY

Ask:
- "What type of template? (outreach, promotional, follow-up, newsletter, custom)"
- "What tone? (formal, casual, friendly)"
- "What variables do you need?"

### Mode 3: IMPLEMENT

**Create a Template:**

Use the Write tool to create the template file.

Example template (`.claude/templates/email/outreach/cold_email.md`):
```
---
subject: Quick question about {{ company }}
---
Hi {{ first_name }},

I noticed {{ company }} is doing great work in your industry.

I wanted to reach out because {{ custom_message }}

Would you be open to a quick chat this week?

Best regards,
{{ my_name }}
```

## Example Workflow

**User:** "Create a follow-up email template"

**Step 1: Todo List**
```json
[
  {"content": "Understand follow-up template requirements", "status": "in_progress", "activeForm": "Understanding requirements"},
  {"content": "Draft template content", "status": "pending", "activeForm": "Drafting template"},
  {"content": "Create template file", "status": "pending", "activeForm": "Creating file"},
  {"content": "Preview template", "status": "pending", "activeForm": "Previewing template"}
]
```

**Step 2: Clarify**
- "What's the follow-up about? (meeting, proposal, introduction, etc.)"
- "How many days after initial contact?"

**Step 3: Create**

Write the template to `.claude/templates/email/follow-up/general.md`:
```
---
subject: Following up - {{ original_subject }}
---
Hi {{ first_name }},

I wanted to follow up on my previous email about {{ topic }}.

{{ custom_message }}

Looking forward to hearing from you.

Best regards,
{{ my_name }}
```

**Step 4: Confirm**
Show the created template and confirm it's saved.

## Template Categories

### Outreach Templates
- `cold.txt` - Initial cold outreach
- `introduction.txt` - Self-introduction
- `networking.txt` - Professional networking

### Promotional Templates
- `product-launch.txt` - New product announcement
- `discount.txt` - Special offer
- `event.txt` - Event invitation

### Follow-up Templates
- `general.txt` - Generic follow-up
- `no-response.txt` - After no reply
- `after-meeting.txt` - Post-meeting follow-up

### Newsletter Templates
- `weekly.txt` - Weekly digest
- `monthly.txt` - Monthly newsletter
- `announcement.txt` - Special announcement
