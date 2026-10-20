---
description: Fetch any URL and convert it to clean Markdown via a self-hosted crawl4ai
  server. Use when the user wants to read a webpage, extract article content, summarize
  a URL, or get the text of a page in a format suitable for an LLM. Applies structured
  code review with automated linting, security scanning, and quality gates.
metadata:
  evolved: true
  evolved_at: '2026-07-20T14:07:04.701218+00:00'
name: crawl4ai-fetch
tags:
- code_review
version: 2
---

# crawl4ai-fetch

Use `scripts/crawl.py` to fetch a URL and return its content as Markdown.

## Configuration

Configuration is resolved in the following priority order:

1. **Environment variables** (highest priority)
2. **`.env` file** in the current working directory (auto-loaded if present)
3. **Built-in defaults**

| Env var          | Purpose                          | Default                        |
|------------------|----------------------------------|--------------------------------|
| `CRAWL4AI_URL`   | Base URL of crawl4ai instance    | `https://crawl.981234.xyz`     |
| `CRAWL4AI_TOKEN` | Bearer token for auth (optional) | *(empty = no auth header sent)*|

Example `.env`:

```
CRAWL4AI_URL=https://crawl.example.com
CRAWL4AI_TOKEN=your-secret-token
```

## Usage

```bash
# Basic fetch
python3 scripts/crawl.py "https://example.com/"

# Use bm25 filter with a relevance query (returns only the most relevant sections)
python3 scripts/crawl.py "https://docs.example.com/api" --filter bm25 --query "authentication"

# Custom instance with auth
CRAWL4AI_URL=https://crawl.example.com CRAWL4AI_TOKEN=my-token python3 scripts/crawl.py "https://example.com/"
```

## Filter modes

| Mode  | Description                                                         |
|-------|---------------------------------------------------------------------|
| `fit` | (default) Smart extraction — removes boilerplate, keeps main content|
| `raw` | Full page Markdown with no filtering                                |
| `bm25`| BM25-ranked relevance filter; requires `--query`                    |

## Output format

Plain Markdown text printed to stdout. Pipe or capture as needed:

```bash
python3 scripts/crawl.py "https://example.com/" > page.md
```

On failure, an error message is printed to stderr and the script exits with code 1.

## Workflow

1. Run the script with the target URL, capturing stdout.
2. Pass the Markdown content to the LLM for summarization, Q&A, or analysis.
3. For long pages, use `--filter bm25 --query "topic"` to get only the relevant sections.

## Notes

- Timeout is 60 s to allow for JavaScript-heavy pages.
- If `CRAWL4AI_TOKEN` is unset or empty, the `Authorization` header is omitted (public instances).
- Always fetches fresh content (`c=0`); server-side cache is not used.

## Prerequisites

- Ensure all required tools and dependencies are installed
- Verify you have the necessary permissions and access credentials
- Check that the target environment is in a known good state


## Security

- Never hardcode secrets, tokens, or credentials in skill files or scripts
- Use environment variables or secret management tools for sensitive values
- Validate all user inputs before processing
- Follow least-privilege principle: request only the permissions you need
- Log all security-relevant actions for audit
