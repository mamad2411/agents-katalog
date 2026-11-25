---
name: docker-management
description: Manage Docker containers and images via MCP. Use when the user asks to docker ps, tail container logs, restart a service, exec into a container, check CPU/memory stats, or clean up images on the local host.
---

# Docker Management via MCP

Use this skill when you need to manage Docker containers, inspect logs, run commands inside containers, or check resource usage.

## Available Tools

| Tool                | What it does                                               |
| ------------------- | ---------------------------------------------------------- |
| `list_containers`   | List running (or all) containers with status, ports, image |
| `container_logs`    | Get recent logs from a container                           |
| `start_container`   | Start a stopped container                                  |
| `stop_container`    | Stop a running container                                   |
| `restart_container` | Restart a container                                        |
| `remove_container`  | Remove a container (optional force)                        |
| `exec_command`      | Execute a command inside a running container               |
| `container_stats`   | Get live CPU, memory, and network stats                    |
| `list_images`       | List all Docker images on the host                         |
| `remove_image`      | Remove a Docker image                                      |

## Workflow

1. Start with `list_containers` to see what's running
2. Use container names or IDs from the list for all other operations
3. For debugging: `container_logs` first, then `exec_command` to investigate
4. Use `container_stats` to check resource usage when diagnosing performance issues

## Key Patterns

- `list_containers` shows only running containers by default; pass `all: true` for stopped ones too
- `container_logs` returns the last N lines; pass `tail` to control how many
- `exec_command` runs inside a running container; the container must be started first
- `remove_container` with `force: true` stops and removes in one step

## Error Scenarios

- Cannot connect to Docker: Docker Desktop/daemon not running or MCP lacks socket permissions
- Container not found: run `list_containers` with `all: true` for stopped IDs/names
- `exec_command` fails: container must be running; shell may not exist in minimal images
- Empty logs: container just started or logging driver differs; increase `tail` or check app stdout

## Safety

- Always confirm before stopping or removing containers
- Never remove containers in production without explicit user approval
- Check `container_stats` before restarting to understand if the issue is resource-related
