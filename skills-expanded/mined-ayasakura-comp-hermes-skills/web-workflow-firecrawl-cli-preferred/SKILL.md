---
name: web-workflow_firecrawl_cli_preferred
description: Prioritizes Firecrawl CLI via npx, falling back to Python SDK.
---

# Firecrawl CLI Preferred

Use this skill when you need to scrape, crawl, or map URLs using Firecrawl. This skill prioritizes using the `firecrawl-cli` via `npx` and falls back to the Python SDK if the CLI is unavailable or fails.

## Prerequisites

- `FIRECRAWL_API_KEY` should be set in your environment or `.env` file.
- `npx` must be available (it is available on this system).

## Workflow

1. **Identify Task**: Determine if the user wants to `scrape`, `crawl`, `map`, or `search`.
2. **Attempt CLI Execution**:
   - Construct the `npx firecrawl-cli <command> [options] <url>` command.
   - Use `terminal()` to execute the command.
   - If successful, parse and return the results.
3. **Fallback to SDK**:
   - If the CLI command returns an error or the command is not found, attempt to use the Firecrawl Python SDK via `execute_code()`.
   - This requires `firecrawl-py` to be installed in the active environment.
4. **Error Handling**:
   - If both methods fail, report the error clearly to the user, specifically noting if it's an authentication issue.

## Commands Supported

- `scrape`: Scrape one or more URLs. Use `--only-main-content` for clean markdown.
- `crawl`: Crawl a website.
- `map`: Map URLs on a website.
- `search`: Search the web using Firecrawl.

## Pitfalls

- **Authentication**: If `FIRECRAWL_API_KEY` is missing, the CLI will fail. Always check for the key in `.env` first.
- **Output Size**: Large crawls or scrapes can produce massive outputs. For large datasets, consider instructing the use to save to a file.
- **Rate Limits**: Firecrawl is subject to API rate limits. Monitor for 429 errors.
