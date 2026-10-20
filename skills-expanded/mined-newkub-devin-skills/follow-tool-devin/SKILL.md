---
name: follow-tool-devin
description: Devin/Cascade AI coding assistant for autonomous software engineering
argument-hint: "[scope]"
related:
  - follow-tool-devin-cli
  - follow-create-plugins
  - update-devin
  - follow-devin-global-skills
  - follow-tool-usage
  - follow-best-practice
  - setup-cicd
  - deep-review-codebase
  - run-verify
---

## Goal

Use this skill to understand and operate the Devin/Cascade AI coding assistant for autonomous software development, code generation, debugging, and testing

## Scope

Use for:
- Operating Devin Desktop and Cascade in the Windsurf IDE
- Understanding the AI models (SWE-2, SWE-1.7, SWE-1.6, SWE-1-mini, swe-grep, swe-check)
- Using Spaces and the Agent Client Protocol (ACP)
- Writing effective prompts for coding agents
- Debugging and reviewing code produced by agents
- Managing fleets of local and cloud agents

- Boundary: this skill covers using Devin/Cascade from the user side — for the terminal `devin` CLI (sessions, modes, MCP, plugins, scripted runs) use `/follow-tool-devin-cli`; for updating this machine's Devin CLI/skills use `/update-devin`; for global skills rules and conventions see `/follow-devin-global-skills`
- Latest model: `SWE-2` (released 2026-09-10, post-trained from Kimi K3 2.8T params) (verified 2026-09-13)
- References: [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### 1. Verify Installation

> Goal: the Devin CLI is ready to use on this machine

1. Run `devin --version` to confirm the CLI is installed (installed via Devin Desktop / Cognition distribution — there is no public registry); for the full CLI workflow run /follow-tool-devin-cli
2. Run `devin --help` to see the command surface the current version supports
3. If missing → install from https://devin.ai — the npm package `devin` is an unrelated package, do not install it
4. For CLI/skills updates, use `/update-devin`

### 2. Start Session

> Goal: open a session on the right project/branch

1. Run `devin` to start an interactive session — pass `--project`, `--branch`, `--issue` per the task context
2. Use Spaces (shared context + Git worktrees) when running several agents concurrently
3. Use the Agent Client Protocol (ACP) when integrating with other editors/agents

### 3. Select Model

> Goal: pick the model that fits the task

1. Choose from Rules → Model Selection: `SWE-2` is the default for coding tasks, `SWE-1-mini` for autocomplete, `swe-grep`/`swe-check` for retrieval and quick review
2. Use `SWE-1.7 Lightning` when low latency is needed without losing intelligence

### 4. Write Effective Prompts

> Goal: prompts that are clear and divide the work

1. Write specific prompts with context, requirements, and constraints
2. Break complex tasks into sub-tasks agents can do one at a time
3. Attach examples/code snippets when a specific output format is needed

### 5. Review And Verify Output

> Goal: agent-produced code is safe and actually works

1. Review the diffs agents produce — use `/deep-review-codebase` for large changes
2. Use `swe-check` for quick reviews while working
3. Do `/run-verify` (lint, typecheck, tests) before accepting
4. Check for security issues and secrets before deploying

## Rules

### 1. Model Selection

- Pick the model by task:
  - `SWE-2`: latest flagship — frontier-level coding, cost-efficient (multi-effort reasoning)
  - `SWE-1.7`: previous flagship, software engineering agents
  - `SWE-1.7 Lightning`: SWE-1.7 on Cerebras — lower latency, equal intelligence
  - `SWE-1.6` / `SWE-1.6 Fast`: prior generation — general / speed priority
  - `SWE-1-mini`: real-time autocomplete (Tab), low latency
  - `swe-grep`: context retrieval and Fast Context
  - `swe-check`: quick review — lightweight code review

### 2. Prompt Engineering

- Write clear, specific prompts
- State the context and requirements in detail
- Use examples and code snippets when needed
- Split complex tasks into sub-tasks

### 3. Code Review

- Review agent-produced code closely
- Test code before deploying
- Check for security vulnerabilities
- Verify performance and scalability

### 4. Security

- Never put sensitive data in prompts
- Review code for security issues
- Use environment variables for secrets
- Follow security best practices

- Use /follow-create-plugins (devin) if needed
- Use /update-devin-global-subagents if needed
- Use /follow-devin-global-skills if needed
- Use /follow-tool-usage if needed
- Use /follow-best-practice if needed
- Use /setup-cicd if needed
- Use /deep-review-codebase if needed
- Use /run-verify if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Devin/Cascade understood and used effectively
- Prompts written that make agents work better
- Agent code debugged and reviewed with confidence
- Agent-produced code deployed safely
- Agent workflow performance optimized
