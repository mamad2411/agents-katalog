---
name: lang-dockerfile
description: Dockerfile multi-stage builds, non-root execution (USER directive), base image pinning, zero secret leakage, and Hadolint compliance.
---

# Dockerfile Hardening & Reliability Contract

## 1. Multi-Stage Builds & Minimal Runtime
- Multi-stage builds are mandatory for compiled and transpiled services: separate compiler tools from runtime artifacts.
- Target minimal runtime base images (distroless, scratch, or Alpine).

## 2. Rootless Execution & Privilege Separation
- Never run application processes as \`root\`.
- Always declare an explicit unprivileged user (\`USER 10001\` or \`USER appuser\`) prior to \`ENTRYPOINT\` or \`CMD\`.

## 3. Immutability & Secret Protection
- Base images must be pinned to explicit release versions or immutable SHA-256 digests (never \`:latest\`).
- Never embed credentials, private keys, or API tokens in image layers; utilize BuildKit secret mounts (\`--mount=type=secret\`).
- Prohibit unbounded \`COPY . .\` in the root directory without a restrictive \`.dockerignore\`.
- Declare an explicit \`HEALTHCHECK\` instruction for long-running service containers.\n