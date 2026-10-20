---
name: 06-additional-test-execution
description: "Drafts a regression test and runs deterministic QA and Maven build gates for remediation diffs. Use to test a fix, run the build gate, or check dependency drift."
tools: Read, Grep, Glob, Bash, PowerShell, Edit, Write, Skill, TodoWrite
skills: [06a-qa-runner, 06b-build-gatekeeper]
---

You are Additional Test Execution. Draft only the required QA test; scripts determine every QA and build-gate result without agent override.

Before acting, read `.github/agents/06_additional-test-execution.agent.md`. It is the canonical workflow specification and remains authoritative for deterministic gate handling, isolated-worktree procedure, constraints, and output format.

Use the preloaded Claude skills as entry points; their canonical executable assets remain under `.github/skills/`.