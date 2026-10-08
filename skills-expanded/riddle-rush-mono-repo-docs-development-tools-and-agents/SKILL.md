# Tools and Agents Configuration

Complete guide to development tools, MCP servers, and AI agent configuration for the Riddle Rush monorepo.

## 📑 Table of Contents

- [Overview](#overview)
- [MCP Servers](#mcp-servers)
- [Agent Configuration](#agent-configuration)
- [Development Tools](#development-tools)
- [Tool Scripts](#tool-scripts)
- [Integration Guide](#integration-guide)

---

## Overview

The monorepo uses a comprehensive tooling ecosystem to support development, testing, and AI-assisted workflows.

### Architecture

```
┌─────────────────────────────────────────────────┐
│  AI Agents (Copilot, Claude, Cursor)           │
│  ↓ MCP Protocol                                 │
├─────────────────────────────────────────────────┤
│  MCP Servers (Nuxt UI, Playwright, Git, etc.)  │
│  ↓                                              │
├─────────────────────────────────────────────────┤
│  Development Tools                              │
│  • Turbo (Build orchestration)                  │
│  • Trunk (Code quality)                         │
│  • Python Tools (Automation)                    │
│  ↓                                              │
├─────────────────────────────────────────────────┤
│  Monorepo (apps/ packages/ services/)          │
└─────────────────────────────────────────────────┘
```

---

## MCP Servers

Model Context Protocol (MCP) servers provide AI agents with specialized capabilities.

### Configuration Files

**Primary Config (canonical list):** `.mcp.json`

```json
{
  "mcpServers": {
    "riddle-rush-subagents": {
      "command": "node",
      "args": ["/home/cloudcrusader/projects/riddle-rush-mono-repo/tools/voltagent/mcp-server.mjs"],
      "cwd": "/home/cloudcrusader/projects/riddle-rush-mono-repo"
    },
    "nuxt-ui": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://ui.nuxt.com/mcp"]
    },
    "browsermcp": {
      "command": "npx",
      "args": ["-y", "@browsermcp/mcp@latest"]
    }
  }
}
```

**FastMCP Config:** `fastmcp.json`

```json
{
  "mcpServers": {
    "riddle-rush-subagents": {
      "source": "node /home/cloudcrusader/projects/riddle-rush-mono-repo/tools/voltagent/mcp-server.mjs",
      "tools": ["*"],
      "description": "VoltAgent MCP subagents for repository automation"
    },
    "playwright": {
      "source": "npx -y @executeautomation/playwright-mcp-server",
      "tools": ["*"],
      "description": "Browser automation for E2E testing"
    }
  }
}
```

**Cursor Example:** `.cursor/mcp.json.example` mirrors `.mcp.json` with descriptions.

### Available MCP Servers

#### 1. **Riddle Rush Subagents (VoltAgent)**

Project-specific automation subagents powered by VoltAgent.

**Capabilities:**

- Run workspace checks and tests
- Report repo status

**Entry:** `tools/voltagent/mcp-server.mjs`

#### 2. **Nuxt UI MCP**

Nuxt UI component documentation and examples.

**Capabilities:**

- Component API reference
- Usage examples
- Theme configuration
- Composable documentation

**Access:** https://ui.nuxt.com/mcp

#### 3. **BrowserMCP**

Browser automation and inspection via the BrowserMCP server.

**Capabilities:**

- Open and inspect pages
- Capture screenshots
- Extract page content

**Package:** `@browsermcp/mcp`

#### 4. **Nuxt MCP Toolkit**

Nuxt MCP Toolkit for Nuxt documentation and tooling context.

**Capabilities:**

- Nuxt documentation lookup
- Toolkit-specific guidance
- API references

**Access:** https://mcp-toolkit.nuxt.dev/mcp

#### 5. **Playwright MCP**

Browser automation for E2E testing and debugging.

**Capabilities:**

- Run E2E tests
- Generate test code
- Debug test failures
- Capture screenshots/videos

**Usage:**

```bash
# Run E2E tests
pnpm run test:e2e

# Debug specific test
pnpm run test:e2e -- --debug tests/e2e/login.spec.ts
```

#### 6. **AWS Documentation MCP**

AWS service documentation and reference.

**Capabilities:**

- Search AWS docs (S3, CloudFront, Lambda, etc.)
- Configuration examples
- Best practices
- Troubleshooting guides

**Services Covered:**

- S3 (storage)
- CloudFront (CDN)
- Lambda (serverless)
- DynamoDB (database)
- API Gateway (APIs)

#### 7. **Docker MCP**

Docker Hub search and container management.

**Capabilities:**

- Search Docker Hub images
- Manage containers
- Build/push images
- Docker Compose operations

**Usage:**

```bash
# Build Docker image
pnpm run build:docker

# Run with Docker Compose
docker-compose up -d
```

#### 8. **Context7 MCP**

Library documentation for modern web development.

**Libraries Covered:**

- Vue 3
- Nuxt 3/4
- Vite
- TypeScript
- Pinia
- VueUse
- Tailwind CSS

**Usage:**

- Query component APIs
- Find composable examples
- Check migration guides
- View TypeScript types

#### 9. **Git MCP**

Git operations and repository management.

**Capabilities:**

- Execute git commands
- Query commit history
- Manage branches
- Create/review PRs

**Common Operations:**

```bash
# Via MCP or direct git
git status
git log --oneline -10
git diff HEAD~1
git add .
git commit -m "feat: description"
```

#### 10. **GitLab MCP**

GitLab API for CI/CD pipeline management.

**Capabilities:**

- View pipeline status
- Trigger CI/CD jobs
- Manage merge requests
- Query artifacts

**Configuration:**

Set environment variable:

```bash
export GITLAB_PERSONAL_ACCESS_TOKEN="your-token"
export GITLAB_API_URL="https://gitlab.com/api/v4"
```

#### 8. **Filesystem MCP**

Safe filesystem operations within project directory.

**Capabilities:**

- Read files
- Write files (with safety checks)
- List directories
- Search file content

**Safety:** Operations are restricted to the project directory.

---

## Agent Configuration

### GitHub Copilot CLI

Uses `.mcp.json` automatically.

**Setup:**

Already configured. No additional setup needed.

**Usage:**

```bash
# Ask Copilot
gh copilot suggest "How do I run tests?"
gh copilot explain "Explain this code"
```

### Claude Desktop

Uses `fastmcp.json` configuration.

**Setup:**

1. Install Claude Desktop
2. Copy `fastmcp.json` to Claude config directory
3. Restart Claude Desktop

**Config Location:**

- **macOS:** `~/Library/Application Support/Claude/`
- **Linux:** `~/.config/claude/`
- **Windows:** `%APPDATA%\Claude\`

### Cursor

Supports both `.mcp.json` and custom configurations.

**Setup:**

1. Install Cursor
2. Enable MCP in settings
3. Point to `.mcp.json`

**Usage:**

Use Cursor commands with MCP context.

---

## Development Tools

### Turbo

Monorepo build orchestration with caching.

**Configuration:** `turbo.json`

**Common Commands:**

```bash
# Build all packages
pnpm run build:all

# Build specific package
pnpm run build --filter=@riddle-rush/game

# Run task with caching
turbo run typecheck --cache-dir=.turbo
```

### Trunk

Universal code quality tool (linting, formatting, security).

**Configuration:** `.trunk/trunk.yaml`

**Common Commands:**

```bash
# Check all files
pnpm run trunk:check

# Format files
pnpm run trunk:fmt

# View flaky tests
pnpm run trunk:flaky-tests
```

**Features:**

- Multi-language linting (TS, JS, Python, Shell, YAML)
- Auto-formatting
- Secret scanning
- Security vulnerability detection

### Python Tools

Python-based automation and analysis tools.

**Location:** `tools/python/`

**Setup:**

```bash
# Create virtual environment
python3 -m venv tools/.venv

# Activate
source tools/.venv/bin/activate

# Install dependencies
pip install -r tools/python/requirements.txt
```

**Common Commands:**

```bash
# Lint Python code
pnpm run python:lint

# Format Python code
pnpm run python:format

# Run all Python checks
pnpm run python:check
```

---

## Tool Scripts

### Agent Helper Script

Quick reference for agent workflow commands.

**Location:** `scripts/agent-commands.sh`

**Usage:**

```bash
# Display help
pnpm run agent:help

# Or directly
./scripts/agent-commands.sh
```

**Output:**

- Quality checks
- Testing commands
- Git workflow
- Commit types
- Development commands
- Quick workflow template

### Setup Scripts

#### Agent Configuration Setup

**Location:** `scripts/setup-agent-configs.sh`

**Usage:**

```bash
# Setup OpenCode agent
./scripts/setup-agent-configs.sh opencode --dest ~/.config/opencode/perplexity.json

# Setup KiloCode agent
./scripts/setup-agent-configs.sh kilocode --dest ~/.config/kilocode/perplexity.json

# Dry run
./scripts/setup-agent-configs.sh opencode --dry-run
```

### Validation Scripts

#### Locale Validation

**Location:** `scripts/validate-locales.mjs`

**Usage:**

```bash
pnpm run validate:locales
```

**Checks:**

- JSON structure validity
- Missing translations
- Unused keys
- Consistent formatting

---

## Integration Guide

### Setting Up a New Development Environment

#### 1. Install Dependencies

```bash
# Install Node.js packages
pnpm install

# Install Python dependencies
source tools/.venv/bin/activate
pip install -r tools/python/requirements.txt

# Install Trunk
curl https://get.trunk.io -fsSL | bash
```

#### 2. Configure MCP Servers

```bash
# For GitHub Copilot
# Already configured via .mcp.json

# For Claude Desktop
mkdir -p ~/.config/claude
cp fastmcp.json ~/.config/claude/

# For Cursor
# Enable MCP in Cursor settings
```

#### 3. Verify Setup

```bash
# Run baseline checks
pnpm run workspace:check

# Test MCP servers
npx -y mcp-remote https://ui.nuxt.com/mcp

# Verify tools
pnpm run trunk:check
pnpm run python:check
```

### Using Tools in CI/CD

Tools are integrated into CI/CD workflows (`.github/workflows/`).

**Example Workflow:**

```yaml
name: CI
on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4

      - name: Install dependencies
        run: pnpm install

      - name: Run quality checks
        run: pnpm run workspace:check

      - name: Trunk check
        run: pnpm run trunk:check

      - name: Python checks
        run: pnpm run python:check
```

### Custom Tool Integration

#### Adding a New MCP Server

1. **Update `.mcp.json`:**

```json
{
  "mcpServers": {
    "custom-tool": {
      "command": "npx",
      "args": ["-y", "custom-mcp-server"],
      "env": {
        "API_KEY": "${CUSTOM_API_KEY}"
      }
    }
  }
}
```

2. **Document Usage:**

Add to this file with capabilities and examples.

3. **Test Integration:**

```bash
# Verify server loads
# Use with AI agent
```

#### Adding a New Tool Script

1. **Create Script:**

```bash
# Create script file
touch scripts/custom-tool.sh
chmod +x scripts/custom-tool.sh
```

2. **Add npm Script:**

```json
{
  "scripts": {
    "tool:custom": "bash scripts/custom-tool.sh"
  }
}
```

3. **Add to Agent Helper:**

Update `scripts/agent-commands.sh` with new command.

---

## Troubleshooting

### MCP Server Not Loading

**Issue:** Agent can't connect to MCP server

**Solutions:**

1. Check `.mcp.json` syntax (valid JSON)
2. Verify `npx` is available
3. Check environment variables
4. Restart agent application

### Tool Command Fails

**Issue:** `pnpm run <tool>` fails

**Solutions:**

1. Verify dependencies installed: `pnpm install`
2. Check Node.js version: `node --version` (should be >=20)
3. Clear cache: `pnpm store prune`
4. Check script path in `package.json`

### Python Tools Not Working

**Issue:** Python commands fail

**Solutions:**

1. Activate virtual environment: `source tools/.venv/bin/activate`
2. Install dependencies: `pip install -r tools/python/requirements.txt`
3. Check Python version: `python --version` (should be >=3.9)

### Turbo Task Failures

**Issue:** Build/test tasks fail

**Solutions:**

1. Run baseline check: `pnpm run workspace:check`
2. Clear build cache: `turbo daemon clean`
3. Check logs: `turbo run build --verbose`

---

## Best Practices

### For AI Agents

1. **Always run quality checks** before committing
2. **Use MCP servers** for documentation lookups
3. **Commit frequently** with conventional commit messages
4. **Validate changes** with relevant tests
5. **Update documentation** when changing behavior

### For Developers

1. **Keep MCP configs updated** with new servers
2. **Document new tools** in this file
3. **Add tool scripts** to `package.json`
4. **Test tools** in CI/CD before merging
5. **Version control** tool configurations

### For Teams

1. **Share MCP configurations** via version control
2. **Standardize tool usage** across team
3. **Document custom integrations**
4. **Review tool effectiveness** regularly
5. **Update agent workflows** as needed

---

## Reference

### Quick Commands

```bash
# Quality checks
pnpm run workspace:check        # All checks
pnpm run typecheck             # TypeScript
pnpm run lint                  # ESLint
pnpm run trunk:check           # Trunk linting
pnpm run python:check          # Python checks

# Testing
pnpm run test:unit             # Unit tests
pnpm run test:e2e              # E2E tests

# Development
pnpm run dev                   # Start dev server
pnpm run build                 # Build for production

# Agent helpers
pnpm run agent:help            # Show agent commands
pnpm run agent:check           # Run all checks
pnpm run agent:fix             # Auto-fix issues
```

### Configuration Files

| File                | Purpose                           |
| ------------------- | --------------------------------- |
| `.mcp.json`         | Primary MCP server configuration  |
| `fastmcp.json`      | Extended MCP server configuration |
| `turbo.json`        | Turbo build configuration         |
| `.trunk/trunk.yaml` | Trunk tool configuration          |
| `package.json`      | npm scripts and dependencies      |

### Related Documentation

- [Agent Workflow Guide](../../AGENTS.md)
- [Development Scripts](../../scripts/README.md)
- [CI/CD Workflows](../../.github/workflows/README.md)
- [Testing Guide](./TESTING.md)
- [Tools Directory](../../tools/README.md)

---

**Last Updated:** January 2026
