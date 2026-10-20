---
name: qwen-code-docs
description: >-
  USE FOR: Reading, searching, or referencing Qwen Code documentation (docs directory, CLI reference, configuration, features, MCP, and design docs).
  DO NOT USE FOR: Executing Qwen Code commands; use appropriate development skills when implementing plugins/extensions.
  You MUST load this skill when you need to consult Qwen Code documentation while working with or using Qwen Code.
license: MIT
---

# Qwen Code Docs

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## When to Use

- **Documentation Lookup**: Finding specific Qwen Code doc pages for features, channels, auto-mode, configuration, and settings.
- **Developer Reference**: Fetching architecture docs, tool specs (file system, MCP server, web fetch), or SDK docs for Java/Python/TypeScript.
- **Design & Architecture**: Looking up plans, structured output design, channels design, worktree specs, telemetry gaps, and E2E test reports.

## When Not to Use

- **Running Qwen Code Commands**: Interacting with a live session — use direct CLI execution instead.
- **Writing Extensions/Skills**: Authoring new agent skills — use the appropriate development skill.

## Core Process

1. **Identify the Topic**: Determine the docs area (users, developers, design, plans, superpowers/plans, e2e-tests, or root).
2. **Fetch Doc Content**: Build the URL path using the pattern:
   ```text
    https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/<section>/<filename>
   ```
3. **Process Content**: Extract relevant information to answer the query.

Use `webfetch` or equivalent to retrieve raw markdown files.

## References

### Docs (root)

- [docs/index.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/index.md)
  - USE FOR: Qwen Code Documentation; trigger words: documentation, index, overview, navigation, table-of-contents

### Design

- [docs/design/2026-05-15-async-memory-recall-design.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/2026-05-15-async-memory-recall-design.md)
  - USE FOR: Async Memory Recall — Design Spec; trigger words: design-spec, architecture, tradeoffs, implementation-notes, async, memory, context-retention, long-running-sessions, recall
- [docs/design/adaptive-output-token-escalation/adaptive-output-token-escalation-design.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/adaptive-output-token-escalation/adaptive-output-token-escalation-design.md)
  - USE FOR: Adaptive Output Token Escalation Design; trigger words: design-spec, architecture, tradeoffs, implementation-notes, adaptive, output, token, escalation
- [docs/design/auth/motivation.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/auth/motivation.md)
  - USE FOR: Auth Provider Registry Motivation; trigger words: design-spec, architecture, tradeoffs, implementation-notes, auth, authentication, login, credentials, api-key, motivation
- [docs/design/auto-compaction-threshold-redesign.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/auto-compaction-threshold-redesign.md)
  - USE FOR: Auto-Compaction Threshold Redesign; trigger words: design-spec, architecture, tradeoffs, implementation-notes, auto, compaction, threshold, redesign
- [docs/design/auto-memory/memory-system.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/auto-memory/memory-system.md)
  - USE FOR: Memory Management System; trigger words: design-spec, architecture, tradeoffs, implementation-notes, auto, memory, context-retention, long-running-sessions, system
- [docs/design/channels/channels-design.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/channels/channels-design.md)
  - USE FOR: Channels Design; trigger words: design-spec, architecture, tradeoffs, implementation-notes, channels
- [docs/design/compact-mode/compact-mode-design.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/compact-mode/compact-mode-design.md)
  - USE FOR: Compact Mode Design: Competitive Analysis & Optimization; trigger words: design-spec, architecture, tradeoffs, implementation-notes, compact, mode
- [docs/design/compaction-image-stripping/compaction-image-stripping-design.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/compaction-image-stripping/compaction-image-stripping-design.md)
  - USE FOR: Compaction Image Stripping + Token Estimation Fix; trigger words: design-spec, architecture, tradeoffs, implementation-notes, compaction, image, stripping
- [docs/design/custom-api-key-auth-wizard-prd.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/custom-api-key-auth-wizard-prd.md)
  - USE FOR: Custom API Key Auth Wizard PRD; trigger words: design-spec, architecture, tradeoffs, implementation-notes, custom, api, key, auth, authentication, login
