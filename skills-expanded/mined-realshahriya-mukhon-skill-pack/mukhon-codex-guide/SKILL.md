---
name: mukhon-codex-guide
description: Comprehensive reference, prompt patterns, and architectural guide for OpenAI Codex and coding agents (including GitHub Copilot CLI, OpenAI Canvas, and custom Agent SDK runners). Covers repository-level instructions, structured tool-calling schemas, AST-guided editing, multi-file diff generation, and autonomous test-driven loops. Use when configuring or orchestrating Codex-based agents.
license: MIT
---

# OpenAI Codex & Coding Agents Guide

Comprehensive engineering reference for OpenAI Codex, OpenAI Agentic Coding SDKs, and GitHub Copilot CLI integrations.

## When to Use This Skill

- Building, configuring, or interacting with OpenAI Codex-powered development tools.
- Writing repository-level instruction files (`.github/copilot-instructions.md`, `.codex/instructions.md`).
- Defining structured function/tool schemas for code execution and AST manipulation.
- Optimizing code generation prompts for complex full-stack refactoring and diff applications.
- Orchestrating Planner-Coder-Critic multi-agent programming loops with Codex.

## System Architecture

```
[ Developer Prompt / GitHub Issue ]
                 │
                 ▼
[ Codex Agent Runtime / OpenAI Responses API ]
                 │
       ┌─────────┴─────────┐
       ▼                   ▼
[ Tool-Calling Loop ]   [ Diff Engine ]
 - ast_search            - Unified diff generation
 - file_patch            - Syntax validation
 - run_test_suite        - Lint check
```

## Detailed Reference Subdocs

1. [CLI & Runtime Patterns](references/cli.md): Scripting headless Codex workflows, OpenAI CLI integrations, and API request schemas.
2. [Repository Instructions](references/instructions.md): Designing `.github/copilot-instructions.md` and project context memory.
3. [Tool-Calling Schemas](references/tool-calling.md): JSON schema contracts for code search, file editing, and sandboxed test execution.
4. [Best Practices & Quality Gates](references/best-practices.md): Token conservation, hallucination prevention, and test-driven validation loops.
