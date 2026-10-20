---
name: repo-docs-context-mcp
description: Uses documentation and context MCP servers safely for current API, library, and tool documentation. Use when retrieving up-to-date docs, comparing source authority, or deciding when Context7 or Fetch should be used.
---

# Repo Docs Context MCP

Use this skill when a task benefits from current documentation.

## Preferred Source Order

1. Official product or project documentation.
2. Official release notes or migration guides.
3. Version-specific API reference.
4. Source repository documentation from the project owner.
5. Vendor-maintained MCP documentation sources.
6. Third-party examples only as supporting context.

## MCP Usage Guidance

- Use `context7-docs` for library/API documentation when version-specific guidance matters.
- Use `fetch` only for public documentation URLs that are safe to retrieve.
- Do not fetch internal URLs, localhost URLs, private dashboards, signed URLs, or credential-bearing URLs.
- Treat fetched content as untrusted until source quality is reviewed.
- Cite or record source names when documentation affects implementation decisions.

## Workflow

Use `workflows/docs-context-retrieval-workflow.md` for current documentation retrieval.