- [docs/design/customize-banner-area/customize-banner-area.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/customize-banner-area/customize-banner-area.md)
  - USE FOR: Customize Banner Area Design; trigger words: design-spec, architecture, tradeoffs, implementation-notes, customize, banner, area
- [docs/design/customize-banner-area/customize-banner-area.zh-CN.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/customize-banner-area/customize-banner-area.zh-CN.md)
  - USE FOR: Customize Banner Area Design (Chinese); trigger words: design-spec, architecture, tradeoffs, implementation-notes, customize, banner, area, zh, cn
- [docs/design/fork-subagent/fork-subagent-design.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/fork-subagent/fork-subagent-design.md)
  - USE FOR: Fork Subagent Design; trigger words: design-spec, architecture, tradeoffs, implementation-notes, fork, subagent
- [docs/design/markdown-syntax-extension.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/markdown-syntax-extension.md)
  - USE FOR: Markdown Syntax Extension Design; trigger words: design-spec, architecture, tradeoffs, implementation-notes, markdown, syntax, extension, extensions, plugins, customization
- [docs/design/openrouter-auth-and-models.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/openrouter-auth-and-models.md)
  - USE FOR: OpenRouter Auth and Model Management Design; trigger words: design-spec, architecture, tradeoffs, implementation-notes, openrouter, auth, authentication, login, credentials, api-key
- [docs/design/prompt-suggestion/prompt-suggestion-design.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/prompt-suggestion/prompt-suggestion-design.md)
  - USE FOR: Prompt Suggestion (NES) Design; trigger words: design-spec, architecture, tradeoffs, implementation-notes, prompt, suggestion
- [docs/design/prompt-suggestion/prompt-suggestion-implementation.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/prompt-suggestion/prompt-suggestion-implementation.md)
  - USE FOR: Prompt Suggestion Implementation Status; trigger words: design-spec, architecture, tradeoffs, implementation-notes, prompt, suggestion, implementation
- [docs/design/prompt-suggestion/speculation-design.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/prompt-suggestion/speculation-design.md)
  - USE FOR: Speculation Engine Design; trigger words: design-spec, architecture, tradeoffs, implementation-notes, prompt, suggestion, speculation
- [docs/design/session-recap/session-recap-design.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/session-recap/session-recap-design.md)
  - USE FOR: Session Recap Design; trigger words: design-spec, architecture, tradeoffs, implementation-notes, session, recap
- [docs/design/session-title/session-title-design.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/session-title/session-title-design.md)
  - USE FOR: Session Title Design; trigger words: design-spec, architecture, tradeoffs, implementation-notes, session, title
- [docs/design/skill-nudge/skill-nudge.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/skill-nudge/skill-nudge.md)
  - USE FOR: AutoSkill Design Document; trigger words: design-spec, architecture, tradeoffs, implementation-notes, skill, nudge
- [docs/design/slash-command/compare.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/slash-command/compare.md)
  - USE FOR: Qwen Code Command Module Refactoring Plan; trigger words: design-spec, architecture, tradeoffs, implementation-notes, slash, command, compare
- [docs/design/slash-command/phase1-technical-design.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/slash-command/phase1-technical-design.md)
  - USE FOR: Phase 1 Technical Design: Infrastructure Reconstruction; trigger words: design-spec, architecture, tradeoffs, implementation-notes, slash, command, phase1, technical
- [docs/design/slash-command/phase2-technical-design.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/slash-command/phase2-technical-design.md)
  - USE FOR: Phase 2 Technical Design: Capability Extension; trigger words: design-spec, architecture, tradeoffs, implementation-notes, slash, command, phase2, technical
- [docs/design/slash-command/phase3-technical-design.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/slash-command/phase3-technical-design.md)
  - USE FOR: Phase 3 Technical Design: Experience Alignment; trigger words: design-spec, architecture, tradeoffs, implementation-notes, slash, command, phase3, technical
- [docs/design/slash-command/roadmap.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/slash-command/roadmap.md)
  - USE FOR: Slash Command Refactoring Roadmap; trigger words: design-spec, architecture, tradeoffs, implementation-notes, slash, command, roadmap, future-work, planned-features
