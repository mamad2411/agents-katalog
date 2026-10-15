---
name: vector-store
description: Store and retrieve knowledge using vector similarity search. Use for semantic search across learnings, documentation, and shared agent knowledge. Supports both local ChromaDB and shared Postgres (pgvector) stores. Use when you need persistent memory, cross-agent knowledge sharing, or semantic search over documents.
---

# Vector Store

Semantic search and persistent knowledge storage for AI agents.

## Overview

Two complementary stores:
1. **Local ChromaDB** — Fast, private, session-scoped
2. **Shared Postgres (pgvector)** — Collaborative, persistent, cross-agent

## Quick Start

### Store Knowledge (Postgres)

```sql
INSERT INTO agent_knowledge (agent_name, category, title, content, metadata)
VALUES (
  'your_agent', 
  'debugging', 
  'Your Title',
  'Your content/learning here',
  '{"tags": ["tag1", "tag2"], "discovered": "2026-02-25"}'
);
```

### Search Knowledge

```sql
-- By category
SELECT * FROM agent_knowledge WHERE category = 'debugging';

-- By agent
SELECT * FROM agent_knowledge WHERE agent_name = 'jean';

-- Full text (basic)
SELECT * FROM agent_knowledge WHERE content ILIKE '%search term%';
```

### Send Inter-Agent Message

```sql
INSERT INTO agent_messages (from_agent, to_agent, message_type, content)
VALUES ('jean', 'jared', 'task', 'Can you review the watchdog script?');
```

### Check Messages

```sql
-- Unread messages for you
SELECT * FROM agent_messages 
WHERE to_agent = 'your_agent' AND read_at IS NULL;

-- Mark as read
UPDATE agent_messages SET read_at = NOW() WHERE id = <message_id>;
```

## Postgres Schema

### agent_knowledge
```sql
CREATE TABLE agent_knowledge (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(50) NOT NULL,
    category VARCHAR(100),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),  -- For future semantic search
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### agent_messages
```sql
CREATE TABLE agent_messages (
    id SERIAL PRIMARY KEY,
    from_agent VARCHAR(50) NOT NULL,
    to_agent VARCHAR(50),
    message_type VARCHAR(50) DEFAULT 'general',
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### agent_tasks
```sql
CREATE TABLE agent_tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    assigned_to VARCHAR(50),
    created_by VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'open',
    priority INT DEFAULT 5,
    github_repo VARCHAR(255),
    github_issue INT,
    due_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### agent_standups
```sql
CREATE TABLE agent_standups (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'online',
    current_task TEXT,
    blockers TEXT,
    next_actions TEXT,
    heartbeat_interval_min INT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Local ChromaDB (Node.js)

For fast local operations:

```javascript
const { ChromaClient } = require('chromadb');

const client = new ChromaClient();
const collection = await client.getOrCreateCollection({ name: 'agent_knowledge' });

// Add
await collection.add({
  ids: ['unique-id'],
  documents: ['Your content here'],
  metadatas: [{ category: 'debugging', title: 'My Learning' }]
});

// Search
const results = await collection.query({
  queryTexts: ['search query'],
  nResults: 5
});
```

## Best Practices

1. **Categorize consistently** — Use standard categories: `debugging`, `patterns`, `tools`, `infrastructure`
2. **Include metadata** — Tags, dates, collaborators help filtering
3. **Search before adding** — Avoid duplicates
4. **Attribute discoveries** — Note which agent discovered what
5. **Use tasks table** — Coordinate work via `agent_tasks`, not just chat

## Connection

Connection string provided securely via environment or direct share. Tables are pre-created and ready to use.

## See Also

- `inter-agent` skill — Communication protocols
- `COMMUNICATIONS.md` — Dispute resolution standards
