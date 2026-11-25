---
name: hermes-atlas-ecosystem-map
description: Build and maintain the Hermes Atlas ecosystem map with quality filtering, RAG chatbot, and live GitHub star tracking
triggers:
  - add a new project to hermes atlas
  - update the hermes ecosystem map
  - rebuild the atlas knowledge base
  - test the hermes atlas rag pipeline
  - filter repos for hermes atlas
  - update github star counts for atlas
  - configure the atlas chatbot
  - review a project for hermes atlas inclusion
---

# Hermes Atlas Ecosystem Map

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## What is Hermes Atlas?

Hermes Atlas is a community-curated directory of the Hermes Agent ecosystem—mapping every tool, skill, integration, and deployment template built for [Hermes Agent](https://github.com/NousResearch/hermes-agent) by Nous Research. It features:

- **Quality-filtered repository catalog** (80+ projects across 12 categories)
- **Live GitHub star counts** with 30-day sparklines
- **RAG-powered chatbot** ("Ask the Atlas") grounded in 27 research files
- **Hybrid search/filter** with trending badges
- **Zero-framework frontend** (vanilla HTML/CSS/JS)
- **Serverless API** (Vercel functions + Redis cache)

## Installation

```bash
git clone https://github.com/ksimback/hermes-ecosystem.git
cd hermes-ecosystem
npm install
```

**Dependencies** (only 2):
- `openai` — for embeddings and OpenRouter API
- `redis` — for star count caching and history

## Key Files

```
hermes-ecosystem/
├── index.html                 # Main map UI (single-page app)
├── data/
│   ├── repos.json            # Single source of truth (84 repos)
│   └── chunks.json           # Pre-computed embeddings (283 chunks, 7MB)
├── api/
│   ├── stars.js              # Live star counts (1hr cache)
│   ├── stars-history.js      # 30-day sparkline data
│   └── chat.js               # RAG chatbot with streaming
├── scripts/
│   ├── build-chunks.js       # Rebuild embeddings from research/
│   └── test-rag.js           # RAG quality tests (27 test cases)
├── research/                  # 27 knowledge base files
└── lib/redis.js              # Shared Redis client
```

## Adding a New Project

### 1. Quality Filter Criteria

Before adding to `data/repos.json`, verify:

- **Built for Hermes Agent** (not generic AI tools)
- **Created after July 22, 2025** (Hermes Agent launch)
- **Shows genuine effort** (not personal pet projects)
- **Passes security review** (check for credential leaks, malicious code)

### 2. Add to repos.json

```json
{
  "categories": {
    "skills": [
      {
        "name": "hermes-skill-example",
        "url": "https://github.com/username/hermes-skill-example",
        "description": "Brief description of what the skill does",
        "tags": ["tag1", "tag2"]
      }
    ]
  }
}
```

**Available categories:**
- `skills` — Core agent skills
- `tools` — External tool integrations
- `plugins` — Hermes plugins
- `deployments` — Hosting/infrastructure templates
- `frameworks` — Multi-skill orchestration
- `integrations` — Third-party service connectors
- `forks` — Modified Hermes Agent versions
- `ui` — User interfaces and dashboards
- `data` — Datasets and evaluation tools
- `research` — Academic papers and experiments
- `templates` — Boilerplates and starters
- `misc` — Everything else

### 3. Verify the Change

```bash
# Check JSON syntax
node -e "require('./data/repos.json')"

# Preview locally
open index.html
```

## Rebuilding the Knowledge Base

After updating files in `research/`, rebuild embeddings:

```bash
# Set API key
export OPENROUTER_API_KEY=sk-or-v1-...

# Rebuild chunks.json (splits + embeds)
node scripts/build-chunks.js

# Test RAG quality
node scripts/test-rag.js
```

**build-chunks.js** does:
1. Reads all `.md` files in `research/`
2. Splits into 500-char chunks with 100-char overlap
3. Embeds each chunk using OpenAI `text-embedding-3-small`
4. Writes to `data/chunks.json` (static file, committed to repo)

**Output:**
```
Processing research/agent-architecture.md...
Processing research/hermes-skills.md...
...
✅ Built 283 chunks (7.2 MB)
```

## Testing the RAG Pipeline

```bash
export OPENROUTER_API_KEY=sk-or-v1-...
node scripts/test-rag.js
```

**Sample test:**
```javascript
// scripts/test-rag.js excerpt
const tests = [
  {
    query: "How do I create a custom Hermes skill?",
    expectedKeywords: ["skill.md", "yaml", "frontmatter", "triggers"]
  },
  {
    query: "What's the difference between a skill and a tool?",
    expectedKeywords: ["skill", "tool", "integration", "plugin"]
  }
];
```

**Output:**
```
Test 1/27: How do I create a custom Hermes skill?
✅ Found 4/4 keywords in context
...
27/27 passed (100%)
```

## API Endpoints

### GET /api/stars

Returns live star counts for all repos in `repos.json`.

**Caching:**
- **1hr TTL** in Redis
- Falls back to direct GitHub API if cache miss
- Rate limit: 5000/hr with `GITHUB_TOKEN`, 60/hr without

**Response:**
```json
{
  "username/repo": 142,
  "anotheruser/hermes-skill": 89
}
```

**Usage in frontend:**
```javascript
const response = await fetch('/api/stars');
const stars = await response.json();
document.querySelector('[data-repo="username/repo"]').textContent = stars['username/repo'];
```

### GET /api/stars-history?repos=user/repo1,user/repo2

Returns 30-day star count history for sparklines.

**Response:**
```json
{
  "user/repo1": [120, 122, 125, 128, 130, ...],
  "user/repo2": [45, 47, 49, 51, 53, ...]
}
```

### POST /api/chat

RAG chatbot endpoint with streaming support.

**Request:**
```json
{
  "message": "How do I deploy Hermes Agent?",
  "conversationHistory": [
    {"role": "user", "content": "What is Hermes Agent?"},
    {"role": "assistant", "content": "Hermes Agent is..."}
  ]
}
```

**Response** (streaming):
```
data: {"type":"context","chunks":[{"text":"...","file":"deployment.md"}]}
data: {"type":"token","content":"To deploy"}
data: {"type":"token","content":" Hermes Agent"}
data: {"type":"done"}
```

**Retrieval pipeline:**
1. **Conversation-aware rewrite** — expands query using chat history
2. **Hybrid search** — BM25 (keyword) + cosine similarity (semantic)
3. **MMR re-ranking** — maximal marginal relevance to reduce redundancy
4. **Top-K selection** — retrieves 5 most relevant chunks
5. **LLM generation** — Gemma 4 31B with fallback chain

## Configuration

### Environment Variables (Vercel)

```bash
# Required
OPENROUTER_API_KEY=sk-or-v1-...
REDIS_URL=redis://default:password@host:port

# Optional
GITHUB_TOKEN=ghp_...                              # Fine-grained PAT (public read-only)
OPENROUTER_MODEL=google/gemma-4-31b-it:free       # Primary LLM
OPENROUTER_FALLBACK_MODELS=google/gemma-4-26b-it:free,google/gemini-3-flash-1.5
```

### vercel.json Configuration

```json
{
  "functions": {
    "api/**/*.js": {
      "maxDuration": 30
    }
  },
  "crons": [
    {
      "path": "/api/stars-daily-snapshot",
      "schedule": "0 0 * * *"
    }
  ]
}
```

## Common Patterns

### Adding Multiple Projects at Once

```javascript
// scripts/batch-add.js (create this if needed)
const fs = require('fs');
const repos = require('../data/repos.json');

const newProjects = [
  { name: "hermes-skill-web-search", url: "https://github.com/...", category: "skills" },
  { name: "hermes-tool-calendar", url: "https://github.com/...", category: "tools" }
];

newProjects.forEach(proj => {
  repos.categories[proj.category].push({
    name: proj.name,
    url: proj.url,
    description: "",  // Fill in manually
    tags: []
  });
});

fs.writeFileSync('./data/repos.json', JSON.stringify(repos, null, 2));
```

### Security Review Checklist

```javascript
// scripts/security-check.js (conceptual)
const checks = [
  {
    name: "No hardcoded credentials",
    test: (code) => !/api[_-]?key\s*=\s*["'][^"']+["']/i.test(code)
  },
  {
    name: "No eval() usage",
    test: (code) => !/eval\(/.test(code)
  },
  {
    name: "Dependencies up to date",
    test: async (repo) => {
      // Check package.json for known vulnerable versions
    }
  }
];
```

### Custom Sparkline Rendering

```javascript
// From index.html (adapted for skill documentation)
function renderSparkline(history) {
  const max = Math.max(...history);
  const min = Math.min(...history);
  const range = max - min || 1;
  
  const points = history.map((val, i) => {
    const x = (i / (history.length - 1)) * 100;
    const y = 100 - ((val - min) / range) * 100;
    return `${x},${y}`;
  }).join(' ');
  
  return `<svg viewBox="0 0 100 100"><polyline points="${points}" /></svg>`;
}
```

## Troubleshooting

### Embeddings Build Fails

**Error:** `Error: 429 Too Many Requests`

**Fix:** Add rate limiting to build-chunks.js:
```javascript
async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

for (const chunk of chunks) {
  const embedding = await getEmbedding(chunk.text);
  chunk.embedding = embedding;
  await sleep(100); // 10 req/sec max
}
```

### Redis Connection Timeout

**Error:** `ECONNREFUSED` or `ETIMEDOUT`

**Fix:** Check `REDIS_URL` format:
```bash
# Correct format
redis://default:password@host.region.cloud.redislabs.com:12345

# Common mistake (missing default user)
redis://:password@host...
```

### Stars Not Updating

**Error:** Cached star counts stale after 1 hour

**Fix:** Manually bust cache:
```bash
# Via Redis CLI
redis-cli -u $REDIS_URL
> DEL stars:cache
```

Or programmatically:
```javascript
// api/stars.js — force refresh
if (req.query.refresh === 'true') {
  await redis.del('stars:cache');
}
```

### RAG Returns Irrelevant Results

**Symptom:** Chatbot answers unrelated to Hermes Agent

**Fix:** Check chunk quality:
```bash
node scripts/test-rag.js --verbose

# Review chunks.json for short/low-quality chunks
node -e "
const chunks = require('./data/chunks.json');
const short = chunks.filter(c => c.text.length < 200);
console.log('Short chunks:', short.length);
"
```

Increase chunk size in `build-chunks.js`:
```javascript
const CHUNK_SIZE = 800;  // was 500
const OVERLAP = 150;     // was 100
```

### GitHub Rate Limit Exceeded

**Error:** `403 rate limit exceeded`

**Fix:** Add `GITHUB_TOKEN` to Vercel env vars:
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. Create token with **Public repositories (read-only)** permission
3. Add to Vercel: `GITHUB_TOKEN=ghp_...`

This increases rate limit from 60/hr to 5000/hr.

## Local Development

```bash
# Open the map in a browser (API endpoints won't work locally)
open index.html

# Test API endpoints locally (requires env vars)
export OPENROUTER_API_KEY=...
export REDIS_URL=...
vercel dev
```

**Note:** The frontend is pure static HTML—no build step required. API endpoints only run on Vercel or with `vercel dev`.

## Deployment

```bash
# Deploy to Vercel
vercel --prod

# Set environment variables
vercel env add OPENROUTER_API_KEY
vercel env add REDIS_URL
vercel env add GITHUB_TOKEN
```

The daily cron job (`/api/stars-daily-snapshot`) automatically runs at midnight UTC to populate sparkline history.

---

**Live site:** [hermesatlas.com](https://hermesatlas.com)  
**Repository:** [github.com/ksimback/hermes-ecosystem](https://github.com/ksimback/hermes-ecosystem)