- [docs/design/structured-output/structured-output.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/structured-output/structured-output.md)
  - USE FOR: Structured Output (`--json-schema`) — Design; trigger words: design-spec, architecture, tradeoffs, implementation-notes, structured, structured-output, json-schema, typed-response, output
- [docs/design/telemetry-llm-request-timing-design.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/telemetry-llm-request-timing-design.md)
  - USE FOR: LLM Request Timing Decomposition Design (P3 Phase 4); trigger words: design-spec, architecture, tradeoffs, implementation-notes, telemetry, observability, metrics, tracing, llm, request
- [docs/design/telemetry-resource-attributes-design.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/telemetry-resource-attributes-design.md)
  - USE FOR: Telemetry: Custom Resource Attributes + Metric Cardinality Controls; trigger words: design-spec, architecture, tradeoffs, implementation-notes, telemetry, observability, metrics, tracing, resource, attributes
- [docs/design/tool-use-summary/tool-use-summary-design.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/tool-use-summary/tool-use-summary-design.md)
  - USE FOR: Tool-Use Summary Design; trigger words: design-spec, architecture, tradeoffs, implementation-notes, tool, use, summary
- [docs/design/workflow-tracing-gaps.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/workflow-tracing-gaps.md)
  - USE FOR: Workflow-Level Span Granularity Analysis (P1); trigger words: design-spec, architecture, tradeoffs, implementation-notes, workflow, tracing, gaps
- [docs/design/worktree.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/design/worktree.md)
  - USE FOR: Worktree General Capability Design; trigger words: design-spec, architecture, tradeoffs, implementation-notes, worktree, parallel-branches, isolated-workspace

### Developers

- [docs/developers/architecture.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/architecture.md)
  - USE FOR: Qwen Code Architecture Overview; trigger words: developer-guide, api-reference, integration, implementation, architecture
- [docs/developers/channel-plugins.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/channel-plugins.md)
  - USE FOR: Channel Plugin Developer Guide; trigger words: developer-guide, api-reference, integration, implementation, channel, channels, messaging-integration, connector, plugins
- [docs/developers/contributing.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/contributing.md)
  - USE FOR: How to Contribute; trigger words: developer-guide, api-reference, integration, implementation, contributing
- [docs/developers/daemon-client-adapters/channel-web.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/daemon-client-adapters/channel-web.md)
  - USE FOR: Channel And Web Backend Daemon Adapter Draft; trigger words: developer-guide, api-reference, integration, implementation, daemon, client, adapters, channel, channels, messaging-integration
- [docs/developers/daemon-client-adapters/ide.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/daemon-client-adapters/ide.md)
  - USE FOR: IDE Daemon Adapter Draft; trigger words: developer-guide, api-reference, integration, implementation, daemon, client, adapters, ide
- [docs/developers/daemon-client-adapters/tui.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/daemon-client-adapters/tui.md)
  - USE FOR: TUI Daemon Adapter Draft; trigger words: developer-guide, api-reference, integration, implementation, daemon, client, adapters, tui
- [docs/developers/development/deployment.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/development/deployment.md)
  - USE FOR: Qwen Code Execution and Deployment; trigger words: developer-guide, api-reference, integration, implementation, development, deployment
- [docs/developers/development/integration-tests.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/development/integration-tests.md)
  - USE FOR: Integration Tests; trigger words: developer-guide, api-reference, integration, implementation, development
- [docs/developers/development/issue-and-pr-automation.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/development/issue-and-pr-automation.md)
  - USE FOR: Automation and Triage Processes; trigger words: developer-guide, api-reference, integration, implementation, development, issue, and, pr, automation
- [docs/developers/development/npm.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/development/npm.md)
  - USE FOR: Package Overview; trigger words: developer-guide, api-reference, integration, implementation, development, npm
- [docs/developers/development/telemetry.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/development/telemetry.md)
  - USE FOR: Observability with OpenTelemetry; trigger words: developer-guide, api-reference, integration, implementation, development, telemetry, observability, metrics, tracing
