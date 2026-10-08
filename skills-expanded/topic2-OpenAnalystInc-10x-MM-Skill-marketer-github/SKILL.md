---
name: marketer-github
description: >
  Connect a GitHub repo to inject the WebMCP runtime snippet for strategy personalization.
  Triggers: connect github, deploy snippet, push snippet, inject snippet, connect repo.
---

# Marketer GitHub Integration Skill

## Overview

Connects the marketing platform to a user's GitHub-hosted website by injecting the WebMCP runtime snippet via PR. This makes any published page an MCP server that AI agents can interact with.

The MCP server handles all auth — you only need `gh` CLI for GitHub operations.

## When To Use

- User wants their external website to use Link Platform strategies
- User says "connect my GitHub repo"
- User says "inject the snippet into my site"
- User wants WebMCP capabilities on their live website

## Prerequisites

- `gh` CLI installed and authenticated (`gh auth status`)
- User's website hosted on GitHub
- `LINK_PLATFORM_HANDLE` env var set
- Strategy already published via `publish_release`

## Procedure

### Step 1: Get Handle Info via MCP

Fetch the user's handle info to verify the connection:

```
system_health()
```

### Step 2: Get WebMCP Snippet

Use the `tracking_list_templates` MCP tool to get the correct embed code:

```
tracking_list_templates({ handle: "<LINK_PLATFORM_HANDLE>", slug: "<slug>" })
```

### Step 3: Clone the User's Repo

```bash
gh repo clone <user/repo> .10x/repos/<repo-name>
```

### Step 4: Create Strategy Branch

```bash
git -C .10x/repos/<repo-name> checkout -b strategy/<strategy-name>
```

### Step 5: Inject WebMCP Snippet

Add the snippet returned by `tracking_list_templates` before `</body>` in each HTML file. Default snippet format:

```html
<!-- Marketing Manager — WebMCP Runtime -->
<script
  src="https://cdn.10x.in/webmcp.js"
  data-handle="<LINK_PLATFORM_HANDLE>"
  data-strategy="<slug>"
  async
></script>
```

This snippet:
- Resolves active strategies for the visitor
- Evaluates segment rules (UTM, device, location)
- Applies personalization to the DOM
- Makes the page discoverable as an MCP server for AI agents

### Step 6: Commit and Open PR

```bash
git -C .10x/repos/<repo-name> add .
git -C .10x/repos/<repo-name> commit -m "feat: inject Marketing Manager WebMCP snippet"
gh pr create \
  --repo <user/repo> \
  --title "Add Marketing Manager strategy: <strategy-name>" \
  --body "Injects WebMCP runtime for strategy personalization via Link Platform handle: <handle>" \
  --head strategy/<strategy-name>
```

### Step 7: Save Connection Reference

Write to `.10x/github.json`:
```json
{
  "repo": "<user/repo>",
  "local_path": ".10x/repos/<repo-name>",
  "handle": "<LINK_PLATFORM_HANDLE>",
  "strategy": "<slug>",
  "pr_url": "<gh pr url>",
  "connected_at": "<ISO timestamp>"
}
```

### Step 8: Report

```
GITHUB CONNECTED
================
Repo:     <user/repo>
Branch:   strategy/<name>
PR:       <pr_url>

Once merged, your site will personalize using:
  Handle:    <handle>.10x.in
  Strategy:  <slug>

User reviews and merges the PR — hosting auto-deploys.
```

## Safety

- Always creates a PR — never pushes to main directly
- Only adds the `<script>` tag — no other modifications
- User must review and merge the PR themselves

## Notes

- No `npm run` commands needed — use `gh` CLI and git directly
- WebMCP snippet is served from CDN — no server changes required
- Multiple strategies can be injected; each gets its own PR
