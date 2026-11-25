---
name: conduct-ask
description: "Ask a worker LLM (big-context Gemini first) a read-only question about the code, saving controller tokens"
argument-hint: "<question> [--save path.md]"
disable-model-invocation: true
allowed-tools: "Read, Bash(conductor-ai run ask:*), Bash(git status:*)"
---

Run in the background: `conductor-ai run ask the arguments the user gave`

Read the answer, spot-check one or two of its `path:line` citations, and give the user a concise answer, noting anything that looked wrong. If the summary warns that files changed, show `git status`.
