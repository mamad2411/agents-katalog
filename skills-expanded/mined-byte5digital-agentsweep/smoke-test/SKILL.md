---
name: smoke-test
description: Runs the smoke test against the local stack.
allowed-tools: Bash(sh scripts/smoke.sh:*)
---

# Smoke test

The stack listens on http://127.0.0.1:8080 while it is running locally. The
shared build machine on the office network answers at http://192.168.10.14:8080
and the container gateway at http://172.20.0.3:8080.
