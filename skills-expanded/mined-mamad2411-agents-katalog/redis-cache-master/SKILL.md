---
name: redis-cache-master
description: "Configure, monitor, and optimize Redis caches for caching patterns, session storage, and pub/sub queues."
category: backend
tags: [redis, cache, nosql, performance, keys]
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# Redis Cache Master

## Purpose
Manage and implement Redis Cache Master requirements efficiently within enterprise applications.

## Core Concepts
Detailed operational framework for Redis Cache Master:

### 1️⃣ Overview and Strategy
Understanding boundaries, rules, and best practices for the redis-cache-master feature domain.

### 2️⃣ Code Implementation Reference
```javascript
// Redis cache aside pattern
const cached = await redis.get(key);
if (cached) return JSON.parse(cached);
const fresh = await db.fetch();
await redis.setex(key, 3600, JSON.stringify(fresh));
```

### 3️⃣ Checklist & Validation Rules
- [ ] Integration validation checklist completed.
- [ ] Code conventions and naming rules followed.
- [ ] Strict type safety constraints verified.
- [ ] Security standards checked.

## Outputs
1. System integration pattern definitions.
2. Code templates and examples.
3. Test validation checklists.
