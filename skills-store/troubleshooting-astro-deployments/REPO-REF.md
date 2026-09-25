# Repo Referensi: astronomer/agents

Repo: https://github.com/astronomer/agents
Ref lokal: /Users/chaali0324/.agents/repo-refs/astronomer_agents
API: curl "localhost:27126/repos/readme?name=astronomer_agents"
Dibuat: 2026-09-16

## Cuplikan README
# astronomer/agents

Source: https://github.com/astronomer/agents
Fetched: 2026-09-16

## README
# agents

AI agent tooling for data engineering workflows. Includes an [MCP server](./astro-airflow-mcp/) for Airflow, a [CLI tool (`af`)](./astro-airflow-mcp/README.md#airflow-cli-tool) for interacting with Airflow from your terminal, and [skills](#skills) that extend AI coding agents with specialized capabilities for working with Airflow and data warehouses. Works with [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Cursor](https://cursor.com), and other agentic coding tools.

Built by [Astronomer](https://www.astronomer.io/). [Apache 2.0 licensed](https://github.com/astronomer/agents/blob/main/LICENSE) and compatible with open-source Apache Airflow.

## Table of Contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Installation](#installation)
  - [Quick Start](#quick-start)
  - [Compatibility](#compatibility)
  - [Claude Code](#claude-code)
  - [Cursor](#cursor)
  - [Other MCP Clients](#other-mcp-clients)
- [Features](#features)
  - [MCP Server](#mcp-server)
  - [Skills](#skills)
- [Why Astro?](#why-astro)
  - [User Journeys](#user-journeys)
  - [Airflow CLI (`af`)](#airflow-cli-af)
- [Configuration](#configuration)
  - [Warehouse Connections](#warehouse-connections)
  - [Airflow](#airflow)
- [Usage](#usage)
  - [Getting Started](#getting-started)
- [Development](#development)
  - [Local Development Setup](#local-development-setup)
  - [Adding Skills](#adding-skills)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [License](#license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Installation

### Quick Start

```bash
npx skills add astronomer/agents --skill '*'
```

This installs all Astronomer skills into your project via [skills.sh](https://skills.sh). You'll be prompted to select which agents to install to. To also select skills individually, omit the `--skill` flag.

> [!IMPORTANT]
> **Claude Code users:** We recommend using the plugin instead (see [Claude Code](#claude-code) section below) for better integration with MCP servers and hooks.

### Compatibility

**Skills:** Works with [25+ AI coding agents](https://github.com/vercel-labs/add-skill?tab=readme-ov-file#available-agents) including Claude Code, Cursor, 
