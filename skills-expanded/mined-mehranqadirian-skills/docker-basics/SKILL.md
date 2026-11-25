---
name: docker-basics
description: Reviews, writes and troubleshoots Dockerfiles and container builds. Use whenever the user shares a Dockerfile or docker-compose file, asks how to containerize an app, shrink an image, speed up builds, stop running as root, handle secrets in images, or debug a container that exits, cannot be reached or has permission errors, even if they only say "my docker build is slow". Lints with a script, explains each finding and proposes a safer version.
---

# docker-basics

Review a Dockerfile for security, size and build-cache problems, then fix it with patterns that work. The linter reads the file only; it never builds or runs anything.

```
docker-basics/
├── SKILL.md
├── scripts/
│   └── lint_dockerfile.py     rules for root user, secrets, apt and pip cache, pinning, ADD, pipe-to-shell
└── references/
    └── patterns.md            solid images, multi-stage builds, .dockerignore, secrets, pinning, failures
```

## When to use

- Writing a Dockerfile for a new app
- Reviewing an existing Dockerfile before it ships
- Image too large, builds too slow, container runs as root
- A secret may have been baked into an image
- Container exits immediately, cannot be reached, or has file permission errors

## Workflow

1. **Lint**: `python3 scripts/lint_dockerfile.py Dockerfile`. Errors need fixing; warnings are likely problems; info is advice. Use `--strict` to fail on warnings.
2. **Explain each finding** in one sentence of why it matters, then show the fix. The most serious are secrets in `ENV` or `ARG`, `apt-get update` alone in a layer, and missing `-y`.
3. **Apply the patterns** from `references/patterns.md`: pin the base image, copy dependency manifests before the code, combine install and cleanup in one `RUN`, add a non-root `USER`, add `.dockerignore`, use multi-stage builds for compiled output.
4. **Handle secrets properly**: runtime environment or build secrets. If a secret was ever committed or baked in, tell the user to rotate it, since deleting a later layer does not remove it from history (see `secrets-hygiene`).
5. **Re-lint**, then give the build and run commands the user should try, and what to expect.
6. **If troubleshooting**, ask for `docker logs`, the exact command, and the host architecture, and use the failure table in the reference.

## Rules

- Never claim an image was built or run unless you ran it; say what you checked and what you did not
- Prefer a version tag or digest over `latest`
- Do not suggest `--privileged`, `chmod 777` or mounting the Docker socket to make an error go away; find the cause
- One process per container is the default; explain exceptions
- Keep changes minimal and explain trade-offs (alpine versus slim, size versus compatibility)

## What to report back

| Field | Content |
|-------|---------|
| Findings | rule, line, severity, why it matters |
| Fixed Dockerfile | with a short comment per change |
| Not verified | build or runtime behavior you could not test |
| Next steps | `.dockerignore`, health check, secret rotation, CI scan |

## Related skills

- `github-actions`: build and push images in CI safely
- `secrets-hygiene`: scan for credentials and respond to leaks
- `linux-troubleshooting`: disk, memory and port problems on the host
