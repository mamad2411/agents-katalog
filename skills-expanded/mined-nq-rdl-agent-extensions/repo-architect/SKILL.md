---
name: repo-architect
description: Use when asked to bootstrap, configure, or audit a GitHub repository's engineering conventions — git hooks, changelog, conventional commits, CI/CD workflows, PR/release flow, and repo-level settings (branch protection, CODEOWNERS, security). It surveys the repo, reports config gaps with severity, and applies fixes by delegating to the gh plugin's skills.
license: MIT
metadata:
  upstream: https://github.com/github/awesome-copilot/blob/main/agents/repo-architect.agent.md
  repo: https://github.com/nq-rdl/agent-extensions
---

# Configure Repo

Detect the repository’s stack and existing hooks, CI, release process, and settings. Default an audit to read-only findings ranked by severity; use the relevant gh skills for authorized bootstrap or updates. Keep one hooks manager and verify local checks and remote settings separately.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
