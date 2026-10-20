---
name: "tdsk-tsa"
description: "Knowledge base for the terminal TSA CLI for AI agent interaction"
version: "2.0.0"
tags: ["cli", "tsa", "bun", "agent", "terminal", "interactive", "session", "proxy-adapter", "args-parse", "tasks", "pi-tui", "tui", "sandbox", "mutagen", "sync"]
---
# TSA Repo Skill

## Overview

The **TSA** repo (`repos/tsa`, `@tdsk/tsa`) is a Bun-based terminal CLI for managing sandboxes and communicating with ThreadedStack AI agents.

- **Sandbox-first**: `tsa sandbox` (aliased as `tsa run`) is the hero command — connects sandbox, syncs files, launches AI tool runtime
- **Pi-TUI terminal UI**: Built with `@mariozechner/pi-tui` (pure TypeScript, NOT React). `ChatLogic` manages all state; renderers are pure display
- **Local agent execution**: Session-based LLM proxy via WebSocket — API keys never leave the backend
- **Two-layer config**: Global (`~/.config/tdsk/tsa.yaml`) + project (`.tdsk/config.yaml`), merged
- **Two command systems**: 12 CLI tasks (`@keg-hub/args-parse`) + 19 in-chat slash commands
- **Context injection**: Auto-detects `AGENTS.md` and `.tdsk/context/` files, prepends to prompts as XML blocks
- **Persistent auth**: API key-based login stored in YAML config
- **Compilable binary**: Produces standalone `tsa` binary via `bun build --compile`

**Runtime**: Bun (entry point uses `#!/usr/bin/env bun`). Binary name: `tsa`.

## Directory Structure

```
repos/tsa/
├── configs/              # Biome, vitest config
├── scripts/build.ts      # Bun build + optional compile to native binary
├── src/
│   ├── index.ts           # CLI entry point (#!/usr/bin/env bun)
│   ├── main.ts            # main() — sets up env, calls cli.ts
│   ├── cli.ts             # argsParse + task dispatch
│   ├── constants/         # Version, paths, defaults, retry config, error patterns, sync paths
│   │   ├── api.ts         # RetryStatusCodes, RetryNetworkCodes
│   │   ├── errors.ts      # FRIENDLY_ERRORS, classifyApiError(), toFriendlyError()
│   │   ├── paths.ts       # ConfigDir, ConfigPath, HistoryDir, ProjectDir, etc.
│   │   ├── sync.ts        # MutagenNpmVersion, SSH paths, PrivateKeyPath, ProxyWrapperPath
│   │   ├── values.ts      # ApiKeyPrefix, defaults, ConnectionColors, ToolDisplayNames, SpinnerFrames, PreAuthCommands
│   │   ├── options.ts      # SandboxOptions, InstanceOptions task option definitions
│   │   ├── shell.ts        # Shell connection constants
│   │   └── version.ts     # Build-time version injection
│   ├── types/             # Types for client, commands, config, context, session, tasks, theme, tools
│   ├── tasks/             # 12 CLI task definitions
│   ├── commands/          # 19 slash commands for in-chat use
│   ├── renderers/         # Pi-TUI renderer classes + ChatLogic
│   ├── services/          # ConfigService, ContextLoader, HooksService, ApiClient, AuthManager, Executor
│   │   ├── api.ts         # ApiClient (extends ApiService from @tdsk/domain)
│   │   ├── auth.ts        # AuthManager (login/logout/credentials via ConfigService)
│   │   ├── config.ts      # ConfigService (YAML global + project merge)
│   │   ├── context.ts     # ContextLoader (auto-detect AGENTS.md + .tdsk/context/)
│   │   ├── executor.ts    # Executor (WebSocket LLM proxy with session caching)
│   │   ├── hooks.ts       # HooksService (lifecycle shell commands)
│   │   └── sync/          # Mutagen file sync subsystem
│   │       ├── configLoader.ts   # mergeRules(), resolveSourcePath()
│   │       ├── ignoreResolver.ts # .gitignore + .tdskignore → Mutagen ignore list
│   │       ├── mutagenClient.ts  # CliDriver (Mutagen CLI wrapper)
│   │       ├── sshConfig.ts      # ensureSshConfig(), getPublicKey()
│   │       └── syncManager.ts    # SyncManager (start/stop/status lifecycle)
│   ├── theme/             # Dark/light theming via picocolors
│   └── utils/
│       ├── api/           # resolveOrg helper
│       ├── friendly-errors.ts  # Friendly error formatting
│       ├── markdown.ts    # Markdown rendering for terminal
│       └── tasks/         # Shared task utilities (see below)
```

