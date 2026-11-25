---
name: slack
description: Read Slack conversations, list channels, and create draft messages (safe, does not send). Use when user mentions Slack, channels, DMs, or workspace messages.
---

# Slack Skill

Read conversations, list channels, and draft messages. All operations are **safe** - this skill does NOT send messages.

## Quick Start

```bash
# List channels
uv run scripts/list_channels.py

# Read conversation history
uv run scripts/read.py --channel <channel_id> --limit 20

# Create draft message (saved locally, not sent)
uv run scripts/draft.py --channel <channel_id> --message "Your message here"
```

## Available Operations

| Operation | Module | Script | Description |
|-----------|--------|--------|-------------|
| List | [LIST.md](modules/LIST.md) | `list_channels.py` | List channels, DMs, groups |
| Read | [READ.md](modules/READ.md) | `read.py` | Read conversation history |
| Draft | [DRAFT.md](modules/DRAFT.md) | `draft.py` | Create draft messages (no send) |

## First-Time Setup

1. Create a Slack App at https://api.slack.com/apps
2. Add Bot Token Scopes:
   - `channels:read` - List public channels
   - `channels:history` - Read public channel messages
   - `groups:read` - List private channels
   - `groups:history` - Read private channel messages
   - `im:read` - List DMs
   - `im:history` - Read DM messages
   - `users:read` - Get user info
3. Install app to workspace
4. Copy Bot User OAuth Token
5. Set environment variable:
   ```bash
   export SLACK_BOT_TOKEN="xoxb-your-token-here"
   ```

## Activation Triggers

- "check Slack", "what's in Slack"
- "read the conversation in #channel"
- "show me messages from..."
- "list Slack channels"
- "draft a Slack message"
- Any mention of "Slack", "channel", "DM"

## Important Notes

- **This skill does NOT send messages** - drafts are saved locally
- User must manually copy and send drafts
- Bot must be invited to private channels to read them
- Rate limits: ~50 requests per minute

## Output Location

Draft messages saved to:
```
workspace/docs/YYYY-MM-DD - Slack Drafts/
```
