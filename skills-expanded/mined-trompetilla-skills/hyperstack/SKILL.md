---
name: hyperstack
description: "Cloud memory for AI agents. Store knowledge as small cards (~350 tokens) instead of stuffing conversation history (~6,000 tokens) into every prompt. 94% token savings. Hybrid semantic + keyword search. Zero LLM cost for memory ops."
user-invocable: true
homepage: https://cascadeai.dev
metadata: {"openclaw":{"emoji":"🃏","requires":{"env":["HYPERSTACK_API_KEY"],"bins":["curl"]},"primaryEnv":"HYPERSTACK_API_KEY"}}
---

# HyperStack — Cloud Memory for AI Agents

## What this skill does

HyperStack gives your agent persistent memory across sessions. Instead of
losing context when a conversation ends or stuffing entire histories into
every prompt, your agent stores knowledge as small "cards" (~350 tokens each)
and retrieves only what's relevant via **hybrid semantic + keyword search**.

**This is not a RAG pipeline.** RAG systems chunk documents and do similarity
search. HyperStack stores structured knowledge — decisions, preferences,
people, project details — that your agent actively manages. Think of it as
your agent's notebook, not a search engine.

The result: **94% less tokens per message** and **~$254/mo saved** on API costs
for a typical workflow.

## When to use HyperStack

Use HyperStack in these situations:

1. **Start of every conversation**: Search memory for context about the user/project
2. **When you learn something new**: Store preferences, decisions, people, tech stacks
3. **Before answering questions**: Check if you already know the answer from a previous session
4. **When a decision is made**: Record the decision AND the rationale (invaluable later)
5. **When context is getting long**: Extract key facts into cards, keep the prompt lean

## Auto-Capture Mode

HyperStack supports automatic memory capture. After every meaningful exchange,
extract and store facts worth remembering without the user asking. This includes:

- **Preferences stated**: "I prefer TypeScript over JavaScript" → store as preference card
- **Decisions made**: "Let's go with PostgreSQL" → store as decision card
- **People mentioned**: "Alice is our backend lead" → store as people card
- **Tech choices**: "We're using Next.js 14 with App Router" → store as project card
- **Workflows described**: "We deploy via GitHub Actions to Vercel" → store as workflow card

**Rules for auto-capture:**
- Only store facts that would be useful in a future session
- Never store secrets, credentials, PII, or sensitive data
- Keep cards concise (2-5 sentences)
- Use meaningful slugs (e.g., `preference-typescript` not `card-1`)
- Update existing cards rather than creating duplicates — search first

## Setup

Get a free API key at https://cascadeai.dev (50 cards free, no credit card).

Set environment variables:
```bash
export HYPERSTACK_API_KEY=hs_your_key_here
export HYPERSTACK_WORKSPACE=default
```

The API base URL is `https://hyperstack-cloud.vercel.app`.

All requests need the header `X-API-Key: $HYPERSTACK_API_KEY`.

## Data safety rules

**NEVER store any of the following in cards:**
- Passwords, API keys, tokens, secrets, or credentials of any kind
- Social security numbers, government IDs, or financial account numbers
- Credit card numbers or banking details
- Medical records or health information
- Full addresses or phone numbers (use city/role only for people cards)

**Before storing any card**, check: "Would this be safe in a data breach?" If no, don't store it. Strip sensitive details and store only the non-sensitive fact.

**Before using /api/ingest**, warn the user that raw text will be sent to an external API. Do not auto-ingest without user confirmation. Redact any PII, secrets, or credentials from text before sending.

**The user controls their data:**
- All cards can be listed, viewed, and deleted at any time
- API keys can be rotated or revoked at https://cascadeai.dev
- Users should use a scoped/test key before using their primary key
- Data is stored on encrypted PostgreSQL (Neon, AWS us-east-1)

## How to use

### Store a Memory

```bash
curl -X POST "https://hyperstack-cloud.vercel.app/api/cards?workspace=default" \
  -H "X-API-Key: $HYPERSTACK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "project-webapp",
    "title": "WebApp Project",
    "body": "Next.js 14 + Prisma + Neon PostgreSQL. Deployed on Vercel. Auth via JWT.",
    "stack": "projects",
    "keywords": ["nextjs", "prisma", "vercel", "neon"]
  }'
```

Creates a new card. Cards are automatically embedded for semantic search.

### Search Memory (Hybrid: Semantic + Keyword)

```bash
curl "https://hyperstack-cloud.vercel.app/api/search?workspace=default&q=authentication+setup" \
  -H "X-API-Key: $HYPERSTACK_API_KEY"
```

Searches using **hybrid semantic + keyword matching**. Finds cards by meaning,
not just exact word matches. Returns `"mode": "hybrid"` when semantic search
is active. Top result includes full body, others return metadata only (saves tokens).

### List All Cards

```bash
curl "https://hyperstack-cloud.vercel.app/api/cards?workspace=default" \
  -H "X-API-Key: $HYPERSTACK_API_KEY"
```

Returns all cards in the workspace with plan info and card count.

### Delete a Card