- [docs/developers/examples/daemon-client-quickstart.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/examples/daemon-client-quickstart.md)
  - USE FOR: DaemonClient quickstart (TypeScript); trigger words: developer-guide, api-reference, integration, implementation, examples, daemon, client
- [docs/developers/examples/proxy-script.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/examples/proxy-script.md)
  - USE FOR: Example Proxy Script; trigger words: developer-guide, api-reference, integration, implementation, examples, proxy, script
- [docs/developers/qwen-serve-protocol.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/qwen-serve-protocol.md)
  - USE FOR: `qwen serve` HTTP protocol reference; trigger words: developer-guide, api-reference, integration, implementation, serve, protocol
- [docs/developers/roadmap.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/roadmap.md)
  - USE FOR: Qwen Code Roadmap; trigger words: developer-guide, api-reference, integration, implementation, roadmap, future-work, planned-features
- [docs/developers/sdk-java.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/sdk-java.md)
  - USE FOR: Qwen Code Java SDK; trigger words: developer-guide, api-reference, integration, implementation, sdk, client-library, api-usage, java
- [docs/developers/sdk-python.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/sdk-python.md)
  - USE FOR: Python SDK; trigger words: developer-guide, api-reference, integration, implementation, sdk, client-library, api-usage, python
- [docs/developers/sdk-typescript.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/sdk-typescript.md)
  - USE FOR: TypeScript SDK; trigger words: developer-guide, api-reference, integration, implementation, sdk, client-library, api-usage, typescript
- [docs/developers/tools/exit-plan-mode.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/tools/exit-plan-mode.md)
  - USE FOR: Exit Plan Mode Tool (`exit_plan_mode`); trigger words: developer-guide, api-reference, integration, implementation, tools, exit, plan, mode
- [docs/developers/tools/file-system.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/tools/file-system.md)
  - USE FOR: Qwen Code file system tools; trigger words: developer-guide, api-reference, integration, implementation, tools, file, system
- [docs/developers/tools/introduction.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/tools/introduction.md)
  - USE FOR: Qwen Code tools; trigger words: developer-guide, api-reference, integration, implementation, tools
- [docs/developers/tools/mcp-server.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/tools/mcp-server.md)
  - USE FOR: MCP servers with Qwen Code; trigger words: developer-guide, api-reference, integration, implementation, tools, mcp, model-context-protocol, tool-integration, servers, server
- [docs/developers/tools/multi-file.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/tools/multi-file.md)
  - USE FOR: Multi File Read Tool (`read_many_files`); trigger words: developer-guide, api-reference, integration, implementation, tools, multi, file
- [docs/developers/tools/sandbox.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/tools/sandbox.md)
  - USE FOR: Sandbox Tool (`sandbox`); trigger words: developer-guide, api-reference, integration, implementation, tools, sandbox, permissions, execution-safety
- [docs/developers/tools/shell.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/tools/shell.md)
  - USE FOR: Shell Tool (`run_shell_command`); trigger words: developer-guide, api-reference, integration, implementation, tools, shell, shell-commands, terminal-execution, command-runner
- [docs/developers/tools/task.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/tools/task.md)
  - USE FOR: Task Tool (`task`); trigger words: developer-guide, api-reference, integration, implementation, tools, task, task-delegation, sub-agent, parallel-work
- [docs/developers/tools/todo-write.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/tools/todo-write.md)
  - USE FOR: Todo Write Tool (`todo_write`); trigger words: developer-guide, api-reference, integration, implementation, tools, todo, write
- [docs/developers/tools/web-fetch.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/tools/web-fetch.md)
  - USE FOR: Web Fetch Tool (`web_fetch`); trigger words: developer-guide, api-reference, integration, implementation, tools, web, fetch
- [docs/developers/tools/web-search.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/developers/tools/web-search.md)
  - USE FOR: Web Search; trigger words: developer-guide, api-reference, integration, implementation, tools, web, search

### E2E Tests

- [docs/e2e-tests/2026-05-18-qwen-memory-benchmark-report.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/e2e-tests/2026-05-18-qwen-memory-benchmark-report.md)
  - USE FOR: Qwen Code Runtime Memory Benchmark Report; trigger words: benchmark, e2e-tests, performance, diagnostics, memory, context-retention, long-running-sessions, latency, throughput, report
