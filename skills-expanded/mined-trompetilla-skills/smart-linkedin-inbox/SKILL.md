---
name: smart-linkedin-inbox
description: Access your LinkedIn inbox through Linxa using MCP.
List and search neriched conversations, and fetch messages — without sharing LinkedIn passwords.
summary: Access your LinkedIn inbox through Linxa using MCP.
---

#Smart LinkedIn Inbox from Linxa

## What this skill does

This skill connects OpenClaw to your Linxa Smart Inbox and lets you:
	- List and search inbox conversations
	- Fetch messages from a specific conversation


## Quickstart (3 minutes)


### 1) Install the [inxa Chrome Extension](https://chromewebstore.google.com/detail/ai-smart-inbox-for-linked/ggkdnjblijkchfmgapnbhbhnphacmabm)


### 2) Sign in to [Linxa](https://app.uselinxa.com/) with LinkedIn


### 3) [Generate](https://app.uselinxa.com/setup-mcp) an access token

###  4) Install the skill
```
clawhub install smart-linkedin-inbox
```

### 5) Set the token
```
export LINXA_TOKEN=YOUR_TOKEN
```

### 6) Tell OpenClaw to run the skill smart-linkedin-inbox read SKILL.md and use for LinkedIn 

## Using the skill (example prompts)

You can interact with the skill using natural language:
- Who am I on LinkedIn?
- What are my latest LinkedIn messages?
- Show my last messages with Mahde Shalaby
- List hot conversations

---

Authentication

All requests require an authorization header:
```
Authorization: Bearer $LINXA_TOKEN
```
Security notes
- No LinkedIn password sharing
- Uses your active LinkedIn browser session
- Token-based access only

---

## Available endpoints (tools)

### 1) Verify current user
```
GET /api/mcp/current-li-user
```

Verifies authentication and returns the current LinkedIn profile.


### 2) List conversations

```
GET /api/mcp/conversations
```

Query parameters:
- limit — number of conversations (default: 50)
- search — keyword search
- label — filter by category
Available values:
Hot, Need Follow Up, Personal, Investors, Clients,
Inbox, Hiring, Junk, Partnership, archived,
scheduled, not-contacted
- sentiment — POSITIVE, NEGATIVE, NEUTRAL
- primary_intent — e.g. sales
- intent_direction — to_me | from_me



### 3) Fetch messages from a conversation

```
GET /api/mcp/messages/{chatId}
```

Returns all messages for the specified conversation.


## Manual testing (curl)

Verify identity
```
curl -L \
  -H "Authorization: Bearer $LINXA_TOKEN" \
  https://app.uselinxa.com/api/mcp/current-li-user
```


List hot conversations
```
curl -L \
  -H "Authorization: Bearer $LINXA_TOKEN" \
  "https://app.uselinxa.com/api/mcp/conversations?label=Hot&limit=5"
```

---

Notes
- URL-encode chatId if it contains special characters
- This skill connects to the public Linxa API (app.uselinxa.com)
- Message sync depends on an active Linxa + Chrome extension session