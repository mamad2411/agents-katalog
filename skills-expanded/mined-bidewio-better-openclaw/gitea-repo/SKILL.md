---
name: gitea-repo
description: "Manage Git repositories using Gitea at {{GITEA_HOST}}:{{GITEA_PORT}}."
metadata:
  openclaw:
    emoji: "🫖"
---

# Gitea Repository Management

Gitea is available at `http://{{GITEA_HOST}}:{{GITEA_PORT}}` within the Docker network.

## List Repositories

```bash
curl "http://{{GITEA_HOST}}:{{GITEA_PORT}}/api/v1/repos/search" \
  -H "Authorization: token $GITEA_TOKEN"
```

## Create Repository

```bash
curl -X POST "http://{{GITEA_HOST}}:{{GITEA_PORT}}/api/v1/user/repos" \
  -H "Content-Type: application/json" \
  -H "Authorization: token $GITEA_TOKEN" \
  -d '{"name": "my-project", "private": true, "auto_init": true}'
```

## Tips for AI Agents

- Gitea provides a lightweight, self-hosted Git forge.
- Supports pull requests, issues, CI/CD (Gitea Actions), and packages.
- Clone via HTTP or SSH within the Docker network.
