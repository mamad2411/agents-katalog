---
name: gemini-cli-docs
description: >-
  USE FOR: Reading, searching, or referencing Gemini CLI documentation (docs directory, CLI reference, tutorials, hooks, extensions, tools, configuration, MCP, and IDE integration guides).
  DO NOT USE FOR: Executing Gemini CLI commands or setting up Gemini authentication/credentials; use appropriate development skills when implementing plugins/extensions/hooks.
  You MUST load this skill when you need to consult Gemini CLI documentation while working with or using the Gemini CLI.
license: MIT
---

# Gemini CLI Docs

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## When to Use

- **Documentation Lookup**: Finding specific Gemini CLI doc pages for features, CLI commands, or configuration.
- **Tutorial Reference**: Fetching how-to guides on automation, MCP setup, skills, shell commands, and memory management.
- **Architecture Reference**: Looking up hooks/extensions specs, tool definitions, IDE companion spec, or policy engine docs.

## When Not to Use

- **Running Gemini CLI Commands**: Interacting with a live `gemini` CLI session — use direct CLI execution instead.
- **Writing Extensions/Skills**: Authoring new Gemini CLI plugins, hooks, or agent skills — use the appropriate development skill.

## Core Process

1. **Identify the Topic**: Determine the docs area (CLI reference, hooks, extensions, tools, tutorials, get-started, admin, reference, or core).
2. **Fetch Doc Content**: Build the URL path using the pattern:
   ```text
   https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/<area>/<filename>
   ```
3. **Process Content**: Extract relevant information to answer the query.

Use `webfetch` or equivalent to retrieve raw markdown files.

## Docs Path Reference

`docs/<area>/` — sub-directories and typical files:

| Area | Key Files |
| --- | --- |
| `(root)` | CONTRIBUTING.md, index.md, local-development.md, npm.md, releases.md |
| `admin/` | enterprise-controls.md |
| `cli/` | CLI reference, skills, model-routing, sandbox, session-management, plan-mode, generation-settings, themes, system-prompt, token-caching, trusted-folders, and more |
| `cli/tutorials/` | automation.md, mcp-setup.md, shell-commands.md, skills-getting-started.md, memory-management.md, task-planning.md, web-tools.md |
| `core/` | gemma-setup.md, local-model-routing.md, remote-agents.md, subagents.md |
| `extensions/` | best-practices.md, reference.md, releasing.md, writing-extensions.md |
| `get-started/` | authentication.mdx, installation.mdx, gemini-3.md |
| `hooks/` | best-practices.md, reference.md, writing-hooks.md |
| `ide-integration/` | ide-companion-spec.md |
| `reference/` | commands.md, configuration.md, tools.md, keyboard-shortcuts.md, policy-engine.md |
| `resources/` | faq.md, troubleshooting.md, quota-and-pricing.md, uninstall.md |
| `tools/` | activate-skill.md, file-system.md, mcp-server.md, memory.md, shell.md, web-fetch.md, planning.md, and more |

## References

### Docs (root)

- [CONTRIBUTING.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/CONTRIBUTING.md)
  - USE FOR: contributing guidelines, code contributions, development setup, pull requests, contributor workflow
- [index.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/index.md)
  - USE FOR: overview, feature index, navigation guide, quick start, install, all feature areas
- [local-development.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/local-development.md)
  - USE FOR: local development, tracing, debugging, telemetry, OpenTelemetry, Genkit UI, Jaeger, Google Cloud Trace
- [npm.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/npm.md)
  - USE FOR: package architecture, monorepo structure, `@google/gemini-cli`, `@google/gemini-cli-core`, npm workspaces
- [releases.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/releases.md)
  - USE FOR: release process, versioning, stable/preview/nightly channels, semver, release cadence, promotion workflow

### Admin

- [enterprise-controls.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/admin/enterprise-controls.md)
  - USE FOR: enterprise policy, admin controls, strict mode, MCP allowlist, extension policy, organization-wide security settings

### CLI

- [cli-reference.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/cli-reference.md)
  - USE FOR: CLI commands cheatsheet, flags, options, positional arguments, interactive REPL commands
- [creating-skills.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/creating-skills.md)
  - USE FOR: creating agent skills, skill directory structure, SKILL.md authoring, skill scaffolding, automated skill creation