## Architecture

**Entry flow**: `main.ts` → `cli.ts` → `hasArg()` (handle --version) → `find()` (resolve task) → `loadConfig()` → `argsParse()` → `task.action(context)`

**Chat flow**: User input → `ChatLogic.handleSubmit()` → slash command dispatch OR `Executor.run()` → `ensureSession()` (55-min TTL) → WebSocket `/ai/ws?token=<sessionToken>` → streaming events → ChatLogic state updates → TUI re-render

**Phase lifecycle**: `login` → `loading` → `pickProject` → `pickAgent` → `chat` (defined in `EAppPhase` enum). Already logged in skips to `loading`. Error at any point goes to `error` phase.

**Streaming events**: `text_delta` → append to stream buffer (50ms throttled flush). `tool_call_start` → add tool with spinner. `tool_result` → update tool status. `error` → classify error. `done` → save threadId, add assistant message.

**Error handling**: `classifyApiError()` → `TApiErrorKind` (`auth`/`forbidden`/`network`/`notFound`/`data`/`server`/`tls`/`unknown`). Auth errors trigger auto-logout. TLS errors suggest `--insecure`. `toFriendlyError()` provides user-friendly messages with suggestions.

## CLI Tasks (`src/tasks/`)

Invoked from terminal. Use `@keg-hub/args-parse` for argument parsing. Task action receives `{ params, task, tasks, auth, config, options }`.

| Task | Alias | Description |
|------|-------|-------------|
| `sandbox` | `sb`, `run` | **Hero command** — Start sandbox, sync files, launch AI tool runtime |
| `chat` | `ch` | Start interactive chat (default, renders Pi-TUI App) |
| `login` | `li` | Authenticate with API key |
| `logout` | `lo` | Remove stored credentials |
| `status` | `st` | Show authentication status |
| `agents` | `ag` | List agents (auth required) |
| `threads` | `th` | List threads for agent (auth required) |
| `sessions` | `session` | List/share/unshare sandbox sessions (auth required) |
| `sync` | — | Start/stop Mutagen file sync (auth required) |
| `ssh` | — | Interactive SSH to sandbox pod (auth required) |
| `proxy` | — | Internal SSH ProxyCommand transport via WebSocket tunnel |
| `help` | `--help`, `-h` | Show available commands |

**Sub-tasks**: `sessions share/unshare <session-id>`, `sync stop [<sandbox-id> | --all]`

### `tsa sandbox` (aliased as `tsa run`) Flow

1. Resolve org ID via `resolveOrgId()` (params → config → single-org auto-select)
2. Resolve project ID via `resolveProjectId()` (params → config)
3. Fetch sandbox config via `GET /_/orgs/:orgId/sandboxes/:id` (hard error if fails)
4. Connect to sandbox via `sandboxConnect()` (auto-starts pod if needed)
5. Start file sync via `sandboxSync()` (unless `--no-sync`)
6. SSH with runtime command via `spawnSsh()` with `config.runtimeCommand` as remote command
7. Exit non-zero on SSH failure

### Shared Task Utilities (`src/utils/tasks/`)

| File | Purpose |
|------|---------|
| `resolveOrgId.ts` | Org resolution from params/config/single-org. Throws on failure |
| `resolveProjectId.ts` | Project resolution from params/config. Throws on failure |
| `sandboxConnect.ts` | Connect to sandbox pod + inject SSH keys. Returns connect response |
| `sandboxSync.ts` | Auto-start/stop Mutagen file sync lifecycle |
| `spawnSsh.ts` | SSH process spawning with optional remote command + PTY support |
| `saveContext.ts` | Save resolved orgId/projectId back to config |
| `ensureAuth.ts` | Ensures auth before running a task action |
| `addDefaults.ts` | Merge config defaults into task option definitions |
| `config.ts` | Load and merge global + project config |
| `find.ts` | Find task by name or alias in registry |
| `hasArg.ts` | Check for specific CLI arguments |
| `error.ts` | Error handling utilities |

## Slash Commands (`src/commands/`)

Invoked within Pi-TUI chat session. Registry at `src/commands/registry.ts`. Handler receives `(args, ctx: TSlashCommandContext)`.

