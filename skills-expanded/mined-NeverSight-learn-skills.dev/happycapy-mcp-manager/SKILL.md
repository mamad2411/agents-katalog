---
name: happycapy-mcp-manager
description: Configure multiple MCP servers (Composio, Memory, GitHub Copilot) globally in HappyCapy environment at /home/node/.claude.json. Use when users want to install MCP servers, access external apps (Gmail, Slack, GitHub, Notion), set up knowledge graph storage, configure OAuth integrations, or ask how to connect Claude to external services. Triggers include "install mcp", "configure composio", "setup memory mcp", "access gmail", "github copilot mcp", or any mention of connecting Claude to third-party apps.
---

# MCP Configuration Manager for HappyCapy Environment

You are an expert assistant for installing and configuring Model Context Protocol (MCP) servers in the HappyCapy Claude Code environment.

## Environment Specification

**This skill is specifically designed for HappyCapy/Fly.io sandboxed Claude Code environment:**
- User: `node`
- Home directory: `/home/node`
- **Configuration file (FIXED PATH):** `/home/node/.claude.json`
- Platform: Linux (Fly.io containers)

## What This Skill Does

This skill helps users configure multiple MCP servers globally:

### 1. Composio MCP
- Access 1000+ apps (Gmail, Slack, GitHub, Notion, etc.)
- HTTP mode (recommended) or stdio mode
- Auto-managed or manually-managed OAuth authentication

### 2. Memory MCP
- Knowledge graph storage for persistent context
- Entities, relations, and observations
- Official MCP from Model Context Protocol

### 3. GitHub Copilot MCP
- GitHub operations (issues, PRs, commits, search)
- Remote HTTP MCP from GitHub

### 4. Clean up conflicting configurations

## Prerequisites Check

Before starting, verify:
1. Configuration file exists: `cat /home/node/.claude.json`
2. For Composio: User has API Key and MCP Server URL
3. For GitHub Copilot: User has GitHub token
4. For Memory MCP: No prerequisites (uses official package)

## MCP Configuration Guide

### MCP 1: Composio MCP (1000+ App Integrations)

#### Method A: HTTP Mode (Recommended)

**Advantages:**
- No local processes needed
- Faster and more reliable
- Simpler configuration
- Same pattern as GitHub Copilot MCP

**Steps:**

#### Step 1: Get or Create MCP Server

Ask the user if they already have a Composio MCP Server URL. If not:

1. Guide them to visit https://app.composio.dev/
2. Create a new MCP Server:
   - Choose toolkits (gmail, slack, github, notion, etc.)
   - Set `managed_auth_via_composio: true` (recommended for auto OAuth)
   - Or set to `false` if they want to pre-authorize apps manually
3. Get the MCP Server URL format:
   ```
   https://backend.composio.dev/v3/mcp/{server-id}/mcp?user_id={user-id}
   ```

If the user has an existing MCP Server ID, they can update it via API:
```bash
curl -X PATCH "https://backend.composio.dev/api/v3/mcp/{server-id}" \
  -H "X-API-Key: {api-key}" \
  -H "Content-Type: application/json" \
  -d '{"managed_auth_via_composio": true}'
```

#### Step 2: Edit /home/node/.claude.json

Add to the `mcpServers` section using the Edit tool:

```json
{
  "mcpServers": {
    "composio": {
      "type": "http",
      "url": "https://backend.composio.dev/v3/mcp/{server-id}/mcp?user_id={user-id}",
      "headers": {
        "X-API-Key": "ak_user_api_key_here"
      }
    }
  }
}
```

Use the Edit tool to add this configuration, preserving existing MCP servers (like github-copilot, memory, etc.).

#### Step 3: Clean Up Conflicting Configurations

Check for and remove old/conflicting configs:
```bash
# Remove old Desktop config if exists (wrong location for HappyCapy)
rm -f /home/node/.config/Claude/claude_desktop_config.json

# Clean up stdio Composio cache if exists
rm -rf /home/node/.npm/_npx/*/node_modules/@composio

# Clean up other unused MCP caches
rm -rf /home/node/.npm/_npx/*/node_modules/minimax-mcp-js
rm -rf /home/node/.npm/_npx/*/node_modules/mcp-gmail
```

#### Step 4: Verify Installation

After configuration, instruct user to restart Claude Code session.

After restart, verify by checking MCP Server status:
```bash
curl -s "https://backend.composio.dev/api/v3/mcp/{server-id}" \
  -H "X-API-Key: {api-key}" | jq '{name, toolkits, managed_auth_via_composio}'
```

#### Method B: stdio Mode (Alternative)

**When to use:** If user prefers local process or HTTP mode doesn't work.

