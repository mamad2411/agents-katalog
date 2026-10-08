# mstro — Maestro/BAR CLI & MCP Server Skill

## What is mstro?

`mstro` is a CLI tool and MCP server that provides cached access to Maestro/BAR (Build Asset Registry) data for .NET dependency flow infrastructure. Use it when investigating subscription health, build flow status, codeflow PRs, or triggering dependency updates. It wraps complex multi-step API workflows (subscription staleness checks, commit distance calculations, backflow status) into single commands with smart caching.

**When to use:** Investigating stale subscriptions, checking if fixes have flowed through the VMR, debugging dependency update issues, tracing build graphs, or triggering subscription updates in the .NET build infrastructure.

## Installation

```bash
dotnet tool install -g lewing.maestro.mcp
```

After installation, `mstro` is available globally. The tool uses a shared SQLite cache at `~/.mstro/cache.db` (WAL mode) — cache is shared between CLI usage and MCP server instances.

## Quick Discovery

```bash
# List all available commands
mstro --help

# Get detailed help for a specific command
mstro <command> --help
```

All query commands support `--json` flag for structured output and `--no-cache` to bypass the cache.

## Authentication

The tool implements a 3-tier authentication cascade:
1. **Explicit PAT** — Set `MAESTRO_BAR_TOKEN` environment variable
2. **Cached Entra ID** — Reuses credentials from `darc authenticate` (`~/.darc/.auth-record-*`)
3. **Anonymous** — Read-only fallback (may be rate-limited)

**Recommended:** Run `darc authenticate` once (from [arcade-services](https://github.com/dotnet/arcade-services)) to cache credentials.

## Quick Start Workflows

### Check Subscription Health
Detect stale subscriptions for a target repository by comparing last-applied builds vs latest available builds:
```bash
mstro subscription-health --target-repository https://github.com/dotnet/dotnet --json
mstro subscription-health --target-repository https://github.com/dotnet/sdk --include-commit-details --json
```

### Get Latest Build
Find the latest build for a repository on a specific channel:
```bash
mstro latest-build https://github.com/dotnet/runtime --channel-name ".NET 10.0.1xx SDK" --json
mstro latest-build https://github.com/dotnet/roslyn --json
```

### Check Codeflow Status
Get forward flow and backflow status for a repository (defaults to VMR):
```bash
mstro codeflow-statuses --json
mstro codeflow-statuses --repository-url https://github.com/dotnet/runtime --branch main --json
```

### Trace a Build
Get build details and dependency graph:
```bash
mstro build 302353 --json
mstro build-graph 302353 --json
```

### List Active Codeflow PRs
List tracked PRs managed by Maestro for dependency flow:
```bash
mstro codeflow-prs --json
mstro codeflow-prs --channel-name ".NET 10 Engineering" --json
```

### Check Backflow Status
Get backflow status for a specific VMR build:
```bash
mstro backflow-status 302627 --json
```

### Trigger Subscription Update
Trigger a subscription to process updates (requires authentication):
```bash
mstro trigger-subscription <subscription-guid> --build-id 302353
mstro trigger-subscription <subscription-guid> --source-repository https://github.com/dotnet/runtime --channel-name ".NET 10.0.1xx SDK"
mstro trigger-subscription <subscription-guid> --build-id 302353 --force
```

Use `--force` to overwrite existing PR branches with fresh VMR content (useful for stale backflow PRs).

## Structured Output

All query commands support `--json` for machine-parseable output:
```bash
mstro subscriptions --source-repository https://github.com/dotnet/runtime --json | jq '.[] | select(.Enabled == true)'
mstro subscription-health --target-repository https://github.com/dotnet/dotnet --json | jq '.StaleSubs | length'
```

The JSON output includes the same data that MCP tools return, but in structured format instead of Markdown.

## Cache Behavior

- **Shared cache:** `~/.mstro/cache.db` is used by both CLI and MCP server instances
- **TTLs:** Subscriptions (5m), Latest Builds (5m), Channels (15m), Build by ID (30m), Build Freshness (10m)
- **Cache bypass:** Use `--no-cache` on any command to force fresh API calls
- **Cache management:**
  ```bash
  mstro cache status    # Show cache statistics
  mstro cache clear     # Clear all cached data
  ```

## Relationship to MCP Server

The same binary (`mstro`) operates in two modes:
- **CLI mode:** When invoked with a command (e.g., `mstro subscription-health`)
- **MCP server mode:** When stdin is piped (e.g., launched by an MCP host)

Both modes share the same cached data layer, authentication cascade, and API client. Using the CLI warms the cache for MCP server instances and vice versa.

## Common Workflows

**Investigate stale subscription:**
```bash
# 1. Check subscription health for a repo
mstro subscription-health --target-repository https://github.com/dotnet/dotnet --json

# 2. Get details on a specific stale subscription
mstro subscription <guid> --json

# 3. Check subscription history to see update attempts
mstro subscription-history <guid> --json

# 4. Trigger the subscription manually
mstro trigger-subscription <guid> --source-repository https://github.com/dotnet/runtime --channel-name ".NET 10.0.1xx SDK"
```

**Trace dependency flow:**
```bash
# 1. Find latest build for source repo
mstro latest-build https://github.com/dotnet/runtime --channel-name ".NET 10.0.1xx SDK" --json

# 2. Get dependency graph for that build
mstro build-graph <build-id> --json

# 3. Check if it's reached the VMR
mstro codeflow-statuses --json
```

**Debug backflow issues:**
```bash
# 1. Get VMR build ID
mstro latest-build https://github.com/dotnet/dotnet --json

# 2. Check backflow status
mstro backflow-status <vmr-build-id> --json

# 3. List active backflow PRs
mstro codeflow-prs --channel-name ".NET 10 Engineering" --json
```

## Further Documentation

For complete command reference: `mstro guide`  
For workflow-organized guide: `mstro guide | less`  
For MCP server setup: See README.md in the package or [github.com/lewing/maestro.mcp](https://github.com/lewing/maestro.mcp)