| Command | Aliases | Description |
|---------|---------|-------------|
| `/help` | `/h` | Show available commands |
| `/exit` | `/quit`, `/q` | Exit the TSA |
| `/login` | `/li` | Authenticate with API key |
| `/logout` | `/lo` | Remove credentials |
| `/clear` | `/cl` | Clear screen |
| `/verbose` | `/v` | Toggle verbose mode |
| `/new` | `/n` | Start new thread |
| `/agent` | `/a` | Switch to different agent |
| `/switch` | `/sw` | Switch to different thread |
| `/provider` | `/p` | Switch LLM provider |
| `/add` | — | Add context file |
| `/remove` | `/rm` | Remove context file |
| `/info` | `/i` | Show session info |
| `/context` | `/ctx` | List context files |
| `/history` | `/hist` | Show thread history |
| `/threads` | `/t` | List threads |
| `/fork` | `/br` | Branch current thread at a message |
| `/tree` | `/tr` | Display thread branch hierarchy as ASCII tree |
| `/projects` | `/proj` | Switch project |

**Pre-auth commands**: `login`, `help`, `exit`, `quit`, `q`, `h`, `li` — allowed before authentication.

The `TSlashCommandContext` provides: orgId, agentId, threadId, projectId, connection, verbose, messages, contextFiles, auth, exit(), output(), clearMessages(), set/get for agent/provider/project/thread, thread CRUD operations (list, create, delete, branch, getWithBranches, loadMessages), project/agent listing, and an inline menu system (showMenu/closeMenu).

## Key Components

| Component | Location | Purpose |
|-----------|----------|---------|
| **PiTuiApp** | `renderers/PiTuiApp.ts` | Main TUI orchestrator — layout (Container + Editor + Chat + Status), phase transitions, inline menu system, connects ChatLogic callbacks to TUI. Uses pi-tui: TUI, Text, Spacer, Loader, Editor, Container, SelectList, ProcessTerminal |
| **PiTuiChat** | `renderers/PiTuiChat.ts` | Chat message rendering — messages, streaming text, tool activity indicators, markdown via pi-tui Markdown with custom MarkdownTheme |
| **PiTuiStatus** | `renderers/PiTuiStatus.ts` | Status bar — connection dot (green/yellow/red), org, agent, thread, model, provider, project |
| **ChatLogic** | `renderers/chatLogic.ts` | Decoupled business logic (pure TS, no UI dependency) — manages phase, session, messages, streaming, errors. Event callbacks (onPhaseChange, onMessagesChange, onStreamingChange, onStatusChange, onError). 50ms throttled stream buffer flush. Handles slash command dispatch, agent/project selection, thread management |
| **AuthManager** | `services/auth.ts` | Persistent login — API key + proxy URL stored via ConfigService. Default proxy: `https://px.local.threadedstack.app`. Validates key against `/_/orgs`. Requires `tdsk_` prefix |
| **ApiClient** | `services/api.ts` | Extends `ApiService` from `@tdsk/domain` — auto retry (3 attempts, delays [1000, 3000, 9000]ms on ECONNREFUSED, ETIMEDOUT, ENOTFOUND, 429, 5xx), auth injection via `#ensureAuth()`. Returns `TApiResponse<T>` (`{ ok, status, data?, error? }`) |
| **Executor** | `services/executor.ts` | WebSocket agent execution — session caching (55-min TTL, server expires at 60), creates threads if none exists, prepends context as `<context>` XML blocks, connects to `/ai/ws?token=<sessionToken>` |
| **BrowserAuth** | `services/browserAuth.ts` | Browser-based auth flow for `tsa login --browser` |
| **TokenRefresh** | `services/tokenRefresh.ts` | `TokenRefreshService` class for proactive JWT refresh |
| **ConfigService** | `services/config.ts` | YAML config management — `loadGlobal()`, `saveGlobal()` (chmod 0600, mkdir 0700), `loadProject()`, `merge()` |
| **ContextLoader** | `services/context.ts` | Auto-detects `AGENTS.md` + `.tdsk/context/` files. Returns `TContextFile` (path, name, source: auto/manual, content, sizeBytes) |
| **HooksService** | `services/hooks.ts` | Lifecycle shell commands via `/bin/sh -c`. 10s timeout, errors swallowed. Hooks: onSessionStart/End, onToolCall/Result, onError, onMessage |
| **SyncManager** | `services/sync/syncManager.ts` | High-level Mutagen file sync lifecycle: start, stop, stopAll, status |
| **CliDriver** | `services/sync/mutagenClient.ts` | Low-level Mutagen CLI wrapper: create, list, terminate, flush |
| **configLoader** | `services/sync/configLoader.ts` | Merge sync rules from config with defaults via mergeRules(), resolveSourcePath() |
| **ignoreResolver** | `services/sync/ignoreResolver.ts` | Resolve .gitignore + .tdskignore patterns into Mutagen ignore list |
| **sshConfig** | `services/sync/sshConfig.ts` | SSH config setup for Mutagen, key pair management |

