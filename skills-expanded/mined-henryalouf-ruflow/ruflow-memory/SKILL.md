# Ruflow Memory System

Persistent vector database memory for cross-session context. Uses sql.js (WASM SQLite) for cross-platform operation.

## Database Location

- **Project DB**: `data/memory/ruflow.db`
- **AgentDB**: `C:\Users\Qadri Laptop\.claude\projects\D--Personal-Smarter-revolution-Ruflow\memory\agentdb.sqlite`

## Quick Reference

### Initialize Database
```bash
node .claude/helpers/memory-init.cjs
```

### Check Status
```bash
node scripts/memory-status.js
```

### Query Memory (CLI)
```bash
# Show database stats
node .claude/helpers/memory-query.cjs stats

# List recent sessions
node .claude/helpers/memory-query.cjs sessions 5

# Search learnings by keyword
node .claude/helpers/memory-query.cjs search-learnings "authentication"

# Search past errors
node .claude/helpers/memory-query.cjs search-errors "ENOENT"

# Show skill usage statistics
node .claude/helpers/memory-query.cjs skills

# Get knowledge by category
node .claude/helpers/memory-query.cjs knowledge "file_edits"
```

### Search Existing AgentDB
```bash
node scripts/memory-db/search.js "pizza website"
node scripts/memory-db/search.js --type session "authentication"
node scripts/memory-db/search.js --recent 7 "memory system"
```

## Programmatic Usage

### Store a Session
```javascript
const mq = require('./.claude/helpers/memory-query.cjs');

await mq.storeSession({ id: 'session-123', summary: 'Built auth module', model: 'opus' });
await mq.endSession('session-123', 'Completed OAuth integration');
```

### Store a Task
```javascript
const taskId = await mq.storeTask({
  session_id: 'session-123',
  description: 'Implement login endpoint',
  skills_used: ['api-design', 'auth-implementation'],
  files_modified: ['src/auth/login.ts', 'tests/auth.test.ts'],
});
await mq.completeTask(taskId, 'Login endpoint working with JWT tokens');
```

### Store a Learning
```javascript
await mq.storeLearning({
  session_id: 'session-123',
  category: 'architecture',
  content: 'Use middleware pattern for auth instead of decorators - better testability',
  importance: 'high',
  tags: ['auth', 'patterns', 'testing'],
});
```

### Store an Error and Fix
```javascript
await mq.storeError({
  session_id: 'session-123',
  error_type: 'build_error',
  error_message: 'Cannot find module sql.js',
  fix_applied: 'Run npm install in scripts/memory-db/',
  file_path: 'scripts/memory-db/lib.js',
});
```

### Search Past Knowledge
```javascript
const learnings = await mq.searchLearnings('authentication');
const errors = await mq.searchErrors('ENOENT');
const knowledge = await mq.searchKnowledge('middleware');
```

### Store and Retrieve Knowledge
```javascript
await mq.storeKnowledge({
  category: 'project_config',
  key: 'auth_provider',
  value: 'JWT with refresh tokens',
  metadata: { decided_on: '2026-04-07' },
});

const config = await mq.getKnowledge('project_config', 'auth_provider');
```

### Track Skill Usage
```javascript
await mq.trackSkillUsage({
  skill_name: 'sparc-methodology',
  session_id: 'session-123',
  success: true,
  context: 'Used for API design phase',
});

const skillStats = await mq.getSkillStats();
```

### Session Hooks
```javascript
const hooks = require('./.claude/helpers/memory-session-hook.cjs');

// Start a session (loads recent context)
const ctx = await hooks.onSessionStart({ id: 'session-123', model: 'opus' });

// Record a completed task
await hooks.onPostTask({ description: 'Built login page', skills_used: ['react-patterns'] });

// Record a learning
await hooks.onLearning({ category: 'performance', content: 'Lazy load auth module', importance: 'high' });

// Record an error and its fix
await hooks.onError({ error_type: 'runtime', error_message: 'Token expired', fix_applied: 'Added refresh logic' });

// End the session
await hooks.onSessionEnd({ summary: 'Auth system complete' });
```

## Database Schema

| Table | Purpose |
|-------|---------|
| `sessions` | Session records with timestamps, model, branch |
| `conversations` | Conversation entries per session |
| `tasks` | Task descriptions, status, skills/agents/files |
| `skills_used` | Skill usage tracking with success rates |
| `learnings` | Decisions, patterns, insights with importance levels |
| `errors` | Errors encountered and fixes applied |
| `embeddings` | Vector embeddings for semantic search |
| `knowledge` | Key-value knowledge base by category |
| `search_chunks` | Full-text search index |

## Architecture

- **sql.js (WASM)**: Cross-platform SQLite, no native compilation needed
- **Location**: `scripts/memory-db/node_modules/sql.js/`
- **TF-IDF Search**: Built-in term-frequency search in `scripts/memory-db/lib.js`
- **Dual DB**: Project-local `ruflow.db` + Claude auto-memory `agentdb.sqlite`