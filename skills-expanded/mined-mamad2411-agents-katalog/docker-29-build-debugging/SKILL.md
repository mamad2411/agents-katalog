---
name: docker-29-build-debugging
description: Troubleshoots Docker Engine 29 build, BuildKit, Buildx, image runtime, container startup, entrypoint, platform, cache, network, filesystem, and permission failures. Use when Docker builds fail or containers behave differently from the host.
license: MIT
compatibility: Requires Docker CLI for runtime debugging commands. Static diagnosis can start from logs and files.
---

# Docker 29 Build Debugging

This skill helps the agent diagnose Docker build and runtime container failures without jumping to destructive commands.

## When to Use

Use this skill when:

- `docker build`, `docker buildx build`, or Compose builds fail.
- Build cache behaves unexpectedly.
- Dockerfile commands work on the host but fail in the image.
- A container exits immediately or ignores signals.
- Runtime user, permissions, ports, volumes, DNS, or platform issues appear.
- The application works outside Docker but fails inside Docker.

## Principles

1. Reproduce with the narrowest command.
2. Capture exact Dockerfile, build context, target, platform, and build args.
3. Prefer read-only inspection before mutation.
4. Use plain progress logs for build diagnosis.
5. Debug one layer of failure at a time: build input, dependency install, output copy, entrypoint, runtime environment, network, volume, or platform.
6. Do not use `--no-cache`, `--pull`, `--privileged`, host networking, or volume deletion as a first response.
7. Ask before running long-lived containers or commands that mutate persistent volumes.

## Workflow Selection

- Use `workflows/build-failure-debugging-workflow.md` when a Dockerfile or Buildx build fails.
- Use `workflows/runtime-container-debugging-workflow.md` when the image builds but the container fails at runtime.

## Resources and Examples

- `resources/docker-debugging-checklist.md`
- `examples/build-debug-command-patterns.md`

## Safe Starting Commands

```bash
docker version
docker buildx version
docker context show
docker build --check -f Dockerfile .
docker build --progress=plain -f Dockerfile .
docker image inspect <image>
docker run --rm --entrypoint sh <image> -lc 'id && pwd && ls -la'
```

Use project-specific commands only after reading the Dockerfile, Compose files, and application entrypoint.
