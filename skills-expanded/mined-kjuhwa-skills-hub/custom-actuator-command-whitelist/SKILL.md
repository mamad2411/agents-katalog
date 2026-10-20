---
tags: [backend, custom, actuator, command, whitelist]
name: custom-actuator-command-whitelist
description: Expose safe remote OS command execution on a Spring Boot service via a custom Actuator endpoint, restricted by a command whitelist, an argument sanitizer, and an execution timeout.
category: backend
version: 1.0.0
source_project: lucida-health
trigger: Ops needs to run read-only diagnostic shell commands (ps, df, free, netstat) on remote services without SSH, with strong guardrails.
---

See `content.md`.
