---
name: gmail
description: Read, search, and manage Gmail inbox. Search emails, read conversations, archive messages, snooze for later, and draft replies (safe, does not send). Use when user asks about email, inbox management, checking messages, or drafting responses.
---

> **Output Style:** This skill works best with `/output-style outreach`

# Gmail Skill

Read, search, sort, and draft emails. All operations are **safe** - this skill does NOT send emails.

## Quick Start

```bash
# Search emails
uv run scripts/search.py --query "from:client@example.com"

# Read a conversation
uv run scripts/read.py --thread-id <thread_id>

# Archive email (remove from inbox)
uv run scripts/sort.py archive <message_id>

# Create draft reply
uv run scripts/draft.py reply --thread-id <thread_id> --body "message.txt"
```

## Available Operations

| Operation | Module | Script | Description |
|-----------|--------|--------|-------------|
| Search | [SEARCH.md](modules/SEARCH.md) | `search.py` | Find emails with Gmail queries |
| Read | [READ.md](modules/READ.md) | `read.py` | Read full email threads |
| Sort | [SORT.md](modules/SORT.md) | `sort.py` | Archive, snooze, label emails |
| Draft | [DRAFT.md](modules/DRAFT.md) | `draft.py` | Create draft replies (no send) |

## First-Time Setup

This skill uses the shared Google OAuth integration:

```bash
cd .claude/integrations/google/scripts
python oauth_setup.py
```

See [SETUP.md](../../integrations/google/modules/SETUP.md) for detailed instructions.

## Activation Triggers

- "check my email", "what emails do I have"
- "search my inbox for..."
- "find the conversation with..."
- "archive this email", "snooze until..."
- "draft a reply to..."
- Any mention of "Gmail", "inbox", "email"

## Important Notes

- **This skill does NOT send emails** - use `gmail-send` skill for sending
- Drafts are created in Gmail - user must manually send
- Archive removes from inbox (does not delete)
- Snooze uses Gmail's native snooze feature

## Output Location

Search results and conversation exports saved to:
```
workspace/docs/YYYY-MM-DD - Gmail/
```
