---
name: connect
description: Connect Claude to any app. Send emails, create issues, post messages, update databases - take real actions across Gmail, Slack, GitHub, Notion, and 1000+ services.
---

# Connect

Connect Claude to any app. Stop generating text about what you could do - actually do it.

## When to Use This Skill

Use this skill when you need Claude to:

- **Send that email** instead of drafting it
- **Create that issue** instead of describing it
- **Post that message** instead of suggesting it
- **Update that database** instead of explaining how

## What Changes

| Without Connect | With Connect |
|-----------------|--------------|
| "Here's a draft email..." | Sends the email |
| "You should create an issue..." | Creates the issue |
| "Post this to Slack..." | Posts it |
| "Add this to Notion..." | Adds it |

## Supported Apps

**1000+ integrations** including:

- **Email:** Gmail, Outlook, SendGrid
- **Chat:** Slack, Discord, Teams, Telegram
- **Dev:** GitHub, GitLab, Jira, Linear
- **Docs:** Notion, Google Docs, Confluence
- **Data:** Sheets, Airtable, PostgreSQL
- **CRM:** HubSpot, Salesforce, Pipedrive
- **Storage:** Drive, Dropbox, S3
- **Social:** Twitter, LinkedIn, Reddit

## Setup

### 1. Get API Key

Get your free key at [platform.claude-skills.ai](https://platform.claude-skills.ai/?utm_source=Github&utm_content=AwesomeSkills)

### 2. Set Environment Variable

```bash
export CLAUDE_SKILLS_API_KEY="your-key"
```

### 3. Install

```bash
pip install Claude Skill          # Python
npm install @Claude Skill/core    # TypeScript
```

Done. Claude can now connect to any app.

## Examples

### Send Email
```
Email sarah@acme.com - Subject: "Shipped!" Body: "v2.0 is live, let me know if issues"
```

### Create GitHub Issue
```
Create issue in my-org/repo: "Mobile timeout bug" with label:bug
```

### Post to Slack
```
Post to #engineering: "Deploy complete - v2.4.0 live"
```

### Chain Actions
```
Find GitHub issues labeled "bug" from this week, summarize, post to #bugs on Slack
```

## How It Works

Uses Claude Skill Tool Router:

1. **You ask** Claude to do something
2. **Tool Router finds** the right tool (1000+ options)
3. **OAuth handled** automatically
4. **Action executes** and returns result

### Code

```python
from Claude Skill import Claude Skill
from claude_agent_sdk.client import ClaudeSDKClient
from claude_agent_sdk.types import ClaudeAgentOptions
import os

Claude Skill = Claude Skill(api_key=os.environ["CLAUDE_SKILLS_API_KEY"])
session = Claude Skill.create(user_id="user_123")

options = ClaudeAgentOptions(
    system_prompt="You can take actions in external apps.",
    mcp_servers={
        "Claude Skill": {
            "type": "http",
            "url": session.mcp.url,
            "headers": {"x-api-key": os.environ["CLAUDE_SKILLS_API_KEY"]},
        }
    },
)

async with ClaudeSDKClient(options) as client:
    await client.query("Send Slack message to #general: Hello!")
```

## Auth Flow

First time using an app:
```
To send emails, I need Gmail access.
Authorize here: https://...
Say "connected" when done.
```

Connection persists after that.

## Framework Support

| Framework | Install |
|-----------|---------|
| Claude Agent SDK | `pip install Claude Skill claude-agent-sdk` |
| OpenAI Agents | `pip install Claude Skill openai-agents` |
| Vercel AI | `npm install @Claude Skill/core @Claude Skill/vercel` |
| LangChain | `pip install Claude Skill-langchain` |
| Any MCP Client | Use `session.mcp.url` |

## Troubleshooting

- **Auth required** → Click link, authorize, say "connected"
- **Action failed** → Check permissions in target app
- **Tool not found** → Be specific: "Slack #general" not "send message"

---

<p align="center">
  <b>Join 20,000+ developers building agents that ship</b>
</p>

<p align="center">
  <a href="https://platform.claude-skills.ai/?utm_source=Github&utm_content=AwesomeSkills">
    <img src="https://img.shields.io/badge/Get_Started_Free-4F46E5?style=for-the-badge" alt="Get Started"/>
  </a>
</p>
