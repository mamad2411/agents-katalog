---
name: forgejo-repo
description: Lightweight code hosting with Forgejo
version: 1.0.0
tags: [git, code-hosting, devops, self-hosted]
---

# Forgejo – Community-Owned Git Forge

Forgejo is a community-governed, lightweight self-hosted Git service
(soft fork of Gitea) under Codeberg e.V.

- **GitHub / Codeberg**: codeberg.org/forgejo/forgejo (7 000+ ⭐)
- **License**: MIT
- **Security**: Community governance. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{FORGEJO_URL}}` | Base URL of the Forgejo instance |
| `{{FORGEJO_TOKEN}}` | Personal access token |

## Usage Examples

### List repositories

```bash
curl -s "{{FORGEJO_URL}}/api/v1/repos/search" \
  -H "Authorization: token {{FORGEJO_TOKEN}}"
```

### Create a repository

```bash
curl -s -X POST "{{FORGEJO_URL}}/api/v1/user/repos" \
  -H "Authorization: token {{FORGEJO_TOKEN}}" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-project", "auto_init": true, "private": false}'
```

## AI Agent Tips

- Gitea-compatible API — most Gitea integrations work directly.
- Supports Actions (CI/CD similar to GitHub Actions).
- Lightweight Docker deployment; runs on minimal resources.
- Community-governed under Codeberg for long-term independence.