- [docs/e2e-tests/2026-05-19-oom-reproduction-report.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/e2e-tests/2026-05-19-oom-reproduction-report.md)
  - USE FOR: OOM Stress Test and Long Task Replay Report; trigger words: benchmark, e2e-tests, performance, diagnostics, oom, out-of-memory, memory-pressure, stress-testing, reproduction, report
- [docs/e2e-tests/2026-05-19-qwen-runtime-diagnostics-benchmark-report.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/e2e-tests/2026-05-19-qwen-runtime-diagnostics-benchmark-report.md)
  - USE FOR: Qwen Code Runtime Diagnostics Benchmark Report; trigger words: benchmark, e2e-tests, performance, diagnostics, runtime, latency, throughput, report
- [docs/e2e-tests/2026-05-21-qwen-0.15.11-default-heap-oom-stress-report.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/e2e-tests/2026-05-21-qwen-0.15.11-default-heap-oom-stress-report.md)
  - USE FOR: Qwen Code 0.15.11 Default Heap OOM Stress Test Report; trigger words: benchmark, e2e-tests, performance, diagnostics, default, heap, oom, out-of-memory, memory-pressure, stress-testing
- [docs/e2e-tests/worktree-phase-c.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/e2e-tests/worktree-phase-c.md)
  - USE FOR: Worktree Phase C E2E Test Plan; trigger words: benchmark, e2e-tests, performance, diagnostics, worktree, parallel-branches, isolated-workspace
- [docs/e2e-tests/worktree.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/e2e-tests/worktree.md)
  - USE FOR: Worktree Feature E2E Test Plan (Phase A + B); trigger words: benchmark, e2e-tests, performance, diagnostics, worktree, parallel-branches, isolated-workspace

### Plans

- [docs/plans/2026-03-22-agent-tool-display-design.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/plans/2026-03-22-agent-tool-display-design.md)
  - USE FOR: Agent Tool Display Implementation Plan; trigger words: implementation-plan, roadmap, milestones, execution-plan, agent, tool, display
- [docs/plans/2026-05-18-qwen-runtime-memory-investigation.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/plans/2026-05-18-qwen-runtime-memory-investigation.md)
  - USE FOR: Qwen Code Runtime Memory Investigation Plan; trigger words: implementation-plan, roadmap, milestones, execution-plan, runtime, memory, context-retention, long-running-sessions, investigation
- [docs/plans/memory-diagnostics-reference-design.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/plans/memory-diagnostics-reference-design.md)
  - USE FOR: Memory Diagnostics Reference Design; trigger words: implementation-plan, roadmap, milestones, execution-plan, memory, context-retention, long-running-sessions, diagnostics

### Superpowers Plans

- [docs/superpowers/plans/2026-05-15-worktree-phase-c.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/superpowers/plans/2026-05-15-worktree-phase-c.md)
  - USE FOR: Worktree Phase C Implementation Plan; trigger words: superpowers, advanced-features, implementation-plan, worktree, parallel-branches, isolated-workspace

### Users

- [docs/users/common-workflow.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/common-workflow.md)
  - USE FOR: Common workflows; trigger words: user-guide, configuration, features, how-to, common, workflow
- [docs/users/configuration/auth.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/configuration/auth.md)
  - USE FOR: Authentication; trigger words: user-guide, configuration, features, how-to, settings, setup, auth, authentication, login, credentials
- [docs/users/configuration/model-providers.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/configuration/model-providers.md)
  - USE FOR: Model Providers; trigger words: user-guide, configuration, features, how-to, settings, setup, model, providers
- [docs/users/configuration/qwen-ignore.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/configuration/qwen-ignore.md)
  - USE FOR: Ignoring Files; trigger words: user-guide, configuration, features, how-to, settings, setup, ignore
- [docs/users/configuration/settings.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/configuration/settings.md)
  - USE FOR: Qwen Code Configuration; trigger words: user-guide, configuration, features, how-to, settings, setup
