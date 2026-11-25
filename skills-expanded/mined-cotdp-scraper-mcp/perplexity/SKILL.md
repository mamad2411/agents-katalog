---
name: perplexity
description: AI-powered web search and reasoning using Perplexity API through the scraper MCP server. Invoked when searching the web with AI synthesis, conducting research with citations, performing complex reasoning tasks, or answering questions requiring real-time information. Provides two tools for different query types.
---

# Perplexity AI Skill

AI-powered web search and reasoning capabilities via the scraper MCP server.

## When to Use This Skill

- Searching the web with AI-synthesized answers
- Research tasks requiring multiple sources with citations
- Complex reasoning and multi-step analysis
- Questions about current events or real-time information
- Comparing options or analyzing trade-offs

## Available Tools

| Tool | Model | Best For |
|------|-------|----------|
| `mcp__scraper__perplexity` | sonar | General queries, quick searches, factual lookups |
| `mcp__scraper__perplexity_reason` | sonar-reasoning-pro | Complex analysis, comparisons, multi-step reasoning |

## Tool Usage

### 1. General Web Search

For straightforward queries and information lookup:

```
mcp__scraper__perplexity(
    messages=[
        {"role": "user", "content": "What are the latest features in Next.js 15?"}
    ],
    model="sonar",
    temperature=0.3,
    max_tokens=4000
)
```

**Response includes:**
- `content`: AI-synthesized answer with citation markers [1], [2], etc.
- `citations`: Array of source URLs
- `model`: Model used
- `usage`: Token statistics

### 2. Complex Reasoning

For analytical queries requiring deep thinking:

```
mcp__scraper__perplexity_reason(
    query="Compare React Server Components vs traditional SSR approaches. Consider performance, developer experience, and migration complexity.",
    temperature=0.3,
    max_tokens=4000
)
```

**Use cases:**
- Technology comparisons
- Architecture decisions
- Trade-off analysis
- Multi-factor evaluations

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `messages` | array | required | Conversation history (perplexity only) |
| `query` | string | required | Question to reason about (perplexity_reason only) |
| `model` | string | "sonar" | "sonar" or "sonar-pro" |
| `temperature` | number | 0.3 | Creativity 0-2 (lower = more focused) |
| `max_tokens` | integer | 4000 | Maximum response length |

## Conversation Format

The `perplexity` tool accepts conversation history:

```
mcp__scraper__perplexity(
    messages=[
        {"role": "system", "content": "You are a technical advisor."},
        {"role": "user", "content": "What database should I use for a real-time chat app?"},
        {"role": "assistant", "content": "For real-time chat, consider..."},
        {"role": "user", "content": "How does Redis compare to PostgreSQL for this use case?"}
    ]
)
```

## Example Use Cases

### Technology Research

```
mcp__scraper__perplexity(
    messages=[
        {"role": "user", "content": "What are the best practices for implementing authentication in Next.js 15 App Router?"}
    ]
)
```

### Current Events

```
mcp__scraper__perplexity(
    messages=[
        {"role": "user", "content": "What are the latest AI model releases in 2025?"}
    ]
)
```

### Product Comparison

```
mcp__scraper__perplexity_reason(
    query="Compare Vercel, Netlify, and AWS Amplify for deploying Next.js applications. Consider pricing, features, performance, and developer experience."
)
```

### Architecture Decisions

```
mcp__scraper__perplexity_reason(
    query="Should I use a monorepo or polyrepo structure for a microservices architecture? Consider team size of 15 developers, 8 services, and CI/CD complexity."
)
```

### Code Pattern Research

```
mcp__scraper__perplexity(
    messages=[
        {"role": "user", "content": "What is the recommended way to handle form validation in React 19 with server actions?"}
    ]
)
```

### Security Research

```
mcp__scraper__perplexity_reason(
    query="Analyze the security implications of storing JWT tokens in localStorage vs httpOnly cookies. Consider XSS, CSRF, and token refresh patterns."
)
```

## Best Practices

### Choose the Right Tool

- **perplexity**: Factual queries, lookups, simple questions
- **perplexity_reason**: Comparisons, trade-offs, complex analysis

### Temperature Settings

```
# Factual accuracy (recommended for most queries)
temperature=0.3

# More creative/exploratory responses
temperature=0.7

# Maximum creativity (use sparingly)
temperature=1.0
```

### Working with Citations

Responses include numbered citations [1], [2], etc. matching URLs in the `citations` array:

```json
{
    "content": "Next.js 15 introduces several features [1] including improved caching [2]...",
    "citations": [
        "https://nextjs.org/blog/next-15",
        "https://nextjs.org/docs/caching"
    ]
}
```

### Iterative Research

Build on previous answers:

```
# Initial query
mcp__scraper__perplexity(messages=[
    {"role": "user", "content": "What is Zustand?"}
])

# Follow-up with context
mcp__scraper__perplexity(messages=[
    {"role": "user", "content": "What is Zustand?"},
    {"role": "assistant", "content": "Zustand is a state management library..."},
    {"role": "user", "content": "How does it compare to Redux Toolkit for a medium-sized application?"}
])
```

## Requirements

The Perplexity tools require `PERPLEXITY_API_KEY` environment variable to be set on the scraper MCP server. Without it, these tools will not be available.
