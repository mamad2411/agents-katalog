---
name: busy_loop
version: 1.0.0
license: MIT
---

# busy_loop

**TEST FIXTURE — not a real skill.**

This skill is a deliberate trap for gateway interrupt/timeout testing. Its
`handler` runs an infinite `while (true) {}` loop with a correct `tool_sha256`
in `/llms.txt`. A conforming gateway running the tool inside a QuickJS sandbox
with an interrupt handler / timeout MUST abort execution rather than hang.