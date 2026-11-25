---
name: conversations-inbox-messages
description: "Conversations Inbox & Messages API skill. Use when working with Conversations Inbox & Messages for conversations. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# Conversations Inbox & Messages
API version: v3

## Auth
OAuth2 | ApiKey private-app in header

## Base URL
https://api.hubapi.com

## Setup
1. Set your API key in the appropriate header
2. GET /conversations/v3/conversations/channel-accounts -- verify access
3. POST /conversations/v3/conversations/actors/batch/read -- create first read

## Endpoints

16 endpoints across 1 groups. See references/api-spec.lap for full details.

### conversations
| Method | Path | Description |
|--------|------|-------------|
| POST | /conversations/v3/conversations/actors/batch/read | Get a group of actors |
| GET | /conversations/v3/conversations/actors/{actorId} | Get a single actor |
| GET | /conversations/v3/conversations/channel-accounts | Get channel accounts |
| GET | /conversations/v3/conversations/channel-accounts/{channelAccountId} | Get a single channel account |
| GET | /conversations/v3/conversations/channels | Get channels |
| GET | /conversations/v3/conversations/channels/{channelId} | Get a single channel |
| GET | /conversations/v3/conversations/inboxes | Get conversations inboxes |
| GET | /conversations/v3/conversations/inboxes/{inboxId} | Get a single conversations inbox |
| GET | /conversations/v3/conversations/threads | Get threads |
| GET | /conversations/v3/conversations/threads/{threadId} | Get a single thread |
| DELETE | /conversations/v3/conversations/threads/{threadId} | Archives a thread |
| PATCH | /conversations/v3/conversations/threads/{threadId} | Update a thread |
| GET | /conversations/v3/conversations/threads/{threadId}/messages | Get message history for a thread |
| POST | /conversations/v3/conversations/threads/{threadId}/messages | Send a message to a thread |
| GET | /conversations/v3/conversations/threads/{threadId}/messages/{messageId} | Get a single message |
| GET | /conversations/v3/conversations/threads/{threadId}/messages/{messageId}/original-content | Get the original content of a single message |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a read?" -> POST /conversations/v3/conversations/actors/batch/read
- "Get actor details?" -> GET /conversations/v3/conversations/actors/{actorId}
- "List all channel-accounts?" -> GET /conversations/v3/conversations/channel-accounts
- "Get channel-account details?" -> GET /conversations/v3/conversations/channel-accounts/{channelAccountId}
- "List all channels?" -> GET /conversations/v3/conversations/channels
- "Get channel details?" -> GET /conversations/v3/conversations/channels/{channelId}
- "List all inboxes?" -> GET /conversations/v3/conversations/inboxes
- "Get inboxe details?" -> GET /conversations/v3/conversations/inboxes/{inboxId}
- "List all threads?" -> GET /conversations/v3/conversations/threads
- "Get thread details?" -> GET /conversations/v3/conversations/threads/{threadId}
- "Delete a thread?" -> DELETE /conversations/v3/conversations/threads/{threadId}
- "Partially update a thread?" -> PATCH /conversations/v3/conversations/threads/{threadId}
- "List all messages?" -> GET /conversations/v3/conversations/threads/{threadId}/messages
- "Create a message?" -> POST /conversations/v3/conversations/threads/{threadId}/messages
- "Get message details?" -> GET /conversations/v3/conversations/threads/{threadId}/messages/{messageId}
- "List all original-content?" -> GET /conversations/v3/conversations/threads/{threadId}/messages/{messageId}/original-content
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