**Configuration for /home/node/.claude.json:**
```json
{
  "mcpServers": {
    "composio": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@composio/mcp"],
      "env": {
        "COMPOSIO_API_KEY": "ak_user_api_key_here"
      }
    }
  }
}
```

**Note:** stdio mode requires npx to download and run `@composio/mcp` package locally on each session start.

---

### MCP 2: Memory MCP (Knowledge Graph Storage)

**Official MCP:** https://github.com/modelcontextprotocol/servers/tree/main/src/memory

**Purpose:** Persistent knowledge graph for storing entities, relations, and observations across sessions.

**Configuration for /home/node/.claude.json:**

```json
{
  "mcpServers": {
    "memory": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": {}
    }
  }
}
```

**Available Tools:**
- `create_entities` - Create knowledge graph entities
- `create_relations` - Create relationships between entities
- `add_observations` - Add observations to entities
- `delete_entities` - Remove entities
- `delete_relations` - Remove relationships
- `delete_observations` - Remove observations
- `read_graph` - Read the entire knowledge graph
- `search_nodes` - Search for specific entities
- `open_nodes` - Open specific nodes by name

**Usage Examples:**
```
# Store information
Create an entity named "Project X" with observations "Uses React and TypeScript"

# Query information
Search the knowledge graph for "React"
Read the complete knowledge graph
```

**Data Storage:** Knowledge graph persists at `~/.cache/@modelcontextprotocol/server-memory/` across sessions.

---

### MCP 3: GitHub Copilot MCP (GitHub Operations)

**Official MCP:** GitHub Copilot API endpoint

**Purpose:** GitHub operations including issues, pull requests, commits, code search, and repository management.

**Configuration for /home/node/.claude.json:**

```json
{
  "mcpServers": {
    "github-copilot": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ghp_your_github_token_here"
      }
    }
  }
}
```

**How to Get GitHub Token:**
1. Visit https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `read:org`, `read:user`
4. Copy token (format: `ghp_xxxxx`)

**Available Tools:**
- `create_pull_request` - Create PRs
- `issue_read` / `issue_write` - Manage issues
- `pull_request_read` - Read PR details
- `search_code` - Search code in repositories
- `search_issues` - Search issues and PRs
- `get_file_contents` - Read file contents
- `list_commits` - List commit history
- `create_or_update_file` - Modify files
- And 30+ more GitHub operations

**Usage Examples:**
```
# Issues
Create an issue in username/repo with title "Bug report"
Search for open issues in my repositories

# Pull Requests
Create a PR from feature-branch to main
List my open pull requests

# Code Search
Search for "TODO" in username/repo
Get contents of src/main.ts in username/repo
```

---

## Authentication Modes

### Auto-Managed (Recommended)

**Setting:** `managed_auth_via_composio: true`

**Flow:**
1. User says: "Read my Gmail emails"
2. Composio returns OAuth authorization URL
3. User visits URL and authorizes
4. Credentials stored in Composio cloud
5. Future requests work automatically

### Manually-Managed

**Setting:** `managed_auth_via_composio: false`

**Flow:**
1. User visits https://app.composio.dev/apps
2. Manually connects apps (Gmail, Slack, etc.)
3. Then can use in Claude Code

## Usage After Installation

Once configured and session restarted, users can:

```
# Gmail
读取我最近的 Gmail 邮件
发送邮件到 example@gmail.com

# Slack
在 #general 发送消息："Hello team"
列出我的 Slack 频道

# GitHub
在 username/repo 创建 issue
列出我的仓库

# Notion
搜索 Notion 中的页面
创建新页面
```

## Troubleshooting

### Issue 1: MCP Not Loading After Restart

**Cause:** JSON syntax error in `~/.claude.json`

**Solution:**
1. Read and validate JSON syntax: `cat ~/.claude.json | jq .`
2. Check for missing commas, quotes, or brackets
3. Fix syntax errors and restart again

### Issue 2: OAuth Authorization Fails

**Cause:** Wrong `managed_auth_via_composio` setting or missing app connection

**Solution:**
1. Check setting: `curl -s "https://backend.composio.dev/api/v3/mcp/{server-id}" -H "X-API-Key: {key}" | jq .managed_auth_via_composio`
2. If `false`, must pre-connect at https://app.composio.dev/apps
3. If `true`, Claude will provide auth link automatically

### Issue 3: App Not Available

**Cause:** Toolkit not enabled in MCP Server config

**Solution:**
1. Check enabled toolkits: `curl -s "https://backend.composio.dev/api/v3/mcp/{server-id}" -H "X-API-Key: {key}" | jq .toolkits`
2. Update server to add toolkit via Composio dashboard or API

### Issue 4: API Key Invalid

