---
name: mcp-integration
description: Detects when a project could benefit from connecting to an MCP server and suggests it. Advisory only — never auto-installs. Recognizes common patterns (database, GitHub, file search, etc.) and maps them to known MCP servers.
invoke_when: Use when setting up a new project, connecting to an external service, or when project diagnosis finds an MCP integration opportunity.
---

# MCP Integration Awareness

## Purpose

MCP (Model Context Protocol) servers extend Claude Code's capabilities by connecting to external tools and services. Many projects would benefit from MCP connections but users don't know they exist. This skill detects opportunities and suggests them.

**This skill is ADVISORY ONLY.** Never auto-install or auto-configure MCP servers. Always suggest and let the user decide.

## Detection Patterns

### Database MCP Servers
**Detect when**: Project has database configuration, ORM setup, or SQL files
- `DATABASE_URL` in `.env` or `.env.example`
- Prisma schema (`prisma/schema.prisma`)
- SQLite files (`.db`, `.sqlite`)
- PostgreSQL/MySQL connection strings in config

**Suggest**: "Your project uses [database]. You could connect the [database] MCP server to let me query your database directly, inspect schemas, and run migrations. Want to set it up?"

### GitHub MCP Server
**Detect when**: Project is a git repo with a GitHub remote
- `.git/config` has a github.com remote

**Suggest**: "This project is on GitHub. The GitHub MCP server would let me create issues, review PRs, and manage releases directly. Want to connect it?"

### File Search MCP
**Detect when**: Large project (50+ source files)

**Suggest**: "This is a larger project. A file search MCP server could help me find relevant code faster. Want to set one up?"

### Monitoring/Observability MCP
**Detect when**: Project has production deployment indicators
- Kubernetes configs, Docker Compose, Vercel/Netlify config
- Sentry DSN in environment variables

**Suggest**: "Your project appears to have production infrastructure. Connecting a monitoring MCP would let me check logs and metrics directly when debugging."

## When to Surface

- **Session start**: If a strong signal is detected (database URL exists, GitHub remote exists), mention it once as a brief note
- **During work**: If the user is struggling with something an MCP would help with (e.g., manually describing database schema), suggest it in context
- **Never**: Don't repeat suggestions the user has declined. If they say no, respect it.

## How to Suggest

Keep suggestions brief and contextual:

> "Tip: I noticed you have a PostgreSQL database. If you connect the Postgres MCP server, I can query your schema directly instead of you describing it to me. Run `/mcp` to see available servers."

Do NOT:
- Block work to suggest MCP servers
- Suggest MCP servers for every project
- Auto-install anything
- Suggest more than one MCP server at a time