- [docs/users/configuration/themes.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/configuration/themes.md)
  - USE FOR: Themes; trigger words: user-guide, configuration, features, how-to, settings, setup, themes
- [docs/users/configuration/trusted-folders.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/configuration/trusted-folders.md)
  - USE FOR: Trusted Folders; trigger words: user-guide, configuration, features, how-to, settings, setup, trusted, folders
- [docs/users/extension/extension-releasing.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/extension/extension-releasing.md)
  - USE FOR: Extension Releasing; trigger words: user-guide, configuration, features, how-to, extension, extensions, plugins, customization, releasing
- [docs/users/extension/getting-started-extensions.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/extension/getting-started-extensions.md)
  - USE FOR: Getting Started with Qwen Code Extensions; trigger words: user-guide, configuration, features, how-to, extension, extensions, plugins, customization, getting, started
- [docs/users/extension/introduction.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/extension/introduction.md)
  - USE FOR: Qwen Code Extensions; trigger words: user-guide, configuration, features, how-to, extension, extensions, plugins, customization
- [docs/users/features/approval-mode.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/approval-mode.md)
  - USE FOR: Approval Mode; trigger words: user-guide, configuration, features, how-to, approval, mode
- [docs/users/features/arena.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/arena.md)
  - USE FOR: Agent Arena; trigger words: user-guide, configuration, features, how-to, arena
- [docs/users/features/auto-mode.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/auto-mode.md)
  - USE FOR: Auto Mode; trigger words: user-guide, configuration, features, how-to, auto, mode
- [docs/users/features/channels/dingtalk.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/channels/dingtalk.md)
  - USE FOR: DingTalk (Dingtalk); trigger words: user-guide, configuration, features, how-to, channels, dingtalk
- [docs/users/features/channels/overview.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/channels/overview.md)
  - USE FOR: Channels; trigger words: user-guide, configuration, features, how-to, channels
- [docs/users/features/channels/plugins.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/channels/plugins.md)
  - USE FOR: Custom Channel Plugins; trigger words: user-guide, configuration, features, how-to, channels, plugins
- [docs/users/features/channels/telegram.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/channels/telegram.md)
  - USE FOR: Telegram; trigger words: user-guide, configuration, features, how-to, channels, telegram
- [docs/users/features/channels/weixin.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/channels/weixin.md)
  - USE FOR: WeChat (Weixin); trigger words: user-guide, configuration, features, how-to, channels, weixin
- [docs/users/features/checkpointing.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/checkpointing.md)
  - USE FOR: Checkpointing; trigger words: user-guide, configuration, features, how-to, checkpointing
- [docs/users/features/code-review.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/code-review.md)
  - USE FOR: Code Review; trigger words: user-guide, configuration, features, how-to, review
- [docs/users/features/commands.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/commands.md)
  - USE FOR: Commands; trigger words: user-guide, configuration, features, how-to, commands, slash-commands, cli-commands, command-reference
- [docs/users/features/dual-output.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/dual-output.md)
  - USE FOR: Dual Output; trigger words: user-guide, configuration, features, how-to, dual, output
- [docs/users/features/followup-suggestions.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/followup-suggestions.md)
  - USE FOR: Followup Suggestions; trigger words: user-guide, configuration, features, how-to, followup, suggestions
- [docs/users/features/headless.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/headless.md)
  - USE FOR: Headless Mode; trigger words: user-guide, configuration, features, how-to, headless
- [docs/users/features/hooks.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/hooks.md)
  - USE FOR: Qwen Code Hooks; trigger words: user-guide, configuration, features, how-to, hooks, automation, event-triggers
- [docs/users/features/language.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/language.md)
  - USE FOR: Internationalization (i18n) & Language; trigger words: user-guide, configuration, features, how-to, language
- [docs/users/features/lsp.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/lsp.md)
  - USE FOR: Language Server Protocol (LSP) Support; trigger words: user-guide, configuration, features, how-to, lsp, language-server-protocol, editor-integration, code-intelligence
- [docs/users/features/markdown-rendering.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/markdown-rendering.md)
  - USE FOR: Markdown Rendering; trigger words: user-guide, configuration, features, how-to, markdown, rendering
