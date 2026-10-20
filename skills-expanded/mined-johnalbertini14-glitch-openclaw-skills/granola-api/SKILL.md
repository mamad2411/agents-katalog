---
name: granola
description: |
  Granola MCP server integration with managed OAuth. Query meeting notes, list meetings, and access transcripts.
  Use this skill when users want to search meeting content, get meeting summaries, find action items, or retrieve transcripts from Granola.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Granola

Access Granola's MCP server with managed OAuth authentication. Query meeting notes, list meetings, search meeting content, and retrieve transcripts.

## Quick Start

```bash
# Query your meeting notes
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': 'What action items came from my last meeting?'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/granola/query_granola_meetings', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://gateway.maton.ai/granola/{tool_name}
```

Replace `{tool_name}` with the MCP tool name. The gateway proxies requests to Granola's MCP server at `mcp.granola.ai` and automatically handles OAuth authentication.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Granola OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=granola&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'granola'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "8a413c45-6427-45d9-b69d-8118ce62ffce",
    "status": "ACTIVE",
    "creation_time": "2026-02-24T11:34:46.204677Z",
    "last_updated_time": "2026-02-24T11:37:01.221812Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "granola",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Granola connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': 'What were my action items?'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/granola/query_granola_meetings', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', '8a413c45-6427-45d9-b69d-8118ce62ffce')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If omitted, the gateway uses the default (oldest) active connection.

## MCP Tools Reference

Granola exposes four MCP tools. All tools are called via POST requests with JSON body parameters.

### query_granola_meetings

Chat with your meeting notes using natural language queries. This is the primary tool for conversational interaction with your meeting data.

**Endpoint:**
```
POST /granola/query_granola_meetings
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Natural language query about your meetings |

**Example:**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': 'What action items came from my meetings this week?'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/granola/query_granola_meetings', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "You had 2 recent meetings:\n**Feb 4, 2026 at 7:30 PM** - \"Team sync\" [[0]](https://notes.granola.ai/d/abc123)\n- Action item: Review Q1 roadmap\n- Action item: Schedule follow-up with engineering\n**Jan 27, 2026 at 1:04 AM** - \"Finance integration\" [[1]](https://notes.granola.ai/d/def456)\n- Discussed workflow automation platforms\n- Action item: Evaluate n8n vs Zapier"
    }
  ],
  "isError": false
}
```

**Use cases:**
- "What action items were assigned to me?"
- "Summarize my meetings from last week"
- "What did we discuss about the product launch?"
- "Find all mentions of budget in my meetings"

---

### list_meetings

List your meetings with metadata including IDs, titles, dates, and attendees. Use this to discover meeting IDs for use with other tools.

**Endpoint:**
```
POST /granola/list_meetings
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| (none) | - | - | Returns recent meetings by default |

**Example:**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({}).encode()
req = urllib.request.Request('https://gateway.maton.ai/granola/list_meetings', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "<meetings_data from=\"Jan 27, 2026\" to=\"Feb 4, 2026\" count=\"2\">\n<meeting id=\"0dba4400-50f1-4262-9ac7-89cd27b79371\" title=\"Team sync\" date=\"Feb 4, 2026 7:30 PM\">\n    <known_participants>\n    John Doe (note creator) from Acme <john@acme.com>\n    Jane Smith from Acme <jane@acme.com>\n    </known_participants>\n  </meeting>\n\n<meeting id=\"4ebc086f-ba8d-49e8-8cd1-ed81ac8f2e3b\" title=\"Finance integration\" date=\"Jan 27, 2026 1:04 AM\">\n    <known_participants>\n    John Doe (note creator) from Acme <john@acme.com>\n    </known_participants>\n  </meeting>\n</meetings_data>"
    }
  ],
  "isError": false
}
```

**Response fields in XML format:**
- `meetings_data`: Container with `from`, `to` date range and `count`
- `meeting`: Individual meeting with `id`, `title`, and `date` attributes
- `known_participants`: List of attendees with name, role, company, and email

---

### get_meetings

Retrieve detailed content for specific meetings by ID, including summaries, enhanced notes, and private notes.

