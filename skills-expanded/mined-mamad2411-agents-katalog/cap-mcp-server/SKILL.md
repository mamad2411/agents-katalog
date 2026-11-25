---
name: cap-mcp-server
description: >
  Use when setting up or using the official SAP MCP Server for CAP development,
  the SAP UI5 MCP Server, or the SAP Fiori Elements MCP Server with AI coding
  agents (Claude Code, OpenCode, GitHub Copilot, Cursor). Covers installation,
  configuration, available tools, and combining MCP servers with skills.
metadata:
  category: cap
  version: "1.0.0"
  keywords: [MCP, Model Context Protocol, CAP MCP server, search_model, search_docs, Claude Code, Copilot, MCP tools]
  related:
    cap-llm-plugin: AI capabilities that benefit from MCP context
    cds-modeling: MCP server provides live CDS model access
---

# CAP MCP Server — Setup & Usage

> **Primary reference**: https://cap.cloud.sap/docs
> **CAP MCP Server**: https://cap.cloud.sap/docs/tools/mcp-server
> **Release announcement**: SAP August 2025 release notes  
> **Community blog**: https://community.sap.com/t5/technology-blog-posts-by-sap/boost-your-cap-development-with-ai-introducing-the-mcp-server-for-cap/ba-p/14202849

## What the CAP MCP Server provides

The official SAP MCP Server for CAP gives AI agents **context-aware tools** that understand both CAP APIs and **your specific project**:

- `search_model` — fuzzy search for CDS entities, services, actions, and relationships in your compiled CSN model
- `search_docs` — semantic search through official CAP documentation for syntax, patterns, and best practices
- **Instant model discovery** — the agent can query your project's entities without reading files
- **Context-aware documentation** — finds relevant capire docs based on semantic similarity, not keywords

## Installation

```bash
# In your CAP project
npm install --save-dev @sap/cds-mcp
```

Or install globally:
```bash
npm install -g @sap/cds-mcp
```

## Configuration with Claude Code

`.claude/settings.json` (project-level):
```json
{
  "mcpServers": {
    "cap": {
      "command": "npx",
      "args": ["@sap/cds-mcp", "--project", "."],
      "env": {}
    }
  }
}
```

Or globally in `~/.claude/settings.json` for use across all CAP projects:
```json
{
  "mcpServers": {
    "cap": {
      "command": "npx",
      "args": ["@sap/cds-mcp"],
      "env": {}
    }
  }
}
```

## Configuration with OpenCode

`.opencode/config.json`:
```json
{
  "mcp": {
    "servers": {
      "cap": {
        "command": "npx @sap/cds-mcp --project ."
      }
    }
  }
}
```

## Configuration with GitHub Copilot (VS Code)

`.vscode/mcp.json`:
```json
{
  "servers": {
    "cap-mcp": {
      "command": "npx",
      "args": ["@sap/cds-mcp", "--project", "${workspaceFolder}"]
    }
  }
}
```

## SAP UI5 MCP Server

```json
{
  "mcpServers": {
    "ui5": {
      "command": "npx",
      "args": ["@sap/ui5-mcp-server"]
    }
  }
}
```

## SAP Fiori Elements MCP Server

```json
{
  "mcpServers": {
    "fiori": {
      "command": "npx",
      "args": ["@sap/fiori-mcp-server"]
    }
  }
}
```

## Combining MCP Servers + Skills (the power combo)

MCP Servers and Skills complement each other:

| | MCP Server | Skills |
|---|---|---|
| **What it does** | Queries your live project model & docs dynamically | Injects static best-practice instructions |
| **Best for** | "What entities does my project have?" | "How should I structure a service handler?" |
| **Updates** | On demand (live) | On commit (versioned) |

**Recommended setup**: use both together. The MCP server gives the agent project context; skills give it your team's conventions and best practices.

```
.claude/
  settings.json         ← MCP server config
  skills/               ← symlinks to SkillOverflow/
    cds-modeling/
    code-review/
    ...
```

## Using the CAP MCP Server in practice

Once configured, the agent can:

```
User: "Add a Books entity to the project"
Agent: [calls search_model to see existing entities]
       [calls search_docs for 'entity definition best practices']
       → Generates code respecting existing model and capire conventions
```

```
User: "Review my Orders service for performance issues"
Agent: [calls search_model to understand Orders entity structure]
       [uses code-review skill for the checklist]
       [calls search_docs for 'performance considerations']
       → Structured review grounded in your actual model
```

## SAP API policy for MCP Servers

As of May 2026 SAP API Policy FAQ v1.1, the three SAP-managed MCP servers (CAP, UI5, Fiori Elements) are **explicitly endorsed** for agentic AI access. No special licensing is required beyond your existing BTP agreement.

## Common mistakes to avoid

- ❌ Running `npx @sap/cds-mcp` without `--project .` — it won't find your CSN model
- ❌ Forgetting to run `cds build` before starting the MCP server — it reads from `gen/`
- ❌ Configuring MCP servers globally when you need project-specific paths
- ❌ Using MCP alone without skills — you get model awareness but no best-practice enforcement
- ❌ Not keeping `@sap/cds-mcp` updated — documentation search improves with each release
