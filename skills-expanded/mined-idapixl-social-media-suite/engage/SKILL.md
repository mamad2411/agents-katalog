---
name: engage
description: Check for and respond to social media engagement — comments, replies, mentions across platforms.
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Agent, WebSearch, WebFetch
argument-hint: [platform]
---

# Engagement Check: $ARGUMENTS

Check for engagement across platforms and draft responses.

## Workflow

1. **Check each platform for new engagement:**

   **Reddit** (via Reddit MCP):
   - Browse r/idapixl for new comments
   - Check recent post replies
   - Under 1K subscribers = reply to EVERY comment

   **YouTube** (via YouTube MCP):
   - `youtube_list_comments` on recent videos
   - Check community post responses

   **Discord** (via Discord MCP):
   - Read #inbox channel for new messages
   - Check #the-wall for community activity

   **Bluesky** (needs Playwright or AT Protocol):
   - Check notifications for mentions/replies

2. **For each engagement item, draft a response:**
   - Read brand guidelines for tone
   - Spawn **social-community-builder** agent for response strategy
   - Prioritize: questions > thoughtful comments > simple reactions
   - Never ignore a question

3. **Present responses for approval** before posting

4. **Log engagement data** to `System/Social/engagement.md`

## Response Guidelines (from brand guidelines)

- Be genuinely responsive, not performative
- Match the depth of the comment — short comment gets short reply, thoughtful comment gets thoughtful reply
- Ask follow-up questions to continue conversations
- Never be defensive about being an AI
- Reference specific details from what they said

## Platform Priority Order

1. Reddit (most important for growth — reply to everything)
2. YouTube (community building, watch time signals)
3. Discord (home base, direct connection)
4. Bluesky (natural voice, conversation-first)
5. X (lowest priority — presence maintenance)
