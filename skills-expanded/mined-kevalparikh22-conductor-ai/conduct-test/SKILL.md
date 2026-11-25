---
name: conduct-test
description: "Delegate writing tests to a free/cheap model, then verify"
argument-hint: "<what to test, e.g. \"src/auth/reset.ts edge cases\">"
disable-model-invocation: true
allowed-tools: "Read, Bash(conductor-ai:*), Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git stash push:*)"
---

You are the controller. Make sure the tree is clean, then run in the background:
`conductor-ai run test "Write tests for: the arguments the user gave" --files <the source files under test>`

Check `conductor-ai diff`: the tests must test real behaviour (not just mocks), follow the existing test style, and must not change production code. If verify passes and the tests are meaningful, commit (`test: ...`). If the worker reports a real bug, tell the user. If the tests are weak, retry once with `--note`, then write them yourself.