**Endpoint:**
```
POST /granola/get_meetings
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `meeting_ids` | array of strings | Yes | List of meeting IDs to retrieve |

**Example:**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'meeting_ids': ['0dba4400-50f1-4262-9ac7-89cd27b79371']}).encode()
req = urllib.request.Request('https://gateway.maton.ai/granola/get_meetings', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "<meetings_data from=\"Feb 4, 2026\" to=\"Feb 4, 2026\" count=\"1\">\n<meeting id=\"0dba4400-50f1-4262-9ac7-89cd27b79371\" title=\"Team sync\" date=\"Feb 4, 2026 7:30 PM\">\n  <known_participants>\n  John Doe (note creator) from Acme <john@acme.com>\n  </known_participants>\n  \n  <summary>\n## Key Decisions\n- Approved Q1 roadmap\n- Budget increased by 15%\n\n## Action Items\n- @john: Review design specs by Friday\n- @jane: Schedule engineering sync\n</summary>\n</meeting>\n</meetings_data>"
    }
  ],
  "isError": false
}
```

**Response includes:**
- Meeting metadata (id, title, date, participants)
- `summary`: AI-generated meeting summary with key decisions and action items
- Enhanced notes and private notes (when available)

---

### get_meeting_transcript

Retrieve the raw transcript for a specific meeting. **Only available on paid Granola tiers.**

**Endpoint:**
```
POST /granola/get_meeting_transcript
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `meeting_id` | string | Yes | The meeting ID to get transcript for |

**Example:**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'meeting_id': '0dba4400-50f1-4262-9ac7-89cd27b79371'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/granola/get_meeting_transcript', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response (paid tier):**
```json
{
  "content": [
    {
      "type": "text",
      "text": "<transcript meeting_id=\"0dba4400-50f1-4262-9ac7-89cd27b79371\">\n[00:00:15] John: Let's get started with the Q1 planning...\n[00:01:23] Jane: I've prepared the budget breakdown...\n[00:03:45] John: That looks good. What about the timeline?\n</transcript>"
    }
  ],
  "isError": false
}
```

**Response (free tier):**
```json
{
  "content": [
    {
      "type": "text",
      "text": "Transcripts are only available to paid Granola tiers"
    }
  ],
  "isError": true
}
```

## Code Examples

### JavaScript

```javascript
// Query meeting notes
const response = await fetch('https://gateway.maton.ai/granola/query_granola_meetings', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'What were the action items from my last meeting?'
  })
});
const data = await response.json();
console.log(data.content[0].text);
```

### Python

```python
import os
import requests

# List all meetings
response = requests.post(
    'https://gateway.maton.ai/granola/list_meetings',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={}
)
data = response.json()

# Get specific meeting content
meeting_ids = ['0dba4400-50f1-4262-9ac7-89cd27b79371']
response = requests.post(
    'https://gateway.maton.ai/granola/get_meetings',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={'meeting_ids': meeting_ids}
)
```

## Notes

- **MCP Protocol**: Granola uses the Model Context Protocol (MCP). All tool calls are POST requests with JSON body parameters.
- **Response Format**: All responses follow MCP format with `content` array containing `type: "text"` objects and an `isError` boolean.
- **Access Control**: Users can only query their own meeting notes. Shared notes from others are not accessible.
- **Free Tier Limits**: Basic (free) plan users are limited to notes from the last 30 days.
- **Transcript Access**: The `get_meeting_transcript` tool is only available on paid Granola tiers.
- **Rate Limits**: Approximately 100 requests per minute (varies by plan tier).

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Granola connection |
| 401 | Invalid or missing Maton API key |
| 429 | Rate limited |
| MCP -32602 | Invalid tool parameters (check required fields) |

**MCP Error Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "MCP error -32602: Input validation error: Invalid arguments for tool get_meetings: [\n  {\n    \"code\": \"invalid_type\",\n    \"expected\": \"array\",\n    \"received\": \"undefined\",\n    \"path\": [\"meeting_ids\"],\n    \"message\": \"Required\"\n  }\n]"
    }
  ],
  "isError": true
}
```

## Resources

- [Granola MCP Documentation](https://docs.granola.ai/help-center/sharing/integrations/mcp)
- [Granola Help Center](https://docs.granola.ai)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
