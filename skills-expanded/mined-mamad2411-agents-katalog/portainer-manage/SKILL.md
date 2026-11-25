---
name: portainer-manage
description: "Manage Docker containers via Portainer at {{PORTAINER_HOST}}:{{PORTAINER_PORT}}."
metadata:
  openclaw:
    emoji: "🐳"
---

# Portainer Container Management

Portainer is available at `http://{{PORTAINER_HOST}}:{{PORTAINER_PORT}}` within the Docker network.

## List Containers

```bash
curl "http://{{PORTAINER_HOST}}:{{PORTAINER_PORT}}/api/endpoints/1/docker/containers/json" \
  -H "X-API-Key: $PORTAINER_API_KEY"
```

## Tips for AI Agents

- Portainer provides a web UI for managing Docker, Swarm, and Kubernetes.
- View logs, stats, and console access for running containers.
- Manage images, volumes, and networks through the API.
