# docs-search

Search indexed documentation for relevant information.

## When to Use

Use this skill when the user asks about:
- How to use a specific library, framework, or API
- Documentation for a package or tool
- Best practices from official docs
- Code examples from documentation

## How to Use

1. First check if the worker is running by making a health check
2. Use the retrieve endpoint to search for relevant documentation
3. Present the results with source URLs

## API Endpoints

**Base URL**: `http://127.0.0.1:7432`

### Search Documentation

```bash
curl -X POST http://127.0.0.1:7432/retrieve \
  -H "Content-Type: application/json" \
  -d '{"query": "your search query", "topK": 5}'
```

### Index New Documentation

```bash
curl -X POST http://127.0.0.1:7432/index \
  -H "Content-Type: application/json" \
  -d '{"baseUrl": "https://docs.example.com", "seedSlug": "/getting-started"}'
```

### Check Status

```bash
curl http://127.0.0.1:7432/status
```

## Example Queries

- "How do I use server components in Next.js?"
- "What are the best practices for React hooks?"
- "How to configure TypeScript paths?"

## Response Format

Results include:
- `title`: Page title
- `heading`: Section heading (if available)
- `content`: Relevant text snippet
- `url`: Source documentation URL
- `score`: Relevance score (0-1)