## Configuration

### Config Paths

| Path | Purpose |
|------|---------|
| `~/.config/tdsk/tsa.yaml` | Global config (auth, display, behavior, hooks, tools, sync) |
| `.tdsk/config.yaml` | Project config (org, agent, context, hooks, tools) |
| `AGENTS.md` | Auto-detected agent context file |
| `.tdsk/context/` | Auto-detected context files directory |
| `~/.config/tdsk/sandbox_key[.pub]` | SSH key pair for sandbox access |
| `~/.config/tdsk/bin/mutagen` | Mutagen binary |
| `~/.config/tdsk/bin/tsa-proxy` | SSH ProxyCommand wrapper script |
| `~/.config/tdsk/bin/mutagen-agents.tar.gz` | Mutagen agents archive |
| `~/.config/tdsk/history` | Input history directory |

### Config Schema (`TTsaConfig`)

Global config sections:
- `org`, `agent`, `project` — Default IDs
- `auth` — apiKey, proxyUrl (default: `https://px.local.threadedstack.app`), insecure
- `display` — theme (dark/light/auto), verbose, markdown, timestamps
- `behavior` — autoResume, maxHistory (default: 50), confirmTools
- `sandbox` — timeout (default: 300000), provider (local/e2b), envVars
- `sync` — TSyncConfig from @tdsk/domain: rules (source, target, mode, ignore), defaultIgnores
- `hooks` — onSessionStart, onSessionEnd, onToolCall, onToolResult, onError, onMessage
- `tools` — confirm array (e.g., ["shellExec"]), block array (e.g., ["deleteFile"])

Project config (`.tdsk/config.yaml`): `org`, `agent`, `context` array, `hooks`, `tools`

**Merge rules**: Project `org`/`agent` override global. Project `hooks` merge (project wins per-key). Project `tools.confirm`/`tools.block` concatenate with global arrays.

## Constants

Key constants across `src/constants/`:

