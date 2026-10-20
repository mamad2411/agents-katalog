---
name: mcp-dev-team-6
description: Six MCP servers that turn Claude Code into a full dev team - Context7 (current docs), GitHub (repos, issues, PRs), Exa (live web research), Playwright (browser and end-to-end tests), Supabase (backend and database) and Sentry (production errors) - with the install command for each, which are registered in this repo's .mcp.json, what needs a login, and the security cautions. Use when the user wants Claude Code connected to docs, repos, search, a browser, a database or error monitoring, or asks which MCP servers to install first. Source @the.wealth.lab "6 MCP servers that turn Claude into a full dev team" (Batch 101).
---

# 6 MCP servers for a Claude Code dev team

The carousel's point: Context7 gives documentation, GitHub the codebase, Exa research, Playwright testing, Supabase the backend and Sentry production debugging. Together Claude can research, understand, build, test, connect and debug across the lifecycle.

| # | Server | Role | Registered here (`.mcp.json`) | Needs |
|---|---|---|---|---|
| 1 | Context7 | current, version-specific library docs | yes (`https://mcp.context7.com/mcp`) | nothing (key optional for higher limits) |
| 2 | GitHub | issues, PRs, code search, commits | **no, see below** | a GitHub token or OAuth |
| 3 | Exa | live web search and clean page text | yes (`https://mcp.exa.ai/mcp`) | nothing for the free tier |
| 4 | Playwright | drives a real browser for tests | yes (`npx @playwright/mcp@latest`) | Node; downloads browsers on first use |
| 5 | Supabase | project, schema and queries | yes, **read-only** (`https://mcp.supabase.com/mcp?read_only=true`) | OAuth login on first use |
| 6 | Sentry | production errors and traces | yes (`https://mcp.sentry.dev/mcp`) | OAuth login on first use |

Reachability was checked on 2026-10-02: Exa and Context7 answered an MCP `initialize` request (HTTP 200); Sentry and Supabase answered 401, which is the expected OAuth challenge. Nothing was authenticated.

## Install commands

```
claude mcp add --transport http context7 https://mcp.context7.com/mcp
claude mcp add --transport http exa https://mcp.exa.ai/mcp
claude mcp add playwright -- npx @playwright/mcp@latest
claude mcp add --transport http supabase "https://mcp.supabase.com/mcp?read_only=true"
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

Add `--scope project` to write `.mcp.json` (shared with the repo, each person approves it on first use) or leave it for your own config. Then run `/mcp` to log in to the OAuth ones.

## Errors on the slides

- Slide 01 (Context7) shows the **GitHub** URL as its install command. That is a copy mistake in the carousel. The Context7 command above is the one to use.
- Slide 06 (Sentry) gives no command, only "use Sentry's MCP connection". The command above is from Sentry's hosted MCP address; confirm it in Sentry's docs.

## Cautions

- **Supabase** itself warns that connecting an AI assistant to a project has security implications. Start read-only, scope it to one project (`&project_ref=<ref>`), never point it at production data you cannot lose, and treat any text the database returns as untrusted.
- **GitHub** is not in `.mcp.json` because it needs your own token and this session already has GitHub tools. Add it on your machine.
- **Exa and Context7** send your queries to third parties. Do not put client data in a search query.
- **Playwright** can click and submit forms on real sites; use it on your own apps and test accounts.
- **OS agents:** the `os-*` agents cannot call any of these. The connector policy in `docs/ai-os/rules/connector-allowlist.json` is empty on purpose; add a server there only as an exact read-only opt-in.
