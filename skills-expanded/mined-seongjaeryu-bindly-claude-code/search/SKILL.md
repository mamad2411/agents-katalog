---
description: Search your Bindly knowledge base
---

Search the user's Bindly knowledge base for relevant context.

## Purpose

Help users find and retrieve knowledge they've previously saved to Bindly.
This searches your account at bindly.app, not local files or conversation history.

## Workflow

When the user wants to search their knowledge:

1. **Understand Intent**: Clarify what the user is looking for
   - A specific topic or concept?
   - Related to a project or domain?
   - Recent activity or older knowledge?

2. **Search**: Use `mcp_search` with appropriate query
   - Semantic search works across all Spaces
   - Can filter by Space if needed

3. **Present Results (Tier 1)**: Show summaries first
   - Title and key points
   - Entities and tags
   - Creation/update date
   - This saves tokens and gives quick overview

4. **Deep Dive (Tier 2)**: On request, retrieve full content
   - Use `mcp_get_binding` with tier=2
   - Show complete source content
   - Offer version history if relevant

5. **Suggest Related**: Help exploration
   - Point out related bindings
   - Suggest Sets that might be relevant
   - Offer to organize findings

## Example Prompts

- "What do I know about authentication patterns?"
- "Find my notes on React performance"
- "Search for anything related to API design"

## Key Points

- Searches bindly.app, not local storage
- Two-tier retrieval: summaries first, full content on demand
- Can search across all Spaces or filter to specific ones
- Results are the same as what you'd see in other connected agents
