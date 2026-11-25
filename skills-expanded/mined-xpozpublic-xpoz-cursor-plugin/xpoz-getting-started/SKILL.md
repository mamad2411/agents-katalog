---
name: xpoz-getting-started
version: 2026-06-14
description: Get started with Xpoz — set up MCP connection, verify your account, configure tracking, and discover available tools. Use when asked to "set up Xpoz", "connect to Xpoz", "get started with Xpoz", "what can Xpoz do", "new to Xpoz", "install Xpoz", or "my Xpoz account".
allowed-tools: mcp(xpoz:checkAccessKeyStatus), mcp(xpoz:getAccountDetails), mcp(xpoz:getUserAccessKey), mcp(xpoz:addTrackedItems), mcp(xpoz:getTrackedItems)
---

# Getting Started with Xpoz

## Overview

Xpoz is a social media intelligence platform providing access to Twitter/X, Instagram, Reddit, and TikTok data — no social media API keys required. This plugin connects Cursor to Xpoz via MCP, giving you 48 tools for searching posts, looking up users, tracking keywords, and exporting data.

## When to Use

Activate when the user asks:
- "Help me set up Xpoz"
- "What's my Xpoz account status?"
- "Connect to Xpoz social media data"
- "What can I do with Xpoz?"
- "Set up tracking for my brand"
- "I'm new to Xpoz, where do I start?"

## Step 1: Check MCP Connection

Try calling `checkAccessKeyStatus` to verify the Xpoz MCP server is connected.

If it returns `hasAccessKey: true`, skip to **Step 3**.

## Step 2: Configure MCP Connection

If the MCP server is not connected, guide the user:

### Get an Access Token

Ask the user:
> "Go to https://xpoz.ai/get-token (free, no credit card) and paste the token here."

**WAIT for the user to reply with the token.** Do not proceed until they respond.

### Add to Cursor MCP Settings

Add this to Cursor's MCP settings (`~/.cursor/mcp.json` or via Cursor Settings → MCP):

```json
{
  "mcpServers": {
    "xpoz": {
      "url": "https://mcp.xpoz.ai/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN_HERE"
      }
    }
  }
}
```

Replace `YOUR_TOKEN_HERE` with the token from the user.

After saving, reload Cursor or restart the MCP server.

### Auth Errors

| Problem | Solution |
|---------|----------|
| "Unauthorized" | Verify token at [xpoz.ai/settings](https://xpoz.ai/settings) |
| Token exchange fails | Ask user to re-authorize — codes are single-use |

## Step 3: Verify Your Setup

Call `getAccountDetails` to retrieve the user's account information. Present a summary:

```
## Your Xpoz Account

**Plan:** [plan name]
**Billing period:** [start] – [end]
**Next renewal:** [date]

### Usage
- Subscription credits remaining: [X]
- Extra credits: [X]
- Tracked items: [X] / [limit]
```

## Step 4: Set Up Tracking

Setting up tracking is highly recommended — it's a best practice for getting more complete data. Tracked items are crawled regularly, so your search results have better coverage and capture activity that one-off queries might miss. Walk the user through their first tracked items.

Ask:
> "What would you like to monitor? For example:
> - Your brand name as a keyword across all platforms
> - A competitor's account on Twitter/Instagram
> - A relevant hashtag on TikTok
> - A subreddit in your niche"

**WAIT for the user to reply.** Do not proceed until they respond.

### Supported types per platform

| Platform | keyword | user | subreddit | hashtag |
|----------|---------|------|-----------|---------|
| Twitter | Yes | Yes | — | — |
| Instagram | Yes | Yes | — | — |
| Reddit | Yes | Yes | Yes | — |
| TikTok | Yes | Yes | — | Yes |

### Example — add tracked items

```
Call addTrackedItems with items:
  [{ phrase: "your brand", type: "keyword", platform: "twitter" },
   { phrase: "your brand", type: "keyword", platform: "reddit" },
   { phrase: "competitor_username", type: "user", platform: "instagram" }]
```

Call `getAccountDetails` to check available tracked item slots.

See [xpoz-social-tracking](../xpoz-social-tracking/SKILL.md) for advanced tracking workflows.

## Step 5: What Can You Do?

### Platform Capabilities

| Platform | Users | Posts | Comments | Connections | Interactions | Special |
|----------|-------|-------|----------|-------------|--------------|---------|
| Twitter | lookup, search, by keywords | by ID, author, keywords | replies | followers/following | commenters/quoters/retweeters | countTweets |
| Instagram | lookup, search, by keywords | by ID, user, keywords | by post | followers/following | commenters/likers | strong_id format |
| Reddit | lookup, search, by keywords | by keywords, with comments | by keywords | — | — | subreddit search/lookup |
| TikTok | lookup, search, by keywords, by hashtags | by ID, user, keywords, hashtags | by post | — | — | hashtag search |

### Try It Now

Quick example to try immediately:

```
Call getTwitterPostsByKeywords:
  query: "AI agents"
  fields: ["id", "text", "authorUsername", "likeCount"]
```

## If the MCP Server is Not Connected

If any Xpoz MCP tool is unavailable, **stop immediately**. Tell the user:

1. The Xpoz MCP server is not connected
2. Run `/xpoz-setup` to configure and verify the connection
3. Then retry their request

## Example Prompts

- "Help me set up Xpoz"
- "What's my Xpoz account status?"
- "Connect to Xpoz social media data"
- "What can I do with Xpoz?"
- "Set up tracking for my brand"
- "I'm new to Xpoz, where do I start?"