- [docs/users/features/mcp.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/mcp.md)
  - USE FOR: Connect Qwen Code to tools via MCP; trigger words: user-guide, configuration, features, how-to, mcp, model-context-protocol, tool-integration, servers
- [docs/users/features/memory.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/memory.md)
  - USE FOR: Memory; trigger words: user-guide, configuration, features, how-to, memory, context-retention, long-running-sessions
- [docs/users/features/sandbox.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/sandbox.md)
  - USE FOR: Sandbox; trigger words: user-guide, configuration, features, how-to, sandbox, permissions, execution-safety
- [docs/users/features/scheduled-tasks.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/scheduled-tasks.md)
  - USE FOR: Run Prompts on a Schedule; trigger words: user-guide, configuration, features, how-to, scheduled, tasks
- [docs/users/features/skills.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/skills.md)
  - USE FOR: Agent Skills; trigger words: user-guide, configuration, features, how-to, skills
- [docs/users/features/status-line.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/status-line.md)
  - USE FOR: Status Line; trigger words: user-guide, configuration, features, how-to, status, status-line, ux-feedback, session-state, line
- [docs/users/features/structured-output.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/structured-output.md)
  - USE FOR: Structured Output (`--json-schema`); trigger words: user-guide, configuration, features, how-to, structured, structured-output, json-schema, typed-response, output
- [docs/users/features/sub-agents.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/sub-agents.md)
  - USE FOR: Subagents; trigger words: user-guide, configuration, features, how-to, sub, agents
- [docs/users/features/tips.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/tips.md)
  - USE FOR: Contextual Tips; trigger words: user-guide, configuration, features, how-to, tips
- [docs/users/features/token-caching.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/token-caching.md)
  - USE FOR: Token Caching and Cost Optimization; trigger words: user-guide, configuration, features, how-to, token, caching
- [docs/users/features/tool-use-summaries.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/features/tool-use-summaries.md)
  - USE FOR: Tool-Use Summaries; trigger words: user-guide, configuration, features, how-to, tool, use, summaries
- [docs/users/ide-integration/ide-companion-spec.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/ide-integration/ide-companion-spec.md)
  - USE FOR: Qwen Code Companion Plugin: Interface Specification; trigger words: user-guide, configuration, features, how-to, ide, integration, companion, spec
- [docs/users/ide-integration/ide-integration.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/ide-integration/ide-integration.md)
  - USE FOR: IDE Integration; trigger words: user-guide, configuration, features, how-to, ide, integration
- [docs/users/integration-github-action.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/integration-github-action.md)
  - USE FOR: GitHub Actions: qwen-code-action; trigger words: user-guide, configuration, features, how-to, integration, action
- [docs/users/integration-jetbrains.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/integration-jetbrains.md)
  - USE FOR: JetBrains IDEs; trigger words: user-guide, configuration, features, how-to, integration, jetbrains
- [docs/users/integration-vscode.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/integration-vscode.md)
  - USE FOR: Visual Studio Code; trigger words: user-guide, configuration, features, how-to, integration, vscode
- [docs/users/integration-zed.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/integration-zed.md)
  - USE FOR: Zed Editor; trigger words: user-guide, configuration, features, how-to, integration, zed
- [docs/users/overview.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/overview.md)
  - USE FOR: Qwen Code overview; trigger words: user-guide, configuration, features, how-to
- [docs/users/quickstart.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/quickstart.md)
  - USE FOR: Quickstart; trigger words: user-guide, configuration, features, how-to
- [docs/users/qwen-serve.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/qwen-serve.md)
  - USE FOR: Daemon mode (`qwen serve`); trigger words: user-guide, configuration, features, how-to, serve
- [docs/users/reference/keyboard-shortcuts.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/reference/keyboard-shortcuts.md)
  - USE FOR: Qwen Code Keyboard Shortcuts; trigger words: user-guide, configuration, features, how-to, keyboard, keyboard-shortcuts, hotkeys, productivity, shortcuts
- [docs/users/support/Uninstall.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/support/Uninstall.md)
  - USE FOR: Uninstall; trigger words: user-guide, configuration, features, how-to, support, uninstall
