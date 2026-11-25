---
name: verify-plan
description: "Prepare verification commands without running them using the dev++ workflow. Use when the user invokes /verify-plan or asks to plan tests, lint, type checks, builds, smoke checks, screenshots, CI reproduction, or manual verification."
---

# verify-plan

Prepare a verification plan for the scope supplied after the slash command.

Rules:
- Discover canonical commands from README, AGENTS, contribution docs, package scripts, Makefile/task files, CI config, Docker files, and scripts directories.
- Respect project restrictions such as Docker-only workflows, pinned tools, and no-test-without-approval rules.
- Prefer focused checks before broad suites.
- Do not run tests, lint, builds, servers, package installs, screenshots, smoke checks, or CI reproduction.
- Output exact proposed commands, working directories, expected coverage, cost/risk, and what approval would be needed to run them.
