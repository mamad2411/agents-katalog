---
name: hello-world
version: 1.0.0
description: Minimal hello-world skill — proves the Aether toolchain works end-to-end.
category: productivity
author: aether-demo
tags: [demo, hello, getting-started]
triggers:
  - hello
  - greet
  - introduce
---

# hello-world

## System Prompt

You are the Aether "hello-world" demo skill. When invoked, you execute a small JavaScript snippet and report the result. Use this to verify that the gateway, sandbox, and skill registry are wired up correctly.

## Code

```javascript
// Returns a deterministic greeting + the current UTC timestamp.
// The sandbox enforces a 5-second timeout and blocks network access.
const greeting = "Hello from Aether Agent";
const when = new Date().toISOString();
return { ok: true, output: `${greeting} @ ${when}`, when };
```
