---
name: mcporter
description: List, auth, and call MCP servers/tools from the terminal.
version: 1.0.0
author: community
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [MCP, Tools, API, Integrations, Interop]
    homepage: https://mcporter.dev
prerequisites:
  commands: [npx]
---

# mcporter

使用 `mcporter` 即可在终端中直接发现、调用和管理 [MCP（模型上下文协议）](https://modelcontextprotocol.io/) 服务器及工具。

## 先决条件

需要安装 Node.js：
```bash
# No install needed (runs via npx)
npx mcporter list

# Or install globally
npm install -g mcporter
```

## 快速入门

```bash
# List MCP servers already configured on this machine
mcporter list

# List tools for a specific server with schema details
mcporter list <server> --schema

# Call a tool
mcporter call <server.tool> key=value
```

## 发现 MCP 服务器

mcporter 能自动检测本地机器上其他 MCP 客户端（如 Claude Desktop、Cursor 等）所配置的服务器。若想找到新的可用服务器，可浏览 [mcpfinder.dev](https://mcpfinder.dev) 或 [mcp.so](https://mcp.so) 等注册表，随后进行临时连接：

```bash
# Connect to any MCP server by URL (no config needed)
mcporter list --http-url https://some-mcp-server.com --name my_server

# Or run a stdio server on the fly
mcporter list --stdio "npx -y @modelcontextprotocol/server-filesystem" --name fs
```

## 调用工具

```bash
# Key=value syntax
mcporter call linear.list_issues team=ENG limit:5

# Function syntax
mcporter call "linear.create_issue(title: \"Bug fix needed\")"

# Ad-hoc HTTP server (no config needed)
mcporter call https://api.example.com/mcp.fetch url=https://example.com

# Ad-hoc stdio server
mcporter call --stdio "bun run ./server.ts" scrape url=https://example.com

# JSON payload
mcporter call <server.tool> --args '{"limit": 5}'

# Machine-readable output (recommended for Hermes)
mcporter call <server.tool> key=value --output json
```

## 认证与配置

```bash
# OAuth login for a server
mcporter auth <server | url> [--reset]

# Manage config
mcporter config list
mcporter config get <key>
mcporter config add <server>
mcporter config remove <server>
mcporter config import <path>
```

配置文件位置：`./config/mcporter.json`（可通过 `--config` 参数进行覆盖）。

## 守护进程

用于保持服务器连接的持久化连接：
```bash
mcporter daemon start
mcporter daemon status
mcporter daemon stop
mcporter daemon restart
```

## 代码生成

```bash
# Generate a CLI wrapper for an MCP server
mcporter generate-cli --server <name>
mcporter generate-cli --command <url>

# Inspect a generated CLI
mcporter inspect-cli <path> [--json]

# Generate TypeScript types/client
mcporter emit-ts <server> --mode client
mcporter emit-ts <server> --mode types
```

## 备注

- 若需结构化输出以便于解析，请使用 `--output json` 选项。
- 临时服务器（HTTP 地址或 `--stdio` 命令）无需任何配置即可使用，非常适合一次性调用场景。
- OAuth 认证可能需要通过浏览器进行交互式验证——如有需要，可使用 `terminal(command="mcporter auth <server>", pty=true)` 命令。
