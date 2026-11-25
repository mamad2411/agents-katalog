---
name: kimi-cli-docs
description: >-
  Reference and APIs for retrieving Kimi CLI documentation programmatically for LLMs.
  USE FOR: searching Kimi CLI docs, MoonshotAI models documentation, kimi-cli API reference, tool integrations.
  DO NOT USE FOR: calling live Kimi API endpoints, invoking models directly without CLI.
license: MIT
---

# kimi-cli-docs

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- **Documentation Search**: Locating specific Kimi CLI or MoonshotAI documentation articles.
- **Article Retrieval**: Fetching the full rendered markdown of a specific Kimi CLI docs page.

## WHEN NOT TO USE

- **Live AI Generation**: Interacting with live Kimi APIs to generate text. Use appropriate API endpoints or SDKs for that.

## References

To fully utilize this skill, you MUST read at least one of the links relevant to the current context:

### Main Sections

- [Configuration Files](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/configuration/config-files.md)
  - USE FOR: configuration files, settings structure, config schema, project/user settings, configuration management
- [Data Locations](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/configuration/data-locations.md)
  - USE FOR: data paths, storage directories, config locations, cache paths, filesystem layout
- [Environment Variables](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/configuration/env-vars.md)
  - USE FOR: environment variables, env overrides, runtime configuration, CLI env settings, deployment config
- [Overrides](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/configuration/overrides.md)
  - USE FOR: configuration overrides, precedence rules, layered settings, profile-specific config, runtime overrides
- [Providers](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/configuration/providers.md)
  - USE FOR: model providers, backend selection, provider configuration, endpoint setup, credential wiring
- [Agents Customization](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/customization/agents.md)
  - USE FOR: agent customization, agent behavior tuning, custom agent profiles, role definitions, agent workflows
- [Hooks Customization](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/customization/hooks.md)
  - USE FOR: hooks customization, pre/post hook scripts, automation hooks, event hooks, hook lifecycle
- [MCP Customization](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/customization/mcp.md)
  - USE FOR: MCP customization, Model Context Protocol setup, MCP servers, tool integration, MCP configuration
- [Plugins Customization](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/customization/plugins.md)
  - USE FOR: plugin customization, plugin architecture, extending CLI, plugin setup, plugin development
- [Print Mode Customization](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/customization/print-mode.md)
  - USE FOR: print mode, output formatting, non-interactive output, CI-friendly output, text rendering
- [Skills Customization](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/customization/skills.md)
  - USE FOR: skills customization, SKILL.md configuration, skill loading settings, skill organization, skill behavior tuning
- [Wire Mode Customization](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/customization/wire-mode.md)
  - USE FOR: wire mode, structured output, machine-readable responses, protocol output, automation integration
- [FAQ](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/faq.md)
  - USE FOR: frequently asked questions, common issues, troubleshooting answers, usage clarifications, known behaviors
- [Getting Started Guide](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/guides/getting-started.md)
  - USE FOR: getting started, first run setup, installation flow, onboarding, quick start
- [IDEs Guide](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/guides/ides.md)
  - USE FOR: IDE integration, editor workflows, VS Code usage, JetBrains setup, developer tooling
- [Integrations Guide](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/guides/integrations.md)
  - USE FOR: integrations, external tools, third-party connections, CI/CD integration, ecosystem interoperability
- [Interaction Guide](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/guides/interaction.md)
  - USE FOR: prompt interaction, chat workflow, command interaction, conversational usage, input patterns
- [Sessions Guide](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/guides/sessions.md)
  - USE FOR: session lifecycle concepts, continuity strategy, multi-session planning, long-running conversations, conceptual session guidance
- [Use Cases Guide](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/guides/use-cases.md)
  - USE FOR: use cases, practical examples, scenario-based workflows, implementation patterns, real-world tasks
- [Index](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/index.md)
  - USE FOR: kimi-cli main index, docs homepage, feature navigation, topic discovery, primary docs entry
- [Keyboard Reference](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/reference/keyboard.md)
  - USE FOR: keyboard shortcuts, keybindings, navigation keys, terminal controls, productivity shortcuts
