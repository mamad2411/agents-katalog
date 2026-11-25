---
description: Search emails semantically using ZeroEntropy. Use when the user asks about emails, wants to find messages, or needs email context.
---

# Search Emails

When the user asks about their emails or wants to find specific messages, use the zemail MCP tools.

## First-time setup flow

1. Call `index_status` to check if emails are already indexed
2. If no index, call `sync_emails`
3. If sync returns "API key not found", tell the user to grab a free key (no credit card required) at https://dashboard.zeroentropy.dev/api-keys and call `set_api_key` with it
4. If sync returns an OAuth URL, show it to the user and ask them to authorize in their browser, then call `sync_emails` again
5. If on a remote machine and auto-auth fails, ask the user for the code from the success page and call `authorize_gmail`

## Searching

- Use `search_emails_tool` with a natural language query
- Use `get_email` with an email ID to read full content

The search uses zembed-1 embeddings for retrieval and zerank-2 for reranking.
