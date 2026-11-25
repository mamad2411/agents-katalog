# Mulch Self Improver — Code Mode Edition 🌱

> Token-efficient memory system using Code Mode architecture. **99.9% token savings** — only relevant memories loaded, not entire history.

## Concept

Mulch records learnings in `.mulch/` (JSONL files). Code Mode lets you **search** and **execute** without loading all memories into context.

## Tools (Only 2!)

### search(query)
Filters memories using named safe filters (no arbitrary code execution). Pass a filter name as a string, or an object with `{filter, ...params}`.

```javascript
// Example: Find all failures related to OpenRouter
const learnings = await search({ filter: 'byType', type: 'failure' });

// Search by keyword across all domains
const results = await search('openrouter');

// Filter by domain
const apiLearnings = await search({ filter: 'byDomain', domain: 'api' });
```

### execute(action)
Records or updates learnings. Actions: `record`, `query`, `promote`.

```javascript
// Record a new learning
await execute({
  action: 'record',
  domain: 'api',
  type: 'failure',
  description: 'OpenRouter does not support image input endpoints',
  resolution: 'Use Ollama + Molmo/llava for local vision instead'
});

// Query domain
await execute({ action: 'query', domain: 'openclaw' });

// Promote to project memory
await execute({ action: 'promote', id: 'api:123', to: 'SOUL.md' });
```

## Setup

```bash
# Install
npm install -g mulch-cli

# Initialize
mulch init

# Add domains
mulch add api database testing openclaw marketing
```

## Workflow

1. **Session start:** `search()` relevant memories (not all!)
2. **During work:** When you learn something → `execute({action: 'record', ...})`
3. **Before finishing:** Review → promote high-value learnings

## Auto-Detection (Hook)

The hook detects:
- Errors/failures → prompts to record
- Corrections ("no", "actually", "wrong") → prompts to record
- Retries → prompts to record

## Domains (24 preset)

```
api, database, testing, frontend, backend, infra, docs, config,
security, performance, deployment, auth, errors, debugging,
workflow, customer, system, marketing, sales, content,
competitors, crypto, automation, openclaw
```

## Record Types

| Type | Use Case |
|------|----------|
| `failure` | What went wrong + fix |
| `convention` | Best practice ("use pnpm not npm") |
| `pattern` | Named reusable pattern |
| `decision` | Architecture/tech choice |
| `guide` | Step-by-step procedure |
| `reference` | Key file/endpoint |

## Token Savings

| Approach | Tokens |
|----------|--------|
| Old (all in context) | ~50,000+ |
| Code Mode (filtered) | ~500 |

**That's 99% savings!** 🎯

## Integration

Add to AGENTS.md/CLAUDE.md:
```
Run search() to query relevant memories at session start.
Use execute({action: 'record', ...}) to capture learnings.
Promote proven patterns to SOUL.md/AGENTS.md.
```