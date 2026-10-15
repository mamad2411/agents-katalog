---
name: trycook
description: Use the TryCook CLI to discover and execute AI-powered tools. Triggers on "trycook", "use trycook", "call tool", "run tool", or any request to use TryCook platform capabilities (image generation, scraping, ad building, voice agents, integrations, etc). This is the core skill — use it before any domain-specific trycook skill.
allowed-tools:
  - Bash(trycook *)
  - Read
---

# TryCook CLI — Core Tool Execution

You have access to the `trycook` CLI, which provides 100+ AI-powered tools across media generation, web research, ad building, voice agents, site/funnel management, and 20+ third-party integrations.

## Prerequisites

The `trycook` binary must be installed at `~/.trycook/bin/trycook`. If not found, install:

```bash
curl -fsSL https://trycook.ai/install.sh | sh
```

## Step 0 — Verify Authentication

**Always run this first before any tool execution:**

```bash
trycook status
```

If not authenticated:
```bash
trycook auth
```

This opens a browser for OAuth login. Credentials are stored at `~/.config/trycook/credentials.json`.

## Step 1 — Discover Tools

Find tools by searching with keywords:

```bash
trycook tools search "image generation"
trycook tools search "scrape website"
trycook tools search "slack"
```

To see all available tools organized by category:

```bash
trycook tools
```

## Step 2 — Get Tool Schema

Before calling a tool, always inspect its input schema:

```bash
trycook tool info generate_image
```

This shows the tool's description, type (sandbox/integration), and full JSON input schema with required and optional parameters.

## Step 3 — Execute Tool

Call the tool with JSON parameters:

```bash
trycook tool call generate_image '{"prompt": "a serene mountain landscape at sunset", "aspect_ratio": "16:9"}'
```

The response is JSON with the tool's output. Common fields:
- `ok`: boolean success indicator
- `output`: the tool's result data
- `imageUrl`: presigned URL (for image/media tools)
- `artifactId`: reference ID for generated artifacts

## Error Handling

| Error | Fix |
|-|-|
| "Not authenticated" | Run `trycook auth` |
| "Unknown tool: X" | Run `trycook tools search` to find the correct name |
| Tool call returns error JSON | Check the `error` field — usually a missing required param |
| Timeout | Server-side tools can take 30-60s. Retry once. |

## Workspace Management

Switch between workspaces:

```bash
trycook workspace show          # current workspace
trycook workspace set <id>      # switch workspace
```

Workspace determines which integrations and data are accessible.

## Anti-Patterns

- **DO NOT** guess tool names. Always `trycook tools search` first.
- **DO NOT** guess parameter names. Always `trycook tool info` first.
- **DO NOT** skip the auth check. Unauthenticated calls fail silently or with cryptic errors.
- **DO NOT** hardcode workspace IDs. Use `trycook workspace show` to check.

## CLI Reference

For the complete command reference and tool categories, read:
[{baseDir}/references/cli-reference.md]({baseDir}/references/cli-reference.md)
