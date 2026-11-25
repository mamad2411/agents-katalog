---
name: claude-cli-from-jvm-via-node-wrapper
description: Shell out to the `claude` CLI from a JVM / Spring Boot app by going through a tiny Node.js wrapper that supplies the required empty stdin — the CLI hangs when invoked with a directly-inherited TTY-less stdin from ProcessBuilder.
category: ai
tags: [claude-cli, subprocess, spring-boot, processbuilder, node-wrapper, stdin, hang]
triggers: ["claude -p", "ProcessBuilder", "claude CLI", "node claude-runner", "execFileSync", "subprocess hang", "cli stdin"]
source_project: webtoon_ai_project_with_wrapper
version: 0.1.0-draft
---