- [generation-settings.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/generation-settings.md)
  - USE FOR: model configuration, hyperparameter tuning, temperature, topP, thinkingBudget, aliases, overrides, agent-scoped model config
- [model-routing.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/model-routing.md)
  - USE FOR: model routing, automatic fallback, model selection precedence, model availability, local routing with Gemma
- [plan-mode.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/plan-mode.md)
  - USE FOR: plan mode, read-only mode, /plan command, approval modes, planning before implementation, Shift+Tab
- [sandbox.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/sandbox.md)
  - USE FOR: sandboxing, security isolation, Docker sandbox, macOS Seatbelt, Podman, container-based isolation, GEMINI_SANDBOX
- [session-management.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/session-management.md)
  - USE FOR: session management, resume session, conversation history, --resume flag, session browser, session listing
- [skills.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/skills.md)
  - USE FOR: agent skills overview, skill lifecycle, skill discovery, activation flow, consent, SKILL.md injection, discovery tiers
- [system-prompt.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/system-prompt.md)
  - USE FOR: system prompt override, GEMINI_SYSTEM_MD, custom persona, full prompt replacement, custom system instructions
- [themes.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/themes.md)
  - USE FOR: themes, color scheme, UI customization, /theme command, custom themes, dark/light themes, settings.json theme
- [token-caching.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/token-caching.md)
  - USE FOR: token caching, cost optimization, cached tokens, API key usage, /stats command
- [trusted-folders.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/trusted-folders.md)
  - USE FOR: trusted folders, folder trust, security, safe mode, project-level security, trustedFolders.json

### CLI Tutorials

- [automation.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/tutorials/automation.md)
  - USE FOR: automation, headless mode, scripting, CI/CD, batch processing, piping input, -p flag, stdout output
- [mcp-setup.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/tutorials/mcp-setup.md)
  - USE FOR: MCP server setup, MCP configuration, GitHub MCP server, Docker MCP, settings.json mcpServers, PAT token
- [memory-management.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/tutorials/memory-management.md)
  - USE FOR: memory management, GEMINI.md, persistent context, project-wide rules, memory hierarchy, /memory command
- [shell-commands.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/tutorials/shell-commands.md)
  - USE FOR: shell commands, shell mode, ! prefix, background processes, running builds, git commands from CLI
- [skills-getting-started.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/tutorials/skills-getting-started.md)
  - USE FOR: skills getting started, first skill tutorial, api-auditor example, skill creation walkthrough, bundling scripts
- [task-planning.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/tutorials/task-planning.md)
  - USE FOR: task planning, todo list, complex task management, write_todos, progress monitoring, Ctrl+T
- [web-tools.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/tutorials/web-tools.md)
  - USE FOR: web search, web fetch, URL retrieval, google_web_search, research documentation, grounding

### Core

- [gemma-setup.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/core/gemma-setup.md)
  - USE FOR: Gemma setup, local model routing, LiteRT, `gemini gemma` commands, cost optimization, automated routing setup
- [local-model-routing.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/core/local-model-routing.md)
  - USE FOR: local model routing manual setup, LiteRT-LM runtime, Gemma routing, platform-specific installation
- [remote-agents.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/core/remote-agents.md)
  - USE FOR: remote agents, A2A protocol, agent-to-agent, remote subagent configuration, proxy settings, agent card
- [subagents.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/core/subagents.md)
  - USE FOR: subagents, codebase_investigator, @ syntax, specialized agents, automatic delegation, subagent context

### Extensions

- [best-practices.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/extensions/best-practices.md)
  - USE FOR: extension best practices, extension security, development workflow, TypeScript extensions, GEMINI.md for extensions, gemini extensions link
- [reference.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/extensions/reference.md)
  - USE FOR: extension reference, gemini-extension.json schema, extension management commands, install/uninstall/update/link/disable/enable
- [releasing.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/extensions/releasing.md)
  - USE FOR: releasing extensions, publishing extensions, gallery listing, GitHub Releases, git repository release, gemini-cli-extension topic
- [writing-extensions.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/extensions/writing-extensions.md)
  - USE FOR: building extensions, extension features, MCP server extension, slash commands, GEMINI.md context, extension template

### Get Started

- [authentication.mdx](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/get-started/authentication.mdx)
  - USE FOR: authentication, API key setup, OAuth login, Vertex AI auth, Google account sign-in, headless auth, env variables for auth
