---
name: claude-api
description: Build apps with the Claude API or Anthropic SDK. TRIGGER when: code imports `anthropic`/`@anthropic-ai/sdk`/`claude_agent_sdk`, or user asks to use Claude API, Anthropic SDKs, or Agent SDK. DO NOT TRIGGER when: code imports `openai`/other AI SDK, general programming, or ML/data-science tasks.
license: Complete terms in LICENSE.txt
---

# claude api

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- `*.py`, `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile` 鈫?**Python** 鈥?read from `python/`
- `*.ts`, `*.tsx`, `package.json`, `tsconfig.json` 鈫?**TypeScript** 鈥?read from `typescript/`
- `*.js`, `*.jsx` (no `.ts` files present) 鈫?**TypeScript** 鈥?JS uses the same SDK, read from `typescript/`
- `*.java`, `pom.xml`, `build.gradle` 鈫?**Java** 鈥?read from `java/`
- `*.kt`, `*.kts`, `build.gradle.kts` 鈫?**Java** 鈥?Kotlin uses the Java SDK, read from `java/`
- `*.scala`, `build.sbt` 鈫?**Java** 鈥?Scala uses the Java SDK, read from `java/`
- `*.go`, `go.mod` 鈫?**Go** 鈥?read from `go/`
- `*.rb`, `Gemfile` 鈫?**Ruby** 鈥?read from `ruby/`

## Available sections

- Building LLM-Powered Applications with Claude
- Defaults
- Language Detection
- Language-Specific Feature Support
- Which Surface Should I Use?
- Decision Tree
- Should I Build an Agent?
- Architecture
- Current Models (cached: 2026-02-17)
- Thinking & Effort (Quick Reference)
- Compaction (Quick Reference)
- Reading Guide

## Bundled resources

- csharp
- curl
- go
- java
- php
- python
- ruby
- shared
- typescript

Open these resources only if the current task needs deeper detail or executable helpers.
