---
name: laborforge
description: "Interact with LaborForge AI platform via HTTP Tool Gateway. Access ecosystem content, memories, agents, and platform data."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔨",
        "priority": "high",
      },
  }
---

# LaborForge Platform Integration

LaborForge is a multi-tenant AI agent platform that provides ecosystems, agents, memories, and content management. As an OpenClaw agent, you can access LaborForge's capabilities through the HTTP Tool Gateway.

## Callback Context

When LaborForge routes a conversation to you, it includes a `laborforge_callback` object in the configuration. This contains everything you need to call back into LaborForge:

```json
{
  "laborforge_callback": {
    "callback_url": "http://api:8000/api/external/tools/execute",
    "available_tools_url": "http://api:8000/api/external/tools/available",
    "agent_token": "lf_ext_abc123...",
    "allowed_categories": ["read", "write", "agent"],
    "available_tools": [
      {"name": "rag_search_content", "category": "read"},
      {"name": "memory_search", "category": "read"},
      {"name": "memory_create", "category": "write"}
    ],
    "rate_limits": {
      "requests_per_minute": 30,
      "requests_per_hour": 1000
    },
    "instructions": "..."
  }
}
```

## Executing Tools

To execute a LaborForge tool, make an HTTP POST request to the `callback_url`:

```bash
curl -X POST "http://api:8000/api/external/tools/execute" \
  -H "Authorization: Bearer lf_ext_abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "rag_search_content",
    "params": {
      "query": "your search query",
      "limit": 10
    },
    "context": {
      "reason": "Searching for relevant documents to answer user question"
    }
  }'
```

### Response Format

```json
{
  "success": true,
  "tool": "rag_search_content",
  "result": {
    "documents": [...],
    "total_found": 5
  },
  "execution_time_ms": 150
}
```

### Error Response

```json
{
  "success": false,
  "tool": "rag_search_content",
  "error": {
    "code": "EXECUTION_FAILED",
    "message": "Details about the error"
  },
  "execution_time_ms": 50
}
```

## Available Tools

### Content & Knowledge (RAG) - Category: `read`

**rag_search_content** - Search documents and content across ecosystems
```json
{
  "tool": "rag_search_content",
  "params": {
    "query": "your search query",
    "ecosystem_id": 1,
    "limit": 10,
    "include_system_content": true
  }
}
```
- Returns relevant document chunks with citations
- `include_system_content: true` searches admin/system ecosystems too
- Results include `source_ecosystem_id` for attribution

**rag_get_document** - Retrieve a specific document
```json
{
  "tool": "rag_get_document",
  "params": {
    "document_id": "uuid-here",
    "include_chunks": true
  }
}
```

### Memory Operations - Category: `read` + `write`

**memory_search** - Search agent/user memories (requires `read`)
```json
{
  "tool": "memory_search",
  "params": {
    "query": "what the user mentioned about...",
    "entity_type": "user",
    "entity_id": 123,
    "limit": 10
  }
}
```

**memory_create** - Store a new memory (requires `write`)
```json
{
  "tool": "memory_create",
  "params": {
    "content": "User prefers dark mode interfaces",
    "entity_type": "user",
    "entity_id": 123,
    "category": "preference",
    "importance": 0.8
  }
}
```

### Platform Information - Category: `read`

**get_platform_capabilities** - Get platform overview
```json
{
  "tool": "get_platform_capabilities",
  "params": {}
}
```
Returns counts of ecosystems, agents, MCP servers, and available tools.

**list_ecosystems** - List available ecosystems
```json
{
  "tool": "list_ecosystems",
  "params": {}
}
```

**list_agents** - List agents in an ecosystem
```json
{
  "tool": "list_agents",
  "params": {
    "ecosystem_id": 1
  }
}
```

### Agent Communication - Category: `agent` (Coming Soon)

**send_message_to_agent** - Send a message to another LaborForge agent
```json
{
  "tool": "send_message_to_agent",
  "params": {
    "target_agent_slug": "researcher",
    "message": "Can you help me find information about...",
    "context": {}
  }
}
```

## Checking Available Tools

Before executing tools, you can check what's available to you:

```bash
curl -X GET "http://api:8000/api/external/tools/available" \
  -H "Authorization: Bearer lf_ext_abc123..."
```

Returns:
```json
{
  "agent_id": 1,
  "agent_slug": "openclaw-main",
  "tools": [
    {"name": "rag_search_content", "category": "read", "description": "..."},
    {"name": "memory_search", "category": "read", "description": "..."}
  ],
  "rate_limits": {
    "requests_per_minute": 30,
    "requests_per_hour": 1000
  }
}
```

## Ecosystem Context

LaborForge organizes everything into **ecosystems** (tenants):
- **admin** (ID: 1) - System administration, platform-wide agents
- **laborforge** (ID: 2) - Main application ecosystem
- **the-lofts** (ID: 3) - Social features and community

When making requests, you can specify `ecosystem_id` in params. If omitted, your agent's ecosystem is used.

## Best Practices

1. **Check available tools first** - Use the `/tools/available` endpoint to see what you can access
2. **Search before creating** - Check if content/memories exist before duplicating
3. **Cite sources** - When using RAG results, include the source document
4. **Include context** - Add a `reason` in the context to help with audit logging
5. **Respect rate limits** - Check `rate_limits` in the callback context
6. **Handle errors gracefully** - Check `success` in responses and handle errors

## Error Handling

HTTP Status Codes:
- `200` - Success (check `success` field in body)
- `401 Unauthorized` - Token invalid or expired
- `403 Forbidden` - Tool not allowed for your access level
- `429 Too Many Requests` - Rate limited, wait and retry

## Example Workflows

### Research a topic
```python
# 1. Search for relevant documents
search_result = await call_tool("rag_search_content", {
    "query": "machine learning best practices",
    "limit": 5,
    "include_system_content": True
})

# 2. Get full content of top result
if search_result["documents"]:
    doc_id = search_result["documents"][0]["id"]
    doc = await call_tool("rag_get_document", {
        "document_id": doc_id,
        "include_chunks": True
    })

# 3. Synthesize findings with citations
```

### Remember user context
```python
# 1. Search for existing memories about user
memories = await call_tool("memory_search", {
    "query": "user preferences",
    "entity_type": "user",
    "entity_id": user_id,
    "limit": 10
})

# 2. Store new insight
await call_tool("memory_create", {
    "content": "User mentioned they're working on a React project",
    "entity_type": "user",
    "entity_id": user_id,
    "category": "context",
    "importance": 0.6
})
```

### Platform exploration
```python
# 1. Get platform overview
capabilities = await call_tool("get_platform_capabilities", {})

# 2. List ecosystems
ecosystems = await call_tool("list_ecosystems", {})

# 3. List agents in a specific ecosystem
agents = await call_tool("list_agents", {"ecosystem_id": 1})
```
