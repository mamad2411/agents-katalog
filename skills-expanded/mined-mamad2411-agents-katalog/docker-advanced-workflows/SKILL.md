---
name: docker-advanced-workflows
description: Multi-stage pipelines, sidecar patterns, healthchecks, init containers, signal handling, and graceful shutdown.
standards-version: 1.10.0
---

# Docker Advanced Workflows

## Trigger

Use this skill when:
- Designing multi-stage build pipelines for production images
- Implementing sidecar containers alongside a primary service
- Configuring healthchecks for containers or compose services
- Setting up init containers or entrypoint scripts
- Handling process signals and graceful shutdown in containers
- Copying files between containers and the host during development
- Monitoring container resource usage in real time
- Updating container resource limits without restarting

## Required Inputs

- The use case: pipeline design, sidecar setup, healthcheck config, signal handling, resource tuning
- Language/runtime of the containerized application (affects signal handling and healthcheck commands)
- Whether the workload is development or production (affects patterns and strictness)

## Workflow

1. **Identify the pattern** - determine which advanced workflow applies (multi-stage, sidecar, healthcheck, init, signal handling, live monitoring).
2. **Check current state** - use `docker_listContainers`, `docker_inspectContainer`, and `docker_stats` to understand the running environment.
3. **Apply the pattern** - write or modify Dockerfiles, compose files, or entrypoint scripts.
4. **Validate** - use `docker_top` to verify processes, `docker_stats` for resource usage, `docker_events` to watch lifecycle events.
5. **Tune** - use `docker_update` to adjust CPU/memory limits live, or `docker_wait` to synchronize on container completion.

## Key References

- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
- [Healthcheck reference](https://docs.docker.com/reference/dockerfile/#healthcheck)
- [docker update reference](https://docs.docker.com/reference/cli/docker/container/update/)
- [docker events reference](https://docs.docker.com/reference/cli/docker/system/events/)
- [Graceful shutdown in containers](https://docs.docker.com/reference/cli/docker/container/stop/)
- [docker cp reference](https://docs.docker.com/reference/cli/docker/container/cp/)

## Example Interaction

**User:** I want to set up a proper healthcheck for my Node.js API container.

**Agent:** Here are three approaches depending on your setup:

**Dockerfile healthcheck:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => { process.exit(r.statusCode === 200 ? 0 : 1) })"
```

**Compose healthcheck:**
```yaml
services:
  api:
    build: .
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:3000/health', (r) => { process.exit(r.statusCode === 200 ? 0 : 1) })"]
      interval: 30s
      timeout: 5s
      start_period: 10s
      retries: 3
    depends_on:
      db:
        condition: service_healthy
```

**Using curl (if available in the image):**
```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

You can verify it's working with `docker_inspectContainer` - look at `State.Health.Status` and `State.Health.Log`.

---

**User:** My container is using too much memory. Can I change the limit without restarting it?

**Agent:** Yes, use `docker_update`:

```
docker_update with containerId="my-api", memory="512m", memorySwap="1g"
```

Then verify with `docker_stats`:
```
docker_stats with containers=["my-api"]
```

If the container is already exceeding the new limit, it may get OOMKilled. Check current usage with `docker_stats` first, then set the limit above current usage but below the problematic threshold.

---

**User:** How do I handle graceful shutdown in my container?

**Agent:** Docker sends SIGTERM to PID 1 when stopping a container, then SIGKILL after the grace period (default 10s).

Key rules:
1. **Trap SIGTERM in your app** - don't ignore it
2. **Use exec form CMD** - `CMD ["node", "server.js"]` not `CMD node server.js` (shell form wraps in `/bin/sh` which may not forward signals)
3. **Use tini for multi-process containers** - if PID 1 isn't your app

```dockerfile
# Good - exec form, signals go directly to node
CMD ["node", "server.js"]

# For multi-process - use tini as init
RUN apk add --no-cache tini
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "server.js"]
```

Node.js signal handler:
```javascript
process.on('SIGTERM', () => {
  console.log('SIGTERM received, closing server...');
  server.close(() => {
    console.log('Server closed, exiting');
    process.exit(0);
  });
  setTimeout(() => process.exit(1), 5000);
});
```

You can test with `docker_stop` using a short timeout and watch events with `docker_events`.

## MCP Usage

| Tool | Purpose |
|------|---------|
| `docker_stats` | Monitor CPU, memory, network I/O for running containers |
| `docker_top` | See running processes inside a container (verify PID 1, check for zombies) |
| `docker_events` | Watch container lifecycle events (start, stop, die, health_status) |
| `docker_update` | Change CPU/memory limits and restart policy without restarting |
| `docker_wait` | Block until a container exits and get its exit code |
| `docker_cp` | Copy files between container and host (configs, logs, debug artifacts) |
| `docker_inspectContainer` | Check healthcheck status, restart count, resource config |
| `docker_exec` | Run commands inside a running container for diagnostics |

**Multi-stage build pipeline flow:**
```
1. docker_build with context and Dockerfile
2. docker_run to test the image
3. docker_stats to verify resource usage
4. docker_top to check process tree
5. docker_tag for versioning
6. docker_push to registry
```

**Live resource tuning flow:**
```
1. docker_stats - observe current CPU/memory usage
2. docker_update - adjust limits (cpus, memory, restartPolicy)
3. docker_stats - verify the change took effect
4. docker_events - watch for OOMKill or restart events
```

## Common Pitfalls

- **Shell form CMD swallows signals** - `CMD node server.js` runs under `/bin/sh -c`, which does not forward SIGTERM to the node process. Always use exec form: `CMD ["node", "server.js"]`.
- **Healthcheck using curl in distroless images** - curl isn't available. Use a language-native healthcheck or a static binary.
- **start_period too short** - if your app takes 30s to boot but start_period is 5s, Docker marks it unhealthy before it's ready. Set start_period generously.
- **Forgetting --init or tini** - without an init process, zombie processes accumulate. Use `--init` flag on `docker run` or install tini.
- **Updating memory below current usage** - calling `docker_update` with a memory limit lower than current RSS triggers an immediate OOMKill. Check `docker_stats` first.
- **docker events without --until** - blocks forever waiting for events. Always set `--until` or use the `docker_events` MCP tool which defaults to a bounded window.
- **Ignoring restart policy interactions** - setting `restart: always` with a crashing container creates an infinite restart loop. Use `on-failure` with a max retry count during development.
- **COPY --from in multi-stage without naming stages** - use `FROM node:22-alpine AS builder` and `COPY --from=builder` instead of numeric indices, which break when stages are reordered.

## See Also

- [Container Debugging](../container-debugging/SKILL.md)
- [Docker Resource Management](../docker-resource-management/SKILL.md)
- [Docker Security](../docker-security/SKILL.md)
- [Dockerfile Best Practices](../dockerfile-best-practices/SKILL.md)