- [Kimi ACP Reference](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/reference/kimi-acp.md)
  - USE FOR: ACP reference, ACP mode usage, ACP commands, protocol behavior, ACP integration
- [Kimi Command Reference](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/reference/kimi-command.md)
  - USE FOR: commands reference, slash commands, command syntax, command options, CLI command catalog
- [Kimi Info Reference](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/reference/kimi-info.md)
  - USE FOR: info command, diagnostics output, environment info, runtime metadata, inspection tools
- [Kimi MCP Reference](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/reference/kimi-mcp.md)
  - USE FOR: MCP reference, MCP command usage, server connections, tool protocol, MCP troubleshooting
- [Kimi Term Reference](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/reference/kimi-term.md)
  - USE FOR: terminal mode, TUI behavior, interactive terminal commands, shell integration, terminal controls
- [Kimi Vis Reference](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/reference/kimi-vis.md)
  - USE FOR: visualization mode, rendering output, visual inspection tools, graph display, UI visualization
- [Kimi Web Reference](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/reference/kimi-web.md)
  - USE FOR: web mode, web retrieval, browsing tools, URL context, web-assisted workflows
- [Slash Commands Reference](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/reference/slash-commands.md)
  - USE FOR: slash commands, command palette, interactive commands, workflow shortcuts, command discoverability
- [Breaking Changes](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/release-notes/breaking-changes.md)
  - USE FOR: breaking changes, migration notes, compatibility impacts, upgrade risks, deprecations
