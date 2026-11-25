---
name: dockerize
description: Writes a Dockerfile and .dockerignore for your project with layer caching, a slim final image and a non-root user.
disable-model-invocation: true
---

Containerize this project. Notes from the user: $ARGUMENTS

1. Detect the runtime from the manifest and lockfile (package.json, pyproject.toml, go.mod, Cargo.toml, pom.xml). Read the start script and note the port the app listens on. If a Dockerfile already exists, stop and ask whether to replace it.
2. Pick a pinned slim base tag (for example node:22-slim, python:3.12-slim, or a distroless runtime). Never use `latest`.
3. Order layers for caching: copy only the manifest and lockfile, install dependencies, then copy the source. Use a multi-stage build when a compiler or dev dependencies are needed, and copy only the built output into the final stage.
4. Create a non-root user and switch to it with USER before CMD. Set EXPOSE, a HEALTHCHECK if the app has a health route, and an exec-form CMD.
5. Write .dockerignore: .git, node_modules, build output, .env files, logs and test fixtures.
6. Run `docker build -t dockerize-check .` and report the image size. Start it briefly and confirm the port answers.

Show both files and the size, then ask before writing them to disk. Never bake secrets into the image.