- [installation.mdx](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/get-started/installation.mdx)
  - USE FOR: installation, npm install, Homebrew, MacPorts, Anaconda, system requirements, Node.js version, running CLI
- [gemini-3.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/get-started/gemini-3.md)
  - USE FOR: Gemini 3, Gemini 3 Pro, Gemini 3 Flash, model selection, usage limits, daily limit, upgrade, capacity errors

### Hooks

- [best-practices.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/hooks/best-practices.md)
  - USE FOR: hooks best practices, hook performance, parallel operations, caching hooks, hook security, AfterAgent/AfterModel/BeforeTool events
- [reference.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/hooks/reference.md)
  - USE FOR: hooks reference, hook schema, hook configuration, exit codes, stdin/stdout communication, hook events specification
- [writing-hooks.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/hooks/writing-hooks.md)
  - USE FOR: writing hooks, hook tutorial, hook scripts, stderr logging, exit code strategies, hook examples

### IDE Integration

- [ide-companion-spec.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/ide-integration/ide-companion-spec.md)
  - USE FOR: IDE integration, companion plugin spec, MCP over HTTP, VS Code extension, JetBrains plugin, port discovery, IDE mode

### Reference

- [commands.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/reference/commands.md)
  - USE FOR: all slash commands, /agents /auth /bug /chat /memory /plan /resume /settings /skills /theme /tools, @ and ! commands
- [configuration.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/reference/configuration.md)
  - USE FOR: configuration reference, settings.json, environment variables, config layers, all settings options, settings files locations
- [keyboard-shortcuts.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/reference/keyboard-shortcuts.md)
  - USE FOR: keyboard shortcuts, keybindings, cursor navigation, input editing, UI controls, Ctrl+C/D/A/E shortcuts
- [policy-engine.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/reference/policy-engine.md)
  - USE FOR: policy engine, tool control rules, allow/deny/ask_user, TOML policy files, commandPrefix, security policies
- [tools.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/reference/tools.md)
  - USE FOR: tools overview, available built-in tools, /tools command, tool security, confirmation prompts, @file and !shell shorthands

### Resources

- [faq.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/resources/faq.md)
  - USE FOR: FAQ, common questions, 429 rate limit error, ERR_REQUIRE_ESM, third-party tools, account suspension
- [quota-and-pricing.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/resources/quota-and-pricing.md)
  - USE FOR: quota, pricing, daily request limits, free tier, paid plans, Google account/API key/Vertex AI quota comparison
- [troubleshooting.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/resources/troubleshooting.md)
  - USE FOR: troubleshooting, auth errors, login failures, debugging tips, GOOGLE_CLOUD_PROJECT errors, location errors
- [uninstall.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/resources/uninstall.md)
  - USE FOR: uninstall, remove CLI, npm uninstall, npx cache clear, Homebrew uninstall, MacPorts uninstall

### Tools

- [activate-skill.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/tools/activate-skill.md)
  - USE FOR: activate_skill tool, skill activation, tool reference for skill loading, skill consent flow
- [file-system.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/tools/file-system.md)
  - USE FOR: file system tools, read_file, write_file, list_directory, glob, patch, replace, file operations reference
- [mcp-server.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/tools/mcp-server.md)
  - USE FOR: MCP server integration, MCP discovery architecture, transport types (stdio/SSE/HTTP), tool registry, MCP resources
- [memory.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/tools/memory.md)
  - USE FOR: memory tool, GEMINI.md editing, persistent memory, memory hierarchy, project/user/global memory
- [planning.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/tools/planning.md)
  - USE FOR: planning tools, enter_plan_mode tool, exit_plan_mode tool, plan file, plan execution, Plan Mode switching
- [shell.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/tools/shell.md)
  - USE FOR: run_shell_command tool, shell tool arguments, background processes, policy integration, commandPrefix/commandRegex
- [web-fetch.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/tools/web-fetch.md)
  - USE FOR: web_fetch tool, URL fetching, web content retrieval, URL context API, Plan Mode web fetch behavior

### Repository

- [Gemini CLI Repository](https://github.com/google-gemini/gemini-cli)
  - USE FOR: source code, issues, pull requests, GitHub releases, extension gallery, repository root