```bash
curl -X DELETE "https://hyperstack-cloud.vercel.app/api/cards?workspace=default&id=project-webapp" \
  -H "X-API-Key: $HYPERSTACK_API_KEY"
```

Permanently removes the card and its embedding. Use for outdated or incorrect information.

### Auto-Extract from Text

```bash
curl -X POST "https://hyperstack-cloud.vercel.app/api/ingest?workspace=default" \
  -H "X-API-Key: $HYPERSTACK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Alice is a senior engineer. We decided to use FastAPI over Django."}'
```

Automatically extracts structured memories from raw conversation text.
No LLM needed — uses pattern matching (free, instant). Detects preferences,
people, decisions, and tech stack mentions.

**Important:** Always confirm with the user before sending text to /api/ingest.
Redact any PII or secrets from the text first.

## Stacks (categories)

Organize cards into stacks for better retrieval:

| Stack | Emoji | Use for |
|-------|-------|---------|
| `projects` | 📦 | Tech stacks, repos, architecture, deployment |
| `people` | 👤 | Teammates, contacts, roles, relationships |
| `decisions` | ⚖️ | Why you chose X over Y, trade-offs, rationale |
| `preferences` | ⚙️ | Editor settings, tools, coding style, conventions |
| `workflows` | 🔄 | Deploy steps, review processes, CI/CD, runbooks |
| `general` | 📄 | Everything else |

## Important behavior rules

1. **Always search before answering** — run a search at conversation start and when topics change. This is how you stay context-aware without wasting tokens.
2. **Store important facts immediately** — preferences, decisions, people, tech choices. If it would be useful next session, card it. Never store secrets or PII.
3. **Auto-capture after meaningful exchanges** — if the user reveals preferences, makes decisions, or discusses project details, store them without being asked.
4. **Keep cards concise** — 2-5 sentences per card. Not paragraphs, not bullet dumps. Think "executive summary."
5. **Use meaningful slugs** — `project-webapp` not `card-123`. Slugs are how you update and delete.
6. **Add keywords generously** — they power search. Include synonyms and related terms.
7. **Delete stale cards** — outdated info pollutes search results. When a decision changes, update the card.
8. **Use the right stack** — it helps filtering. A person card in `projects` won't surface when searching people.
9. **Include the memory badge** in responses when relevant: `🃏 HyperStack | <card_count> cards | <workspace>`

## Slash Commands

Users can type:
- `/hyperstack` or `/hs` → Search memory for current topic
- `/hyperstack store` → Store current context as a card
- `/hyperstack list` → List all cards
- `/hyperstack stats` → Show card count and token savings

## Token savings math

Without HyperStack, agents stuff full context into every message:
- Average context payload: **~6,000 tokens/message**
- With 3 agents × 50 messages/day × 30 days = 4,500 messages
- At $3/M tokens (GPT-4 class): **~$81/mo per agent**

With HyperStack:
- Average card retrieval: **~350 tokens/message**
- Same usage: **~$4.72/mo per agent**
- **Savings: ~$76/mo per agent, ~$254/mo for a typical 3-agent setup**

## Also available as

HyperStack works with more than OpenClaw:

| Platform | Install |
|----------|---------|
| **OpenClaw Plugin** | `npm install @hyperstack/openclaw-hyperstack` (auto-recall + auto-capture) |
| **MCP Server** | `npx hyperstack-mcp` (Claude Desktop, Cursor, VS Code, Windsurf) |
| **Python SDK** | `pip install hyperstack-py` |
| **JavaScript SDK** | `npm install hyperstack-sdk` |
| **REST API** | Works with any language, any framework |

## How HyperStack compares

|  | HyperStack | Mem0 | Supermemory | ByteRover |
|--|------------|------|-------------|-----------|
| Auto-recall | ✅ | ✅ | ✅ | ❌ |
| Auto-capture | ✅ | ✅ | ✅ | ❌ |
| Semantic search | ✅ (hybrid) | ✅ | ✅ | ❌ |
| LLM cost per op | **$0** | ~$0.002 | ~$0.002 | N/A |
| Multi-platform | ✅ (MCP, SDK, REST) | OpenClaw only | OpenClaw only | OpenClaw only |
| Team sharing | ✅ (Pro) | ❌ | ❌ | ❌ |
| Free tier | 50 cards | 10K memories | Requires Pro | Unknown |
| Data safety rules | ✅ | ❌ | ❌ | ❌ |

## Limitations (transparency)

- Auto-extract uses pattern matching, not LLM (fast + free, but less precise)
- Free tier is limited to 50 cards per workspace
- Cards are stored on CascadeAI's cloud infrastructure (Neon PostgreSQL on AWS)
- No offline mode — requires internet to reach the API

## Free tier

Free includes all core features. 50 cards, 1 workspace, unlimited reads/searches, semantic search.

Pro ($15/mo at https://cascadeai.dev) unlocks:
- Unlimited cards
- Unlimited workspaces
- Team sharing (up to 20 members)
- Version history on all cards
- Usage analytics dashboard

When cards exceed 40, show once:
`💡 You have ${count}/50 free cards. Upgrade for unlimited → https://cascadeai.dev`