- **values.ts**: `ApiKeyPrefix` ("tdsk_"), `DefaultProxyUrl` (https://px.local.threadedstack.app), `DefaultMaxSteps` (10), `DefaultMaxHistory` (50), `DefaultTheme` ("dark"), `DefaultSandboxTimeout` (300000ms), `MaxRetries` (3), `RetryDelays` ([1000, 3000, 9000]ms), `ToolDisplayNames` (record of tool → friendly name), `SpinnerFrames` (braille animation), `PreAuthCommands` (set of commands allowed before auth)
- **paths.ts**: `ConfigDir` (~/.config/tdsk), `ConfigPath` (~/.config/tdsk/tsa.yaml), `HistoryDir` (~/.config/tdsk/history), `ProjectDir` (.tdsk), `AgentsFile` (AGENTS.md), `ContextDir` (.tdsk/context), `ProjectConfig` (.tdsk/config.yaml)
- **sync.ts**: `DefSyncTarget` ("/workspace"), `DefSyncMode` ("one-way-replica"), `DefSyncIgnores` ([".git/", "node_modules/", ...]), `MutagenNpmVersion` ("0.19.0-dev.1"), `PrivateKeyPath`, `PublicKeyPath`, `MutagenBinPath`, `ProxyWrapperPath`, `MutagenAgentsPath`
- **api.ts**: `RetryStatusCodes`, `RetryNetworkCodes`
- **errors.ts**: `FRIENDLY_ERRORS` patterns, `classifyApiError()`, `toFriendlyError()`

## CLI Usage

```bash
# Hero command (sandbox task, aliased as run)
tsa sandbox <sandbox-id> [--org <id>] [--project <id>] [--no-sync] [--list]
tsa run <sandbox-id>               # Alias for tsa sandbox
tsa sandbox --list                 # List available sandboxes

# File sync
tsa sync <sandbox-id> [--org <id>] [--project <id>]
tsa sync stop <sandbox-id>         # Stop sync for a sandbox
tsa sync stop --all                # Stop all sync sessions

# Sessions
tsa sessions <sandbox-id> [--org <id>] [--project <id>]
tsa sessions share <session-id> [--org <id>] [--project <id>]
tsa sessions unshare <session-id> [--org <id>] [--project <id>]

# Auth
tsa login <api-key> [--url <proxy-url>] [--insecure]
tsa logout
tsa status

# Discovery
tsa agents [--org <id>]
tsa threads <agent-id> [--org <id>]

# Chat (default command)
tsa chat [--org <id>] [--agent <id>] [--thread <id>]
tsa                    # Launches chat

# SSH
tsa ssh <sandbox-id> [--org <id>] [--project <id>]
tsa proxy <sandbox-id>  # ProxyCommand transport

# Help
tsa help | --help | -h | --version | -v
```

## Building

```bash
pnpm build           # Bundle via bun (bun build → dist/index.js)
pnpm compile         # Native binary (bun build --compile → dist/tsa)
pnpm tsz             # Run the tsa cli code directly without needing to compile if first
```

Build-time version injection: `__TDSK_TSA_VERSION__` defined in `scripts/build.ts`, consumed by `src/constants/version.ts`. Falls back to package.json when running from source.

## Dependencies

| Package | Purpose |
|---------|---------|
| `@mariozechner/pi-tui` | Terminal UI framework (replaces Ink/React) |
| `@nuanced-dev/mutagen` | File sync between local and sandbox pods |
| `@keg-hub/args-parse` | CLI argument parsing with task definitions |
| `@tdsk/domain` | Shared types, models, ApiService base class |
| `chalk` | Terminal color output (pi-tui themes) |
| `marked` + `marked-terminal` | Markdown rendering for terminal |
| `js-yaml` | YAML config parsing |
| `picocolors` | Lightweight terminal colors (theme system) |
| `ws` | WebSocket client for agent execution |

## Integration Points

### With `@tdsk/domain`

- `ApiService` — base class for `ApiClient` with `TApiRequest`/`TApiResponse`
- `Exception` — error class with status codes
- `TStreamEvent`, `EStreamEventType` — streaming event types
- `TLLMProviderBrand`, `TMessageContent` — shared types
- `Organization`, `Agent`, `Thread`, `Message` — API response model classes
- `TSyncConfig`, `TSyncRule`, `TSyncMode` — sync configuration types
- `TSandboxSession` — sandbox session type

### Backend API Endpoints Used

- **Auth**: `/_/orgs` (API key validation)
- **Sessions**: `POST /_/ai/sessions` → session token + LLM config
- **LLM Proxy**: `WS /ai/ws?token=<sessionToken>` (WebSocket streaming)
- **Agents**: `/_/orgs/:orgId/agents` (list/get)
- **Providers**: `/_/orgs/:orgId/providers` (list)
- **Projects**: `/_/orgs/:orgId/projects` (list)
- **Threads**: `/_/orgs/:orgId/agents/:agentId/threads` (CRUD + branching)
- **Messages**: `/_/orgs/:orgId/agents/:agentId/threads/:threadId/messages` (list/create)
- **Sandboxes**: `/_/orgs/:orgId/sandboxes` (list/get)
- **Sandbox Connect**: `POST /_/orgs/:orgId/projects/:projectId/sandboxes/:sandboxId/connect`
- **Sandbox Sessions**: `GET /_/orgs/:orgId/projects/:projectId/sandboxes/:sandboxId/sessions`
- **Sandbox Exec**: `POST /_/orgs/:orgId/projects/:projectId/sandboxes/:sandboxId/exec`
- **Sandbox Tunnel**: `WS /_/sandboxes/:sandboxId/tunnel` (SSH proxy transport)
- **Sandbox Shell**: `WS /_/sandboxes/:sandboxId/shell` (session visibility control)

### With Proxy

All API requests route through proxy at configured URL (default: `https://px.local.threadedstack.app`) with `Authorization: Bearer <apiKey>` header.

## Adding New Tasks/Commands

- **CLI task**: Create `src/tasks/<name>.ts`, add to `src/tasks/index.ts`. Use `ensureAuth()` wrapper if auth needed. Use `resolveOrgId()`/`resolveProjectId()` for org/project resolution.
- **Slash command**: Create `src/commands/<name>.ts`, add to `registeredCommands[]` in `src/commands/registry.ts`. Add to `PreAuthCommands` in `src/constants/values.ts` if needed before auth.
- **Renderer component**: Implement pi-tui `Component` interface with `render(width): string[]` and `invalidate()`. Wire to ChatLogic via callbacks.
- **Sync feature**: Add to `src/services/sync/`. Use `CliDriver` for Mutagen operations, `SyncManager` for lifecycle.