- [Changelog](https://raw.githubusercontent.com/MoonshotAI/kimi-cli/refs/tags/1.44.0/docs/en/release-notes/changelog.md)
  - USE FOR: changelog, release notes, feature history, bug fixes, version changes

### CLI Section

- [ACP Mode](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/acp-mode.md)
  - USE FOR: ACP mode, protocol mode, acp workflow, agent protocol integration, acp configuration
- [Auto Memory](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/auto-memory.md)
  - USE FOR: auto memory, persistent memory, memory automation, context retention, memory updates
- [Checkpointing](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/checkpointing.md)
  - USE FOR: checkpointing, snapshots, rollback, state restore, recovery workflow
- [CLI Reference](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/cli-reference.md)
  - USE FOR: CLI reference, command syntax, flags, options, terminal commands
- [Creating Skills](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/creating-skills.md)
  - USE FOR: authoring new skills, SKILL.md structure, skill scaffolding workflow, custom skill implementation, skill development setup
- [Custom Commands](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/custom-commands.md)
  - USE FOR: custom commands, command aliases, slash command extension, workflow commands, command customization
- [Enterprise](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/enterprise.md)
  - USE FOR: enterprise controls, org policy, governance settings, compliance, enterprise deployment
- [Gemini Ignore](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/gemini-ignore.md)
  - USE FOR: ignore patterns, file exclusion, context filtering, privacy filters, .geminiignore behavior
- [Gemini MD](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/gemini-md.md)
  - USE FOR: GEMINI.md, project instructions, persistent memory file, policy context, instruction hierarchy
- [Generation Settings](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/generation-settings.md)
  - USE FOR: generation settings, temperature, top-p, model parameters, response tuning
- [Git Worktrees](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/git-worktrees.md)
  - USE FOR: git worktrees, parallel branches, multi-worktree workflow, branch isolation, repository layout
- [Headless](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/headless.md)
  - USE FOR: headless mode, non-interactive execution, scripting automation, CI runs, prompt mode
- [Model Routing](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/model-routing.md)
  - USE FOR: model routing, fallback strategy, model selection, routing rules, provider preference
- [Model Steering](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/model-steering.md)
  - USE FOR: model steering, behavior control, instruction steering, response style tuning, constraints
- [Model](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/model.md)
  - USE FOR: model selection, model options, model capabilities, selecting default model, model config
- [Notifications](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/notifications.md)
  - USE FOR: notifications, desktop alerts, completion alerts, user prompts, notification settings
- [Plan Mode](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/plan-mode.md)
  - USE FOR: plan mode, planning workflow, read-only planning, task decomposition, implementation planning
- [Rewind](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/rewind.md)
  - USE FOR: rewind, history rollback, undo actions, timeline navigation, state recovery
- [Sandbox](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/sandbox.md)
  - USE FOR: sandbox, execution isolation, command restrictions, security boundaries, safe execution
- [Session Management](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/session-management.md)
  - USE FOR: session CLI commands, session command reference, resume command usage, history operations, persistence controls
- [Settings](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/settings.md)
  - USE FOR: settings, config options, preferences, settings files, global/project configuration
- [Skills Best Practices](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/skills-best-practices.md)
  - USE FOR: skills best practices, skill quality, maintainable skills, documentation standards, skill governance
- [Skills](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/skills.md)
  - USE FOR: skill system architecture, discovery and activation flow, skills architecture concepts, capability composition, skills conceptual model
- [System Prompt](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/system-prompt.md)
  - USE FOR: system prompt, prompt overrides, base instructions, behavior policy, instruction customization
- [Telemetry](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/telemetry.md)
  - USE FOR: telemetry, usage metrics, analytics, observability, privacy controls
- [Themes](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/themes.md)
  - USE FOR: themes, terminal UI styling, color schemes, customization, display preferences
- [Token Caching](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/token-caching.md)
  - USE FOR: token caching, cost optimization, reuse tokens, caching strategy, performance tuning
- [Trusted Folders](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/trusted-folders.md)
  - USE FOR: trusted folders, workspace trust, security prompts, safe directories, trust configuration
- [Using Agent Skills](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/using-agent-skills.md)
  - USE FOR: using existing skills, runtime skill invocation, task-to-skill matching, context injection in execution, operational skill orchestration

#### Tutorials

- [Automation](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/tutorials/automation.md)
  - USE FOR: automation tutorial, scripting workflows, CI automation, batch tasks, headless examples
- [File Management](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/tutorials/file-management.md)
  - USE FOR: file management tutorial, filesystem operations, create/read/update files, workspace manipulation, path handling
- [MCP Setup](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/tutorials/mcp-setup.md)
  - USE FOR: MCP setup tutorial, server configuration, transport setup, MCP onboarding, tool wiring
- [Memory Management](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/tutorials/memory-management.md)
  - USE FOR: memory management tutorial, context memory, persistence strategy, memory updates, long-running context
- [Plan Mode Steering](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/tutorials/plan-mode-steering.md)
  - USE FOR: plan mode steering, planning controls, steering plans, strategic prompts, plan refinement
- [Session Management](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/tutorials/session-management.md)
  - USE FOR: session management tutorial, step-by-step session workflows, guided resume examples, conversation history walkthrough, tutorial exercises
- [Shell Commands](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/tutorials/shell-commands.md)
  - USE FOR: shell commands tutorial, terminal execution, command safety, bash integration, command workflows
- [Skills Getting Started](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/tutorials/skills-getting-started.md)
  - USE FOR: first-skill tutorial, beginner walkthrough, hands-on skill setup, guided skill example, starter exercises
- [Task Planning](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/tutorials/task-planning.md)
  - USE FOR: task planning tutorial, todo planning, execution steps, prioritization, progress tracking
- [Web Tools](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/cli/tutorials/web-tools.md)
  - USE FOR: web tools tutorial, web search/fetch, URL retrieval, web-grounded answers, browsing workflows

### Core Section

- [Gemma Setup](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/core/gemma-setup.md)
  - USE FOR: Gemma setup, local models, Gemma installation, local inference, model runtime setup
- [Index](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/core/index.md)
  - USE FOR: core docs index, core concepts overview, architecture navigation, foundational topics, core entrypoint
- [Local Model Routing](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/core/local-model-routing.md)
  - USE FOR: local model routing, on-device routing, provider selection, local fallback, routing configuration
- [Remote Agents](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/core/remote-agents.md)
  - USE FOR: remote agents, distributed agents, A2A connectivity, remote execution, networked agent workflows
- [Subagents](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/tags/v0.43.0/docs/core/subagents.md)
  - USE FOR: subagents, delegation strategy, specialized agents, parallel tasks, agent orchestration

### Repository

- [Main Repository](https://github.com/MoonshotAI/kimi-cli)
  - USE FOR: source repository, upstream code, issues, pull requests, releases, project roadmap