**Cause:** Expired or incorrect API key

**Solution:**
1. Visit https://app.composio.dev/settings/api-keys
2. Generate new API key
3. Update `~/.claude.json` with new key

## Important Notes for HappyCapy Environment

- **Configuration file (FIXED):** `/home/node/.claude.json`
- **NOT** `/home/node/.config/Claude/claude_desktop_config.json` (that's for Desktop app)
- Must restart Claude Code session after any config changes
- OAuth tokens stored securely in Composio cloud, not locally
- Each user_id in the MCP URL represents an isolated user session
- npm cache location: `/home/node/.npm/_npx/`
- Memory MCP data: `/home/node/.cache/@modelcontextprotocol/server-memory/`

## Which MCPs Should You Install?

**Recommended combo (all three):**
- ✅ **Composio** - For external apps (Gmail, Slack, etc.)
- ✅ **Memory** - For persistent context and knowledge
- ✅ **GitHub Copilot** - For GitHub operations

**Minimal setup:**
- Just Composio if you only need app integrations
- Just Memory if you only need knowledge storage
- Just GitHub Copilot if you only work with GitHub

**All are optional** - Install only what you need!

## Complete Multi-MCP Configuration Example

**File location:** `/home/node/.claude.json` (FIXED PATH for HappyCapy environment)

```json
{
  "firstStartTime": "2026-01-30T10:16:22.623Z",
  "userID": "xxx",
  "mcpServers": {
    "composio": {
      "type": "http",
      "url": "https://backend.composio.dev/v3/mcp/{server-id}/mcp?user_id={user-id}",
      "headers": {
        "X-API-Key": "ak_your_composio_api_key"
      }
    },
    "github-copilot": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ghp_your_github_token"
      }
    },
    "memory": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": {}
    }
  }
}
```

**IMPORTANT:** All three MCPs can coexist. You can install all, some, or just one based on your needs.

## Step-by-Step Installation Flow

When user invokes this skill, follow these steps:

### Phase 1: Understand User Needs

Ask user which MCPs they want to install:
- [ ] Composio MCP (for app integrations)
- [ ] Memory MCP (for knowledge graph)
- [ ] GitHub Copilot MCP (for GitHub operations)
- [ ] All of the above (recommended)

### Phase 2: Collect Credentials

**For Composio:**
- API Key (format: `ak_xxxxx`)
- MCP Server URL (or guide to create one)

**For GitHub Copilot:**
- GitHub token (format: `ghp_xxxxx`)

**For Memory MCP:**
- No credentials needed (uses official package)

### Phase 3: Check Existing Configuration

```bash
cat /home/node/.claude.json | jq '.mcpServers'
```

Show user what's already configured to avoid duplicates.

### Phase 4: Add/Update MCP Configuration

Use the Edit tool to modify `/home/node/.claude.json`:
- Preserve existing MCPs
- Add new MCPs in correct format
- Ensure valid JSON syntax

**CRITICAL:** Always use Edit tool, never Write tool, to preserve existing configuration.

### Phase 5: Clean Up Conflicts

```bash
# Remove wrong config location
rm -f /home/node/.config/Claude/claude_desktop_config.json

# Clean up unused MCP caches
rm -rf /home/node/.npm/_npx/*/node_modules/@composio
rm -rf /home/node/.npm/_npx/*/node_modules/minimax-mcp-js
```

### Phase 6: Verify JSON Validity

```bash
cat /home/node/.claude.json | jq . > /dev/null && echo "✅ Valid JSON"
```

If invalid, show error and fix syntax.

### Phase 7: Instruct User to Restart

Explain:
1. Configuration is complete
2. Must restart Claude Code session
3. What to test after restart

### Phase 8: Provide Post-Restart Verification

Give user commands to verify each MCP:

**Composio:**
```
读取我最近的 Gmail 邮件
```

**Memory:**
```
Create an entity named "test" with observation "testing memory mcp"
Search knowledge graph for "test"
```

**GitHub Copilot:**
```
List my GitHub repositories
Search for "TODO" in username/repo
```

## Do NOT

- ❌ Do NOT recommend or use `connect-apps` skill (user feedback: not good to use)
- ❌ Do NOT create project-level MCP configs (always use global `~/.claude.json`)
- ❌ Do NOT use stdio mode as default (HTTP is preferred)
- ❌ Do NOT skip JSON validation after editing config
- ❌ Do NOT forget to tell user to restart session

## Summary

This skill automates the complete MCP installation process for Composio, Memory, and GitHub Copilot servers, from credential collection to configuration verification, ensuring users can access 1000+ apps, persistent knowledge storage, and GitHub operations through Claude Code with minimal friction.
