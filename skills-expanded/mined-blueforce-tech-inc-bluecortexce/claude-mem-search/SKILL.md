---
name: claude-mem-search
description: Searches Claude-Mem memory system for historical observations,
  summaries, and context from past sessions. Use when user asks about
  "what did we do before", "last time we", "search memory", "find previous",
  "recall when", "上次我们", "之前是怎么", "搜索记忆", "查找之前", or when
  context from past work sessions would be helpful for the current task.
  Requires Claude-Mem Java backend running at localhost:37777.
---

# Claude-Mem Memory Search

Search and retrieve context from past development sessions stored in Claude-Mem.

## When to Use

Activate this skill when:
- User references past work ("上次我们...", "之前是怎么...", "last time we...")
- User asks to search history ("搜索记忆", "查找之前的实现", "recall when...")
- Current task may benefit from historical context
- User wants to know what was done in a previous session

## Prerequisites

Claude-Mem Java backend must be running:

```bash
curl -s http://127.0.0.1:37777/actuator/health
# Should return: {"status":"UP",...}
```

If not running, tell user to start the Java backend first.

---

## Three-Step Memory Retrieval Workflow

### Step 1: Search Memory Index

Search for relevant observations by semantic query or filter:

```bash
# Semantic search
curl -s "http://127.0.0.1:37777/api/search?project=PROJECT_PATH&query=SEARCH_QUERY&limit=5"

# Filter by type
curl -s "http://127.0.0.1:37777/api/search?project=PROJECT_PATH&type=discovery&limit=5"

# Filter by concept
curl -s "http://127.0.0.1:37777/api/search?project=PROJECT_PATH&concept=architecture&limit=5"
```

**Parameters:**
- `project` (required): Project path, e.g., `/Users/username/projects/myapp`
- `query`: Semantic search query
- `type`: Filter by observation type (discovery, decision, error, etc.)
- `concept`: Filter by concept (architecture, testing, security, etc.)
- `limit`: Max results (default: 20)

**Returns:** List of observations with IDs and metadata.

### Step 2: Get Timeline Context (Optional)

Get observations around a specific anchor point:

```bash
# By anchor ID
curl -s "http://127.0.0.1:37777/api/context/timeline?project=PROJECT_PATH&anchorId=OBSERVATION_ID&depthBefore=3&depthAfter=3"

# By query (finds best matching anchor)
curl -s "http://127.0.0.1:37777/api/context/timeline?project=PROJECT_PATH&query=SEARCH_QUERY&depthBefore=3&depthAfter=3"
```

**Parameters:**
- `project` (required): Project path
- `anchorId`: Anchor observation ID
- `query`: Query to find best matching anchor
- `depthBefore`: Items before anchor (default: 5)
- `depthAfter`: Items after anchor (default: 5)

### Step 3: Get Full Observation Details

Fetch complete details for specific observation IDs:

```bash
curl -s -X POST "http://127.0.0.1:37777/api/observations/batch" \
  -H "Content-Type: application/json" \
  -d '{"ids": ["id1", "id2"], "project": "PROJECT_PATH"}'
```

---

## Quick Access Methods

### Recent Sessions

Get summaries of recent work sessions:

```bash
curl -s "http://127.0.0.1:37777/api/context/recent?project=PROJECT_PATH&limit=3"
```

### Save Manual Memory

To save manual memories, use the MCP tool `save_memory` or use the observation endpoint:

```bash
# Via MCP tool save_memory (recommended)
# The MCP tool is available when connected via MCP protocol

# Or via direct observation (for testing)
curl -s -X POST "http://127.0.0.1:37777/api/ingest/observation" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "SESSION_ID", "project_path": "PROJECT_PATH", "content": "Important insight to remember", "title": "Key Decision"}'
```

---

## Workflow Example

When user asks "上次我们是怎么解决登录问题的？":

```bash
# Step 1: Search for login-related observations
curl -s "http://127.0.0.1:37777/api/search?project=/path/to/project&query=login%20problem%20solution&limit=5"

# Step 2: Get context around the most relevant result
curl -s "http://127.0.0.1:37777/api/context/timeline?project=/path/to/project&query=login%20solution&depthBefore=2&depthAfter=2"

# Step 3: Get full details if needed
curl -s -X POST "http://127.0.0.1:37777/api/observations/batch" \
  -H "Content-Type: application/json" \
  -d '{"ids": ["found-id-1", "found-id-2"], "project": "/path/to/project"}'
```

---

## Response Format

All responses are JSON. Key fields:

```json
{
  "observations": [...],
  "count": 5,
  "strategy": "vector_search"
}
```

Each observation contains:
- `id`: Unique identifier
- `title`: Short title
- `content`: Full content text
- `type`: Observation type
- `concepts`: Related concepts
- `createdAtEpoch`: Timestamp
- `filePath`: Related file path (if any)

---

## Error Handling

If the backend is unreachable:
```
Claude-Mem backend is not responding. Please start it with:
cd /path/to/your/BlueCortexCE/backend
java -jar target/cortex-ce-0.1.0-beta.jar
```

If no results found:
- Try broader search terms
- Check project path is correct
- Verify observations exist with `/api/stats`
