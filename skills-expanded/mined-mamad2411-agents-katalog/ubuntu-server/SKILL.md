---
name: ubuntu-server
description: "SSH into the persistent ubuntu-server container to deploy web apps and run long-lived processes"
version: 1.0.0
author: local-ai-stack
metadata:
  hermes:
    tags: [ssh, ubuntu, deployment, web, server]
    category: infrastructure
---

# Ubuntu Server

## When to Use
Use this skill when you need to deploy a web app, run a long-lived process, or store files that must outlive agent container restarts.

## Access

```bash
ssh -o StrictHostKeyChecking=no ai@ubuntu-server
# password: localai
```

The `ai` user has passwordless sudo (`sudo -n <cmd>`).

## Web Server

nginx runs on port 80. The server is reachable from a browser at `http://www.localai` (or `https://www.localai` if TLS is configured).

- Place static files in `/var/www/html/`
- Add a virtual host config to `/etc/nginx/sites-enabled/` then run `sudo nginx -s reload`

## Pitfalls

- Always pass `-o StrictHostKeyChecking=no` — the agent container won't have the host key cached
- Files placed on the server persist across both server and agent restarts
