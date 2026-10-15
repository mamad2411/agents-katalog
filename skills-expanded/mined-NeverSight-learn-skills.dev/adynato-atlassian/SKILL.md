---
name: adynato-atlassian
description: Work with Jira, Confluence, and Atlassian Cloud links via Atlassian MCP instead of browser automation. Covers reading `atlassian.net` URLs, preferring MCP over Puppeteer for tickets and pages, summarizing issue state and comments, and falling back only when visual inspection is explicitly needed or MCP is unavailable. Use when a prompt includes Jira tickets, Confluence pages, or Atlassian links.
---

# Atlassian Skill

Use this skill when a prompt includes Jira tickets, Confluence pages, or `atlassian.net` links.

## Prefer Atlassian MCP for Atlassian Links

- If the user provides an `atlassian.net` link, use Atlassian MCP to read it first
- Do not default to Puppeteer or browser automation just to inspect Jira or Confluence content
- Prefer MCP because it returns structured, authenticated Atlassian data instead of brittle rendered UI
- Use browser automation only if the user explicitly asks for a visual/UI check or Atlassian MCP is genuinely unavailable after confirming setup

## Ticket Handling Workflow

When reading a Jira issue through Atlassian MCP, capture the parts the next decision depends on:

- Issue key and summary
- Status, assignee, priority, and type
- Description, acceptance criteria, reproduction notes, or implementation details
- Recent comments, blockers, and open questions
- Linked issues, related pages, or dependent work when relevant

Prefer MCP follow-up queries over manually clicking through browser pages.

## Confluence and Related Context

- Use Atlassian MCP for Confluence page content when a page link is provided
- Follow linked Jira or Confluence context through MCP when it matters to the task
- Avoid scraping rendered HTML when structured content is available from MCP

## If Atlassian MCP Is Not Set Up

- Prefer setting up Atlassian MCP in `.omp/mcp.json` rather than using the browser as the default workaround
- Follow the repo-local setup conventions in `adynato-omp-mcp`
- Do not act like browser automation is an equivalent replacement for authenticated MCP access

## Atlassian Rovo MCP Endpoint

Use the official endpoint for new setups:

```text
https://mcp.atlassian.com/v1/mcp
```

Prefer `/mcp` for new configurations; Atlassian is deprecating `/sse`.