- [docs/users/support/tos-privacy.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/support/tos-privacy.md)
  - USE FOR: Qwen Code: Terms of Service and Privacy Notice; trigger words: user-guide, configuration, features, how-to, support, tos, privacy
- [docs/users/support/troubleshooting.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/docs/users/support/troubleshooting.md)
  - USE FOR: Troubleshooting; trigger words: user-guide, configuration, features, how-to, support, troubleshooting, faq, debugging

### Skills

- [.qwen/skills/bugfix/SKILL.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/.qwen/skills/bugfix/SKILL.md)
  - USE FOR: Reproduce-first workflow for fixing GitHub issue bugs from report to verification; trigger words: bugfix, github-issue, reproduction, verification, regression
- [.qwen/skills/codegraph/SKILL.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/.qwen/skills/codegraph/SKILL.md)
  - USE FOR: Graph + vector index analysis for call graphs, dependencies, architecture, bug tracing, and PR risk/conflict review; trigger words: codegraph, call-graph, dependencies, architecture, impact-analysis, pr-review
- [.qwen/skills/docs-audit-and-refresh/SKILL.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/.qwen/skills/docs-audit-and-refresh/SKILL.md)
  - USE FOR: Audit docs against current code and refresh missing, incorrect, or stale documentation; trigger words: docs-audit, documentation-drift, coverage-gaps, docs-refresh
- [.qwen/skills/docs-update-from-diff/SKILL.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/.qwen/skills/docs-update-from-diff/SKILL.md)
  - USE FOR: Update official docs based on local `git diff` and behavior changes in current branch; trigger words: docs-update, git-diff, changelog-sync, docs-from-code
- [.qwen/skills/e2e-testing/SKILL.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/.qwen/skills/e2e-testing/SKILL.md)
  - USE FOR: End-to-end CLI testing with headless mode, MCP integration checks, and raw API traffic inspection; trigger words: e2e-testing, headless, mcp-testing, api-logs, reproduction
- [.qwen/skills/feat-dev/SKILL.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/.qwen/skills/feat-dev/SKILL.md)
  - USE FOR: Full non-trivial feature workflow: investigation, design, test planning, implementation, verification, and review; trigger words: feature-development, design-doc, e2e-plan, implementation, code-review
- [.qwen/skills/qwen-code-claw/SKILL.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/.qwen/skills/qwen-code-claw/SKILL.md)
  - USE FOR: Using Qwen Code as a coding agent for code understanding, generation, refactoring, bug fixes, and reviews; trigger words: code-agent, coding-tasks, refactoring, bug-fix, project-generation
- [.qwen/skills/structured-debugging/SKILL.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/.qwen/skills/structured-debugging/SKILL.md)
  - USE FOR: Hypothesis-driven debugging for hard bugs, flaky tests, and complex root-cause analysis; trigger words: structured-debugging, hypothesis, instrumentation, root-cause, flaky-tests
- [.qwen/skills/terminal-capture/SKILL.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/.qwen/skills/terminal-capture/SKILL.md)
  - USE FOR: Automated terminal UI screenshot scenarios for CLI output and slash-command visual verification; trigger words: terminal-capture, screenshot-testing, cli-visuals, slash-commands
- [.qwen/skills/tmux-real-user-testing/SKILL.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/.qwen/skills/tmux-real-user-testing/SKILL.md)
  - USE FOR: Real-user-style tmux TUI testing with readable step-by-step logs and reproducible artifacts; trigger words: tmux-testing, tui, real-user-flow, readable-logs, interaction-testing

### Repository

- [Qwen Code Repository](https://github.com/QwenLM/qwen-code)
  - USE FOR: source code, issues, pull requests, main entry point; trigger words: source-code, issues, pull-requests, releases, contributing, repository
- [README.md](https://raw.githubusercontent.com/QwenLM/qwen-code/refs/tags/v0.16.1/README.md)
  - USE FOR: project overview, installation, quick start, authentication, configuration, usage; trigger words: project-overview, installation, quickstart, authentication, configuration, cli-usage
